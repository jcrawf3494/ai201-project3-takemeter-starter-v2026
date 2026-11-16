"""Free-text TakeMeter inference using the original fine-tuned classifier.

Validation and logging are independent of the model so they can be tested
without downloading the checkpoint. Never use an untrained substitute.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Callable

LABELS = frozenset({"analysis", "hot_take", "personal_preference", "proposal"})
MAX_INPUT_CHARS = 3000
MAX_TOKENS = 256


class InvalidOpinion(ValueError):
    """The submitted opinion is missing or exceeds the input limit."""


def validate_opinion(text: object) -> str:
    if not isinstance(text, str):
        raise InvalidOpinion("Please enter an opinion as text.")
    opinion = text.strip()
    if not opinion:
        raise InvalidOpinion("Enter an opinion before selecting Classify.")
    if len(opinion) > MAX_INPUT_CHARS:
        raise InvalidOpinion(f"Opinions must be {MAX_INPUT_CHARS:,} characters or fewer.")
    return opinion


def load_trained_model(checkpoint: str, subfolder: str = ""):
    """Load the saved four-label checkpoint, optionally from a Hub subfolder."""
    if not isinstance(subfolder, str):
        raise ValueError("Model subfolder must be a string.")
    subfolder = subfolder.strip()
    if subfolder and (
        subfolder.startswith(("/", "\\"))
        or "\\" in subfolder
        or any(part in ("", ".", "..") for part in subfolder.split("/"))
    ):
        raise ValueError("Model subfolder must be a relative repository folder path.")
    if not checkpoint or not checkpoint.strip():
        raise RuntimeError("No trained model configured. See RUNNING.md.")
    if checkpoint.startswith("./") and not Path(checkpoint).is_dir():
        raise RuntimeError(
            "Trained model not found. Export the fine-tuned notebook model first."
        )

    import torch
    from transformers import AutoModelForSequenceClassification, DistilBertTokenizerFast

    # Capstone measured improvement: optional single-thread CPU inference for
    # short posts. Leave unset for original behavior; set to 1 only for the
    # after trial. This can help or hurt depending on the actual CPU.
    thread_setting = os.environ.get("TAKEMETER_TORCH_THREADS")
    if thread_setting is not None:
        try:
            thread_count = int(thread_setting)
        except ValueError as exc:
            raise ValueError("TAKEMETER_TORCH_THREADS must be a positive integer.") from exc
        if not 1 <= thread_count <= 64:
            raise ValueError("TAKEMETER_TORCH_THREADS must be between 1 and 64.")
        torch.set_num_threads(thread_count)

    # The model files may be stored in a Hugging Face repository subfolder.
    # Transformers handles this through its explicit subfolder argument,
    # not by appending the folder name to the repository ID.
    loader_options = {"trust_remote_code": False}
    if subfolder:
        loader_options["subfolder"] = subfolder

    # Use the saved fast tokenizer.json directly. Some hosted checkpoints
    # carry tokenizer_class="DistilBertTokenizer" (the slow class) and
    # accidentally resolve vocab_file=None during AutoTokenizer loading.
    # The notebook exported tokenizer.json, so explicitly load its fast
    # DistilBERT implementation rather than reconstructing a slow tokenizer.
    try:
        tokenizer = DistilBertTokenizerFast.from_pretrained(
            checkpoint, **loader_options
        )
    except (TypeError, OSError, ValueError) as exc:
        raise RuntimeError(
            "Tokenizer load failed. Ensure tokenizer.json, vocab.txt, "
            "tokenizer_config.json and special_tokens_map.json are uploaded "
            "inside the configured model subfolder (or repository root if "
            "no subfolder was configured)."
        ) from exc
    model = AutoModelForSequenceClassification.from_pretrained(
        checkpoint, **loader_options
    )
    model.to("cpu")
    model.eval()

    labels = {str(value) for value in model.config.id2label.values()}
    if labels != LABELS:
        raise RuntimeError(
            "Checkpoint labels do not match TakeMeter's four categories."
        )

    def predict(opinion: str) -> tuple[str, float]:
        encoded = tokenizer(
            opinion, return_tensors="pt", truncation=True, max_length=MAX_TOKENS
        )
        with torch.inference_mode():
            logits = model(**encoded).logits[0]
            probabilities = torch.softmax(logits, dim=-1)
            index = int(torch.argmax(probabilities))
        return str(model.config.id2label[index]), float(probabilities[index].item())

    return predict


def classify_opinion(
    text: object,
    predictor: Callable[[str], tuple[str, float]],
    log_path: str | Path = "logs/inference.jsonl",
    model_name: str = "takemeter-distilbert",
) -> dict:
    """Validate, classify, and write one JSONL record for every outcome.

    The input is logged as its length and SHA-256, not raw visitor text. For
    synthetic test inputs only, TAKEMETER_LOG_TEXT=1 enables raw text logging.
    Keep logs and credentials out of public GitHub.
    """
    started = perf_counter()
    raw_input = text if isinstance(text, str) else ""
    input_data = {
        "length": len(raw_input),
        "sha256": hashlib.sha256(raw_input.encode("utf-8")).hexdigest(),
    }
    if os.getenv("TAKEMETER_LOG_TEXT") == "1" and isinstance(text, str):
        input_data["text"] = text

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": input_data,
        "model": model_name,
        "status": None,
        "output": None,
        "error": None,
        "duration_ms": None,
    }

    try:
        opinion = validate_opinion(text)
        label, confidence = predictor(opinion)
        if label not in LABELS:
            raise RuntimeError("Model returned an unknown category.")
        confidence = float(confidence)
        if not (math.isfinite(confidence) and 0.0 <= confidence <= 1.0):
            raise RuntimeError("Model returned an invalid confidence.")
        record["status"] = "ok"
        record["output"] = {"label": label, "confidence": confidence}
        return record["output"]
    except InvalidOpinion as exc:
        record["status"] = "invalid_input"
        record["error"] = str(exc)
        raise
    except Exception:
        # Dependency exceptions can expose paths and credentials; sanitize logs.
        record["status"] = "model_error"
        record["error"] = "Inference failed"
        raise
    finally:
        record["duration_ms"] = round((perf_counter() - started) * 1000, 3)
        destination = Path(log_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

"""Insert actual sanitized local measurements into the Capstone README.

Only known synthetic inputs from measure_extension.py may appear as log examples.
Run on the machine containing the checkpoint and local logs. No credentials used.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

from measure_extension import OPINIONS, INVALID
from takemeter_inference import LABELS

BEGIN = "<!-- CAPSTONE SANITIZED LOG START -->"
END = "<!-- CAPSTONE SANITIZED LOG END -->"
CRITERIA = [
    ("Valid predictions", "10/10", "valid_predictions", 10),
    ("Invalid inputs rejected", "6/6", "invalid_rejections", 6),
    ("Structured records", "16/16", "structured_logs", 16),
    ("Predictions under 5 seconds", ">=9/10", "under_5_seconds", 9),
    ("Matches direct model", "10/10", "model_agreement", 10),
]


def summary(phase):
    path = Path("capstone_results_" + phase + ".json")
    if not path.exists():
        raise FileNotFoundError(f"{path} not found; run measure_extension.py first.")
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("phase") != phase or len(value.get("trials", [])) != 3:
        raise ValueError(f"{path} must contain three {phase} trials.")
    seconds = float(value["mean_wall_seconds_per_valid_request"])
    if not math.isfinite(seconds) or seconds < 0:
        raise ValueError("Invalid recorded measurement")
    return value


def known_inputs():
    result = {}
    for value in OPINIONS + INVALID:
        raw = value if isinstance(value, str) else ""
        fingerprint = (len(raw), hashlib.sha256(raw.encode("utf-8")).hexdigest())
        if not isinstance(value, str):
            preview = "[synthetic empty or non-string input]"
        elif not raw.strip():
            preview = "[synthetic empty or non-string input]"
        elif len(raw) > 150:
            preview = f"[synthetic length-limit input: {len(raw)} characters]"
        else:
            preview = raw
        result[fingerprint] = preview
    return result


def log_excerpt():
    path = Path("logs/before_trial_events.jsonl")
    if not path.exists():
        raise FileNotFoundError(f"{path} not found; run the before trials first.")
    catalog = known_inputs()
    success, invalid = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        inp = record.get("input", {})
        key = (inp.get("length"), inp.get("sha256"))
        if key not in catalog:
            continue  # No unknown visitor text may be published.
        if record.get("status") not in ("ok", "invalid_input"):
            continue
        duration = record.get("duration_ms")
        if not isinstance(duration, (int, float)) or not math.isfinite(duration):
            continue
        if record["status"] == "ok":
            result = record.get("output")
            if not isinstance(result, dict) or result.get("label") not in LABELS:
                continue
            confidence = result.get("confidence")
            if not isinstance(confidence, (int, float)) or not math.isfinite(confidence):
                continue
            output = {"label": result["label"], "confidence": float(confidence)}
        else:
            output = None
        safe = {
            "timestamp": str(record.get("timestamp", "")),
            "input": {"synthetic_example": catalog[key], "length": inp["length"],
                      "sha256": inp["sha256"]},
            "status": record["status"],
            "output": output,
            "error": "Input rejected by validation" if output is None else None,
            "duration_ms": float(duration),
        }
        (success if output is not None else invalid).append(safe)
    if len(success) < 10 or not invalid:
        raise ValueError("Need ten real synthetic success logs and one rejection.")
    shown = success[:10] + invalid[:1]
    lines = "\n".join(json.dumps(row, ensure_ascii=False) for row in shown)
    return (
        BEGIN + "\n**Eleven actual sanitized JSONL entries from the local "
        "before trials (ten successes and one rejected input):**\n\n"
        + "~~~json\n" + lines + "\n~~~\n\n"
        + "Each input was matched to a fixed synthetic test string by SHA-256. "
        "Private or unmatched visitor text was not published.\n" + END
    )


def table(results):
    lines = ["| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |",
             "|---|---|---|---|---|---|"]
    missed = []
    for name, target, key, minimum in CRITERIA:
        values = [row[key] for row in results["trials"]]
        passed = all(
            isinstance(v, str) and v.endswith("/" + str(10 if key not in
            ("invalid_rejections", "structured_logs") else
            (6 if key == "invalid_rejections" else 16)))
            and int(v.split("/")[0]) >= minimum for v in values
        )
        if not passed:
            missed.append(name)
        lines.append("| " + " | ".join([name, target, *values,
                                        "MET" if passed else "MISSED"]) + " |")
    return "\n".join(lines), missed


def publish(include_after):
    before = summary("before")
    after = summary("after") if include_after else None
    snippet = log_excerpt()  # Validate all inputs before modifying README.
    path = Path("README.md")
    source = path.read_text(encoding="utf-8")
    position = source.find("\n## Capstone\n")
    if position == -1:
        raise ValueError("Capstone README section not found.")
    prefix, cap = source[:position], source[position:]

    if BEGIN in cap and END in cap:
        a, b = cap.index(BEGIN), cap.index(END) + len(END)
        cap = cap[:a] + snippet + cap[b:]
    else:
        anchor = "**What It Costs**"
        if cap.count(anchor) != 1:
            raise ValueError("Instrumentation insertion point not found.")
        cap = cap.replace(anchor, snippet + "\n\n" + anchor, 1)

    if after:
        after_table, misses = table(after)
        old = float(before["mean_wall_seconds_per_valid_request"])
        new = float(after["mean_wall_seconds_per_valid_request"])
        verdict = "faster" if new < old else ("slower" if new > old else "unchanged")
        change_ms = (new - old) * 1000
        note = ("All original criteria were met in the after run."
                if not misses else
                "MISSED: " + ", ".join(misses) +
                ". Diagnose each failed stage using the local logs.")
        replacement = (
            "**The Improvement**\n\n"
            "The original five criteria all passed, but the five-second warm "
            "response target was loose relative to the measured average. "
            "The one tested improvement is optional single-thread CPU "
            "inference using TAKEMETER_TORCH_THREADS=1. This may help or "
            "hurt depending on CPU hardware; the same trained checkpoint, "
            "fixed test inputs, and criteria were retained.\n\n"
            "**After improvement — measured three-trial results:**\n\n"
            + after_table + "\n\n"
            "| Measure | Before | After | Difference |\n"
            "|---|---:|---:|---:|\n"
            + f"| Warm mean seconds/request | {old:.4f} | {new:.4f} | {change_ms:+.2f} ms |\n"
            + f"| Seconds per 100 warm requests | {100*old:.2f} | "
            + f"{100*new:.2f} | {100*(new-old):+.2f} s |\n\n"
            + f"The change was **{verdict}** on average. "
            + "These are measured local wall-clock times, not a hosting bill.\n\n"
            + note + "\n\n"
        )
        a, b = cap.find("**The Improvement**"), cap.find("**What's Still Broken**")
        if a < 0 or b <= a:
            raise ValueError("Improvement section missing.")
        cap = cap[:a] + replacement + cap[b:]
        cap = cap.replace(
            "The submission still needs at least ten actual, sanitized log lines "
            "in **Instrumentation**, an after-improvement three-trial run "
            "following one targeted change, and verification of the free hosted URL.",
            "The required synthetic log excerpt and three after trials are now "
            "documented. The free hosted URL still needs verification."
        )
    path.write_text(prefix + cap, encoding="utf-8")
    print("README.md updated from measured local files.")
    print("Review: git diff -- README.md")
    print("Do NOT commit logs/, deployment_model/, or secrets.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-after", action="store_true")
    args = parser.parse_args()
    publish(args.include_after)

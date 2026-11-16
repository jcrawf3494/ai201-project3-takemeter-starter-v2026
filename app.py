"""TakeMeter website: classify a visitor's own opinion with trained DistilBERT."""
import os
import logging
import traceback

import streamlit as st

from takemeter_inference import (
    InvalidOpinion,
    MAX_INPUT_CHARS,
    classify_opinion,
    load_trained_model,
)

LOGGER = logging.getLogger("takemeter")

st.set_page_config(page_title="TakeMeter", page_icon="🗣️", layout="centered")
st.title("TakeMeter")
st.write("Enter an unpopular opinion to predict its category.")
st.caption("Categories: analysis · hot_take · personal_preference · proposal")

try:
    configured_model = st.secrets.get("TAKEMETER_MODEL_ID")
    configured_subfolder = st.secrets.get("TAKEMETER_MODEL_SUBFOLDER")
except Exception:
    configured_model = None
    configured_subfolder = None

checkpoint = configured_model or os.getenv("TAKEMETER_MODEL_ID", "./deployment_model")
model_subfolder = (
    configured_subfolder
    if configured_subfolder is not None
    else os.getenv("TAKEMETER_MODEL_SUBFOLDER", "")
)
model_source = (
    "Streamlit Secrets" if configured_model
    else "environment variable" if os.getenv("TAKEMETER_MODEL_ID")
    else "local fallback"
)


def error_diagnostic(exc: Exception) -> tuple[str, str]:
    """Give a useful diagnosis without exposing exception text or credentials."""
    message = str(exc).lower()
    if not isinstance(checkpoint, str) or not checkpoint.strip():
        return ("MODEL_ID_INVALID",
                "TAKEMETER_MODEL_ID must be a single quoted string such as "
                "username/takemeter-distilbert in Streamlit Secrets.")
    if model_source == "local fallback" and not os.path.isdir("./deployment_model"):
        return ("MODEL_ID_MISSING",
                "The hosted app has no trained model configured. Set "
                "TAKEMETER_MODEL_ID in Streamlit Settings → Secrets to the "
                "public Hugging Face model repository ID.")
    if "checkpoint labels do not match" in message:
        return ("LABEL_CONFIG_MISMATCH",
                "The uploaded config.json does not define TakeMeter's four "
                "expected labels: analysis, hot_take, personal_preference, proposal.")
    if "out of memory" in message or "cannot allocate memory" in message:
        return ("OUT_OF_MEMORY",
                "The cloud instance may not have enough memory to load the model.")
    if ("repository not found" in message or "not a valid model identifier" in message
            or "gatedrepoerror" in type(exc).__name__.lower()):
        return ("MODEL_REPOSITORY_UNAVAILABLE",
                "Check the exact Hugging Face model repository ID and whether "
                "the repository is public.")
    if "config.json" in message or "model.safetensors" in message or "tokenizer" in message:
        return ("MODEL_FILES_OR_CONFIG",
                "Check that all six exported model and tokenizer files exist "
                "in the configured Hugging Face repository subfolder "
                "(or at the root if no subfolder is set).")
    return ("MODEL_RUNTIME_ERROR",
            "Check the model repository, uploaded files, and Streamlit Cloud logs.")


def safe_error_location(exc: Exception) -> str:
    """Only show code locations, never exception messages or visitor text."""
    frames = traceback.extract_tb(exc.__traceback__)
    return " → ".join(
        f"{os.path.basename(frame.filename)}:{frame.lineno} ({frame.name})"
        for frame in frames[-5:]
    ) or "unknown"


@st.cache_resource(show_spinner="Loading trained TakeMeter model …")
def cached_predictor(checkpoint_name: str, subfolder_name: str):
    return load_trained_model(checkpoint_name, subfolder=subfolder_name)


with st.form("opinion_form"):
    opinion = st.text_area(
        "Your opinion",
        placeholder="e.g. Cooking classes should be mandatory in schools.",
        height=130,
        max_chars=MAX_INPUT_CHARS + 100,
    )
    submitted = st.form_submit_button("Classify opinion", type="primary")

if submitted:
    step = {"stage": "validating_input"}

    def model_prediction(text: str):
        step["stage"] = "loading_model"
        predictor = cached_predictor(checkpoint, model_subfolder)
        step["stage"] = "running_inference"
        outcome = predictor(text)
        step["stage"] = "validating_result_or_writing_log"
        return outcome

    try:
        with st.spinner("Classifying …"):
            result = classify_opinion(
                opinion,
                model_prediction,
                model_name=checkpoint,
            )
        st.subheader(f"Prediction: {result['label']}")
        st.write(f"Model confidence: **{result['confidence']:.1%}**")
        st.caption("Confidence is a model score, not a guarantee of correctness.")
    except InvalidOpinion as exc:
        st.warning(str(exc))
    except Exception as exc:
        code, advice = error_diagnostic(exc)
        LOGGER.error(
            "TakeMeter classification failed: code=%s exception_type=%s "
            "model_source=%s stage=%s code_location=%s",
            code,
            type(exc).__name__,
            model_source,
            step["stage"],
            safe_error_location(exc),
        )
        st.error(
            f"Classification failed [{code}]. {advice} "
            f"(Stage: {step['stage']}; Exception: {type(exc).__name__})"
        )

st.caption("This classifier categorizes opinions; it does not fact-check claims.")

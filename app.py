"""TakeMeter website: classify a visitor's own opinion with trained DistilBERT."""
import os

import streamlit as st

from takemeter_inference import (
    InvalidOpinion,
    MAX_INPUT_CHARS,
    classify_opinion,
    load_trained_model,
)

st.set_page_config(page_title="TakeMeter", page_icon="🗣️", layout="centered")
st.title("TakeMeter")
st.write("Enter an unpopular opinion to predict its category.")
st.caption("Categories: analysis · hot_take · personal_preference · proposal")

try:
    configured_model = st.secrets.get("TAKEMETER_MODEL_ID")
except Exception:
    configured_model = None

checkpoint = configured_model or os.getenv("TAKEMETER_MODEL_ID", "./deployment_model")


@st.cache_resource(show_spinner="Loading trained TakeMeter model …")
def cached_predictor(checkpoint_name: str):
    return load_trained_model(checkpoint_name)


with st.form("opinion_form"):
    opinion = st.text_area(
        "Your opinion",
        placeholder="e.g. Cooking classes should be mandatory in schools.",
        height=130,
        max_chars=MAX_INPUT_CHARS + 100,
    )
    submitted = st.form_submit_button("Classify opinion", type="primary")

if submitted:
    try:
        with st.spinner("Classifying …"):
            result = classify_opinion(
                opinion,
                lambda text: cached_predictor(checkpoint)(text),
                model_name=checkpoint,
            )
        st.subheader(f"Prediction: {result['label']}")
        st.write(f"Model confidence: **{result['confidence']:.1%}**")
        st.caption("Confidence is a model score, not a guarantee of correctness.")
    except InvalidOpinion as exc:
        st.warning(str(exc))
    except Exception:
        st.error(
            "The trained model is unavailable or classification failed. "
            "Check the model export and deployment configuration."
        )

st.caption("This classifier categorizes opinions; it does not fact-check claims.")

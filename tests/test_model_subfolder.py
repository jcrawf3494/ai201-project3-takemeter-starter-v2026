"""Verify the same Hub subfolder is supplied for tokenizer and model loading.

These tests mock Transformers so they require neither trained weights nor a
Hugging Face download, and do not touch actual Streamlit Secrets.
"""
import os
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

from takemeter_inference import load_trained_model


class TrainedModelSubfolderTests(unittest.TestCase):
    def setUp(self):
        self.model = MagicMock()
        self.model.config.id2label = {
            0: "analysis",
            1: "hot_take",
            2: "personal_preference",
            3: "proposal",
        }
        self.tokenizer_loader = MagicMock(return_value=MagicMock())
        self.model_loader = MagicMock(return_value=self.model)
        transformers = types.ModuleType("transformers")
        transformers.DistilBertTokenizerFast = types.SimpleNamespace(
            from_pretrained=self.tokenizer_loader
        )
        transformers.AutoModelForSequenceClassification = types.SimpleNamespace(
            from_pretrained=self.model_loader
        )
        self.module_patch = patch.dict(sys.modules, {
            "torch": types.ModuleType("torch"),
            "transformers": transformers,
        })
        self.env_patch = patch.dict(os.environ, {"TAKEMETER_TORCH_THREADS": ""})
        self.module_patch.start()
        self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop()
        self.module_patch.stop()

    def test_hub_subfolder_applies_to_both_tokenizer_and_model(self):
        # An empty env variable must not cause an invalid thread count.
        os.environ.pop("TAKEMETER_TORCH_THREADS", None)
        predict = load_trained_model(
            "jcrawf1077/takemeter-distilbert", subfolder="deployment_model"
        )
        self.assertTrue(callable(predict))
        self.tokenizer_loader.assert_called_once_with(
            "jcrawf1077/takemeter-distilbert",
            trust_remote_code=False,
            subfolder="deployment_model",
        )
        self.model_loader.assert_called_once_with(
            "jcrawf1077/takemeter-distilbert",
            trust_remote_code=False,
            subfolder="deployment_model",
        )

    def test_local_checkpoint_still_loads_without_subfolder(self):
        os.environ.pop("TAKEMETER_TORCH_THREADS", None)
        load_trained_model("jcrawf1077/takemeter-distilbert")
        self.tokenizer_loader.assert_called_once_with(
            "jcrawf1077/takemeter-distilbert", trust_remote_code=False
        )
        self.model_loader.assert_called_once_with(
            "jcrawf1077/takemeter-distilbert", trust_remote_code=False
        )

    def test_unsafe_subfolder_is_rejected(self):
        os.environ.pop("TAKEMETER_TORCH_THREADS", None)
        for name in ("../secrets", "/root", r"folder\other", "folder//nested"):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    load_trained_model(
                        "jcrawf1077/takemeter-distilbert", subfolder=name
                    )
        self.tokenizer_loader.assert_not_called()


if __name__ == "__main__":
    unittest.main()

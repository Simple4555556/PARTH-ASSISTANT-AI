"""
PARTH ASSISTANT AI — ML Inference Engine
Predicts intent and calculates confidence probability score.
"""

import os
import pickle
import numpy as np
from typing import Dict, Any

from ml.preprocess import preprocess_text

_vectorizer = None
_classifier = None


def _load_model_artifacts():
    global _vectorizer, _classifier
    if _vectorizer is not None and _classifier is not None:
        return

    base_dir = os.path.dirname(__file__)
    model_dir = os.path.join(base_dir, "model")
    vec_path = os.path.join(model_dir, "vectorizer.pkl")
    cls_path = os.path.join(model_dir, "model.pkl")

    if not os.path.exists(vec_path) or not os.path.exists(cls_path):
        from ml.train import train_model
        _vectorizer, _classifier = train_model()
    else:
        with open(vec_path, "rb") as f:
            _vectorizer = pickle.load(f)
        with open(cls_path, "rb") as f:
            _classifier = pickle.load(f)


def predict_intent(text: str) -> Dict[str, Any]:
    _load_model_artifacts()
    clean = preprocess_text(text)
    if not clean:
        return {"intent": "UNKNOWN", "confidence": 0.0}

    tfidf = _vectorizer.transform([clean])
    probas = _classifier.predict_proba(tfidf)[0]
    max_idx = np.argmax(probas)
    predicted_intent = _classifier.classes_[max_idx]
    confidence = round(float(probas[max_idx]), 4)

    return {
        "intent": predicted_intent,
        "confidence": confidence,
        "raw_text": text
    }

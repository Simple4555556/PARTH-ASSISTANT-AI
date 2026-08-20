"""
PARTH ASSISTANT AI — ML Evaluation & Metrics Engine
Calculates Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

from ml.preprocess import preprocess_text


def evaluate_model():
    base_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(base_dir, "dataset", "intents.csv")
    model_dir = os.path.join(base_dir, "model")
    metrics_dir = os.path.join(base_dir, "metrics")
    os.makedirs(metrics_dir, exist_ok=True)

    vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")
    model_path = os.path.join(model_dir, "model.pkl")

    if not os.path.exists(vectorizer_path) or not os.path.exists(model_path):
        from ml.train import train_model
        train_model()

    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)
    with open(model_path, "rb") as f:
        classifier = pickle.load(f)

    df = pd.read_csv(dataset_path)
    X = df["text"].apply(preprocess_text)
    y_true = df["intent"]

    X_tfidf = vectorizer.transform(X)
    y_pred = classifier.predict(X_tfidf)

    acc = float(accuracy_score(y_true, y_pred))
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)

    cm = confusion_matrix(y_true, y_pred)
    labels = list(sorted(set(y_true)))

    report = {
        "dataset_samples": len(df),
        "accuracy": round(acc, 4),
        "precision": round(float(p), 4),
        "recall": round(float(r), 4),
        "f1_score": round(float(f1), 4),
        "classes": labels
    }

    cm_report = {
        "classes": labels,
        "confusion_matrix": cm.tolist()
    }

    with open(os.path.join(metrics_dir, "evaluation_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    with open(os.path.join(metrics_dir, "confusion_matrix.json"), "w") as f:
        json.dump(cm_report, f, indent=2)

    print(f"Evaluation complete! Accuracy: {report['accuracy']*100:.2f}%, F1: {report['f1_score']:.4f}")
    return report


if __name__ == "__main__":
    evaluate_model()

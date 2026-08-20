"""
PARTH ASSISTANT AI — ML Training Pipeline
Fits TF-IDF Vectorizer + Logistic Regression Classifier and saves model artifacts.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from ml.preprocess import preprocess_text


def train_model():
    base_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(base_dir, "dataset", "intents.csv")
    model_dir = os.path.join(base_dir, "model")
    os.makedirs(model_dir, exist_ok=True)

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")

    df = pd.read_csv(dataset_path)
    df["clean_text"] = df["text"].apply(preprocess_text)

    X = df["clean_text"]
    y = df["intent"]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_tfidf = vectorizer.fit_transform(X)

    classifier = LogisticRegression(C=1.0, max_iter=500, random_state=42)
    classifier.fit(X_tfidf, y)

    # Save artifacts
    vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")
    model_path = os.path.join(model_dir, "model.pkl")

    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)

    with open(model_path, "wb") as f:
        pickle.dump(classifier, f)

    print(f"Model successfully trained on {len(df)} samples and saved to {model_dir}")
    return vectorizer, classifier


if __name__ == "__main__":
    train_model()

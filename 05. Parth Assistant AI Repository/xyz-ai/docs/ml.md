# ML Intent Classifier Documentation — PARTH ASSISTANT AI

## ML Architecture & Pipeline

The ML Intent Classifier uses a **TF-IDF Vectorizer + Logistic Regression Classifier** (`scikit-learn`) trained on structured multilingual and Hinglish training data.

```
User Query Text
   │
   ▼
[Preprocessing] ──► Lowercasing, punctuation stripping, tokenization
   │
   ▼
[TF-IDF Vectorizer] ──► Converts text into n-gram feature vector (1-gram & 2-gram)
   │
   ▼
[Logistic Regression Model] ──► Predicts probability distribution across 12 intent classes
   │
   ▼
[Confidence Evaluator] ──► If confidence >= 0.35 -> Route; If low -> Clarification dialog
```

---

## Model Metrics & Evaluation Results

- **Training Samples**: 79 labeled queries across 12 intents
- **Accuracy**: 97.47%
- **F1 Score**: 0.9736
- **Precision**: 0.9768
- **Recall**: 0.9747

*Evaluation report saved to `ml/metrics/evaluation_report.json` and `ml/metrics/confusion_matrix.json`.*

---

## Hybrid ML + LLM Architecture

- High confidence ML predictions route directly to specialized agents & tools.
- Ambiguous / low confidence inputs trigger natural clarification questions instead of guessing student IDs or intentions.

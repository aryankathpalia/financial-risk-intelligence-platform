# Financial Risk Intelligence Platform

A full-stack, production-oriented fraud risk intelligence system that combines machine learning, anomaly detection, decision policying, and model explainability (SHAP) to score, triage, and review financial transactions in real time.

This project demonstrates **end-to-end ML system design**, not just model training.

---

## 🚀 Key Capabilities

### 1. Real-Time Transaction Scoring
- Fraud probability (LightGBM classifier)
- Anomaly score (Isolation Forest)
- Final decision: **ALLOW / REVIEW / BLOCK**

---

### 2. Decision Engine (Policy Layer)
- Deterministic, explainable thresholds
- Separates ML prediction from business decisions

---

### 3. Model Explainability (SHAP)
- Only computed for risky transactions
- Feature-level contributions
- Natural-language explanations

---

### 4. Analyst Dashboard
- Transaction explorer
- SHAP visualizations
- Risk insights

---

### 5. Backend Architecture
- FastAPI
- SQLAlchemy
- Clean API design
- Environment-based config

---

## 🧠 ML Stack

- LightGBM (Fraud detection)
- Isolation Forest (Anomaly detection)
- SHAP (Explainability)

---

## ⚙️ Future Improvements

- Streaming ingestion (Kafka)
- Model versioning
- Feedback loop training
- Alert workflows

---

## 👨‍💻 Author

**Aryan Kathpalia**  
Machine Learning • AI Systems • Fraud Detection • Data Engineering
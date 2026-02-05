Financial Risk Intelligence Platform

A full-stack, production-oriented fraud risk intelligence system that combines machine learning, anomaly detection, decision policying, and model explainability (SHAP) to score, triage, and review financial transactions in real time.

This project is designed to demonstrate end-to-end ML system design, not just model training.

Key Capabilities
1. Real-Time Transaction Scoring
  Ingests raw transaction data and assigns:
   - Fraud probability (LightGBM classifier)
   - Anomaly score (Isolation Forest)
   - Final decision: ALLOW / REVIEW / BLOCK
     
- Scoring happens once at ingestion time (production-correct design)

2. Decision Engine (Policy Layer)
  - Deterministic, explainable thresholds
  - Separates model prediction from business decisioning
  - Supports multiple severity levels and review paths

3. Model Explainability (SHAP)
  - SHAP values computed only for REVIEW / BLOCK transactions
  - Feature-level contribution scores
  - Natural-language explanations surfaced in the UI
  - Designed with latency and cost awareness

4.  Analyst Review Dashboard
  - Transaction explorer with detailed drill-down
  - SHAP bar visualizations
  - Decision rationale and risk drivers
  - Built with SvelteKit + Tailwind CSS

5.  Production-Grade Backend
  - FastAPI service architecture
  - SQLAlchemy ORM
  - Clean API boundaries
  - Health check endpoint for hosting platforms
  - Environment-based configuration (no hardcoding)

Machine Learning Stack
- Fraud Classifier: LightGBM (binary classification)
- Anomaly Detection: Isolation Forest
- Explainability: SHAP TreeExplainer
- Feature Contract:
  - Strict inference-time feature alignment
  - No feature learning at runtime
- Offline ↔ Online parity checks included


SHAP Explainability Design
- SHAP is computed only when necessary
  - REVIEW or BLOCK decisions
- Prevents unnecessary latency and compute cost
- Stored at ingestion time
- Displayed as:
  - Ranked feature contributions
  - Visual bars
  - Natural language summaries

Example:
“Transaction amount unusually high compared to user history (+2.02 risk)”

Environment Configuration
- All sensitive or environment-specific values are injected via .env.

Future Improvements
- Async ingestion workers
- Streaming ingestion (Kafka / PubSub)
- Model versioning and A/B rollout
- Analyst feedback loop for retraining
- Alert escalation workflows

Author
Aryan Kathpalia
Machine Learning & Systems Engineering


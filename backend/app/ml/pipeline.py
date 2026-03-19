from app.ml.fraud_classifier import FraudClassifier
from app.ml.decision_engine import DecisionEngine
from app.ml.anomaly.isolation_forest import AnomalyScorer


class RiskPipeline:
    def __init__(self):
        self.fraud_model = FraudClassifier()
        self.decision_engine = DecisionEngine()
        self.anomaly_scorer = AnomalyScorer()

    def score(self, tx):
        fraud_prob = self.fraud_model.predict(tx)
        anomaly_score = self.anomaly_scorer.score(tx)

        decision = self.decision_engine.decide(
            fraud_prob=fraud_prob,
            anomaly_score=anomaly_score,
        )

        # SHAP only for analyst-visible decisions
        if decision["decision"] in ("REVIEW", "BLOCK"):
            shap_values = self.fraud_model.explain(tx)
        else:
            shap_values = []

        return {
            "fraud_prob": fraud_prob,
            "anomaly_score": anomaly_score,
            "decision": decision["decision"],
            "severity": decision["severity"],
            "reasons": decision.get("reasons", []),
            "shap_values": shap_values,
        }

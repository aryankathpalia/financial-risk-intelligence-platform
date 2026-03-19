class DecisionEngine:
    """
    Production fraud decision policy
    Tuned using offline ↔ online parity checks
    """

    REVIEW_TH = 0.50
    SOFT_BLOCK_TH = 0.70
    HARD_BLOCK_TH = 0.80

    def decide(self, fraud_prob: float, anomaly_score: float | None = None):
        reasons = []

        if fraud_prob >= self.HARD_BLOCK_TH:
            reasons.append("Extremely high fraud probability")
            return {
                "decision": "BLOCK",
                "severity": "HIGH",
                "fraud_prob": fraud_prob,
                "anomaly_score": anomaly_score,
                "reasons": reasons,
            }

        if fraud_prob >= self.SOFT_BLOCK_TH:
            reasons.append("High fraud probability (manual review required)")
            return {
                "decision": "REVIEW",
                "severity": "HIGH",
                "fraud_prob": fraud_prob,
                "anomaly_score": anomaly_score,
                "reasons": reasons,
            }

        if fraud_prob >= self.REVIEW_TH:
            reasons.append("Elevated fraud probability")
            return {
                "decision": "REVIEW",
                "severity": "MEDIUM",
                "fraud_prob": fraud_prob,
                "anomaly_score": anomaly_score,
                "reasons": reasons,
            }

        return {
            "decision": "ALLOW",
            "severity": "LOW",
            "fraud_prob": fraud_prob,
            "anomaly_score": anomaly_score,
            "reasons": reasons,
        }

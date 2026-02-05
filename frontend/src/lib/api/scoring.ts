import { apiFetch } from "./client";

export interface ModelSignals {
  fraud_prob: number;
  anomaly_score: number;
  decision: "ALLOW" | "REVIEW" | "BLOCK";
  reasons?: string[];
}

export function fetchModelSignals(
  transactionId: string,
  signal?: AbortSignal
) {
  return apiFetch<ModelSignals>(
    `/api/scoring/score/${transactionId}`,
    {
      method: "POST",
      signal
    }
  );
}

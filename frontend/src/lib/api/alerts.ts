import { apiFetch } from "./client";

/* ===================== TYPES ===================== */

export interface Alert {
  id: string;
  transaction_id: string;
  user_id: string;
  risk_score: number;
  severity: "low" | "medium" | "high";
  status: "pending" | "resolved";
  created_at: string;
  anomaly_score: number | null;
  reasons: string[]; 
}

export type AnalystDecision = "APPROVE" | "CONFIRM_FRAUD";

/* ===================== API ===================== */

export function fetchAlerts(): Promise<Alert[]> {
  return apiFetch<Alert[]>("/api/alerts");
}

export function resolveAlert(
  transactionId: string,
  decision: AnalystDecision,
  reason?: string
) {
  return apiFetch(`/api/alerts/${transactionId}/resolve`, {
    method: "POST",
    body: JSON.stringify({ decision, reason }),
  });
}

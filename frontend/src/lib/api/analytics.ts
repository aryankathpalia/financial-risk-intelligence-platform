// frontend/src/lib/api/analytics.ts
import { apiFetch } from "./client";

export interface ScoreDistributionResponse {
  buckets: number[];
}

export function fetchScoreDistribution(): Promise<ScoreDistributionResponse> {
  return apiFetch("/api/analytics/score-distribution");
}

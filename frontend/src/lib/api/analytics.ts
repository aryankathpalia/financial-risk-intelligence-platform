import { apiFetch } from "./client";

export interface ScoreDistributionResponse {
  buckets: number[];
}

export function fetchScoreDistribution(): Promise<ScoreDistributionResponse> {
  return apiFetch("/analytics/score-distribution");
}

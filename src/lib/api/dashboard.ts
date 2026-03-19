import { apiFetch } from "./client";

export interface DashboardKPIs {
  total_transactions: number;
  flagged_transactions: number;
  high_severity_alerts: number;
  flag_rate: number;
}


export function fetchDashboardKPIs() {
  return apiFetch<DashboardKPIs>("/api/dashboard/kpis");
}

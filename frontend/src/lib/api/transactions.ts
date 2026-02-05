import { apiFetch } from "./client";

export interface Transaction {
  id: string;
  user_id: string;
  amount: number;
  merchant: string;
  country: string;
  created_at: string;

  fraud_prob: number;
  anomaly_score: number;
  decision: "ALLOW" | "REVIEW" | "BLOCK";
}

// ----------------------------------
// SINGLE TRANSACTION (WITH ABORT)
// ----------------------------------
export function fetchTransactionById(
  id: string,
  signal?: AbortSignal
) {
  return apiFetch<Transaction>(
    `/api/transactions/${id}`,
    { signal }
  );
}

// ----------------------------------
// PAGINATED LIST
// ----------------------------------
export interface PaginatedTransactions {
  items: Transaction[];
  total: number;
  page: number;
  page_size: number;
}

export function fetchTransactions(page = 1, pageSize = 15) {
  return apiFetch<PaginatedTransactions>(
    `/api/transactions?page=${page}&page_size=${pageSize}`
  );
}

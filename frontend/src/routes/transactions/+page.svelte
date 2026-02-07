<script lang="ts">
  import { onMount } from "svelte";
  import {
    fetchTransactions,
    type Transaction,
    type PaginatedTransactions
  } from "$lib/api/transactions";

  /* ---------------------------
     STATE
  --------------------------- */
  let transactions: Transaction[] = [];

  let page = 1;
  let pageSize = 15;
  let total = 0;

  let loading = true;
  let error: string | null = null;

  /* ---------------------------
     LOAD DATA
  --------------------------- */
  async function loadTransactions() {
    loading = true;
    error = null;

    try {
      const res: PaginatedTransactions = await fetchTransactions(page, pageSize);
      transactions = res.items;
      total = res.total;
    } catch (e) {
      console.error("Transactions fetch failed:", e);
      error = e instanceof Error ? e.message : "Failed to load transactions";
    } finally {
      loading = false;
    }
  }

  onMount(loadTransactions);

  /* ---------------------------
     HELPERS
  --------------------------- */
  function riskPercent(tx: Transaction) {
    return Math.round(tx.fraud_prob * 1000) / 10;
  }

  function severity(tx: Transaction) {
    if (tx.decision === "BLOCK") return "high";
    if (tx.decision === "REVIEW") return "medium";
    return "low";
  }

  function status(tx: Transaction) {
    if (tx.decision === "ALLOW") return "Approved";
    if (tx.decision === "REVIEW") return "Needs Review";
    return "Blocked";
  }

  /* ---------------------------
     PAGINATION
  --------------------------- */
  function nextPage() {
    if (page * pageSize < total) {
      page++;
      loadTransactions();
    }
  }

  function prevPage() {
    if (page > 1) {
      page--;
      loadTransactions();
    }
  }

  $: totalPages = Math.ceil(total / pageSize);
</script>


<section class="min-h-screen bg-slate-950 p-4 text-slate-100">
  <div
    class="min-h-[calc(100vh-2rem)] rounded-2xl
           bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950
           ring-1 ring-white/5 shadow-2xl"
  >
    <div class="p-6 space-y-6 rounded-2xl bg-slate-900/95">

      <!-- HEADER -->
      <header class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-semibold tracking-tight">
            Transactions
          </h1>
          <p class="text-sm text-slate-400 mt-1">
            Review and investigate transaction-level risk signals
          </p>
        </div>
      </header>

      <!-- FILTER BAR -->
      <div class="flex flex-wrap items-center gap-3">
        <div class="px-3 py-1.5 rounded-md bg-slate-800 text-xs text-slate-300">
          Status: All
        </div>
        <div class="px-3 py-1.5 rounded-md bg-slate-800 text-xs text-slate-300">
          Risk: Any
        </div>
        <div class="px-3 py-1.5 rounded-md bg-slate-800 text-xs text-slate-300">
          Date: Last 24h
        </div>
      </div>

      <!-- TABLE -->
      <div class="rounded-xl bg-slate-800 overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-slate-900 text-slate-400">
            <tr>
              <th class="px-4 py-3 text-left">Transaction</th>
              <th class="px-4 py-3 text-left">User</th>
              <th class="px-4 py-3 text-left">Risk Score</th>
              <th class="px-4 py-3 text-left">Severity</th>
              <th class="px-4 py-3 text-left">Status</th>
              <th class="px-4 py-3 text-right">Action</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-700">
            {#each transactions as tx}
              <tr class="hover:bg-slate-700/40 transition">

                <!-- Transaction ID -->
                <td class="px-4 py-3 font-mono text-xs">
                  {tx.id.slice(0, 8)}…
                </td>

                <!-- User -->
                <td class="px-4 py-3">
                  {tx.user_id}
                </td>

                <!-- Risk Score -->
                <td class="px-4 py-3">
                  {riskPercent(tx)}%
                </td>

                <!-- Severity -->
                <td class="px-4 py-3">
                  <span
                    class="px-2 py-0.5 rounded-full text-xs
                      {severity(tx) === 'high'
                        ? 'bg-rose-500/20 text-rose-400'
                        : severity(tx) === 'medium'
                        ? 'bg-amber-500/20 text-amber-400'
                        : 'bg-emerald-500/20 text-emerald-400'}"
                  >
                    {severity(tx)}
                  </span>
                </td>

                <!-- Status -->
                <td class="px-4 py-3">
                  <span
                    class="px-2 py-0.5 rounded-full text-xs
                      {status(tx) === 'Blocked'
                        ? 'bg-rose-500/20 text-rose-400'
                        : status(tx) === 'Needs Review'
                        ? 'bg-amber-500/20 text-amber-400'
                        : 'bg-emerald-500/20 text-emerald-400'}"
                  >
                    {status(tx)}
                  </span>
                </td>

                <!-- Action -->
                <td class="px-4 py-3 text-right">
                  <a
                    href={`/transactions/${tx.id}`}
                    class="text-xs text-blue-400 hover:underline"
                  >
                    View
                  </a>
                </td>

              </tr>
            {/each}
          </tbody>

        </table>
      </div>
<div class="flex items-center justify-between pt-4 text-sm text-slate-400">
  <span>
    Page {page} of {Math.ceil(total / pageSize)}
  </span>

  <div class="flex gap-2">
    <button
      class="px-3 py-1 rounded bg-slate-800 disabled:opacity-40"
      disabled={page === 1}
      on:click={() => {
        page--;
        loadTransactions();
      }}
    >
      Previous
    </button>

    <button
      class="px-3 py-1 rounded bg-slate-800 disabled:opacity-40"
      disabled={page * pageSize >= total}
      on:click={() => {
        page++;
        loadTransactions();
      }}
    >
      Next
    </button>
  </div>
</div>

    </div>
  </div>
</section>

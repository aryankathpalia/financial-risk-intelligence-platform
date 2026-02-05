<script lang="ts">
  import { page } from "$app/stores";

type ShapValue = {
  feature: string;
  contribution: number;
};

type TransactionDetail = {
  id: string;
  user_id: string;
  merchant: string;
  amount: number;
  fraud_prob: number;
  anomaly_score: number;
  decision: "ALLOW" | "REVIEW" | "BLOCK";
  ingested_at: string;
  shap_values: ShapValue[];
};


  let transaction: TransactionDetail | null = null;
  let loading = false;
  let error: string | null = null;

  let lastFetchedId: string | null = null;



  function isUUID(id: string): boolean {
    return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(
      id
    );
  }

  // SAFE REACTIVE FETCH (GUARDED)
  $: {
    const id = $page.params.id;

    if (!id || id === lastFetchedId) {
      // do nothing
    } else if (!isUUID(id)) {
      error = "Invalid transaction id";
      transaction = null;
      loading = false;
      lastFetchedId = id;
    } else {
      lastFetchedId = id;
      loading = true;
      error = null;
      transaction = null;

      fetch(`http://127.0.0.1:8000/api/transactions/${id}`)
        .then((res) => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.json();
        })
        .then((data) => {
          transaction = data;
        })
        .catch(() => {
          error = "Unable to load transaction details";
        })
        .finally(() => {
          loading = false;
        });
    }
  }

  function sortedShap(values: ShapValue[]) {
  return [...values].sort(
    (a, b) => Math.abs(b.contribution) - Math.abs(a.contribution)
  );
}

function shapColor(value: number) {
  return value > 0
    ? "text-rose-400"
    : "text-emerald-400";
}

function shapBarColor(value: number) {
  return value > 0
    ? "bg-rose-500"
    : "bg-emerald-500";
}

function shapSummary(shapValues: ShapValue[]) {
  if (!shapValues?.length) return "";

  const top = shapValues[0];
  const direction =
    top.contribution > 0 ? "increases" : "reduces";

  return `${top.feature} ${direction} fraud risk (${top.contribution > 0 ? "+" : ""}${top.contribution.toFixed(2)})`;
}


</script>

<section class="min-h-screen bg-slate-950 p-4 text-slate-100">
  <div class="min-h-[calc(100vh-2rem)] rounded-2xl bg-slate-900/95 p-6">

    <header class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-semibold">Transaction Review</h1>
        <p class="text-sm text-slate-400">
          Detailed risk assessment and model signals
        </p>
      </div>

      {#if transaction}
        <div class="flex gap-2">
          <button class="px-4 py-1.5 text-xs rounded bg-emerald-600 text-white">
            Approve
          </button>
          <button class="px-4 py-1.5 text-xs rounded bg-rose-600 text-white">
            Escalate
          </button>
        </div>
      {/if}
    </header>

    {#if loading}
      <p class="text-slate-400">Loading transaction…</p>

    {:else if error}
      <p class="text-rose-400">{error}</p>

    {:else if transaction}
      <div class="grid grid-cols-4 gap-4 mb-6">
        <div class="bg-slate-800 p-4 rounded">
          <p class="text-xs text-slate-400">Transaction ID</p>
          <p class="font-mono text-sm">{transaction.id}</p>
        </div>

        <div class="bg-slate-800 p-4 rounded">
          <p class="text-xs text-slate-400">User</p>
          <p>{transaction.user_id}</p>
        </div>

        <div class="bg-slate-800 p-4 rounded">
          <p class="text-xs text-slate-400">Amount</p>
          <p class="text-xl font-semibold">
            ${transaction.amount.toFixed(2)}
          </p>
        </div>

        <div class="bg-slate-800 p-4 rounded">
          <p class="text-xs text-slate-400">Decision</p>
          <p>{transaction.decision}</p>
        </div>
      </div>
    {/if}


    {#if transaction}
  <div class="mb-6 bg-slate-800 p-4 rounded">
    <div class="flex justify-between items-center">
      <span class="text-sm text-slate-300">
        Fraud Probability
      </span>

      <span class="text-lg font-semibold text-white">
        {(transaction.fraud_prob * 100).toFixed(2)}%
      </span>
    </div>

    <div class="mt-2 h-2 w-full bg-slate-700 rounded overflow-hidden">
      <div
        class="h-full bg-rose-500"
        style={`width: ${Math.min(
          transaction.fraud_prob * 100,
          100
        )}%`}
      ></div>
    </div>
  </div>
{/if}


    {#if transaction && transaction.shap_values?.length}
  <div class="mt-6 bg-slate-800 rounded p-4">
    <p class="text-xs text-slate-400 uppercase mb-3">
      Model Explanation (SHAP)
    </p>

    <div class="space-y-3">
      {#each sortedShap(transaction.shap_values).slice(0, 8) as shap}
        <div>
          <div class="flex justify-between text-sm mb-1">
            <span class="font-mono text-slate-300">
              {shap.feature}
            </span>
            <span class={`font-mono ${shapColor(shap.contribution)}`}>
              {shap.contribution > 0 ? "+" : ""}
              {shap.contribution.toFixed(4)}
            </span>
          </div>

          <div class="w-full h-2 bg-slate-700 rounded overflow-hidden">
            <div
              class={`h-full ${shapBarColor(shap.contribution)}`}
              style={`width: ${Math.min(
                Math.abs(shap.contribution) * 100,
                100
              )}%`}
            ></div>
          </div>
        </div>
      {/each}
    </div>

    <p class="mt-3 text-xs text-slate-400">
      Positive values increase fraud risk · Negative values reduce risk
    </p>
  </div>
{/if}


{#if transaction && transaction.shap_values?.length}
  <p class="mt-4 text-sm text-slate-300 italic">
    SHAP Insight →
    <span class="text-slate-100">
      {shapSummary(sortedShap(transaction.shap_values))}
    </span>
  </p>
{/if}


  </div>
</section>

<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import SectionHeader from "$lib/ui/SectionHeader.svelte";
  import Panel from "$lib/ui/Panel.svelte";
  import Badge from "$lib/ui/Badge.svelte";
  import Button from "$lib/ui/Button.svelte";
  import { fetchTransactionById } from "$lib/api/transactions";

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
  let abort: AbortController | null = null;

  $: if ($page.params.id && $page.params.id !== lastFetchedId) {
    const id = $page.params.id;
    lastFetchedId = id;

    abort?.abort();
    abort = new AbortController();

    loading = true;
    error = null;
    transaction = null;

    fetchTransactionById(id, abort.signal)
      .then((data) => {
        transaction = data as any;
      })
      .catch((e) => {
        if (e?.name === "AbortError") return;
        error = "Unable to load transaction details";
      })
      .finally(() => {
        if (!abort?.signal.aborted) loading = false;
      });
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
  <div class="min-h-[calc(100vh-2rem)] rounded-2xl bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 ring-1 ring-white/5 shadow-2xl">
    <div class="p-6 space-y-6">
      <SectionHeader
        eyebrow="Investigate"
        title="Transaction review"
        subtitle="Detailed risk assessment, model signals, and explanation for an analyst decision."
      >
        <svelte:fragment slot="actions">
          <Button variant="ghost" size="sm" on:click={() => goto("/transactions")}>
            Back
          </Button>
          {#if transaction}
            <Button variant="primary" size="sm" disabled>
              Approve
            </Button>
            <Button variant="secondary" size="sm" disabled>
              Escalate
            </Button>
          {/if}
        </svelte:fragment>
      </SectionHeader>

    {#if loading}
      <p class="text-slate-400">Loading transaction…</p>

    {:else if error}
      <p class="text-rose-400">{error}</p>

    {:else if transaction}
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <Panel padding="md" subtle>
          <p class="text-xs text-slate-400 uppercase tracking-wide">Transaction</p>
          <p class="mt-2 font-mono text-xs text-slate-200 break-all">{transaction.id}</p>
        </Panel>

        <Panel padding="md" subtle>
          <p class="text-xs text-slate-400 uppercase tracking-wide">User</p>
          <p class="mt-2 text-sm text-slate-200">{transaction.user_id}</p>
        </Panel>

        <Panel padding="md" subtle>
          <p class="text-xs text-slate-400 uppercase tracking-wide">Amount</p>
          <p class="mt-2 text-xl font-semibold text-slate-50 tabular-nums">
            ${transaction.amount.toFixed(2)}
          </p>
        </Panel>

        <Panel padding="md" subtle>
          <p class="text-xs text-slate-400 uppercase tracking-wide">Decision</p>
          <div class="mt-2">
            <Badge
              tone={transaction.decision === "BLOCK" ? "danger" : transaction.decision === "REVIEW" ? "warning" : "success"}
              size="sm"
            >
              {transaction.decision}
            </Badge>
          </div>
        </Panel>
      </div>
    {/if}

    {#if transaction}
      <Panel padding="lg">
        <div class="flex justify-between items-center">
          <span class="text-sm text-slate-300">
            Fraud probability
          </span>
          <span class="text-lg font-semibold text-slate-50 tabular-nums">
            {(transaction.fraud_prob * 100).toFixed(2)}%
          </span>
        </div>

        <div class="mt-3 h-2 w-full bg-slate-800 rounded-full overflow-hidden">
          <div
            class="h-full bg-gradient-to-r from-rose-400 via-rose-500 to-fuchsia-500 rounded-full"
            style={`width: ${Math.min(transaction.fraud_prob * 100, 100)}%`}
          ></div>
        </div>
      </Panel>
    {/if}


    {#if transaction && transaction.shap_values?.length}
      <Panel padding="lg">
        <div class="flex items-start justify-between gap-4 mb-3">
          <div>
            <p class="text-xs text-slate-400 uppercase tracking-wide">
              Model explanation (SHAP)
            </p>
            <p class="text-xs text-slate-500">
              Top contributing features for this decision.
            </p>
          </div>
        </div>

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

              <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  class={`h-full ${shapBarColor(shap.contribution)} rounded-full`}
                  style={`width: ${Math.min(Math.abs(shap.contribution) * 100, 100)}%`}
                ></div>
              </div>
            </div>
          {/each}
        </div>

        <p class="mt-3 text-xs text-slate-400">
          Positive values increase fraud risk · Negative values reduce risk
        </p>
      </Panel>
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
    </div>
</section>

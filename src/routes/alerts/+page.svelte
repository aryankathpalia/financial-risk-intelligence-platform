<script lang="ts">
  import { onMount } from "svelte";
  import { fetchAlerts, type Alert, resolveAlert } from "$lib/api/alerts";
  import { fetchTransactionById, type Transaction } from "$lib/api/transactions";
  import { goto } from "$app/navigation";
  import SectionHeader from "$lib/ui/SectionHeader.svelte";
  import Panel from "$lib/ui/Panel.svelte";
  import Badge from "$lib/ui/Badge.svelte";
  import Button from "$lib/ui/Button.svelte";


  let alerts: Alert[] = [];
  let loading = true;

  let selectedAlert: Alert | null = null;
  let transaction: Transaction | null = null;

  let detailsLoading = false;
  let detailsAbort: AbortController | null = null;

  $: isResolved = selectedAlert?.status === "resolved";
  $: selectedTransactionId = selectedAlert?.transaction_id ?? null;

  // ---------------------------
  // ON MOUNT
  // ---------------------------
  onMount(() => {
    let alive = true;

    (async () => {
      try {
        const data = await fetchAlerts();
        if (!alive) return;

        alerts = data;

        selectedAlert = alerts.length ? alerts[0] : null;

        if (selectedAlert) {
          loadAlertDetails(selectedAlert);
        }

        
      } catch (e) {
        console.error("Failed to load alerts", e);
      } finally {
        if (alive) loading = false;
      }
    })();

    return () => {
      alive = false;
      if (detailsAbort) detailsAbort.abort();
    };
  });

  // ---------------------------
  // HELPERS
  // ---------------------------
  function shortTxn(id: string) {
    return id.slice(0, 6) + "…";
  }

  function timeAgo(date: string) {
    const diff = (Date.now() - new Date(date).getTime()) / 60000;
    return diff < 1 ? "just now" : `${Math.floor(diff)}m ago`;
  }

  // ---------------------------
  // LOAD ALERT DETAILS (UUID ONLY)
  // ---------------------------
  async function loadAlertDetails(alert: Alert) {
    if (detailsAbort) detailsAbort.abort();

    detailsAbort = new AbortController();
    const signal = detailsAbort.signal;

    detailsLoading = true;
    transaction = null;

    try {
      const tx = await fetchTransactionById(alert.transaction_id, signal);

      if (signal.aborted) return;
      transaction = tx;
    } catch (e: any) {
      if (e.name !== "AbortError") {
        console.error("Failed to load alert details", e);
      }
    } finally {
      if (!signal.aborted) {
        detailsLoading = false;
      }
    }
  }

  // ---------------------------
  // APPROVE / BLOCK
  // ---------------------------
  async function handleAction(action: "approve" | "block") {
    if (!selectedAlert) return;

    await resolveAlert(
      selectedAlert.transaction_id,
      action === "approve" ? "APPROVE" : "CONFIRM_FRAUD"
    );

    alerts = alerts.filter(a => a.id !== selectedAlert!.id);
    selectedAlert = alerts.length ? alerts[0] : null;

    transaction = null;

    if (selectedAlert) {
  loadAlertDetails(selectedAlert);
}
  }

  function formatAnomaly(score: number | null) {
  if (score === null || score === undefined) return "—";
  return score.toFixed(3);
}

  function anomalyLabel(score: number | null) {
  if (score === null || score === undefined) return "Unavailable";
  if (score < -0.15) return "Highly anomalous";
  if (score < -0.05) return "Moderately anomalous";
  return "Normal behavior";
}

function hasReasons(alert: Alert | null) {
  return alert?.reasons && alert.reasons.length > 0;
}

function severityColor(sev: string) {
  const s = sev?.toLowerCase();

  if (s === "high") return "bg-rose-500/20 text-rose-400";
  if (s === "medium") return "bg-amber-500/20 text-amber-400";
  return "bg-emerald-500/20 text-emerald-400";
}

function severityTone(sev: string) {
  const s = sev?.toLowerCase();
  if (s === "high") return "danger";
  if (s === "medium") return "warning";
  return "success";
}

function goToTransaction(transactionId: string) {
  goto(`/transactions/${transactionId}`);
}

function reasonDotColor(severity: string) {
  const s = severity?.toLowerCase();
  if (s === "high") return "bg-rose-500";
  if (s === "medium") return "bg-amber-400";
  return "bg-slate-400";
}


</script>





<section class="min-h-screen bg-slate-950 p-4 text-slate-100">
  <div class="min-h-[calc(100vh-2rem)] rounded-2xl bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 ring-1 ring-white/5 shadow-2xl">
    <div class="p-6 h-[calc(100vh-2rem-3rem)] min-h-0 flex flex-col gap-6">
      <SectionHeader
        eyebrow="Investigate"
        title="Alert investigations"
        subtitle="Triage queued alerts, inspect transaction context, and take action with a consistent analyst workflow."
      >
        <svelte:fragment slot="actions">
          <Button variant="soft" size="sm" disabled>
            Create case
          </Button>
        </svelte:fragment>
      </SectionHeader>

      <div class="flex-1 min-h-0 grid grid-cols-12 gap-6">

      <!-- LEFT: ALERT QUEUE -->
      <aside class="col-span-12 xl:col-span-4 min-h-0">
        <Panel padding="lg" class="h-full flex flex-col min-h-0">

        <div class="flex items-center justify-between mb-3">
          <div>
            <h2 class="text-sm font-semibold text-slate-50">Alert queue</h2>
            <p class="text-xs text-slate-400">Pending alerts requiring review.</p>
          </div>
          <Badge tone={loading ? "neutral" : "success"} size="xs">
            {loading ? "Loading" : `${alerts.length} open`}
          </Badge>
        </div>

        <!-- SCROLL CONTAINER (ONLY THIS SCROLLS) -->
        <div class="flex-1 min-h-0 overflow-y-auto space-y-2 pr-1">

          {#if loading}
            <p class="text-sm text-slate-400">Loading alerts…</p>

          {:else if alerts.length === 0}
            <p class="text-sm text-slate-400">No pending alerts</p>

          {:else}
            {#each alerts as alert (alert.id)}
              <button
                type="button"
                class="w-full text-left rounded-lg p-3 cursor-pointer transition border
                  {selectedAlert?.id === alert.id
                    ? 'bg-slate-900/80 border-sky-500/50 shadow-[0_0_0_1px_rgba(56,189,248,0.15)]'
                    : 'bg-slate-950/40 border-slate-800/80 hover:bg-slate-900/70 hover:border-slate-700/80'}"
                on:click={() => {
                  selectedAlert = alert;
                  loadAlertDetails(alert);
                }}
              >
                <div class="flex justify-between items-center">
                  <Badge tone={severityTone(alert.severity)} size="xs">
                    {alert.severity.toUpperCase()}
                  </Badge>


                  <span class="text-xs text-slate-400">
                    {timeAgo(alert.created_at)}
                  </span>
                </div>

                <p class="mt-2 text-sm font-medium font-mono">
                  TXN-{shortTxn(alert.transaction_id)}
                </p>

                <p class="text-xs text-slate-400">
                  Risk {(alert.risk_score * 100).toFixed(1)}%
                </p>
              </button>
            {/each}
          {/if}

        </div>

        </Panel>
      </aside>

      <!-- RIGHT: ALERT DETAILS -->
      <section class="col-span-12 xl:col-span-8 min-h-0">
        <Panel padding="lg" class="h-full flex flex-col min-h-0">

        <!-- HEADER -->
        <div class="flex justify-between items-start">
          <div>
            <h2 class="text-lg font-semibold">
              Alert Investigation
            </h2>
             {#if selectedTransactionId}
  <p class="text-sm text-slate-400 mt-1">
    Transaction TXN-{shortTxn(selectedTransactionId)}
  </p>
{/if}

{#if isResolved}
  <span class="mt-2 inline-block text-xs px-2 py-1 rounded
               bg-emerald-500/20 text-emerald-400">
    Resolved
  </span>
{/if}

          </div>

          <div class="flex gap-2 flex-wrap justify-end">

          {#if selectedTransactionId}
            <Button
              variant="secondary"
              size="xs"
              on:click={() => goToTransaction(selectedTransactionId)}
            >
              View details
            </Button>
{/if}



            <Button variant="ghost" size="xs" disabled>
              Assign
            </Button>
            <Button
              variant="primary"
              size="xs"
              disabled={isResolved}
              on:click={() => handleAction("approve")}
            >
              Approve
            </Button>
            <Button
              variant="secondary"
              size="xs"
              disabled={isResolved}
              on:click={() => handleAction("block")}
            >
              Block
            </Button>


          </div>
        </div>

        <!-- Overflow guard: prevents long content breaking layout -->
        <div class="min-w-0 overflow-x-auto">
          <div class="min-w-[640px]">
        <!-- DETAILS GRID -->
        <div class="grid grid-cols-2 gap-4 mt-6">

          <div class="rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
  <p class="text-xs text-slate-400 uppercase">Transaction</p>

  {#if detailsLoading}
    <p class="mt-2 text-sm text-slate-400">Loading transaction…</p>

  {:else if transaction}
    <p class="mt-2 text-sm">
      Amount: ${transaction.amount.toFixed(2)}
    </p>
    <p class="text-sm">
      Merchant: {transaction.merchant}
    </p>
    <p class="text-sm">
      User: {transaction.user_id}
    </p>

  {:else}
    <p class="mt-2 text-sm text-slate-400">
      No transaction loaded
    </p>
  {/if}
</div>


          <div class="rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
            <p class="text-xs text-slate-400 uppercase">Risk Summary</p>
            {#if selectedAlert}
  <p class="mt-2 text-sm">
    Risk Score: {(selectedAlert.risk_score * 100).toFixed(1)}%
  </p>
  <p class="text-sm">
    Severity: {selectedAlert.severity}
  </p>
  <p class="text-sm">
    Status: {selectedAlert.status}
  </p>
{:else}
  <p class="text-sm text-slate-400">Select an alert</p>
{/if}

          </div>

        </div>
<!-- MODEL SIGNALS (STACKED, SAME WIDTH AS GRID) -->
<div class="mt-4 rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
  <p class="text-xs text-slate-400 uppercase mb-2">
    Model Signals
  </p>

  {#if selectedAlert}
    <div class="space-y-2 text-sm">

<div class="flex justify-between text-white">
  <span>Fraud Probability</span>
  <span class="font-semibold">
    {(selectedAlert.risk_score * 100).toFixed(1)}%
  </span>
</div>

<div class="flex justify-between text-white">
  <span>Isolation Forest Score</span>
  <span class="font-mono">
    {formatAnomaly(selectedAlert.anomaly_score)}
  </span>
</div>




    </div>
  {:else}
    <p class="text-sm text-slate-400">
      Select an alert to view model signals
    </p>
  {/if}
</div>


<!-- DECISION REASONS -->
{#if selectedAlert && hasReasons(selectedAlert)}
  <div class="mt-4 rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
    <p class="text-xs text-slate-400 uppercase mb-2">
      Decision Rationale
    </p>

    <ul class="space-y-1 text-sm">
      {#each selectedAlert.reasons as reason}
        <li class="flex items-start gap-2">
          <span
  class={`mt-1 h-1.5 w-1.5 rounded-full ${reasonDotColor(selectedAlert.severity)}`}
></span>

          <span class="text-slate-200">{reason}</span>
        </li>
      {/each}
    </ul>
  </div>
{/if}
          </div>
        </div>

        </Panel>
      </section>
      </div>
    </div>
  </div>
</section>




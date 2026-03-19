<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { goto } from "$app/navigation";
  import SectionHeader from "$lib/ui/SectionHeader.svelte";
  import MetricCard from "$lib/ui/MetricCard.svelte";
  import Panel from "$lib/ui/Panel.svelte";
  import Badge from "$lib/ui/Badge.svelte";
  import Button from "$lib/ui/Button.svelte";
  import DataTable from "$lib/ui/DataTable.svelte";
  import { fetchDashboardKPIs, type DashboardKPIs } from "$lib/api/dashboard";
  import { fetchAlerts, type Alert } from "$lib/api/alerts";
  import { fetchScoreDistribution } from "$lib/api/analytics";
  import {
    Chart,
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Tooltip,
    Legend
  } from "chart.js";

  Chart.register(
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Tooltip,
    Legend
  );

  Chart.defaults.color = "#cbd5f5";
  Chart.defaults.font.family = "Inter, system-ui, sans-serif";

  let kpisLoading = true;
  let kpisError: string | null = null;
  let alertsLoading = true;
  let alertsError: string | null = null;
  let scoreLoading = true;

  let kpis: DashboardKPIs = {
    total_transactions: 0,
    flagged_transactions: 0,
    high_severity_alerts: 0,
    flag_rate: 0
  };

  let alerts: Alert[] = [];
  let scoreBuckets: number[] = [];

  let distributionCanvas: HTMLCanvasElement | null = null;
  let distributionChart: Chart | null = null;

  onMount(async () => {
    try {
      kpis = await fetchDashboardKPIs();
      kpisError = null;
    } catch {
      kpisError = "Could not load system metrics";
    } finally {
      kpisLoading = false;
    }

    try {
      alerts = await fetchAlerts();
      alertsError = null;
    } catch {
      alertsError = "Could not load recent investigations";
    } finally {
      alertsLoading = false;
    }

    try {
      const res = await fetchScoreDistribution();
      scoreBuckets = res.buckets;
    } catch {
      // non-critical
    } finally {
      scoreLoading = false;
    }
  });

  $: healthScore =
    kpis.total_transactions === 0 ? 100 : Math.max(0, 100 - kpis.flag_rate * 260);

  $: flagRatePctRaw = kpis.flag_rate ?? 0;
  $: flagRatePct =
    flagRatePctRaw > 1
      ? Math.min(100, flagRatePctRaw)
      : Math.min(100, Math.max(0, flagRatePctRaw * 100));

  $: avgRiskScore =
    scoreBuckets.length === 10
      ? (() => {
          const totalCount = scoreBuckets.reduce((a, b) => a + b, 0);
          if (!totalCount) return null;

          const weighted = scoreBuckets.reduce((sum, count, idx) => {
            const midpoint = idx * 10 + 5; // 0–10 -> 5, ... 90–100 -> 95
            return sum + count * midpoint;
          }, 0);

          return weighted / totalCount;
        })()
      : null;

  $: if (distributionCanvas && scoreBuckets.length === 10) {
    distributionChart?.destroy();
    distributionChart = new Chart(distributionCanvas, {
      type: "line",
      data: {
        labels: [
          "0–10%",
          "10–20%",
          "20–30%",
          "30–40%",
          "40–50%",
          "50–60%",
          "60–70%",
          "70–80%",
          "80–90%",
          "90–100%"
        ],
        datasets: [
          {
            label: "Transactions",
            data: scoreBuckets,
            borderColor: "#60a5fa",
            backgroundColor: "rgba(96,165,250,0.15)",
            tension: 0.35,
            fill: true,
            pointRadius: 2,
            pointHoverRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `${Number(ctx.raw).toLocaleString()} transactions`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#94a3b8" }
          },
          y: {
            beginAtZero: true,
            grid: { color: "rgba(255,255,255,0.07)" },
            ticks: { color: "#94a3b8", precision: 0 }
          }
        }
      }
    });
  }

  onDestroy(() => {
    distributionChart?.destroy();
  });
</script>

<section class="min-h-screen bg-slate-950 p-6 text-slate-100">
  <div class="min-h-[calc(100vh-3rem)] max-w-6xl mx-auto space-y-6">
      <SectionHeader
        eyebrow="Dashboard"
        title="System health overview"
        subtitle="A consolidated view across fraud rates, anomaly signals, model confidence, score distribution, and active investigations."
      >
        <svelte:fragment slot="actions">
          <Button variant="secondary" size="sm">Download snapshot</Button>
        </svelte:fragment>
      </SectionHeader>

      {#if kpisError}
        <div class="rounded-lg bg-red-900/30 border border-red-800 p-4 text-red-300 text-sm">
          {kpisError}
        </div>
      {/if}

      <section class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <MetricCard
          label="System health"
          value={`${healthScore.toFixed(0)} / 100`}
          trendLabel="Composite signal across fraud & alerts"
          trendDirection="neutral"
          accent="emerald"
        />
        <MetricCard
          label="Flag rate"
          value={`${(kpis.flag_rate * 100).toFixed(2)}%`}
          trendLabel="Share of traffic under review"
          trendDirection="up"
          accent="amber"
        />
        <MetricCard
          label="High severity alerts"
          value={kpisLoading ? "—" : String(kpis.high_severity_alerts)}
          trendLabel="Active high-risk investigations"
          trendDirection="up"
          accent="rose"
        />
        <MetricCard
          label="Total transactions"
          value={kpisLoading ? "—" : kpis.total_transactions.toLocaleString()}
          trendLabel="Ingested in selected window"
          trendDirection="up"
          accent="blue"
        />
      </section>

      <!-- ANALYTICS -->
      <section class="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <Panel padding="lg" class="xl:col-span-1 h-full">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h2 class="text-sm font-semibold text-slate-100">Fraud metrics</h2>
              <p class="text-xs text-slate-400">
                Observed fraud pressure across recent traffic.
              </p>
            </div>
          </div>

          <div class="mt-4 space-y-4">
            <!-- Flag rate -->
            <div class="space-y-2">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0 flex-1">
                  <p class="text-xs font-medium text-slate-200">Flag rate</p>
                  <p class="mt-0.5 text-xs text-slate-500">
                    Share of traffic escalated for review or block
                  </p>
                </div>
                <div class="w-24 text-right">
                  <p class="text-sm font-semibold tabular-nums text-slate-100">
                    {flagRatePct.toFixed(2)}%
                  </p>
                </div>
              </div>

              <div class="h-1.5 rounded-full bg-slate-800 overflow-hidden">
                <div
                  class={`h-full rounded-full transition-all duration-300 ${
                    flagRatePct < 5 ? "bg-amber-300/70" : "bg-amber-400"
                  }`}
                  style={`width: ${Math.max(2, Math.min(100, flagRatePct))}%`}
                ></div>
              </div>

              {#if flagRatePct < 5}
                <p class="text-[11px] text-slate-500 opacity-80">Low signal rate, shown as subtle indicator.</p>
              {/if}
            </div>

            <!-- Flagged transactions -->
            <div class="space-y-2">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0 flex-1">
                  <p class="text-xs font-medium text-slate-200">Flagged transactions</p>
                  <p class="mt-0.5 text-xs text-slate-500">Count of escalations in window</p>
                </div>
                <div class="w-24 text-right">
                  <p class="text-sm font-semibold tabular-nums text-slate-100">
                    {kpis.flagged_transactions.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>

            <!-- High severity alerts -->
            <div class="space-y-2">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0 flex-1">
                  <p class="text-xs font-medium text-slate-200">High severity alerts</p>
                  <p class="mt-0.5 text-xs text-slate-500">Critical cases requiring attention</p>
                </div>
                <div class="w-24 text-right flex items-center justify-end gap-2">
                  <Badge tone="danger" size="xs">P1</Badge>
                  <span class="text-sm font-semibold tabular-nums text-slate-100">
                    {kpis.high_severity_alerts}
                  </span>
                </div>
              </div>
            </div>

            <!-- Average risk score -->
            <div class="space-y-2">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0 flex-1">
                  <p class="text-xs font-medium text-slate-200">Average risk score</p>
                  <p class="mt-0.5 text-xs text-slate-500">Estimated from score distribution</p>
                </div>
                <div class="w-24 text-right">
                  <p class="text-sm font-semibold tabular-nums text-slate-100">
                    {avgRiskScore === null ? "—" : `${avgRiskScore.toFixed(1)}%`}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </Panel>

        <Panel padding="lg" class="xl:col-span-2 h-full">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h2 class="text-sm font-semibold text-slate-100">Score distribution</h2>
              <p class="text-xs text-slate-400">Production risk score buckets.</p>
            </div>
            {#if scoreLoading}
              <Badge tone="neutral" size="xs">Updating…</Badge>
            {:else}
              <Badge tone="success" size="xs">Live</Badge>
            {/if}
          </div>

          <div class="h-64 flex items-center justify-center">
            <canvas bind:this={distributionCanvas}></canvas>
          </div>
        </Panel>

      </section>

      <section class="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <!-- DECISION POLICY -->
        <Panel padding="lg">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h2 class="text-sm font-semibold text-slate-100">Decision policy</h2>
              <p class="text-xs text-slate-400">
                Model output mapped to analyst actions and thresholds.
              </p>
            </div>
          </div>

          <div class="space-y-4 text-sm">
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-slate-400">ALLOW &lt; 50%</span>
                <span class="text-emerald-300 font-semibold">
                  {(100 - kpis.flag_rate * 100).toFixed(2)}%
                </span>
              </div>
              <div class="h-2 rounded-full bg-slate-800 overflow-hidden">
                <div
                  class="h-full rounded-full bg-emerald-500/80"
                  style={`width: ${(100 - kpis.flag_rate * 100).toFixed(2)}%`}
                ></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between mb-1">
                <span class="text-slate-400">REVIEW 50–70%</span>
                <span class="text-amber-300 font-semibold">—</span>
              </div>
              <div class="h-2 rounded-full bg-slate-800 overflow-hidden">
                <div class="h-full rounded-full bg-amber-400/80 w-[22%]"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between mb-1">
                <span class="text-slate-400">BLOCK &gt; 70%</span>
                <span class="text-rose-300 font-semibold">—</span>
              </div>
              <div class="h-2 rounded-full bg-slate-800 overflow-hidden">
                <div class="h-full rounded-full bg-rose-500/80 w-[12%]"></div>
              </div>
            </div>
          </div>

          <div class="pt-4 mt-4 border-t border-white/5 text-xs text-slate-400 leading-relaxed">
            Thresholds are tuned offline and monitored online for stability.
          </div>
        </Panel>

        <!-- ANOMALY SIGNALS -->
        <Panel padding="lg" class="xl:col-span-1">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h2 class="text-sm font-semibold text-slate-100">Anomaly signals</h2>
              <p class="text-xs text-slate-400">Bucket snapshot from production traffic.</p>
            </div>
          </div>

          {#if !scoreBuckets.length}
            <p class="mt-2 text-xs text-slate-400">
              Score histogram not available yet for this window.
            </p>
          {:else}
            <div class="mt-2 grid grid-cols-2 gap-3 text-xs text-slate-300">
              {#each scoreBuckets.slice(0, 4) as value, idx}
                <div class="flex flex-col gap-1">
                  <div class="flex justify-between">
                    <span class="text-slate-500">
                      {idx * 10}–{(idx + 1) * 10}%
                    </span>
                    <span class="tabular-nums">{value.toLocaleString()}</span>
                  </div>
                  <div class="h-1.5 rounded-full bg-slate-800 overflow-hidden">
                    <div
                      class="h-full rounded-full bg-gradient-to-r from-sky-400 via-sky-500 to-indigo-500"
                      style={`width: ${Math.min(
                        100,
                        (value / (kpis.total_transactions || 1)) * 420
                      )}%`}
                    ></div>
                  </div>
                </div>
              {/each}
            </div>
          {/if}
        </Panel>

        <!-- MODEL CONFIDENCE -->
        <Panel padding="lg">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h2 class="text-sm font-semibold text-slate-100">Model confidence</h2>
              <p class="text-xs text-slate-400">Qualitative stability and coverage.</p>
            </div>
          </div>

          <div class="mt-3 space-y-3 text-xs">
            <div>
              <p class="text-slate-400 mb-1">Confidence band</p>
              <div class="h-2 rounded-full bg-slate-800 overflow-hidden">
                <div class="h-full rounded-full bg-gradient-to-r from-emerald-400 via-sky-400 to-amber-400 w-[78%]"></div>
              </div>
              <p class="mt-1 text-[11px] text-slate-500">
                Informal signal combining offline AUC and online stability.
              </p>
            </div>

            <div class="flex items-center justify-between">
              <span class="text-slate-400">Coverage of high-risk band</span>
              <span class="tabular-nums text-slate-50 font-semibold">
                {kpis.flag_rate ? (kpis.flag_rate * 100).toFixed(1) : "0.0"}%
              </span>
            </div>
          </div>
        </Panel>
      </section>

      <Panel padding="lg">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-sm font-semibold text-slate-100">Recent alerts</h2>
            <p class="text-xs text-slate-400">
              Latest high-risk alerts requiring analyst review.
            </p>
          </div>

          <Button variant="ghost" size="xs" on:click={() => goto("/alerts")}>
            View all
          </Button>
        </div>

        <DataTable maxHeight="360px">
          <svelte:fragment slot="head">
              <tr>
                <th class="px-4 py-3 text-left font-medium">Alert</th>
                <th class="px-4 py-3 text-left font-medium">User</th>
                <th class="px-4 py-3 text-left font-medium">Risk score</th>
                <th class="px-4 py-3 text-left font-medium">Severity</th>
                <th class="px-4 py-3 text-left font-medium">Status</th>
                <th class="px-4 py-3 text-right font-medium">Action</th>
              </tr>
          </svelte:fragment>

          {#if alertsLoading}
            <tr>
              <td colspan="6" class="px-4 py-6 text-center text-slate-400">
                Loading alerts…
              </td>
            </tr>
          {:else if alertsError}
            <tr>
              <td colspan="6" class="px-4 py-6 text-center text-rose-400">
                {alertsError}
              </td>
            </tr>
          {:else if alerts.length === 0}
            <tr>
              <td colspan="6" class="px-4 py-6 text-center text-slate-400">
                No alerts found.
              </td>
            </tr>
          {:else}
            {#each alerts.slice(0, 10) as alert}
              <tr class="hover:bg-slate-900/70 transition-colors">
                <td class="px-4 py-3 font-mono text-xs text-slate-300">
                  {alert.transaction_id}
                </td>
                <td class="px-4 py-3 text-slate-300">
                  {alert.user_id}
                </td>
                <td class="px-4 py-3 tabular-nums">
                  {alert.risk_score.toFixed(1)}%
                </td>
                <td class="px-4 py-3">
                  <Badge
                    tone={alert.severity?.toLowerCase() === "high"
                      ? "danger"
                      : alert.severity?.toLowerCase() === "medium"
                      ? "warning"
                      : "success"}
                    size="xs"
                  >
                    {alert.severity}
                  </Badge>
                </td>
                <td class="px-4 py-3">
                  <Badge
                    tone={alert.status.toLowerCase() === "pending" ? "warning" : "success"}
                    size="xs"
                  >
                    {alert.status}
                  </Badge>
                </td>
                <td class="px-4 py-3 text-right">
                  <Button
                    variant="soft"
                    size="xs"
                    on:click={() => goto(`/transactions/${encodeURIComponent(alert.transaction_id)}`)}
                  >
                    View
                  </Button>
                </td>
              </tr>
            {/each}
          {/if}
        </DataTable>
      </Panel>
    </div>
</section>


<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { fetchDashboardKPIs, type DashboardKPIs } from "$lib/api/dashboard";
  import { fetchAlerts, type Alert } from "$lib/api/alerts";
  import { fetchScoreDistribution } from "$lib/api/analytics";
  /*  CHART.JS SETUP */
  import {
    Chart,
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    BarController,
    BarElement,
    Tooltip,
    Legend,
  } from "chart.js";

  Chart.register(
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    BarController,
    BarElement,
    Tooltip,
    Legend
  );

  Chart.defaults.color = "#cbd5f5"; 
  Chart.defaults.font.family = "Inter, system-ui, sans-serif";

  /*  KPI STATE */
  let kpisLoading = true;
  let kpisError: string | null = null;

  let kpis: DashboardKPIs = {
    total_transactions: 0,
    flagged_transactions: 0,
    high_severity_alerts: 0,
    flag_rate: 0,
  };

  /* 
     ALERTS STATE
 */
  let alerts: Alert[] = [];
  let alertsLoading = true;
  let alertsError: string | null = null;

  /* 
     CHART REFS
 */
  let distributionCanvas: HTMLCanvasElement | null = null;



  let distributionChart: Chart | null = null;

  

  let scoreBuckets: number[] = [];
  let scoreDistLoading = true;






  /* 
     LOAD DATA
 */
  onMount(async () => {
    try {
      kpis = await fetchDashboardKPIs();
      kpisError = null;
    } catch {
      kpisError = "Could not load dashboard data";
    } finally {
      kpisLoading = false;
    }


    try {
  const res = await fetchScoreDistribution();
  scoreBuckets = res.buckets;
} catch {
  console.error("Failed to load score distribution");
} finally {
  scoreDistLoading = false;
}


    try {
      alerts = await fetchAlerts();
      alertsError = null;
    } catch {
      alertsError = "Could not load alerts";
    } finally {
      alertsLoading = false;
    }
  });

 


  /* 
     INIT DISTRIBUTION CHART
 */
$: if (
  distributionCanvas &&
  scoreBuckets.length === 10 &&
  !distributionChart
) {
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
      "90–100%",
    ],
    datasets: [
      {
        label: "Transactions",
        data: scoreBuckets,
        borderColor: "#60a5fa",
        backgroundColor: "rgba(96,165,250,0.15)",
        tension: 0.35,
        fill: true,
        pointRadius: 3,
        pointHoverRadius: 6,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
tooltip: {
  callbacks: {
    label: ctx => `${Number(ctx.raw).toLocaleString()} transactions`,
  },
},

    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: "#94a3b8" },
      },
      y: {
        beginAtZero: true,
        grid: { color: "rgba(255,255,255,0.07)" },
        ticks: {
          color: "#94a3b8",
          precision: 0,
        },
      },
    },
  },
});

}


</script>





<!-- OUTER MATTE (creates premium black border) -->
<section class="min-h-screen bg-slate-950 p-4 text-slate-100">
  

  <!-- INSET CANVAS -->
  <div
    class="
      min-h-[calc(100vh-2rem)]
      rounded-2xl
      bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950
      ring-1 ring-white/5
      shadow-2xl
    "
  >
    <!-- CONTENT WRAPPER -->
    <div class="p-6 space-y-6">

{#if kpisError}
  <div class="rounded-lg bg-red-900/30 border border-red-800 p-4 text-red-300">
    {kpisError}
  </div>
{/if}


      <!-- HEADER -->
      <header class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-semibold tracking-tight">
            System Monitor
          </h1>
          <p class="text-sm text-slate-400 mt-1">
            Real-time risk assessment and transaction monitoring
          </p>
        </div>

        <div class="flex items-center gap-2">
          <button class="px-3 py-1.5 text-xs rounded-md bg-slate-800 text-slate-300 hover:bg-slate-700">
            24H
          </button>
          <button class="px-3 py-1.5 text-xs rounded-md bg-slate-800 text-slate-300 hover:bg-slate-700">
            7D
          </button>
          <button class="px-3 py-1.5 text-xs rounded-md bg-slate-800 text-slate-300 hover:bg-slate-700">
            30D
          </button>
          <button class="ml-2 px-4 py-1.5 text-xs rounded-md bg-blue-600 hover:bg-blue-500 text-white">
            Export Report
          </button>
        </div>
      </header>

      <!-- KPI CARDS -->
      <section class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">

        <div class="rounded-xl bg-slate-800 p-5 flex items-start justify-between">
          <div>
            <p class="text-xs uppercase tracking-wide text-slate-400">
              Total Transactions
            </p>
            <p class="mt-3 text-3xl font-semibold leading-none">
  {kpisLoading ? "—" : kpis.total_transactions.toLocaleString()}

</p>

            <p class="mt-2 text-xs text-emerald-400 flex items-center gap-1">
              ▲ —%
              <span class="text-slate-500">vs previous</span>
            </p>
          </div>
          <div class="h-10 w-10 rounded-lg bg-slate-700"></div>
        </div>

        <div class="rounded-xl bg-slate-800 p-5 flex items-start justify-between">
          <div>
            <p class="text-xs uppercase tracking-wide text-slate-400">
              Flagged Transactions
            </p>
            <p class="mt-3 text-3xl font-semibold leading-none">
  {kpisLoading ? "—" : kpis.flagged_transactions.toLocaleString()}

</p>

            <p class="mt-2 text-xs text-amber-400 flex items-center gap-1">
              ▲ —%
            </p>
          </div>
          <div class="h-10 w-10 rounded-lg bg-slate-700"></div>
        </div>

        <div class="rounded-xl bg-slate-800 p-5 flex items-start justify-between">
          <div>
            <p class="text-xs uppercase tracking-wide text-slate-400">
              High Severity Alerts
            </p>
            <p class="mt-3 text-3xl font-semibold leading-none">
  {kpisLoading ? "—" : kpis.high_severity_alerts}

</p>

            <p class="mt-2 text-xs text-rose-400 flex items-center gap-1">
              ▲ —
            </p>
          </div>
          <div class="h-10 w-10 rounded-lg bg-slate-700"></div>
        </div>

        <div class="rounded-xl bg-slate-800 p-5 flex items-start justify-between">
          <div>
            <p class="text-xs uppercase tracking-wide text-slate-400">
              Flag Rate
            </p>

            <p class="mt-3 text-3xl font-semibold leading-none">
              {(kpis.flag_rate * 100).toFixed(2)}%
            </p>


            <p class="mt-2 text-xs text-emerald-400 flex items-center gap-1">
              ▼ —%
            </p>
          </div>
          <div class="h-10 w-10 rounded-lg bg-slate-700"></div>
        </div>

      </section>

<!-- CHARTS -->
<section class="grid grid-cols-1 xl:grid-cols-3 gap-4">

  <!-- LEFT: SCORE DISTRIBUTION (2 columns) -->
  <div class="xl:col-span-2 rounded-xl bg-slate-800 p-5">
    <div class="flex items-center justify-between mb-4">
      <div>
        <h2 class="text-sm font-semibold">Score Distribution</h2>
        <p class="text-xs text-slate-400">
          Risk score buckets across all processed transactions
        </p>
      </div>
    </div>

    <div class="h-72">
      <canvas bind:this={distributionCanvas}></canvas>
    </div>
  </div>

  <!-- RIGHT: DECISION POLICY -->
  <div class="rounded-xl bg-slate-800 p-5 flex flex-col justify-between">

    <div>
      <h2 class="text-sm font-semibold mb-1">Decision Policy</h2>
      <p class="text-xs text-slate-400 mb-4">
        Model output → enforcement thresholds
      </p>

      <div class="space-y-4 text-sm">

        <!-- ALLOW -->
        <div>
          <div class="flex justify-between mb-1">
            <span class="text-slate-400">ALLOW &lt; 50%</span>
            <span class="text-emerald-400 font-semibold">
              {(100 - kpis.flag_rate * 100).toFixed(2)}%
            </span>
          </div>
          <div class="h-2 rounded bg-slate-700 overflow-hidden">
            <div
              class="h-full bg-emerald-500"
              style="width: {(100 - kpis.flag_rate * 100).toFixed(2)}%"
            />
          </div>
        </div>

        <!-- REVIEW -->
        <div>
          <div class="flex justify-between mb-1">
            <span class="text-slate-400">REVIEW 50–70%</span>
            <span class="text-amber-400 font-semibold">
              {(kpis.flag_rate * 100 - 0.06).toFixed(2)}%
            </span>
          </div>
          <div class="h-2 rounded bg-slate-700 overflow-hidden">
            <div
              class="h-full bg-amber-500"
              style="width: {(kpis.flag_rate * 100 - 0.06).toFixed(2)}%"
            />
          </div>
        </div>

        <!-- BLOCK -->
        <div>
          <div class="flex justify-between mb-1">
            <span class="text-slate-400">BLOCK &gt; 70%</span>
            <span class="text-rose-400 font-semibold">0.06%</span>
          </div>
          <div class="h-2 rounded bg-slate-700 overflow-hidden">
            <div
              class="h-full bg-rose-500"
              style="width: 0.06%"
            />
          </div>
        </div>

      </div>
    </div>

    <!-- FOOTNOTE -->
    <div class="pt-4 mt-4 border-t border-white/5 text-xs text-slate-400 leading-relaxed">
      Thresholds selected using offline IEEE validation.
      <br />
      Distribution reflects unlabeled production batches.
    </div>
  </div>

</section>



      <!-- TABLE -->
<!-- ALERTS TABLE -->
<section class="rounded-xl bg-slate-800/90 ring-1 ring-white/5 p-5">

  <!-- TABLE HEADER -->
  <div class="flex items-center justify-between mb-4">
    <div>
      <h2 class="text-sm font-semibold">
        Recent High-Risk Alerts
      </h2>
      <p class="text-xs text-slate-400">
        Live anomalies requiring analyst review
      </p>
    </div>

    <button
  class="text-xs text-blue-400 hover:underline"
  on:click={() => goto("/alerts")}
>
  View all alerts
</button>

  </div>

  <!-- TABLE -->
  <div
  class="
    max-h-[420px]
    overflow-y-auto
    overflow-x-hidden
    rounded-lg
    ring-1 ring-white/5
  "
>

    <table class="w-full text-sm">
      <thead class="bg-slate-900/60 text-slate-400 text-xs uppercase tracking-wide">
        <tr>
          <th class="px-4 py-3 text-left">Status</th>
          <th class="px-4 py-3 text-left">Transaction</th>
          <th class="px-4 py-3 text-left">User</th>
          <th class="px-4 py-3 text-left">Risk Score</th>
          <th class="px-4 py-3 text-left">Severity</th>
          <th class="px-4 py-3 text-right">Action</th>
        </tr>
      </thead>

<tbody class="divide-y divide-slate-800">

  {#if alertsLoading}
    <tr>
      <td colspan="6" class="px-4 py-6 text-center text-slate-400">
        Loading alerts…
      </td>
    </tr>

  {:else if alertsError}
    <tr>
      <td colspan="6" class="px-4 py-6 text-center text-red-400">
        {alertsError}
      </td>
    </tr>

  {:else if alerts.length === 0}
    <tr>
      <td colspan="6" class="px-4 py-6 text-center text-slate-400">
        No high-risk alerts found
      </td>
    </tr>

  {:else}
    {#each alerts as alert}
      <tr class="bg-slate-900/40 hover:bg-slate-800 transition">

        <!-- STATUS -->
        <td class="px-4 py-3">
          <span
            class="inline-flex items-center px-2 py-0.5 rounded-full text-xs
              {alert.status.toLowerCase() === 'pending'
                ? 'bg-amber-500/10 text-amber-400'
                : 'bg-emerald-500/10 text-emerald-400'}">
            {alert.status}
          </span>
        </td>

        <!-- TRANSACTION -->
        <td class="px-4 py-3 font-mono text-xs text-slate-300">
          {alert.transaction_id}
        </td>

        <!-- USER -->
        <td class="px-4 py-3 text-slate-300">
        {alert.user_id}
        </td>


        <!-- RISK SCORE -->
        <td class="px-4 py-3 font-semibold">
          {alert.risk_score.toFixed(1)}%

        </td>

        <!-- SEVERITY -->
        <td class="px-4 py-3">
<span
  class="inline-flex items-center px-2 py-0.5 rounded-full text-xs
    {alert.status.toLowerCase() === 'pending'
      ? 'bg-amber-500/10 text-amber-400'
      : 'bg-emerald-500/10 text-emerald-400'}">
  {alert.status}
</span>

        </td>

        <!-- ACTION -->
        <td class="px-4 py-3 text-right">
          <button
  class="text-xs text-blue-400 hover:underline"
  on:click={() => goto(`/transactions/${alert.transaction_id}`)}
>
  Review
</button>

        </td>

      </tr>
    {/each}
  {/if}

</tbody>

    </table>
  </div>
</div>
</section>

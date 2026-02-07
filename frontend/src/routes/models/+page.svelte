<script lang="ts">
  import { onMount } from "svelte";

  const API = import.meta.env.VITE_API_BASE_URL;

  let offline: any = null;
  let online: any = null;
  let loading = true;
  let error: string | null = null;

  onMount(async () => {
    try {
      const [offlineRes, onlineRes] = await Promise.all([
        fetch(`${API}/api/models/offline-metrics`),
        fetch(`${API}/api/models/online-stats`)
      ]);

      if (!offlineRes.ok || !onlineRes.ok) {
        throw new Error("Failed to load model metrics");
      }

      offline = await offlineRes.json();
      online = await onlineRes.json();
    } catch {
      error = "Unable to load model metrics";
    } finally {
      loading = false;
    }
  });
</script>


<section class="min-h-screen bg-slate-950 p-4 text-slate-100">
  <div class="rounded-2xl bg-slate-900/95 p-6 space-y-8">

    <!-- HEADER -->
    <header>
      <h1 class="text-2xl font-semibold">Model Evaluation & Monitoring</h1>
      <p class="text-sm text-slate-400 mt-1">
        Offline validation (derived) & live production behavior
      </p>
    </header>

    {#if loading}
      <p class="text-slate-400">Loading model metrics…</p>

    {:else if error}
      <p class="text-rose-400">{error}</p>

    {:else if offline?.status === "missing"}
  <p class="text-amber-400">
    Offline metrics not generated yet.
  </p>

    {:else}


    <!-- OFFLINE EVALUATION -->
    <section class="rounded-xl bg-slate-800 p-5 space-y-6">
      <h2 class="text-sm font-semibold text-emerald-400">
        Offline Validation (IEEE – Identity Aware)
      </h2>

      <!-- KPI STRIP -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="rounded-lg bg-slate-900 p-4">
          <p class="text-xs text-slate-400 uppercase">ROC-AUC</p>
          <p class="mt-2 text-xl font-semibold">{offline.roc_auc}</p>
        </div>

        <div class="rounded-lg bg-slate-900 p-4">
          <p class="text-xs text-slate-400 uppercase">Operating Threshold</p>
          <p class="mt-2 text-xl font-semibold">
            {offline.operating_point.threshold}
          </p>
        </div>

        <div class="rounded-lg bg-slate-900 p-4">
          <p class="text-xs text-slate-400 uppercase">Recall</p>
          <p class="mt-2 text-xl font-semibold">
            {(offline.operating_point.recall * 100).toFixed(2)}%
          </p>
        </div>

        <div class="rounded-lg bg-slate-900 p-4">
          <p class="text-xs text-slate-400 uppercase">False Positive Rate</p>
          <p class="mt-2 text-xl font-semibold">
            {(offline.operating_point.fpr * 100).toFixed(2)}%
          </p>
        </div>
      </div>

      <!-- THRESHOLD SWEEP -->
      <div class="space-y-3">
        <p class="text-xs text-slate-400 uppercase tracking-wide">
          Threshold Sweep (Validation Set)
        </p>

        <table class="w-full text-sm">
          <thead class="text-slate-400 border-b border-slate-700">
            <tr>
              <th class="py-2 text-left">Threshold</th>
              <th class="py-2 text-left">Recall</th>
              <th class="py-2 text-left">FPR</th>
            </tr>
          </thead>
          <tbody>
            {#each offline.threshold_sweep as row}
              <tr class="border-b border-slate-800">
                <td class="py-2">{row.threshold}</td>
                <td class="py-2">{(row.recall * 100).toFixed(2)}%</td>
                <td class="py-2">{(row.fpr * 100).toFixed(2)}%</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>

      <!-- SCORE DISTRIBUTION -->
      <div class="space-y-3">
        <p class="text-xs text-slate-400 uppercase tracking-wide">
          Score Distribution (Validation)
        </p>

        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
          {#each Object.entries(offline.score_distribution ?? {}) as [k, v]}
            <div class="rounded-lg bg-slate-900 p-3">
              <p class="text-xs text-slate-400 uppercase">{k}</p>
              <p class="mt-1 font-semibold">{v}</p>
            </div>
          {/each}
        </div>
      </div>

      <!-- FEATURE IMPORTANCE -->
      <div class="space-y-3">
        <p class="text-xs text-slate-400 uppercase tracking-wide">
          Top Feature Importance (Gain)
        </p>

        <div class="grid md:grid-cols-2 gap-2">
          {#each offline.feature_importance as f}
            <div class="flex justify-between rounded bg-slate-900 px-3 py-2 text-sm">
              <span class="truncate">{f.feature}</span>
              <span class="text-slate-400">{f.gain}</span>
            </div>
          {/each}
        </div>
      </div>

      <p class="text-xs text-slate-400 italic">
        Offline metrics are static and valid until the next model retrain.
      </p>
    </section>

    <!-- ONLINE MONITORING -->
    <section class="rounded-xl bg-slate-800 p-5 space-y-4">
      <h2 class="text-sm font-semibold text-blue-400">
        Online Monitoring (Unlabeled Production Data)
      </h2>

      <div class="grid grid-cols-3 gap-4 max-w-2xl">
        <div class="rounded-lg bg-slate-900 p-4">
          <p class="text-xs text-slate-400 uppercase">ALLOW %</p>
          <p class="mt-2 text-xl font-semibold">{online.allow_pct}%</p>
        </div>

        <div class="rounded-lg bg-slate-900 p-4">
          <p class="text-xs text-slate-400 uppercase">REVIEW %</p>
          <p class="mt-2 text-xl font-semibold">{online.review_pct}%</p>
        </div>

        <div class="rounded-lg bg-slate-900 p-4">
          <p class="text-xs text-slate-400 uppercase">BLOCK %</p>
          <p class="mt-2 text-xl font-semibold">{online.block_pct}%</p>
        </div>
      </div>

      <p class="text-xs text-slate-400">
        Live production behavior (no labels). Used for drift & ops monitoring.
      </p>
    </section>

    {/if}
  </div>
</section>

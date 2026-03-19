<script lang="ts">
  import { onMount } from "svelte";
  import SectionHeader from "$lib/ui/SectionHeader.svelte";
  import Panel from "$lib/ui/Panel.svelte";
  import Badge from "$lib/ui/Badge.svelte";
  import DataTable from "$lib/ui/DataTable.svelte";

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
  <div class="min-h-[calc(100vh-2rem)] rounded-2xl bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 ring-1 ring-white/5 shadow-2xl">
    <div class="p-6 space-y-6">
      <SectionHeader
        eyebrow="Models"
        title="Model evaluation & monitoring"
        subtitle="Offline validation metrics alongside unlabeled production behavior for drift and operational monitoring."
      />

    {#if loading}
      <p class="text-slate-400">Loading model metrics…</p>

    {:else if error}
      <p class="text-rose-400">{error}</p>

    {:else if offline?.status === "missing"}
      <div class="rounded-lg bg-amber-500/10 border border-amber-500/20 p-4 text-amber-200 text-sm">
        Offline metrics not generated yet.
      </div>

    {:else}


    <!-- OFFLINE EVALUATION -->
    <Panel padding="lg">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h2 class="text-sm font-semibold text-slate-50">
            Offline validation
          </h2>
          <p class="text-xs text-slate-400">
            IEEE identity-aware evaluation metrics and threshold selection.
          </p>
        </div>
        <Badge tone="success" size="xs">Derived</Badge>
      </div>

      <!-- KPI STRIP -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
          <p class="text-xs text-slate-400 uppercase">ROC-AUC</p>
          <p class="mt-2 text-xl font-semibold">{offline.roc_auc}</p>
        </div>

        <div class="rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
          <p class="text-xs text-slate-400 uppercase">Operating Threshold</p>
          <p class="mt-2 text-xl font-semibold">
            {offline.operating_point.threshold}
          </p>
        </div>

        <div class="rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
          <p class="text-xs text-slate-400 uppercase">Recall</p>
          <p class="mt-2 text-xl font-semibold">
            {(offline.operating_point.recall * 100).toFixed(2)}%
          </p>
        </div>

        <div class="rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
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
        <DataTable maxHeight="260px">
          <svelte:fragment slot="head">
            <tr>
              <th class="px-4 py-3 text-left font-medium">Threshold</th>
              <th class="px-4 py-3 text-left font-medium">Recall</th>
              <th class="px-4 py-3 text-left font-medium">FPR</th>
            </tr>
          </svelte:fragment>

          {#each offline.threshold_sweep as row}
            <tr class="hover:bg-slate-900/70 transition-colors">
              <td class="px-4 py-3 tabular-nums">{row.threshold}</td>
              <td class="px-4 py-3 tabular-nums">{(row.recall * 100).toFixed(2)}%</td>
              <td class="px-4 py-3 tabular-nums">{(row.fpr * 100).toFixed(2)}%</td>
            </tr>
          {/each}
        </DataTable>
      </div>

      <!-- SCORE DISTRIBUTION -->
      <div class="space-y-3">
        <p class="text-xs text-slate-400 uppercase tracking-wide">
          Score Distribution (Validation)
        </p>

        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
          {#each Object.entries(offline.score_distribution ?? {}) as [k, v]}
            <div class="rounded-lg bg-slate-950/40 border border-slate-800/80 p-3">
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
            <div class="flex justify-between rounded-lg border border-slate-800/80 bg-slate-950/40 px-3 py-2 text-sm">
              <span class="truncate">{f.feature}</span>
              <span class="text-slate-400">{f.gain}</span>
            </div>
          {/each}
        </div>
      </div>

      <p class="text-xs text-slate-400 italic">
        Offline metrics are static and valid until the next model retrain.
      </p>
    </Panel>

    <!-- ONLINE MONITORING -->
    <Panel padding="lg">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h2 class="text-sm font-semibold text-slate-50">
            Online monitoring
          </h2>
          <p class="text-xs text-slate-400">
            Live production behavior (no labels). Used for drift and ops monitoring.
          </p>
        </div>
        <Badge tone="neutral" size="xs">Production</Badge>
      </div>

      <div class="grid grid-cols-3 gap-4 max-w-2xl">
        <div class="rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
          <p class="text-xs text-slate-400 uppercase">ALLOW %</p>
          <p class="mt-2 text-xl font-semibold">{online.allow_pct}%</p>
        </div>

        <div class="rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
          <p class="text-xs text-slate-400 uppercase">REVIEW %</p>
          <p class="mt-2 text-xl font-semibold">{online.review_pct}%</p>
        </div>

        <div class="rounded-lg bg-slate-950/40 border border-slate-800/80 p-4">
          <p class="text-xs text-slate-400 uppercase">BLOCK %</p>
          <p class="mt-2 text-xl font-semibold">{online.block_pct}%</p>
        </div>
      </div>
    </Panel>

    {/if}
    </div>
  </div>
</section>

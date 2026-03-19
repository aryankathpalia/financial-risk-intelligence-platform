<script lang="ts">
  export let label: string;
  export let value: string;
  export let trendLabel: string | null = null;
  export let trendDirection: 'up' | 'down' | 'neutral' = 'neutral';
  export let accent: 'blue' | 'emerald' | 'amber' | 'rose' | 'slate' = 'slate';
  let className = '';
  export { className as class };
</script>

<div
  {...$$restProps}
  class={`group relative rounded-xl border border-slate-800/60 bg-slate-900/90 px-4 py-4 md:px-5 md:py-5 min-h-[112px] ${className}`}
>
  <div class="flex items-start justify-between gap-3">
    <div>
      <p class="text-[11px] uppercase tracking-[0.18em] text-slate-500">
        {label}
      </p>

      <p class="mt-2 text-2xl md:text-3xl font-semibold tabular-nums text-slate-100">
        {value}
      </p>

      {#if trendLabel}
        <p class="mt-2 text-[11px] md:text-xs text-slate-400 flex items-center gap-1.5">
          {#if trendDirection !== 'neutral'}
            <span
              class={`inline-flex h-3 w-3 items-center justify-center rounded-full border text-[9px]
                ${
                  trendDirection === 'up'
                    ? 'border-emerald-400/40 text-emerald-400 bg-emerald-500/5'
                    : 'border-rose-400/40 text-rose-400 bg-rose-500/5'
                }`}
            >
              {trendDirection === 'up' ? '▲' : '▼'}
            </span>
          {/if}

          <span>{trendLabel}</span>
        </p>
      {/if}
    </div>

    <div
      class={`mt-1 h-8 w-8 md:h-9 md:w-9 rounded-md border border-slate-700/70
        ${
          accent === 'blue'
            ? 'bg-sky-500/10'
            : accent === 'emerald'
            ? 'bg-emerald-500/10'
            : accent === 'amber'
            ? 'bg-amber-400/10'
            : accent === 'rose'
            ? 'bg-rose-500/10'
            : 'bg-slate-600/20'
        }`}
    >
      <slot name="icon" />
    </div>
  </div>
</div>


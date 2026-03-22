<script lang="ts">
  import {
    Activity,
    ShieldCheck,
    Siren,
    ChartLine,
    Workflow,
    Eye
  } from "lucide-svelte";

  export let title: string;
  export let description: string;
  export let icon: 'pulse' | 'shield' | 'alert' | 'chart' | 'flow' | 'eye';
  export let variant: 'default' | 'tinted' | 'highlight' = 'default';
</script>

<article class={`group relative overflow-hidden rounded-2xl p-4 md:p-5 backdrop-blur-md shadow-[0_4px_24px_rgba(15,23,42,0.45)] transition duration-300 hover:scale-[1.02]
  ${
    variant === 'highlight'
      ? 'border border-sky-500/35 bg-gradient-to-br from-slate-900/85 via-slate-900/80 to-indigo-950/45 hover:border-sky-400/55 hover:shadow-[0_12px_34px_rgba(56,189,248,0.2)]'
      : variant === 'tinted'
      ? 'border border-indigo-500/20 bg-gradient-to-br from-[#0b1220]/85 to-[#1a2240]/70 hover:border-indigo-400/35 hover:shadow-[0_10px_30px_rgba(99,102,241,0.18)]'
      : 'border border-slate-700/60 bg-slate-900/65 hover:border-sky-500/35 hover:shadow-[0_10px_30px_rgba(56,189,248,0.16)]'
  }`}>
  <div class="pointer-events-none absolute inset-0 bg-gradient-to-br from-sky-500/0 via-sky-400/0 to-indigo-500/0 opacity-0 transition-opacity duration-300 group-hover:opacity-100 group-hover:from-sky-500/10 group-hover:via-sky-400/5 group-hover:to-indigo-500/10"></div>

  <div class="relative flex items-start gap-3">
    <span class="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-slate-700/70 bg-slate-950/70 text-sky-300 shadow-[0_0_20px_rgba(56,189,248,0.18)]">
      {#if icon === 'pulse'}
        <Activity size={20} strokeWidth={1.9} aria-hidden="true" />
      {:else if icon === 'shield'}
        <ShieldCheck size={20} strokeWidth={1.9} aria-hidden="true" />
      {:else if icon === 'alert'}
        <Siren size={20} strokeWidth={1.9} aria-hidden="true" />
      {:else if icon === 'chart'}
        <ChartLine size={20} strokeWidth={1.9} aria-hidden="true" />
      {:else if icon === 'flow'}
        <Workflow size={20} strokeWidth={1.9} aria-hidden="true" />
      {:else}
        <Eye size={20} strokeWidth={1.9} aria-hidden="true" />
      {/if}
    </span>

    <div>
      <h3 class="text-sm font-semibold text-slate-100">{title}</h3>
      <p class="mt-1.5 text-sm leading-relaxed text-slate-400">{description}</p>
    </div>
  </div>
</article>

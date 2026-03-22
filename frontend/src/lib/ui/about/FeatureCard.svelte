<script lang="ts">
  export let icon: string = 'pulse';
  export let title: string;
  export let description: string;
  export let variant: 'default' | 'tinted' | 'highlight' = 'default';

  const iconLabel: Record<string, string> = {
    pulse: 'TM',
    shield: 'ML',
    alert: 'AL'
  };
</script>

<article
  class={`rounded-xl border px-4 py-4 transition duration-300 hover:scale-[1.01]
    ${
      variant === 'highlight'
        ? 'border-sky-500/35 bg-gradient-to-br from-slate-900/85 to-sky-950/25 hover:border-sky-400/45'
        : variant === 'tinted'
        ? 'border-indigo-500/30 bg-gradient-to-br from-slate-900/85 to-indigo-950/25 hover:border-indigo-400/40'
        : 'border-slate-700/70 bg-slate-900/65 hover:border-slate-600/80'
    }`}
>
  <div class="inline-flex h-8 w-8 items-center justify-center rounded-lg border border-slate-700/70 bg-slate-900/85 text-[11px] font-semibold text-sky-300">
    {iconLabel[icon] ?? 'FX'}
  </div>

  <h3 class="mt-3 text-sm font-semibold text-slate-100">{title}</h3>
  <p class="mt-1.5 text-xs leading-relaxed text-slate-400">{description}</p>
</article>

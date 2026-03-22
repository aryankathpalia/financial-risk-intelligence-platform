<script lang="ts">
  export let icon: string;
  export let label: string;

  const iconLabel: Record<string, string> = {
    ml: 'ML',
    pipeline: 'PL',
    explain: 'EX'
  };
</script>

<span class="inline-flex items-center gap-2 rounded-full border border-slate-700/70 bg-slate-900/70 px-3 py-1.5 text-xs text-slate-300">
  <span class="inline-flex h-5 w-5 items-center justify-center rounded-md border border-slate-700/80 bg-slate-900 text-[10px] font-semibold text-sky-300">
    {iconLabel[icon] ?? 'AI'}
  </span>
  <span>{label}</span>
</span>

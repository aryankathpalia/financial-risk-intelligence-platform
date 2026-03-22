<script lang="ts">
  import { Cpu, Workflow, Sparkles } from "lucide-svelte";

  export let label: string;
  export let icon: 'ml' | 'pipeline' | 'explain';
</script>

<div class="inline-flex items-center gap-2 rounded-full border border-slate-700/80 bg-slate-900/75 px-3 py-1.5 text-xs text-slate-200 backdrop-blur-sm transition duration-300 hover:border-sky-500/40 hover:shadow-[0_6px_16px_rgba(56,189,248,0.18)]">
  <span class="inline-flex h-5 w-5 items-center justify-center rounded-full bg-slate-800 text-sky-300">
    {#if icon === 'ml'}
      <Cpu size={14} strokeWidth={1.9} aria-hidden="true" />
    {:else if icon === 'pipeline'}
      <Workflow size={14} strokeWidth={1.9} aria-hidden="true" />
    {:else}
      <Sparkles size={14} strokeWidth={1.9} aria-hidden="true" />
    {/if}
  </span>
  <span class="font-medium">{label}</span>
</div>

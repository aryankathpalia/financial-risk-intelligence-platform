<script lang="ts">
  import { CreditCard, Layers3, Activity, Bell, UserRound } from "lucide-svelte";

  export let step: string;
  export let icon: 'tx' | 'model' | 'score' | 'alert' | 'review';
  export let showConnector = false;
</script>

<div class="group relative flex items-center gap-3 rounded-xl border border-slate-800/70 bg-slate-900/75 px-4 py-3 backdrop-blur-sm transition duration-300 hover:scale-[1.02] hover:border-sky-500/40 hover:shadow-[0_8px_24px_rgba(56,189,248,0.14)]">
  <span class="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-slate-700/80 bg-slate-950/80 text-sky-300 shadow-[0_0_20px_rgba(56,189,248,0.12)] transition group-hover:text-sky-200">
    {#if icon === 'tx'}
      <CreditCard size={18} strokeWidth={1.9} aria-hidden="true" />
    {:else if icon === 'model'}
      <Layers3 size={18} strokeWidth={1.9} aria-hidden="true" />
    {:else if icon === 'score'}
      <Activity size={18} strokeWidth={1.9} aria-hidden="true" />
    {:else if icon === 'alert'}
      <Bell size={18} strokeWidth={1.9} aria-hidden="true" />
    {:else}
      <UserRound size={18} strokeWidth={1.9} aria-hidden="true" />
    {/if}
  </span>

  <p class="text-sm font-medium text-slate-200">{step}</p>

  {#if showConnector}
    <span class="pointer-events-none absolute -right-3 hidden h-px w-6 bg-gradient-to-r from-sky-400/60 to-indigo-400/40 lg:block animate-pulse"></span>
  {/if}
</div>

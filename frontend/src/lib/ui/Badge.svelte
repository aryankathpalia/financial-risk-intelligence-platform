<script lang="ts">
  export let tone: 'neutral' | 'success' | 'warning' | 'danger' = 'neutral';
  export let size: 'xs' | 'sm' = 'xs';
</script>

<span
  class={`inline-flex items-center rounded-full font-medium
    ${
      size === 'xs'
        ? 'px-2 py-0.5 text-[11px] leading-[14px]'
        : 'px-2.5 py-0.5 text-xs leading-[16px]'
    }
    ${
      tone === 'success'
        ? 'bg-emerald-500/10 text-emerald-400 ring-1 ring-emerald-500/30'
        : tone === 'warning'
        ? 'bg-amber-500/10 text-amber-300 ring-1 ring-amber-500/30'
        : tone === 'danger'
        ? 'bg-rose-500/10 text-rose-300 ring-1 ring-rose-500/35'
        : 'bg-slate-800 text-slate-300 ring-1 ring-slate-600/70'
    }`}
>
  <slot />
</span>


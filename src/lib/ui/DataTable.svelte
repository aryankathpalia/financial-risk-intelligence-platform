<script lang="ts">
  export let maxHeight: string | null = null; // e.g. "360px"
  export let stickyHeader: boolean = true;
</script>

<div
  class="rounded-lg border border-slate-800/80 overflow-hidden bg-slate-950/40"
>
  <div
    class={maxHeight ? "overflow-auto" : "overflow-x-auto"}
    style={maxHeight ? `max-height:${maxHeight}` : undefined}
  >
    <table class="w-full text-sm">
      <thead
        class={`bg-slate-900/70 text-slate-400 text-xs uppercase tracking-wide
          ${stickyHeader ? "sticky top-0 z-10" : ""}`}
      >
        <slot name="head" />
      </thead>
      <tbody class="divide-y divide-slate-800/80">
        <slot />
      </tbody>
    </table>
  </div>
</div>


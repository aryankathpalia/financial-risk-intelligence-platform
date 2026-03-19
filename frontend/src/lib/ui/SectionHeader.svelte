<script lang="ts">
  export let title: string;
  export let subtitle: string | null = null;
  export let eyebrow: string | null = null;
</script>

<header class="flex items-start justify-between gap-4">
  <div>
    {#if eyebrow}
      <p class="text-[11px] uppercase tracking-[0.16em] text-slate-500 mb-1">
        {eyebrow}
      </p>
    {/if}

    <h1 class="text-xl md:text-2xl font-semibold tracking-tight text-slate-100">
      {title}
    </h1>

    {#if subtitle}
      <p class="mt-1 text-[13px] md:text-sm leading-relaxed text-slate-400 max-w-2xl">
        {subtitle}
      </p>
    {/if}
  </div>

  <div class="flex items-center gap-2">
    <slot name="actions" />
  </div>
</header>


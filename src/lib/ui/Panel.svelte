<script lang="ts">
  export let padding: 'sm' | 'md' | 'lg' = 'md';
  export let subtle: boolean = false;
  let className = '';
  export { className as class };
</script>

<section
  {...$$restProps}
  class={`rounded-xl border border-slate-800/60 bg-slate-900/90 shadow-sm
    ${
      padding === 'sm'
        ? 'px-4 py-3'
        : padding === 'lg'
        ? 'px-6 py-6'
        : 'px-5 py-5'
    }
    ${subtle ? 'bg-slate-900/80 border-slate-800/60 shadow-none' : ''}
    ${className}`}
>
  <slot />
</section>


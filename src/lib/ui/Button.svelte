<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let variant: 'primary' | 'secondary' | 'soft' | 'ghost' = 'primary';
  export let size: 'xs' | 'sm' | 'md' = 'sm';
  export let fullWidth = false;
  export let disabled = false;
  export let type: 'button' | 'submit' = 'button';

  const dispatch = createEventDispatcher<{ click: MouseEvent }>();
</script>

<button
  {type}
  {disabled}
  on:click={(e) => dispatch("click", e)}
  class={`inline-flex items-center justify-center gap-1.5 rounded-md font-medium transition
    ${
      size === 'xs'
        ? 'px-2.5 py-1 text-[11px]'
        : size === 'sm'
        ? 'px-3 py-1.5 text-xs'
        : 'px-3.5 py-1.5 text-sm'
    }
    ${fullWidth ? 'w-full' : ''}
    ${
      variant === 'primary'
        ? 'bg-sky-500 text-slate-950 hover:bg-sky-400 active:bg-sky-500/80 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400 disabled:bg-slate-700 disabled:text-slate-400'
        : variant === 'secondary'
        ? 'bg-slate-800 text-slate-100 hover:bg-slate-700 border border-slate-600/80 active:bg-slate-700/90 disabled:bg-slate-800 disabled:text-slate-500'
        : variant === 'soft'
        ? 'bg-sky-500/10 text-sky-300 hover:bg-sky-500/15 border border-sky-500/25 disabled:bg-slate-800 disabled:text-slate-500'
        : 'text-slate-300 hover:bg-slate-800/80 disabled:text-slate-500'
    }`}
>
  <slot />
</button>


<script lang="ts">
  import { page } from '$app/stores';
  import '../app.css';

  const nav = [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Transactions', href: '/transactions' },
    { label: 'Alerts', href: '/alerts' },
    { label: 'Models', href: '/models' }
  ];
</script>

<div class="min-h-screen bg-slate-950 text-slate-100 flex">

  <!-- SIDEBAR -->
  <aside class="w-64 bg-slate-900 border-r border-slate-800 flex flex-col">

    <!-- BRAND (micro-polished alignment) -->
    <div class="px-6 py-5 flex items-center gap-[2px]">
      <img
        src="/logo/riskapp_logo2.png"
        alt="RiskIntel"
        class="h-9 w-auto"
      />
      <span class="text-2xl font-semibold tracking-tight leading-none">
        RiskIntel
      </span>
    </div>

    <!-- NAV -->
    <nav class="flex-1 px-3 space-y-1">
      {#each nav as item}
      <a
  href={item.href}
  class={
    `relative block px-4 py-2 rounded-md text-sm transition ${
      $page.url.pathname.startsWith(item.href)
        ? 'bg-slate-800 text-white before:absolute before:left-0 before:top-1/2 before:-translate-y-1/2 before:h-5 before:w-1 before:bg-blue-500 before:rounded-r'
        : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
    }`
  }
>
  {item.label}
</a>

      {/each}
    </nav>

    <!-- FOOTER -->
    <div class="px-4 py-4 border-t border-slate-800 text-xs text-slate-500">
      Financial Risk Intelligence
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="flex-1 bg-slate-900 overflow-y-auto">
    <slot />
  </main>

</div>

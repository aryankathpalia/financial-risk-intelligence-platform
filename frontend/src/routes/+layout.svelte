<script lang="ts">
  import { page } from '$app/stores';
  import '../app.css';

  const nav = [
    { label: 'Dashboard', href: '/dashboard', group: 'Monitor' },
    { label: 'Transactions', href: '/transactions', group: 'Investigate' },
    { label: 'Alerts', href: '/alerts', group: 'Investigate' },
    { label: 'Models', href: '/models', group: 'Models' },
    { label: 'About', href: '/about', group: 'About' }
  ];

  const groups = Array.from(new Set(nav.map((item) => item.group)));
</script>




<div class="min-h-screen bg-slate-950 text-slate-100 flex">

  <!-- SIDEBAR -->
  <aside class="w-64 bg-slate-950/95 border-r border-slate-800/80 flex flex-col backdrop-blur">
    <!-- BRAND -->
    <div class="px-6 pt-5 pb-4 flex items-center gap-3">
      <div class="relative">
        <img
          src="/logo/riskapp_logo2.png"
          alt="RiskIntel"
          class="h-9 w-auto"
        />
      </div>
      <div>
        <div class="flex items-center gap-1">
          <span class="text-xl font-semibold tracking-tight leading-none text-slate-50">
            RiskIntel
          </span>
        </div>
        <p class="mt-1 text-xs text-slate-500">
          Real-time risk intelligence
        </p>
      </div>
    </div>

    <!-- NAV -->
    <nav class="flex-1 px-3 pt-3 pb-4 space-y-5 overflow-y-auto">
      {#each groups as group}
        <div class="space-y-1.5">
          <p class="px-3 text-[11px] font-medium uppercase tracking-[0.18em] text-slate-500">
            {group}
          </p>

          {#each nav.filter((item) => item.group === group) as item}
            <a
              href={item.href}
              data-sveltekit-preload-data="hover"
              class={`group relative flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm
                ${
                  $page.url.pathname === item.href || $page.url.pathname.startsWith(item.href + '/')
                    ? 'text-slate-50 bg-slate-800/90 shadow-[0_0_0_1px_rgba(30,64,175,0.7),0_16px_35px_rgba(15,23,42,0.9)]'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                } transition`}
            >
              <!-- Active rail -->
              <span
                class={`absolute left-0 top-1/2 -translate-y-1/2 h-6 w-[2px] rounded-full
                  ${
                    $page.url.pathname === item.href || $page.url.pathname.startsWith(item.href + '/')
                      ? 'bg-gradient-to-b from-sky-400 via-blue-500 to-indigo-500'
                      : 'bg-transparent'
                  }`}
              ></span>

              <!-- Simple icon glyph (no external deps) -->
              <span
                class={`flex h-6 w-6 items-center justify-center rounded-md border text-[11px]
                  ${
                    $page.url.pathname === item.href || $page.url.pathname.startsWith(item.href + '/')
                      ? 'border-sky-500/70 bg-sky-500/10 text-sky-300'
                      : 'border-slate-700/80 bg-slate-900/80 text-slate-400 group-hover:border-slate-500/80'
                  }`}
              >
                {item.label.slice(0, 2).toUpperCase()}
              </span>

              <span class="truncate">{item.label}</span>
            </a>
          {/each}
        </div>
      {/each}
    </nav>

    <!-- FOOTER -->
    <div class="px-4 py-4 border-t border-slate-800/80 text-[11px] text-slate-500 flex items-center justify-between">
      <span>Financial Risk Intelligence</span>
      <span class="text-slate-600">v0.1</span>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="flex-1 bg-slate-950/95 overflow-y-auto">
    <slot />
  </main>

</div>

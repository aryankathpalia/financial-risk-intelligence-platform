<script lang="ts">
  import { page } from '$app/stores';
  import '../app.css';
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  const nav = [
    { label: 'Dashboard', href: '/dashboard', group: 'Monitor' },
    { label: 'Transactions', href: '/transactions', group: 'Investigate' },
    { label: 'Alerts', href: '/alerts', group: 'Investigate' },
    { label: 'Models', href: '/models', group: 'Models' },
    { label: 'About', href: '/about', group: 'About' }
  ];

  const groups = Array.from(new Set(nav.map((item) => item.group)));

  let collapsed = false;

  function toggleSidebar() {
    collapsed = !collapsed;
  }

  onMount(() => {
    if (browser) {
      collapsed = localStorage.getItem('sidebar') === 'true';
    }
  });

  $: if (browser) {
    localStorage.setItem('sidebar', String(collapsed));
  }
</script>

<div class="min-h-screen bg-slate-950 text-slate-100 flex">

  <!-- SIDEBAR -->
  <aside
    class={`${
      collapsed ? 'w-20' : 'w-64'
    } bg-slate-950/95 border-r border-slate-800/80 flex flex-col backdrop-blur transition-all duration-300`}
  >

    <!-- BRAND -->
    <div class="px-4 pt-5 pb-4 flex items-center justify-between">

      {#if collapsed}
        <!-- COLLAPSED: LOGO ONLY -->
        <div
          class="w-full flex justify-center cursor-pointer"
          on:click={toggleSidebar}
        >
          <img
            src="/logo/riskapp_logo2.png"
            alt="RiskIntel"
            class="h-9 w-auto"
          />
        </div>
      {:else}
        <!-- EXPANDED -->
        <div class="flex items-center justify-between w-full">

          <div class="flex items-center gap-3 min-w-0">
            <img
              src="/logo/riskapp_logo2.png"
              alt="RiskIntel"
              class="h-9 w-auto"
            />

            <div class="min-w-0">
              <span class="text-xl font-semibold text-slate-50 block leading-tight">
                RiskIntel
              </span>
              <p class="text-xs text-slate-500 whitespace-nowrap">
                Real-time risk intelligence
              </p>
            </div>
          </div>

          <!-- HAMBURGER -->
          <button
            on:click={toggleSidebar}
            class="flex items-center justify-center h-8 w-8 rounded-md border border-slate-700/80 bg-slate-900/80 text-slate-400 hover:text-white hover:border-slate-500 transition shrink-0"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <line x1="4" y1="6" x2="20" y2="6" />
              <line x1="4" y1="12" x2="20" y2="12" />
              <line x1="4" y1="18" x2="20" y2="18" />
            </svg>
          </button>

        </div>
      {/if}

    </div>

    <!-- NAV -->
    <nav class="flex-1 px-2 pt-3 pb-4 space-y-5 overflow-y-auto">
      {#each groups as group}
        <div class="space-y-1.5">

          {#if !collapsed}
            <p class="px-3 text-[11px] font-medium uppercase tracking-[0.18em] text-slate-500">
              {group}
            </p>
          {/if}

          {#each nav.filter((item) => item.group === group) as item}
            <a
              href={item.href}
              data-sveltekit-preload-data="hover"
              class={`group relative flex items-center ${
                collapsed ? 'justify-center' : 'gap-2.5'
              } px-3 py-2 rounded-lg text-sm
                ${
                  $page.url.pathname === item.href ||
                  $page.url.pathname.startsWith(item.href + '/')
                    ? 'text-slate-50 bg-slate-800/90'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                } transition`}
            >

              <!-- Active rail -->
              <span
                class={`absolute left-0 top-1/2 -translate-y-1/2 h-6 w-[2px]
                ${
                  $page.url.pathname === item.href ||
                  $page.url.pathname.startsWith(item.href + '/')
                    ? 'bg-gradient-to-b from-sky-400 to-indigo-500'
                    : 'bg-transparent'
                }`}
              ></span>

              <!-- ICON -->
              <span
                class={`flex h-6 w-6 items-center justify-center rounded-md border text-[11px]
                  ${
                    $page.url.pathname === item.href ||
                    $page.url.pathname.startsWith(item.href + '/')
                      ? 'border-sky-500/70 bg-sky-500/10 text-sky-300'
                      : 'border-slate-700/80 bg-slate-900/80 text-slate-400'
                  }`}
              >
                {item.label.slice(0, 2).toUpperCase()}
              </span>

              <!-- TEXT -->
              {#if !collapsed}
                <span class="truncate">{item.label}</span>
              {/if}

              <!-- TOOLTIP -->
              {#if collapsed}
                <span class="absolute left-full ml-2 text-xs bg-slate-800 px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition whitespace-nowrap z-50">
                  {item.label}
                </span>
              {/if}
            </a>
          {/each}
        </div>
      {/each}
    </nav>

    <!-- FOOTER -->
    <div class="px-4 py-4 border-t border-slate-800/80 text-[11px] text-slate-500 flex items-center justify-between">
      {#if !collapsed}
        <span>Financial Risk Intelligence</span>
      {/if}
      <span class="text-slate-600">v0.1</span>
    </div>
  </aside>

  <!-- MAIN -->
  <main class="flex-1 bg-slate-950/95 overflow-y-auto">
    <slot />
  </main>

</div>
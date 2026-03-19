<script lang="ts">
  import { goto } from "$app/navigation";

  function goToDashboard() {
    goto("/dashboard");
  }
</script>

<div class="min-h-screen bg-[#020617] text-slate-300 flex items-center justify-center px-6">
  <div class="text-center">

    <!-- Title -->
    <h1 class="text-3xl md:text-4xl font-semibold text-white mb-4 tracking-tight">
      About Page Coming Soon
    </h1>

    <!-- Subtext -->
    <p class="text-slate-500 mb-6 text-sm">
      We're working on something better here.
    </p>

    <!-- Button -->
    <button
      on:click={goToDashboard}
      class="text-sm text-blue-400 hover:text-blue-300 transition-colors underline underline-offset-4"
    >
      Go to Dashboard →
    </button>

  </div>
</div>
<script lang="ts">
  import { onMount } from "svelte";
  import {
    Chart,
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Tooltip,
    Filler
  } from "chart.js";
  import Panel from "$lib/ui/Panel.svelte";
  import Badge from "$lib/ui/Badge.svelte";
  import FeatureCard from "$lib/ui/about/FeatureCard.svelte";
  import TechPill from "$lib/ui/about/TechPill.svelte";
  import {
    Clock3,
    Database,
    TriangleAlert,
    ShieldX,
    Cpu,
    BadgeAlert,
    CircleGauge,
    BellRing,
    UserRoundCheck,
    Target,
    BarChart3,
    GitBranch,
    Layers
  } from "lucide-svelte";

  Chart.register(
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Tooltip,
    Filler
  );

  const whatItDoes = [
    {
      icon: "pulse",
      title: "Transaction monitoring",
      description:
        "Tracks transaction activity in real time and surfaces suspicious behavior before losses grow."
    },
    {
      icon: "shield",
      title: "Risk scoring with ML",
      description:
        "Scores each event with production ML models so teams can quickly prioritize high-risk cases."
    },
    {
      icon: "alert",
      title: "Alerts and investigation",
      description:
        "Routes high-priority alerts into analyst workflows with clear context for faster decisions."
    }
  ] as const;

  const flowSteps = [
    {
      label: "Transactions",
      description: "Incoming payment events"
    },
    {
      label: "Model",
      description: "LightGBM + isolation signals"
    },
    {
      label: "Risk Score",
      description: "Probability + anomaly output"
    },
    {
      label: "Alerts",
      description: "High-risk cases prioritized"
    },
    {
      label: "Analyst",
      description: "Review and final decision"
    }
  ] as const;

  const coreCapabilities = [
    {
      icon: Target,
      title: "High-recall fraud detection",
      description:
        "Model tuning prioritizes recall so high-risk transactions are caught early while keeping operations manageable.",
      highlighted: true
    },
    {
      icon: BarChart3,
      title: "Validation-backed model quality",
      description:
        "Tracks around ROC-AUC 0.98 with stable false positive control near 1.2%.",
      highlighted: false
    },
    {
      icon: GitBranch,
      title: "Operational decision flow",
      description:
        "Alerts, risk evidence, and analyst actions connect in one workflow for consistent outcomes.",
      highlighted: false
    },
    {
      icon: Layers,
      title: "Production-ready scoring stack",
      description:
        "From dataset ingestion to scoring APIs and dashboard monitoring, built like a real production product.",
      highlighted: false
    }
  ] as const;

  const techApproach = [
    { icon: "ml", label: "ML classifiers in production" },
    { icon: "pipeline", label: "Real-time scoring pipelines" },
    { icon: "explain", label: "SHAP-style explanation signals" }
  ] as const;

  const heroStats = [
    { value: "590K+", label: "transactions processed" },
    { value: "95%+", label: "fraud recall" },
    { value: "< 180ms", label: "scoring latency" }
  ] as const;

  const overviewMetrics = [
    { label: "Signals analyzed", value: "590K+", icon: Database },
    { label: "ROC-AUC", value: "0.98", icon: CircleGauge },
    { label: "High-risk flagged", value: "2.05%", icon: TriangleAlert },
    { label: "False positives", value: "1.2%", icon: ShieldX },
    { label: "Decision latency", value: "< 180ms", icon: Clock3 }
  ] as const;

  const credibilityTags = [
    "Based on IEEE Fraud Dataset",
    "Model: LightGBM + Isolation Forest",
    "Evaluation: Validation Set Metrics"
  ] as const;

  const activityLabels = [
    "09:00",
    "09:10",
    "09:20",
    "09:30",
    "09:40",
    "09:50",
    "10:00",
    "10:10",
    "10:20",
    "10:30"
  ] as const;
  const activitySeries = [120, 180, 150, 300, 280, 350, 260, 400, 370, 420] as const;

  let activityCanvas: HTMLCanvasElement | null = null;
  let activityChart: Chart | null = null;

  onMount(() => {
    if (activityCanvas) {
      const context = activityCanvas.getContext("2d");
      if (context) {
        const strokeGradient = context.createLinearGradient(0, 0, activityCanvas.width || 700, 0);
        strokeGradient.addColorStop(0, "#38bdf8");
        strokeGradient.addColorStop(1, "#a78bfa");

        const areaGradient = context.createLinearGradient(0, 0, 0, activityCanvas.height || 240);
        areaGradient.addColorStop(0, "rgba(56,189,248,0.28)");
        areaGradient.addColorStop(1, "rgba(56,189,248,0.02)");

        activityChart?.destroy();
        activityChart = new Chart(activityCanvas, {
          type: "line",
          data: {
            labels: [...activityLabels],
            datasets: [
              {
                label: "Live Transaction Activity (Simulated)",
                data: [...activitySeries],
                borderColor: strokeGradient,
                backgroundColor: areaGradient,
                fill: true,
                tension: 0.28,
                pointRadius: 2,
                pointHoverRadius: 5,
                pointBackgroundColor: "#67e8f9",
                pointBorderWidth: 0,
                borderWidth: 2.6
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: "rgba(15,23,42,0.95)",
                borderColor: "rgba(56,189,248,0.35)",
                borderWidth: 1,
                displayColors: false,
                callbacks: {
                  label: (item) => `${Number(item.raw).toLocaleString()} transactions/min`
                }
              }
            },
            interaction: {
              mode: "index",
              intersect: false
            },
            scales: {
              x: {
                grid: { color: "rgba(148,163,184,0.09)" },
                ticks: {
                  color: "#94a3b8",
                  maxRotation: 0,
                  autoSkip: true,
                  maxTicksLimit: 6
                }
              },
              y: {
                beginAtZero: true,
                grid: { color: "rgba(148,163,184,0.11)" },
                ticks: {
                  color: "#94a3b8",
                  callback: (value) => `${Math.round(Number(value))}`
                }
              }
            }
          }
        });
      }
    }

    const targets = document.querySelectorAll<HTMLElement>("[data-reveal]");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );

    targets.forEach((target) => observer.observe(target));

    return () => {
      observer.disconnect();
      activityChart?.destroy();
    };
  });
</script>

<section class="min-h-screen bg-slate-950 p-6 text-slate-100">
  <div class="min-h-[calc(100vh-3rem)] max-w-6xl mx-auto space-y-12">
    <Panel padding="lg" data-reveal class="reveal is-visible relative overflow-hidden border-sky-500/20 bg-gradient-to-br from-[#070d1a] via-[#0f172a] to-[#1a2240]/70 backdrop-blur-sm shadow-[0_18px_60px_rgba(2,6,23,0.6)]">
      <div class="pointer-events-none absolute inset-0 opacity-20" style="background-image: linear-gradient(rgba(148,163,184,0.12) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,0.12) 1px, transparent 1px); background-size: 26px 26px;"></div>
      <div class="pointer-events-none absolute -top-24 right-12 h-64 w-64 rounded-full bg-sky-500/25 blur-3xl"></div>
      <div class="pointer-events-none absolute -bottom-24 left-20 h-52 w-52 rounded-full bg-indigo-500/25 blur-3xl"></div>
      <div class="pointer-events-none absolute top-1/3 left-1/3 h-32 w-32 rounded-full bg-fuchsia-500/10 blur-3xl"></div>

      <div class="relative space-y-6">
        <Badge tone="success" size="sm">AI Risk Intelligence Platform</Badge>

        <div class="space-y-4 max-w-2xl">
          <p class="text-[11px] uppercase tracking-[0.18em] text-slate-500">About</p>
          <h1 class="text-5xl md:text-6xl font-bold tracking-tight text-slate-50 [text-shadow:0_0_34px_rgba(56,189,248,0.32)]">
            About RiskIntel
          </h1>
          <p class="max-w-2xl text-sm md:text-base leading-relaxed text-slate-300">
            RiskIntel helps teams monitor transactions in real time, score risk with ML, and support analyst decisions with clear alerts and explainable signals.
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 max-w-3xl">
          {#each heroStats as stat}
            <div class="rounded-xl border border-slate-700/65 bg-slate-900/60 px-4 py-3 backdrop-blur-sm transition duration-300 hover:scale-[1.02] hover:border-sky-500/35">
              <p class="text-base font-semibold text-slate-100">{stat.value}</p>
              <p class="text-xs text-slate-400 mt-0.5">{stat.label}</p>
            </div>
          {/each}
        </div>

        <div class="flex flex-wrap gap-2">
          {#each credibilityTags as tag}
            <span class="inline-flex items-center rounded-full border border-slate-700/70 bg-slate-900/55 px-3 py-1 text-[11px] text-slate-300">
              {tag}
            </span>
          {/each}
        </div>
      </div>
    </Panel>

    <section data-reveal class="reveal space-y-6 border-t border-white/5 pt-9">
      <div>
        <h2 class="text-2xl font-bold text-slate-100">What it does</h2>
        <p class="mt-2 text-sm text-slate-400 max-w-2xl">Core product capabilities for fraud operations teams.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        {#each whatItDoes as item, index}
          <FeatureCard
            icon={item.icon}
            title={item.title}
            description={item.description}
            variant={index === 2 ? 'highlight' : index === 1 ? 'tinted' : 'default'}
          />
        {/each}
      </div>
    </section>

    <Panel padding="lg" data-reveal class="reveal space-y-6 border-slate-700/70 bg-slate-900/65 backdrop-blur-sm">
      <div>
        <h2 class="text-2xl font-bold text-slate-100">How it works</h2>
        <p class="mt-2 text-sm text-slate-400 max-w-2xl">A pipeline from incoming activity to analyst action.</p>
      </div>

      <div class="relative grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        <span class="pointer-events-none hidden lg:block absolute left-[10%] right-[10%] top-7 h-px bg-gradient-to-r from-sky-500/50 via-indigo-400/45 to-sky-500/50"></span>

        {#each flowSteps as step, index}
          <div class="group relative rounded-xl border border-slate-700/70 bg-slate-950/55 px-3.5 py-3 transition duration-300 hover:scale-[1.02] hover:border-sky-500/40 hover:shadow-[0_8px_24px_rgba(56,189,248,0.14)]">
            <div class="flex items-center gap-2.5">
              <span class="inline-flex h-8 w-8 items-center justify-center rounded-lg border border-slate-700/70 bg-slate-900/80 text-sky-300">
                {#if index === 0}
                  <Database size={16} strokeWidth={1.9} aria-hidden="true" />
                {:else if index === 1}
                  <Cpu size={16} strokeWidth={1.9} aria-hidden="true" />
                {:else if index === 2}
                  <CircleGauge size={16} strokeWidth={1.9} aria-hidden="true" />
                {:else if index === 3}
                  <BadgeAlert size={16} strokeWidth={1.9} aria-hidden="true" />
                {:else}
                  <UserRoundCheck size={16} strokeWidth={1.9} aria-hidden="true" />
                {/if}
              </span>
              <p class="text-sm font-semibold text-slate-100">{step.label}</p>
            </div>

            <p class="mt-2 text-xs text-slate-400">{step.description}</p>

            {#if index < flowSteps.length - 1}
              <span class="pointer-events-none absolute -right-2 top-1/2 -translate-y-1/2 hidden lg:flex h-4 w-4 items-center justify-center rounded-full border border-slate-700/70 bg-slate-900/85 text-slate-400">
                <BellRing size={10} strokeWidth={2} aria-hidden="true" />
              </span>
            {/if}
          </div>
        {/each}
      </div>
    </Panel>

    <section data-reveal class="reveal space-y-6 border-t border-white/5 pt-9">
      <div>
        <h2 class="text-2xl font-bold text-slate-100">Core capabilities</h2>
        <p class="mt-2 text-sm text-slate-400 max-w-2xl">Deeper platform value for production fraud operations.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 items-stretch">
        {#each coreCapabilities as capability}
          <article class={`flex flex-col rounded-2xl border p-5 backdrop-blur-sm transition duration-300 hover:scale-[1.02] hover:shadow-[0_10px_26px_rgba(56,189,248,0.14)] ${capability.highlighted ? 'border-sky-500/40 bg-gradient-to-br from-[#0b1220]/90 to-[#1a2240]/70 shadow-[0_10px_28px_rgba(56,189,248,0.15)] hover:border-sky-400/55' : 'border-slate-700/70 bg-slate-900/75 hover:border-sky-500/35'}`}>
            <span class="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-slate-700/70 bg-slate-900/80 text-sky-300 mb-3 shrink-0">
              <svelte:component this={capability.icon} size={18} strokeWidth={1.9} aria-hidden="true" />
            </span>
            <h3 class="text-base font-semibold text-slate-100">{capability.title}</h3>
            <p class="mt-1.5 text-sm leading-relaxed text-slate-300">{capability.description}</p>
          </article>
        {/each}
      </div>
    </section>

    <Panel padding="lg" data-reveal class="reveal border-slate-700/70 bg-gradient-to-br from-slate-900/70 via-slate-900/65 to-indigo-950/20 backdrop-blur-sm space-y-6">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h2 class="text-2xl font-bold text-slate-100">Platform in action</h2>
          <p class="mt-2 text-sm text-slate-400 max-w-2xl">A quick operational snapshot showing live risk intelligence signals and review pressure.</p>
        </div>
        <Badge tone="neutral" size="sm">System overview</Badge>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-5 gap-4 items-stretch">
        <div class="xl:col-span-3 rounded-2xl border border-sky-500/25 bg-gradient-to-br from-slate-950/80 to-slate-900/55 p-4 shadow-[0_10px_30px_rgba(56,189,248,0.12)] relative overflow-hidden flex flex-col justify-between">
          <span class="pointer-events-none absolute -top-14 -right-8 h-40 w-40 rounded-full bg-sky-500/15 blur-3xl"></span>
          <div class="flex flex-col flex-1">
            <div class="flex items-center justify-between">
              <p class="text-xs uppercase tracking-[0.14em] text-slate-500">Recent activity</p>
              <span class="text-xs text-slate-300">Live simulation</span>
            </div>

            <p class="mt-2 text-xs text-slate-400">Live Transaction Activity (Simulated)</p>

            <div class="mt-3 rounded-xl border border-slate-800/70 bg-slate-950/70 p-3 flex-1 min-h-[12rem]">
              <canvas bind:this={activityCanvas} class="h-full w-full"></canvas>
            </div>
          </div>

          <div class="mt-4 grid grid-cols-3 gap-3 border-t border-slate-800/70 pt-3 shrink-0">
            <div>
              <p class="text-[10px] uppercase tracking-[0.12em] text-slate-500">Avg txn/min</p>
              <p class="mt-0.5 text-sm font-semibold text-slate-200">293</p>
            </div>
            <div>
              <p class="text-[10px] uppercase tracking-[0.12em] text-slate-500">Peak spike</p>
              <p class="mt-0.5 text-sm font-semibold text-sky-300">420</p>
            </div>
            <div>
              <p class="text-[10px] uppercase tracking-[0.12em] text-slate-500">Volatility</p>
              <p class="mt-0.5 text-sm font-semibold text-amber-300">Medium</p>
            </div>
          </div>
        </div>

        <div class="xl:col-span-2 flex flex-col gap-3">
          {#each overviewMetrics as metric, index}
            <div class={`rounded-xl border px-4 py-3 transition duration-300 hover:scale-[1.02] flex-1
              ${
                index === 0
                  ? 'border-sky-500/30 bg-gradient-to-br from-slate-950/70 to-sky-950/30 hover:shadow-[0_8px_20px_rgba(56,189,248,0.16)]'
                  : 'border-slate-700/70 bg-slate-950/60 hover:border-sky-500/30 hover:shadow-[0_8px_20px_rgba(56,189,248,0.12)]'
              }`}>
              <div class="flex items-start justify-between gap-3">
                <div>
                  <p class="text-xs uppercase tracking-[0.14em] text-slate-500">{metric.label}</p>
                  <p class="mt-1.5 text-lg font-semibold text-slate-100">{metric.value}</p>
                </div>
                <span class="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-slate-700/70 bg-slate-900/65 text-sky-300">
                  <svelte:component this={metric.icon} size={18} strokeWidth={1.9} aria-hidden="true" />
                </span>
              </div>
              <p class="mt-2 text-[11px] text-slate-400">Based on validation data</p>
            </div>
          {/each}
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div class="rounded-lg border border-slate-700/70 bg-slate-950/55 px-4 py-3">
          <p class="text-[11px] uppercase tracking-[0.14em] text-slate-500">Allow</p>
          <p class="mt-1 text-sm font-semibold text-emerald-300">97.9%</p>
        </div>
        <div class="rounded-lg border border-slate-700/70 bg-slate-950/55 px-4 py-3">
          <p class="text-[11px] uppercase tracking-[0.14em] text-slate-500">Review</p>
          <p class="mt-1 text-sm font-semibold text-amber-300">2.05%</p>
        </div>
        <div class="rounded-lg border border-slate-700/70 bg-slate-950/55 px-4 py-3">
          <p class="text-[11px] uppercase tracking-[0.14em] text-slate-500">Block</p>
          <p class="mt-1 text-sm font-semibold text-rose-300">0.05%</p>
        </div>
      </div>
    </Panel>

    <section data-reveal class="reveal grid grid-cols-1 lg:grid-cols-2 gap-4 border-t border-white/5 pt-9">
      <Panel padding="lg" class="space-y-5 border-slate-700/70 bg-slate-900/65 backdrop-blur-sm">
        <div>
          <h2 class="text-2xl font-bold text-slate-100">Tech approach</h2>
          <p class="mt-2 text-sm text-slate-400 max-w-2xl">Simple, production-focused architecture choices.</p>
        </div>

        <div class="flex flex-wrap gap-2.5">
          {#each techApproach as item}
            <TechPill icon={item.icon} label={item.label} />
          {/each}
        </div>
      </Panel>

      <Panel padding="lg" class="border-sky-500/30 bg-gradient-to-br from-slate-900/95 via-slate-900 to-sky-950/25 space-y-4 shadow-[0_10px_30px_rgba(56,189,248,0.1)]">
        <h2 class="text-2xl font-bold text-slate-100">Why this project exists</h2>
        <p class="text-sm leading-relaxed text-slate-300">
          Fraud is messy and constantly changing. Teams need more than rules—they need tools that are fast, clear, and practical to use every day.
        </p>
        <p class="text-sm leading-relaxed text-slate-400">
          RiskIntel is built around that reality: better signals, explainable outputs, and workflows that help people make better calls under pressure.
        </p>
      </Panel>
    </section>

    <Panel padding="lg" data-reveal class="reveal border-sky-500/25 bg-gradient-to-br from-slate-900/95 via-slate-900 to-indigo-950/25 shadow-[0_12px_34px_rgba(56,189,248,0.12)]">
      <div class="grid grid-cols-1 md:grid-cols-[auto,1fr] gap-6 md:gap-7 items-start">
        <div class="flex justify-center md:justify-start">
          <div class="relative h-28 w-28 md:h-32 md:w-32 rounded-full ring-2 ring-sky-400/35 shadow-[0_0_38px_rgba(56,189,248,0.25)] overflow-hidden bg-slate-800">
            <img
              src="/developer.jpg"
              alt="Aryan Kathpalia"
              class="h-full w-full object-cover"
              loading="lazy"
            />
          </div>
        </div>

        <div class="space-y-4 max-w-2xl">
          <h2 class="text-2xl font-bold text-slate-100">About the builder</h2>

          <p class="text-sm leading-relaxed text-slate-300">
            Hi, I’m Aryan Kathpalia. I build AI systems focused on solving real-world problems, with a strong emphasis on machine learning and production-ready applications.
          </p>

          <p class="text-sm leading-relaxed text-slate-400">
            RiskIntel was built as a practical fraud detection platform to simulate how modern systems monitor transactions, score risk, and support analyst decisions in real time. I worked on the full pipeline — from training models on large-scale fraud datasets to building APIs, scoring systems, and the frontend dashboard.
          </p>

          <p class="text-sm leading-relaxed text-slate-400">
            The system uses models like LightGBM for risk scoring and isolation forest for risk signals, with a focus on recall and explainability to ensure high-risk transactions are caught while keeping false positives controlled.
          </p>

          <p class="text-sm leading-relaxed text-slate-400">
            My approach is simple: AI is not just about using models — it’s about adapting them to real business use cases and making them reliable in production.
          </p>
        </div>
      </div>
    </Panel>

    <div class="h-px w-full bg-gradient-to-r from-transparent via-slate-700/60 to-transparent"></div>
  </div>
</section>

<style>

  .reveal {
    opacity: 0;
    transform: translateY(8px);
    transition: opacity 500ms ease, transform 500ms ease;
  }

  .reveal.is-visible {
    opacity: 1;
    transform: translateY(0);
  }
</style>
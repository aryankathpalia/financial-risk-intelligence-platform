<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import SectionHeader from "$lib/ui/SectionHeader.svelte";
  import Panel from "$lib/ui/Panel.svelte";
  import Badge from "$lib/ui/Badge.svelte";
  import Button from "$lib/ui/Button.svelte";
  import DataTable from "$lib/ui/DataTable.svelte";
  import {
    fetchTransactions,
    type Transaction,
    type PaginatedTransactions
  } from "$lib/api/transactions";

  /* ---------------------------
     STATE
  --------------------------- */
  let transactions: Transaction[] = [];

  let page = 1;
  let pageSize = 15;
  let total = 0;

  let loading = true;
  let error: string | null = null;

  /* ---------------------------
     LOAD DATA
  --------------------------- */
  async function loadTransactions() {
    loading = true;
    error = null;

    try {
      const res: PaginatedTransactions = await fetchTransactions(page, pageSize);
      transactions = res.items;
      total = res.total;
    } catch (e) {
      console.error("Transactions fetch failed:", e);
      error = e instanceof Error ? e.message : "Failed to load transactions";
    } finally {
      loading = false;
    }
  }

  onMount(loadTransactions);

  /* ---------------------------
     HELPERS
  --------------------------- */
  function riskPercent(tx: Transaction) {
    return Math.round(tx.fraud_prob * 1000) / 10;
  }

  function severity(tx: Transaction) {
    if (tx.decision === "BLOCK") return "high";
    if (tx.decision === "REVIEW") return "medium";
    return "low";
  }

  function status(tx: Transaction) {
    if (tx.decision === "ALLOW") return "Approved";
    if (tx.decision === "REVIEW") return "Needs Review";
    return "Blocked";
  }

  function decisionTone(tx: Transaction) {
    if (tx.decision === "BLOCK") return "danger";
    if (tx.decision === "REVIEW") return "warning";
    return "success";
  }

  /* ---------------------------
     PAGINATION
  --------------------------- */
  function nextPage() {
    if (page * pageSize < total) {
      page++;
      loadTransactions();
    }
  }

  function prevPage() {
    if (page > 1) {
      page--;
      loadTransactions();
    }
  }

  $: totalPages = Math.ceil(total / pageSize);
</script>


<section class="min-h-screen bg-slate-950 p-4 text-slate-100">
  <div class="min-h-[calc(100vh-2rem)] rounded-2xl bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 ring-1 ring-white/5 shadow-2xl">
    <div class="p-6 space-y-6">
      <SectionHeader
        eyebrow="Investigate"
        title="Transactions"
        subtitle="Review transaction-level risk signals and drill into model explanations."
      >
        <svelte:fragment slot="actions">
          <Button variant="soft" size="sm">
            Export
          </Button>
        </svelte:fragment>
      </SectionHeader>

      <Panel padding="lg" subtle>
        <div class="flex flex-wrap items-center gap-2">
          <Badge tone="neutral" size="sm">Status: All</Badge>
          <Badge tone="neutral" size="sm">Risk: Any</Badge>
          <Badge tone="neutral" size="sm">Date: Last 24h</Badge>
        </div>
      </Panel>

      <Panel padding="lg">
        {#if error}
          <div class="rounded-lg bg-red-900/30 border border-red-800 p-4 text-red-300 text-sm mb-4">
            {error}
          </div>
        {/if}

        <DataTable maxHeight="520px">
          <svelte:fragment slot="head">
            <tr>
              <th class="px-4 py-3 text-left font-medium">Transaction</th>
              <th class="px-4 py-3 text-left font-medium">User</th>
              <th class="px-4 py-3 text-left font-medium">Risk score</th>
              <th class="px-4 py-3 text-left font-medium">Decision</th>
              <th class="px-4 py-3 text-left font-medium">Status</th>
              <th class="px-4 py-3 text-right font-medium">Action</th>
            </tr>
          </svelte:fragment>

          {#if loading}
            <tr>
              <td colspan="6" class="px-4 py-6 text-center text-slate-400">
                Loading transactions…
              </td>
            </tr>
          {:else if transactions.length === 0}
            <tr>
              <td colspan="6" class="px-4 py-6 text-center text-slate-400">
                No transactions found.
              </td>
            </tr>
          {:else}
            {#each transactions as tx}
              <tr class="hover:bg-slate-900/70 transition-colors">
                <td class="px-4 py-3 font-mono text-xs text-slate-300">
                  {tx.id}
                </td>
                <td class="px-4 py-3 text-slate-300">
                  {tx.user_id}
                </td>
                <td class="px-4 py-3 tabular-nums text-slate-50 font-semibold">
                  {riskPercent(tx)}%
                </td>
                <td class="px-4 py-3">
                  <Badge tone={decisionTone(tx)} size="xs">
                    {tx.decision}
                  </Badge>
                </td>
                <td class="px-4 py-3">
                  <Badge tone={decisionTone(tx)} size="xs">
                    {status(tx)}
                  </Badge>
                </td>
                <td class="px-4 py-3 text-right">
                  <Button
                    variant="soft"
                    size="xs"
                    on:click={() => {
                      goto(`/transactions/${encodeURIComponent(tx.id)}`);
                    }}
                  >
                    View
                  </Button>
                </td>
              </tr>
            {/each}
          {/if}
        </DataTable>

        <div class="flex items-center justify-between pt-4 text-sm text-slate-400">
          <span>
            Page {page} of {totalPages || 1}
          </span>

          <div class="flex gap-2">
            <Button
              variant="secondary"
              size="xs"
              disabled={page === 1}
              on:click={() => {
                page--;
                loadTransactions();
              }}
            >
              Previous
            </Button>
            <Button
              variant="secondary"
              size="xs"
              disabled={page * pageSize >= total}
              on:click={() => {
                page++;
                loadTransactions();
              }}
            >
              Next
            </Button>
          </div>
        </div>
      </Panel>
    </div>
  </div>
</section>

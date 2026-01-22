<script lang="ts">
  import { deposit, withdrawAll, gasMultiplier, portfolio } from '../stores/gameStore.svelte';
  import type { Pool } from '../../types/game';

  interface Props {
    pool: Pool;
  }

  let { pool }: Props = $props();

  const gasMult = $derived(gasMultiplier.value);
  const portfolioVal = $derived(portfolio.value);

  const depositAmount = 1000;
  const depositCost = $derived(depositAmount * gasMult);
  const canDeposit = $derived(!pool.isRugged && portfolioVal >= depositCost);
  const canWithdraw = $derived(!pool.isRugged && pool.deposited > 0);

  const riskConfig = {
    safe: { label: 'Low Risk', color: 'text-emerald-400', bg: 'bg-emerald-500/20', border: 'border-emerald-500/40' },
    medium: { label: 'Medium', color: 'text-amber-400', bg: 'bg-amber-500/20', border: 'border-amber-500/40' },
    degen: { label: 'High Risk', color: 'text-rose-400', bg: 'bg-rose-500/20', border: 'border-rose-500/40' },
  };

  const config = $derived(riskConfig[pool.riskLevel]);

  const tvl = $derived(Math.floor(1000000 / (pool.apy / 100 + 1)));

  function formatTVL(amount: number): string {
    if (amount >= 1_000_000) return `$${(amount / 1_000_000).toFixed(2)}M`;
    if (amount >= 1_000) return `$${(amount / 1_000).toFixed(0)}K`;
    return `$${amount}`;
  }
</script>

<div
  class="w-full bg-slate-900/60 backdrop-blur-lg rounded-lg border overflow-hidden transition-all duration-200
         {pool.isRugged ? 'opacity-50 border-white/10' : 'border-white/10 hover:border-white/20 hover:bg-slate-900/70'}
         {pool.isPumping ? 'border-emerald-500/50 shadow-lg shadow-emerald-500/10' : ''}"
>
  <div class="p-8">
    <!-- Header Row -->
    <div class="flex items-center justify-between mb-8">
      <!-- Token Info -->
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 rounded-lg bg-white/10 border border-white/10 flex items-center justify-center text-2xl">
          {pool.emoji}
        </div>
        <div>
          <h3 class="font-bold text-white">{pool.name}</h3>
          <p class="text-white/40 text-sm">/ USDC</p>
        </div>
      </div>

      <!-- Risk Badge -->
      <span class="px-2 py-1 text-xs font-semibold rounded border {config.bg} {config.color} {config.border}">
        {config.label}
      </span>
    </div>

    <!-- Stats Row -->
    <div class="flex items-center gap-8 mb-8">
      <!-- APR -->
      <div>
        <p class="text-white/40 text-xs uppercase tracking-wider mb-1">APR</p>
        <p class="font-mono font-bold text-3xl text-white">
          {pool.apy}%
          {#if pool.isPumping}
            <span class="text-emerald-400 text-lg ml-1">🔥</span>
          {/if}
        </p>
      </div>

      <!-- TVL -->
      <div>
        <p class="text-white/40 text-xs uppercase tracking-wider mb-1">TVL</p>
        <p class="font-mono text-white/70 text-xl">{formatTVL(tvl)}</p>
      </div>
    </div>

    <!-- Your Position Box -->
    <div class="bg-white/5 border border-white/10 rounded-lg p-5 mb-8">
      <div class="flex items-center justify-between">
        <span class="text-white/50 text-sm">Your Position</span>
        <span class="font-mono text-white font-semibold">
          ${pool.deposited.toLocaleString(undefined, { maximumFractionDigits: 0 })}
        </span>
      </div>
    </div>

    <!-- Action Buttons -->
    {#if !pool.isRugged}
      <div class="flex gap-3">
        <!-- Deposit Button -->
        <button
          onclick={() => deposit(pool.id, depositAmount)}
          disabled={!canDeposit}
          class="flex-1 py-3 font-semibold text-sm rounded-lg transition-all
                 {canDeposit
                   ? 'bg-white text-gray-900 hover:bg-white/90'
                   : 'bg-white/10 text-white/30 cursor-not-allowed'}"
        >
          Deposit +$1K
        </button>

        <!-- Withdraw Button -->
        <button
          onclick={() => withdrawAll(pool.id)}
          disabled={!canWithdraw}
          class="flex-1 py-3 font-semibold text-sm rounded-lg transition-all border
                 {canWithdraw
                   ? 'bg-transparent border-white/20 text-white hover:bg-white/10'
                   : 'bg-transparent border-white/10 text-white/30 cursor-not-allowed'}"
        >
          Withdraw
        </button>
      </div>
    {:else}
      <div class="py-3 bg-red-500/20 border border-red-500/30 rounded-lg text-center">
        <p class="text-red-400 font-semibold flex items-center justify-center gap-2">
          <span>⚠️</span> Pool Rugged
        </p>
      </div>
    {/if}
  </div>
</div>

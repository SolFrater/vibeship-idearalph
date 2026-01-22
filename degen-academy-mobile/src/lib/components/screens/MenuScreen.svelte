<script lang="ts">
  import { startGame } from '../../stores/gameStore.svelte';
</script>

<div class="min-h-screen min-h-dvh flex flex-col bg-cover bg-center bg-fixed relative"
     style="background-image: url('/ralph-lab-bg.png');">

  <!-- Dark overlay -->
  <div class="absolute inset-0 bg-slate-950/85"></div>

  <!-- Content -->
  <div class="relative z-10 flex flex-col min-h-screen min-h-dvh p-6 sm:p-8">

    <!-- Header -->
    <header class="text-center" style="padding-top: 10vh;">
      <h1 class="text-4xl sm:text-5xl font-chalk text-white">
        Ralph's Degen Academy
      </h1>
    </header>

    <!-- Play Button -->
    <div class="flex justify-center" style="margin-top: 16px;">
      <button
        onclick={() => startGame()}
        class="play-btn group font-chalk"
      >
        <svg class="arrows-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M13 5l7 7-7 7M5 5l7 7-7 7"/>
        </svg>
        <span>Enter the Lab</span>
      </button>
    </div>

    <!-- Spacer -->
    <div class="flex-1"></div>

    <!-- Section Title - Thought bubble style -->
    <div class="flex justify-center" style="margin-bottom: 20px;">
      <div class="section-bubble">
        <p class="font-handwritten text-lg text-center" style="color: #2D3436;">
          Learn DeFi by getting rekt (safely)
        </p>
      </div>
    </div>

    <!-- What You'll Learn - 3 Info Boxes -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4" style="margin-bottom: 32px; max-width: 800px; margin-left: auto; margin-right: auto; width: 100%;">
      <!-- Box 1: Yield Farming -->
      <div class="info-box">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color: #4ade80;">
          <path d="M7 20h10"/>
          <path d="M10 20c5.5-2.5 5-7.5 1-8.5"/>
          <path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/>
          <path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/>
        </svg>
        <h3 class="text-white font-chalk text-base" style="margin-top: 16px;">Yield Farming</h3>
        <p class="text-white/60 text-xs" style="margin-top: 8px;">Learn how APY works and why "too good to be true" usually is</p>
      </div>

      <!-- Box 2: Risk Management -->
      <div class="info-box">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color: #fbbf24;">
          <path d="M12 3l8 4v5c0 5.5-3.8 10.2-8 12-4.2-1.8-8-6.5-8-12V7l8-4z"/>
          <path d="M9 12l2 2 4-4"/>
        </svg>
        <h3 class="text-white font-chalk text-base" style="margin-top: 16px;">Risk Management</h3>
        <p class="text-white/60 text-xs" style="margin-top: 8px;">Understand rug pulls, exploits, and how to protect yourself</p>
      </div>

      <!-- Box 3: DeFi Basics -->
      <div class="info-box">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color: #60a5fa;">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
        </svg>
        <h3 class="text-white font-chalk text-base" style="margin-top: 16px;">DeFi Mechanics</h3>
        <p class="text-white/60 text-xs" style="margin-top: 8px;">Halvings, gas fees, whale dumps — experience it all risk-free</p>
      </div>
    </div>

    <!-- Footer -->
    <footer class="text-center" style="padding: 24px 0;">
      <p class="text-white/40 text-xs">
        No real money. Just vibes and education.
      </p>
    </footer>
  </div>
</div>

<style>
  .play-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 14px 28px;
    font-size: 17px;
    color: #2D3436;
    background: #FFD93D;
    border: 3px solid #2D3436;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.15s ease;
    box-shadow: 3px 3px 0px #2D3436;
  }

  .play-btn:hover {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0px #2D3436;
  }

  .play-btn:active {
    transform: translate(4px, 4px);
    box-shadow: 0px 0px 0px #2D3436;
  }

  .arrows-icon {
    color: #2D3436;
    transition: transform 0.2s ease;
  }

  .play-btn:hover .arrows-icon {
    animation: arrows-move 0.6s ease-in-out infinite;
  }

  @keyframes arrows-move {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(4px); }
  }

  .info-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 20px 16px;
    background: #3d3d4a;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    cursor: default;
    transition: transform 0.2s ease;
  }

  .info-box:nth-child(1):hover {
    transform: rotate(1deg) translateY(-4px);
  }

  .info-box:nth-child(2):hover {
    transform: rotate(-1deg) translateY(-4px);
  }

  .info-box:nth-child(3):hover {
    transform: rotate(1deg) translateY(-4px);
  }

  /* Section bubble - thought bubble style */
  .section-bubble {
    display: inline-block;
    padding: 12px 24px;
    background: white;
    border: 3px solid #2D3436;
    border-radius: 20px;
    box-shadow: 3px 3px 0px #2D3436;
  }
</style>

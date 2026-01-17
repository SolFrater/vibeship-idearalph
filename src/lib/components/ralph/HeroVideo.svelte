<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    src?: string;
    poster?: string;
    fallbackEmoji?: boolean;
    size?: 'compact' | 'half' | 'full';
    children?: Snippet;
  }

  let {
    src = '/videos/ralph-hero.mp4',
    poster = '/images/ralph-hero-poster.jpg',
    fallbackEmoji = true,
    size = 'compact',
    children
  }: Props = $props();

  let videoLoaded = $state(false);
  let videoError = $state(false);

  function handleLoaded() {
    videoLoaded = true;
  }

  function handleError() {
    videoError = true;
  }
</script>

{#if size === 'half' || size === 'full'}
  <!-- BANNER MODE: Video as background with overlay content -->
  <div class="hero-banner relative overflow-hidden {size === 'full' ? 'min-h-screen' : 'h-[50vh]'} bg-chalkboard">
    <!-- Video Background Layer -->
    <div class="absolute inset-0 z-0">
      <video
        autoplay
        loop
        muted
        playsinline
        class="w-full h-full object-cover"
      >
        <source src={src} type="video/mp4" />
      </video>

      <!-- Gradient overlay for readability -->
      <div class="absolute inset-0 bg-gradient-to-b from-playground-sunset/40 via-transparent to-playground-sunset/70"></div>
    </div>

    <!-- Content Overlay Layer -->
    <div class="relative z-20 h-full flex flex-col items-center justify-center px-4 py-12">
      {#if children}
        {@render children()}
      {/if}
    </div>
  </div>

{:else}
  <!-- COMPACT MODE: Original rounded video display -->
  <div class="hero-video-container relative">
    {#if !videoError && src}
      <div
        class="relative w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96 rounded-3xl overflow-hidden
               border-4 border-chalkboard shadow-crayon-lg
               transition-opacity duration-500 {videoLoaded ? 'opacity-100' : 'opacity-0'}"
      >
        <video
          autoplay
          loop
          muted
          playsinline
          {poster}
          onloadeddata={handleLoaded}
          onerror={handleError}
          class="w-full h-full object-cover"
        >
          <source {src} type="video/mp4" />
          <source src={src.replace('.mp4', '.webm')} type="video/webm" />
        </video>

        <div class="absolute inset-0 pointer-events-none bg-gradient-to-t from-playground-sunset/30 via-transparent to-transparent"></div>

        <div class="absolute inset-0 pointer-events-none overflow-hidden">
          <div class="sparkle sparkle-1">💡</div>
          <div class="sparkle sparkle-2">✨</div>
          <div class="sparkle sparkle-3">⭐</div>
          <div class="sparkle sparkle-4">💡</div>
        </div>
      </div>

      {#if !videoLoaded}
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96 bg-ralph-yellow/30 rounded-3xl
                      border-4 border-chalkboard animate-pulse flex items-center justify-center">
            <span class="text-6xl animate-bounce">🧒</span>
          </div>
        </div>
      {/if}
    {:else if fallbackEmoji}
      <div
        class="w-48 h-48 md:w-64 md:h-64 bg-ralph-yellow rounded-full
               border-4 border-chalkboard shadow-crayon-lg
               flex items-center justify-center animate-float"
      >
        <span class="text-6xl md:text-8xl">🧒</span>
      </div>
    {/if}
  </div>
{/if}

<style>
  /* Compact mode sparkles */
  .sparkle {
    position: absolute;
    font-size: 1.5rem;
    animation: float-up 3s ease-in-out infinite;
    opacity: 0;
  }

  .sparkle-1 { left: 20%; animation-delay: 0s; }
  .sparkle-2 { left: 50%; animation-delay: 0.8s; }
  .sparkle-3 { left: 75%; animation-delay: 1.5s; }
  .sparkle-4 { left: 35%; animation-delay: 2.2s; }

  @keyframes float-up {
    0% { bottom: 10%; opacity: 0; transform: scale(0.5); }
    20% { opacity: 1; transform: scale(1); }
    80% { opacity: 1; }
    100% { bottom: 90%; opacity: 0; transform: scale(0.8); }
  }
</style>

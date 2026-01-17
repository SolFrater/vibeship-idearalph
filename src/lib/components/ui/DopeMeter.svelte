<script lang="ts">
  import { DOPE_LEVELS } from '$lib/ralph/types';

  interface Props {
    level: number;
    size?: 'sm' | 'md' | 'lg';
    showLabel?: boolean;
    animated?: boolean;
  }

  let { level, size = 'md', showLabel = true, animated = true }: Props = $props();

  const sizeClasses = {
    sm: 'h-2 text-xs',
    md: 'h-4 text-sm',
    lg: 'h-6 text-base'
  };

  const starSizes = {
    sm: 'text-sm',
    md: 'text-lg',
    lg: 'text-2xl'
  };

  const levelColors = [
    'bg-gray-400', // 0
    'bg-playground-red', // 1
    'bg-orange-400', // 2
    'bg-ralph-yellow', // 3
    'bg-playground-green', // 4
    'bg-sky-blue' // 5
  ];
</script>

<div class="dope-meter">
  <!-- Star display -->
  <div class="flex gap-1 mb-1">
    {#each Array(5) as _, i}
      <span
        class="{starSizes[size]} transition-all duration-300 {animated
          ? 'hover:scale-125'
          : ''}"
        style="opacity: {i < level ? 1 : 0.3}"
      >
        {#if i < level}
          ⭐
        {:else}
          ☆
        {/if}
      </span>
    {/each}
  </div>

  <!-- Progress bar -->
  <div
    class="w-full bg-chalkboard/20 rounded-full overflow-hidden border-2 border-chalkboard {sizeClasses[
      size
    ]}"
  >
    <div
      class="h-full transition-all duration-500 {levelColors[level]} {animated
        ? 'animate-pulse'
        : ''}"
      style="width: {(level / 5) * 100}%"
    ></div>
  </div>

  <!-- Label -->
  {#if showLabel}
    <p class="ralph-voice {sizeClasses[size]} text-chalkboard/80 mt-1">
      "{DOPE_LEVELS[level]}"
    </p>
  {/if}
</div>

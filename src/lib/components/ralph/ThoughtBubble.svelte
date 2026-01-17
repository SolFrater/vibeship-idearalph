<script lang="ts">
  interface Props {
    quote: string;
    position?: 'left' | 'right' | 'top';
    size?: 'sm' | 'md' | 'lg';
  }

  let { quote, position = 'right', size = 'md' }: Props = $props();

  const sizeClasses = {
    sm: 'p-3 text-sm max-w-xs',
    md: 'p-4 text-base max-w-sm',
    lg: 'p-6 text-lg max-w-md'
  };

  const positionClasses = {
    left: 'before:-left-3 before:top-1/2',
    right: 'before:-right-3 before:top-1/2',
    top: 'before:left-1/2 before:-top-3'
  };
</script>

<div
  class="thought-bubble {sizeClasses[size]} {positionClasses[position]}
         bg-paper border-4 border-chalkboard rounded-2xl shadow-crayon
         relative"
>
  <p class="ralph-voice text-chalkboard">"{quote}"</p>

  <!-- Thought bubble dots -->
  {#if position === 'left'}
    <div class="absolute -left-6 top-1/2 flex flex-col gap-1">
      <div class="w-3 h-3 bg-paper border-2 border-chalkboard rounded-full"></div>
      <div class="w-2 h-2 bg-paper border-2 border-chalkboard rounded-full ml-1"></div>
    </div>
  {:else if position === 'right'}
    <div class="absolute -right-6 top-1/2 flex flex-col gap-1">
      <div class="w-3 h-3 bg-paper border-2 border-chalkboard rounded-full"></div>
      <div class="w-2 h-2 bg-paper border-2 border-chalkboard rounded-full mr-1"></div>
    </div>
  {:else}
    <div class="absolute left-1/2 -top-6 flex gap-1 -translate-x-1/2">
      <div class="w-3 h-3 bg-paper border-2 border-chalkboard rounded-full"></div>
      <div class="w-2 h-2 bg-paper border-2 border-chalkboard rounded-full mt-1"></div>
    </div>
  {/if}
</div>

<script lang="ts">
  import DopeMeter from '$lib/components/ui/DopeMeter.svelte';
  import type { RalphIdea } from '$lib/ralph/types';

  interface Props {
    idea: RalphIdea;
    onclick?: () => void;
    selected?: boolean;
  }

  let { idea, onclick, selected = false }: Props = $props();

  const statusColors = {
    sandbox: 'bg-ralph-yellow/20 border-ralph-yellow',
    validating: 'bg-sky-blue/20 border-sky-blue',
    refining: 'bg-playground-green/20 border-playground-green',
    completed: 'bg-gold-star/20 border-gold-star',
    archived: 'bg-gray-200 border-gray-400'
  };

  const statusIcons = {
    sandbox: '🏖️',
    validating: '🔍',
    refining: '🎢',
    completed: '⭐',
    archived: '📦'
  };
</script>

<button
  {onclick}
  class="idea-card w-full text-left p-4 rounded-lg border-4 transition-all duration-200
         {statusColors[idea.status]}
         {selected ? 'ring-4 ring-chalkboard scale-[1.02]' : ''}
         hover:scale-[1.01] hover:shadow-crayon"
>
  <div class="flex justify-between items-start mb-2">
    <h3 class="font-chalk text-lg text-chalkboard">{idea.name}</h3>
    <span class="text-xl">{statusIcons[idea.status]}</span>
  </div>

  <p class="text-sm text-chalkboard/80 line-clamp-2 mb-3">
    {idea.refinedIdea || idea.rawIdea}
  </p>

  <DopeMeter level={idea.dopeLevel} size="sm" showLabel={false} />

  {#if idea.ralphQuote}
    <p class="ralph-voice text-xs text-chalkboard/60 mt-2 italic truncate">
      "{idea.ralphQuote}"
    </p>
  {/if}
</button>

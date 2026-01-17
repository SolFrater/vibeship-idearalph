<script lang="ts">
  import { RalphAvatar, DopeMeter } from '$lib/components';
  import { marked } from 'marked';
  import type { Database } from '$lib/types/database';

  type IdeaRow = Database['public']['Tables']['ideas']['Row'];

  let { data } = $props();

  let isGenerating = $state(false);
  let prdMarkdown = $state<string | null>(null);
  let error = $state<string | null>(null);

  const idea: IdeaRow = data.idea;

  async function generatePRD() {
    if (!idea || !idea.pmf_market_size) return;

    isGenerating = true;
    error = null;

    try {
      const response = await fetch('/api/prd/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          idea: idea.refined_idea || idea.raw_idea,
          name: idea.name,
          pmfScores: {
            marketSize: idea.pmf_market_size,
            problemSeverity: idea.pmf_problem_severity,
            solutionFit: idea.pmf_solution_fit,
            competition: idea.pmf_competition,
            vibeCodeable: idea.pmf_vibe_codeable,
            virality: idea.pmf_virality
          }
        })
      });

      if (!response.ok) {
        throw new Error('Failed to generate PRD');
      }

      const result = await response.json();
      prdMarkdown = result.data.markdown;
    } catch (err) {
      error = 'Could not generate PRD. Try again!';
    } finally {
      isGenerating = false;
    }
  }

  function downloadPRD() {
    if (!prdMarkdown) return;

    const blob = new Blob([prdMarkdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${idea.name.toLowerCase().replace(/\s+/g, '-')}-prd.md`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function copyToClipboard() {
    if (!prdMarkdown) return;
    navigator.clipboard.writeText(prdMarkdown);
  }

  // Render markdown to HTML
  const renderedHTML = $derived(prdMarkdown ? marked(prdMarkdown) : null);
</script>

<svelte:head>
  <title>{idea.name} - PRD | IdeaRalph</title>
</svelte:head>

<main class="min-h-screen bg-paper">
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Header -->
    <header class="flex items-center justify-between mb-8">
      <div class="flex items-center gap-4">
        <a href="/playground" class="text-chalkboard hover:text-sky-blue">
          <span class="text-2xl">⬅️</span> Back
        </a>
      </div>
      <div class="flex items-center gap-4">
        <RalphAvatar size="sm" mood={isGenerating ? 'thinking' : 'excited'} />
      </div>
    </header>

    <!-- Idea Summary -->
    <div class="bg-white rounded-lg border-4 border-chalkboard p-6 mb-8">
      <div class="flex items-start justify-between">
        <div>
          <div class="flex items-center gap-2 mb-2">
            <span class="gold-star text-2xl">⭐</span>
            <h1 class="font-chalk text-3xl text-chalkboard">{idea.name}</h1>
          </div>
          <p class="text-chalkboard/80 mb-4">
            {idea.refined_idea || idea.raw_idea}
          </p>
          {#if idea.ralph_quote}
            <p class="ralph-voice text-chalkboard/60 italic">
              "{idea.ralph_quote}"
            </p>
          {/if}
        </div>
        <DopeMeter level={idea.dope_level} size="sm" />
      </div>
    </div>

    <!-- PRD Generation -->
    {#if !prdMarkdown}
      <div class="bg-ralph-yellow/20 rounded-lg border-4 border-ralph-yellow p-8 text-center">
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">Ready to Make a PRD!</h2>
        <p class="ralph-voice text-chalkboard/80 mb-6">
          "A PRD is like a permission slip for building stuff!"
        </p>

        <button
          onclick={generatePRD}
          disabled={isGenerating}
          class="btn-crayon text-xl {isGenerating ? 'animate-wiggle' : ''}"
        >
          {#if isGenerating}
            📝 Writing...
          {:else}
            📝 Generate PRD
          {/if}
        </button>

        {#if error}
          <p class="text-playground-red text-sm mt-4">{error}</p>
        {/if}
      </div>
    {:else}
      <!-- PRD Display -->
      <div class="bg-white rounded-lg border-4 border-chalkboard">
        <!-- Toolbar -->
        <div class="flex items-center justify-between p-4 border-b-2 border-chalkboard/20">
          <h2 class="font-chalk text-xl text-chalkboard">Your PRD</h2>
          <div class="flex gap-2">
            <button onclick={copyToClipboard} class="btn-crayon text-sm bg-gray-100">
              📋 Copy
            </button>
            <button onclick={downloadPRD} class="btn-crayon text-sm bg-playground-green">
              ⬇️ Download
            </button>
            <button onclick={generatePRD} class="btn-crayon text-sm" disabled={isGenerating}>
              🔄 Regenerate
            </button>
          </div>
        </div>

        <!-- Markdown Content -->
        <div class="p-6 prose prose-lg max-w-none">
          {@html renderedHTML}
        </div>
      </div>
    {/if}
  </div>
</main>

<style>
  :global(.prose h1) {
    font-family: 'Fredoka One', cursive;
    color: #2D3436;
  }
  :global(.prose h2) {
    font-family: 'Fredoka One', cursive;
    color: #2D3436;
    border-bottom: 2px solid #FFD93D;
    padding-bottom: 0.5rem;
  }
  :global(.prose blockquote) {
    font-family: 'Patrick Hand', cursive;
    border-left-color: #FFD93D;
    background: #FFD93D20;
    padding: 1rem;
    border-radius: 0.5rem;
  }
</style>

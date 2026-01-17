<script lang="ts">
  import { RalphAvatar, ThoughtBubble, DopeMeter, PMFRadar, ChaosSlider, IdeaCard } from '$lib/components';
  import type { RalphIdea, PMFScores } from '$lib/ralph/types';
  import { RALPH_QUOTES } from '$lib/ralph/types';

  let { data } = $props();

  // State
  let prompt = $state('');
  let chaosLevel = $state(5);
  let isGenerating = $state(false);
  let isRefining = $state(false);
  let currentIdea = $state<RalphIdea | null>(null);
  let ideas = $state<RalphIdea[]>([]);
  let ralphMood = $state<'neutral' | 'thinking' | 'excited' | 'confused'>('neutral');
  let ralphQuote = $state(getRandomQuote('thinking'));
  let error = $state<string | null>(null);

  function getRandomQuote(mood: keyof typeof RALPH_QUOTES): string {
    const quotes = RALPH_QUOTES[mood];
    return quotes[Math.floor(Math.random() * quotes.length)];
  }

  async function generateIdea() {
    isGenerating = true;
    ralphMood = 'thinking';
    ralphQuote = getRandomQuote('thinking');
    error = null;

    try {
      const response = await fetch('/api/ralph/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt || undefined, chaosLevel })
      });

      if (!response.ok) {
        throw new Error('Failed to generate idea');
      }

      const result = await response.json();
      const ideaData = result.data;

      currentIdea = {
        id: crypto.randomUUID(),
        name: ideaData.name,
        rawIdea: ideaData.idea,
        refinedIdea: null,
        ralphQuote: ideaData.ralphQuote,
        status: ideaData.dopeLevel >= 4 ? 'completed' : 'sandbox',
        dopeLevel: ideaData.dopeLevel,
        iteration: 0,
        maxIterations: 3,
        pmfScores: ideaData.pmfScores,
        chaosLevel,
        context: {}
      };

      ralphMood = ideaData.dopeLevel >= 4 ? 'excited' : 'neutral';
      ralphQuote = ideaData.ralphQuote;

      // Add to ideas list
      ideas = [currentIdea, ...ideas];
    } catch (err) {
      error = 'Ralph got confused! Try again.';
      ralphMood = 'confused';
      ralphQuote = getRandomQuote('meh');
    } finally {
      isGenerating = false;
    }
  }

  async function refineIdea() {
    if (!currentIdea) return;

    isRefining = true;
    ralphMood = 'thinking';
    ralphQuote = "I'm making it better!";
    error = null;

    try {
      const response = await fetch('/api/ralph/refine', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          currentIdea: currentIdea.refinedIdea || currentIdea.rawIdea,
          currentDopeLevel: currentIdea.dopeLevel,
          iteration: currentIdea.iteration,
          maxIterations: currentIdea.maxIterations,
          chaosLevel
        })
      });

      if (!response.ok) {
        throw new Error('Failed to refine idea');
      }

      const result = await response.json();
      const ideaData = result.data;

      currentIdea = {
        ...currentIdea,
        name: ideaData.name,
        refinedIdea: ideaData.idea,
        ralphQuote: ideaData.ralphQuote,
        dopeLevel: ideaData.dopeLevel,
        iteration: currentIdea.iteration + 1,
        pmfScores: ideaData.pmfScores,
        status: ideaData.dopeLevel >= 4 ? 'completed' : 'refining'
      };

      ralphMood = ideaData.dopeLevel >= 4 ? 'excited' : 'thinking';
      ralphQuote = ideaData.ralphQuote;

      // Update in ideas list
      ideas = ideas.map(i => i.id === currentIdea!.id ? currentIdea! : i);
    } catch (err) {
      error = 'Refinement got weird. Try again!';
      ralphMood = 'confused';
    } finally {
      isRefining = false;
    }
  }

  async function saveIdea() {
    if (!currentIdea) return;

    try {
      const response = await fetch('/api/ideas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: currentIdea.name,
          rawIdea: currentIdea.rawIdea,
          refinedIdea: currentIdea.refinedIdea,
          ralphQuote: currentIdea.ralphQuote,
          status: currentIdea.status,
          dopeLevel: currentIdea.dopeLevel,
          chaosLevel: currentIdea.chaosLevel,
          pmfScores: currentIdea.pmfScores
        })
      });

      if (response.ok) {
        ralphQuote = "I saved it in my brain box!";
      }
    } catch (err) {
      error = 'Could not save idea';
    }
  }

  function selectIdea(idea: RalphIdea) {
    currentIdea = idea;
    ralphQuote = idea.ralphQuote || getRandomQuote('thinking');
  }

  function newIdea() {
    currentIdea = null;
    prompt = '';
    ralphMood = 'neutral';
    ralphQuote = getRandomQuote('thinking');
  }

  const isLoading = $derived(isGenerating || isRefining);
  const canRefine = $derived(currentIdea && currentIdea.dopeLevel < 4 && currentIdea.iteration < currentIdea.maxIterations);
  const hasGoldStar = $derived((currentIdea?.dopeLevel ?? 0) >= 4);
</script>

<main class="min-h-screen bg-playground-sunset">
  <div class="max-w-7xl mx-auto px-4 py-8">
    <!-- Header -->
    <header class="flex items-center justify-between mb-8">
      <div class="flex items-center gap-4">
        <a href="/" class="text-chalkboard hover:text-sky-blue">
          <span class="text-2xl">🏠</span>
        </a>
        <h1 class="font-chalk text-3xl text-chalkboard">Playground</h1>
      </div>
      <div class="flex items-center gap-4">
        <span class="text-sm text-chalkboard/60">Welcome, {data.user?.email?.split('@')[0]}</span>
        <form action="/auth/logout" method="POST">
          <button class="text-sm text-chalkboard/60 hover:text-chalkboard">Logout</button>
        </form>
      </div>
    </header>

    <div class="grid lg:grid-cols-3 gap-8">
      <!-- Left Column: Ralph & Input -->
      <div class="lg:col-span-1 space-y-6">
        <!-- Ralph Avatar & Quote -->
        <div class="bg-paper rounded-lg border-4 border-chalkboard p-6 text-center">
          <RalphAvatar size="lg" mood={ralphMood} animated={isLoading} />
          <ThoughtBubble quote={ralphQuote} position="top" size="sm" />
        </div>

        <!-- Input Area -->
        <div class="bg-paper rounded-lg border-4 border-chalkboard p-6">
          <h2 class="font-chalk text-xl text-chalkboard mb-4">Ring the Bell!</h2>

          <div class="space-y-4">
            <div>
              <label for="prompt" class="block text-sm font-chalk text-chalkboard mb-2">
                Give Ralph a hint (optional)
              </label>
              <textarea
                id="prompt"
                bind:value={prompt}
                placeholder="Dogs, but for cats? Or something about blockchain cheese?"
                class="w-full px-4 py-3 rounded-lg border-2 border-chalkboard bg-white focus:outline-none focus:ring-2 focus:ring-sky-blue resize-none"
                rows="3"
                disabled={isLoading}
              ></textarea>
            </div>

            <ChaosSlider bind:value={chaosLevel} />

            <div class="flex gap-2">
              {#if currentIdea}
                <button
                  onclick={newIdea}
                  class="flex-1 btn-crayon bg-gray-100"
                  disabled={isLoading}
                >
                  New Idea
                </button>
              {/if}
              <button
                onclick={generateIdea}
                class="flex-1 btn-crayon {isGenerating ? 'animate-wiggle' : ''}"
                disabled={isLoading}
              >
                {#if isGenerating}
                  🔔 Generating...
                {:else}
                  🔔 {currentIdea ? 'Generate New' : 'Ring Bell!'}
                {/if}
              </button>
            </div>
          </div>

          {#if error}
            <p class="text-playground-red text-sm mt-4">{error}</p>
          {/if}
        </div>

        <!-- Ideas History -->
        <div class="bg-paper rounded-lg border-4 border-chalkboard p-6">
          <h2 class="font-chalk text-xl text-chalkboard mb-4">My Ideas ({ideas.length})</h2>
          <div class="space-y-2 max-h-64 overflow-y-auto">
            {#each ideas as idea (idea.id)}
              <IdeaCard
                {idea}
                onclick={() => selectIdea(idea)}
                selected={currentIdea?.id === idea.id}
              />
            {/each}
            {#if ideas.length === 0}
              <p class="text-chalkboard/60 text-sm text-center py-4">
                No ideas yet. Ring the bell!
              </p>
            {/if}
          </div>
        </div>
      </div>

      <!-- Right Column: Current Idea -->
      <div class="lg:col-span-2">
        {#if currentIdea}
          <div class="bg-paper rounded-lg border-4 border-chalkboard p-6">
            <!-- Header -->
            <div class="flex items-start justify-between mb-6">
              <div>
                <div class="flex items-center gap-2 mb-2">
                  {#if hasGoldStar}
                    <span class="gold-star text-3xl">⭐</span>
                  {/if}
                  <h2 class="font-chalk text-2xl text-chalkboard">{currentIdea.name}</h2>
                </div>
                <div class="flex items-center gap-4 text-sm text-chalkboard/60">
                  <span>Iteration: {currentIdea.iteration}/{currentIdea.maxIterations}</span>
                  <span>Status: {currentIdea.status}</span>
                </div>
              </div>
              <DopeMeter level={currentIdea.dopeLevel} size="md" />
            </div>

            <!-- Idea Content -->
            <div class="mb-6">
              <h3 class="font-chalk text-lg text-chalkboard mb-2">The Idea</h3>
              <div class="bg-white/50 rounded-lg p-4 border-2 border-chalkboard/20">
                <p class="text-chalkboard whitespace-pre-wrap">
                  {currentIdea.refinedIdea || currentIdea.rawIdea}
                </p>
              </div>
            </div>

            <!-- PMF Scores -->
            {#if currentIdea.pmfScores}
              <div class="mb-6">
                <h3 class="font-chalk text-lg text-chalkboard mb-4">PMF Analysis</h3>
                <div class="flex justify-center">
                  <PMFRadar scores={currentIdea.pmfScores} size={280} />
                </div>
              </div>
            {/if}

            <!-- Actions -->
            <div class="flex gap-4">
              {#if canRefine}
                <button
                  onclick={refineIdea}
                  class="btn-crayon flex-1 {isRefining ? 'animate-wiggle' : ''}"
                  disabled={isLoading}
                >
                  {#if isRefining}
                    🎢 Refining...
                  {:else}
                    🎢 Refine on Swing Set
                  {/if}
                </button>
              {/if}

              {#if hasGoldStar}
                <a
                  href="/prd/{currentIdea.id}"
                  class="btn-crayon flex-1 bg-gold-star text-center"
                >
                  📝 Generate PRD
                </a>
              {/if}

              <button
                onclick={saveIdea}
                class="btn-crayon bg-playground-green"
                disabled={isLoading}
              >
                💾 Save
              </button>
            </div>
          </div>
        {:else}
          <!-- Empty State -->
          <div class="bg-paper rounded-lg border-4 border-chalkboard p-12 text-center">
            <div class="w-32 h-32 bg-ralph-yellow/30 rounded-full mx-auto mb-6 flex items-center justify-center border-4 border-dashed border-chalkboard/30">
              <span class="text-6xl opacity-50">💡</span>
            </div>
            <h2 class="font-chalk text-2xl text-chalkboard mb-2">The Sandbox is Empty!</h2>
            <p class="ralph-voice text-chalkboard/80 mb-6">
              "Ring the bell and I'll dig up an idea from my brain!"
            </p>
            <button onclick={generateIdea} class="btn-crayon text-xl" disabled={isLoading}>
              🔔 Ring the Bell!
            </button>
          </div>
        {/if}
      </div>
    </div>
  </div>
</main>

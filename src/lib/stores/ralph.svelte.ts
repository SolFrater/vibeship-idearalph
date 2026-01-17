// Ralph Store - Svelte 5 Runes for Ralph Loop State
// Uses $state and $derived for reactive state management

import type { RalphIdea, RalphIteration, PMFScores } from '$lib/ralph/types';

// Create reactive state using Svelte 5 runes pattern
function createRalphStore() {
  // Core state
  let ideas = $state<RalphIdea[]>([]);
  let currentIdea = $state<RalphIdea | null>(null);
  let iterations = $state<RalphIteration[]>([]);
  let isGenerating = $state(false);
  let isRefining = $state(false);
  let error = $state<string | null>(null);
  let chaosLevel = $state(5);

  // Derived state
  const currentDopeLevel = $derived(currentIdea?.dopeLevel ?? 0);
  const currentPMF = $derived(currentIdea?.pmfScores ?? null);
  const isLoading = $derived(isGenerating || isRefining);
  const hasReachedGoldStar = $derived(currentDopeLevel >= 4);

  const pmfAverage = $derived.by(() => {
    if (!currentPMF) return 0;
    const values = Object.values(currentPMF);
    return values.reduce((sum, val) => sum + val, 0) / values.length;
  });

  // Get ideas sorted by dope level
  const topIdeas = $derived(
    [...ideas].sort((a, b) => b.dopeLevel - a.dopeLevel).slice(0, 10)
  );

  // Actions
  function setCurrentIdea(idea: RalphIdea | null) {
    currentIdea = idea;
    if (idea) {
      // Load iterations for this idea
      loadIterations(idea.id);
    } else {
      iterations = [];
    }
  }

  function addIdea(idea: RalphIdea) {
    ideas = [...ideas, idea];
  }

  function updateIdea(updatedIdea: RalphIdea) {
    ideas = ideas.map((i) => (i.id === updatedIdea.id ? updatedIdea : i));
    if (currentIdea?.id === updatedIdea.id) {
      currentIdea = updatedIdea;
    }
  }

  function removeIdea(ideaId: string) {
    ideas = ideas.filter((i) => i.id !== ideaId);
    if (currentIdea?.id === ideaId) {
      currentIdea = null;
      iterations = [];
    }
  }

  function addIteration(iteration: RalphIteration) {
    iterations = [...iterations, iteration];
  }

  function loadIterations(ideaId: string) {
    // This will be called by API - just sets up the container
    iterations = iterations.filter((i) => i.ideaId === ideaId);
  }

  function setIterations(newIterations: RalphIteration[]) {
    iterations = newIterations;
  }

  function setIdeas(newIdeas: RalphIdea[]) {
    ideas = newIdeas;
  }

  function setGenerating(value: boolean) {
    isGenerating = value;
    if (value) error = null;
  }

  function setRefining(value: boolean) {
    isRefining = value;
    if (value) error = null;
  }

  function setError(message: string | null) {
    error = message;
    isGenerating = false;
    isRefining = false;
  }

  function setChaosLevel(level: number) {
    chaosLevel = Math.min(10, Math.max(1, level));
  }

  function reset() {
    currentIdea = null;
    iterations = [];
    isGenerating = false;
    isRefining = false;
    error = null;
  }

  return {
    // State (getters)
    get ideas() { return ideas; },
    get currentIdea() { return currentIdea; },
    get iterations() { return iterations; },
    get isGenerating() { return isGenerating; },
    get isRefining() { return isRefining; },
    get error() { return error; },
    get chaosLevel() { return chaosLevel; },

    // Derived
    get currentDopeLevel() { return currentDopeLevel; },
    get currentPMF() { return currentPMF; },
    get isLoading() { return isLoading; },
    get hasReachedGoldStar() { return hasReachedGoldStar; },
    get pmfAverage() { return pmfAverage; },
    get topIdeas() { return topIdeas; },

    // Actions
    setCurrentIdea,
    addIdea,
    updateIdea,
    removeIdea,
    addIteration,
    loadIterations,
    setIterations,
    setIdeas,
    setGenerating,
    setRefining,
    setError,
    setChaosLevel,
    reset
  };
}

// Export singleton store
export const ralphStore = createRalphStore();

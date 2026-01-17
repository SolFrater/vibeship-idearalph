// Ralph Loop Engine - The Core AI System
// This orchestrates the idea generation and refinement loop

import { askClaude, parseClaudeJSON } from '$lib/server/claude';
import {
  GENERATE_IDEA_PROMPT,
  REFINE_IDEA_PROMPT,
  GENERATE_PRD_PROMPT,
  EVALUATE_IDEA_PROMPT
} from './prompts';
import type {
  RalphIdea,
  RalphIteration,
  RalphLoopConfig,
  RalphLoopResult,
  RalphResponse,
  PMFScores,
  GenerateIdeaInput,
  RefineIdeaInput
} from './types';
import { RALPH_QUOTES } from './types';

/**
 * Get a random Ralph quote for a given mood
 */
function getRandomQuote(mood: 'thinking' | 'excited' | 'meh' | 'dope'): string {
  const quotes = RALPH_QUOTES[mood];
  return quotes[Math.floor(Math.random() * quotes.length)];
}

/**
 * Calculate average PMF score
 */
export function calculatePMFAverage(scores: PMFScores): number {
  const values = Object.values(scores);
  return values.reduce((sum, val) => sum + val, 0) / values.length;
}

/**
 * Determine if idea should continue refining
 */
function shouldContinueRefining(
  dopeLevel: number,
  iteration: number,
  maxIterations: number,
  threshold: number
): boolean {
  // Stop if we've hit max iterations
  if (iteration >= maxIterations) return false;

  // Stop if we've reached the dope threshold
  if (dopeLevel >= threshold) return false;

  // Continue refining
  return true;
}

/**
 * Generate a new idea from scratch
 */
export async function generateIdea(input: GenerateIdeaInput = {}): Promise<RalphResponse> {
  const { prompt, chaosLevel = 5 } = input;

  const promptText = GENERATE_IDEA_PROMPT(chaosLevel, prompt);

  const response = await askClaude(promptText, {
    temperature: 0.7 + (chaosLevel * 0.03), // Higher chaos = more temperature
    maxTokens: 2048
  });

  const parsed = parseClaudeJSON<RalphResponse & { changesMade?: string }>(response);

  return {
    idea: parsed.idea,
    name: parsed.name,
    ralphQuote: parsed.ralphQuote,
    dopeLevel: Math.min(5, Math.max(0, parsed.dopeLevel)),
    pmfScores: parsed.pmfScores,
    feedback: parsed.feedback,
    shouldContinue: parsed.dopeLevel < 4
  };
}

/**
 * Refine an existing idea
 */
export async function refineIdea(
  currentIdea: string,
  currentDopeLevel: number,
  iteration: number,
  maxIterations: number,
  userFeedback?: string,
  chaosLevel: number = 5
): Promise<RalphResponse & { changesMade: string }> {
  const promptText = REFINE_IDEA_PROMPT(
    currentIdea,
    currentDopeLevel,
    iteration,
    maxIterations,
    userFeedback,
    chaosLevel
  );

  const response = await askClaude(promptText, {
    temperature: 0.6 + (chaosLevel * 0.02),
    maxTokens: 2048
  });

  const parsed = parseClaudeJSON<RalphResponse & { changesMade: string }>(response);

  return {
    idea: parsed.idea,
    name: parsed.name,
    ralphQuote: parsed.ralphQuote,
    dopeLevel: Math.min(5, Math.max(0, parsed.dopeLevel)),
    pmfScores: parsed.pmfScores,
    feedback: parsed.feedback,
    changesMade: parsed.changesMade || 'Various improvements',
    shouldContinue: shouldContinueRefining(
      parsed.dopeLevel,
      iteration + 1,
      maxIterations,
      4
    )
  };
}

/**
 * Evaluate an existing idea without modifying it
 */
export async function evaluateIdea(idea: string): Promise<{
  pmfScores: PMFScores;
  dopeLevel: number;
  feedback: string;
  strengths: string[];
  weaknesses: string[];
  ralphQuote: string;
}> {
  const promptText = EVALUATE_IDEA_PROMPT(idea);

  const response = await askClaude(promptText, {
    temperature: 0.5,
    maxTokens: 1024
  });

  return parseClaudeJSON(response);
}

/**
 * Generate a PRD for a completed idea
 */
export async function generatePRD(
  idea: string,
  name: string,
  pmfScores: PMFScores
): Promise<string> {
  const promptText = GENERATE_PRD_PROMPT(idea, name, pmfScores);

  const response = await askClaude(promptText, {
    temperature: 0.6,
    maxTokens: 4096
  });

  return response;
}

/**
 * Run the complete Ralph Loop
 * Generates an idea and refines it until it reaches dope level 4+
 */
export async function runRalphLoop(
  config: RalphLoopConfig,
  initialPrompt?: string
): Promise<RalphLoopResult> {
  const { maxIterations = 3, dopeThreshold = 4, chaosLevel = 5, userId } = config;

  const iterations: RalphIteration[] = [];

  // Generate initial idea
  const initial = await generateIdea({
    prompt: initialPrompt,
    chaosLevel
  });

  let currentIdea: RalphIdea = {
    id: crypto.randomUUID(),
    name: initial.name,
    rawIdea: initial.idea,
    refinedIdea: null,
    ralphQuote: initial.ralphQuote,
    status: 'sandbox',
    dopeLevel: initial.dopeLevel,
    iteration: 0,
    maxIterations,
    pmfScores: initial.pmfScores,
    chaosLevel,
    context: { userId }
  };

  // Store initial iteration
  iterations.push({
    id: crypto.randomUUID(),
    ideaId: currentIdea.id,
    iterationNumber: 0,
    ideaContent: initial.idea,
    dopeLevel: initial.dopeLevel,
    pmfScores: initial.pmfScores,
    ralphFeedback: initial.feedback,
    changesMade: null,
    createdAt: new Date().toISOString()
  });

  // Refine until we hit threshold or max iterations
  let iterationCount = 0;

  while (
    currentIdea.dopeLevel < dopeThreshold &&
    iterationCount < maxIterations
  ) {
    iterationCount++;
    currentIdea.status = 'refining';
    currentIdea.iteration = iterationCount;

    const refined = await refineIdea(
      currentIdea.refinedIdea || currentIdea.rawIdea,
      currentIdea.dopeLevel,
      iterationCount,
      maxIterations,
      undefined,
      chaosLevel
    );

    // Update idea
    currentIdea.name = refined.name;
    currentIdea.refinedIdea = refined.idea;
    currentIdea.ralphQuote = refined.ralphQuote;
    currentIdea.dopeLevel = refined.dopeLevel;
    currentIdea.pmfScores = refined.pmfScores;

    // Store iteration
    iterations.push({
      id: crypto.randomUUID(),
      ideaId: currentIdea.id,
      iterationNumber: iterationCount,
      ideaContent: refined.idea,
      dopeLevel: refined.dopeLevel,
      pmfScores: refined.pmfScores,
      ralphFeedback: refined.feedback,
      changesMade: refined.changesMade,
      createdAt: new Date().toISOString()
    });

    // Check if we should stop
    if (!refined.shouldContinue) break;
  }

  // Set final status
  currentIdea.status = currentIdea.dopeLevel >= dopeThreshold ? 'completed' : 'sandbox';

  return {
    success: currentIdea.dopeLevel >= dopeThreshold,
    idea: currentIdea,
    iterations,
    finalDopeLevel: currentIdea.dopeLevel,
    totalIterations: iterationCount + 1
  };
}

/**
 * Get a status message based on the loop result
 */
export function getLoopStatusMessage(result: RalphLoopResult): {
  title: string;
  message: string;
  quote: string;
} {
  if (result.success) {
    return {
      title: 'Gold Star Achievement!',
      message: `Your idea achieved dope level ${result.finalDopeLevel} in ${result.totalIterations} iterations!`,
      quote: getRandomQuote('dope')
    };
  }

  if (result.finalDopeLevel >= 3) {
    return {
      title: 'Almost There!',
      message: `Dope level ${result.finalDopeLevel} after ${result.totalIterations} iterations. Keep refining!`,
      quote: getRandomQuote('thinking')
    };
  }

  return {
    title: 'Back to the Sandbox',
    message: `Dope level ${result.finalDopeLevel}. This idea needs more work.`,
    quote: getRandomQuote('meh')
  };
}

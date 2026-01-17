// POST /api/ralph/refine - Refine an existing idea
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { refineIdea } from '$lib/ralph/engine';
import { z } from 'zod';

const RefineSchema = z.object({
  currentIdea: z.string().min(1),
  currentDopeLevel: z.number().min(0).max(5),
  iteration: z.number().min(0),
  maxIterations: z.number().min(1).max(10).optional().default(3),
  feedback: z.string().optional(),
  chaosLevel: z.number().min(1).max(10).optional().default(5)
});

export const POST: RequestHandler = async ({ request, locals }) => {
  // Check authentication
  if (!locals.session || !locals.user) {
    throw error(401, 'Authentication required');
  }

  try {
    const body = await request.json();
    const { currentIdea, currentDopeLevel, iteration, maxIterations, feedback, chaosLevel } =
      RefineSchema.parse(body);

    // Refine idea using Ralph
    const result = await refineIdea(
      currentIdea,
      currentDopeLevel,
      iteration,
      maxIterations,
      feedback,
      chaosLevel
    );

    return json({
      success: true,
      data: {
        name: result.name,
        idea: result.idea,
        ralphQuote: result.ralphQuote,
        dopeLevel: result.dopeLevel,
        pmfScores: result.pmfScores,
        feedback: result.feedback,
        changesMade: result.changesMade,
        shouldContinue: result.shouldContinue
      }
    });
  } catch (err) {
    console.error('Error refining idea:', err);

    if (err instanceof z.ZodError) {
      throw error(400, 'Invalid request data');
    }

    throw error(500, 'Failed to refine idea');
  }
};

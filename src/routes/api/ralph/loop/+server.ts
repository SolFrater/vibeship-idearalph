// POST /api/ralph/loop - Run the full Ralph Loop
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { runRalphLoop, getLoopStatusMessage } from '$lib/ralph/engine';
import { z } from 'zod';

const LoopSchema = z.object({
  prompt: z.string().optional(),
  chaosLevel: z.number().min(1).max(10).optional().default(5),
  maxIterations: z.number().min(1).max(10).optional().default(3),
  dopeThreshold: z.number().min(1).max(5).optional().default(4)
});

export const POST: RequestHandler = async ({ request, locals }) => {
  // Check authentication
  if (!locals.session || !locals.user) {
    throw error(401, 'Authentication required');
  }

  try {
    const body = await request.json();
    const { prompt, chaosLevel, maxIterations, dopeThreshold } = LoopSchema.parse(body);

    // Run the full Ralph Loop
    const result = await runRalphLoop(
      {
        maxIterations,
        dopeThreshold,
        chaosLevel,
        userId: locals.user.id
      },
      prompt
    );

    const statusMessage = getLoopStatusMessage(result);

    return json({
      success: result.success,
      data: {
        idea: result.idea,
        iterations: result.iterations,
        finalDopeLevel: result.finalDopeLevel,
        totalIterations: result.totalIterations,
        status: statusMessage
      }
    });
  } catch (err) {
    console.error('Error running Ralph Loop:', err);

    if (err instanceof z.ZodError) {
      throw error(400, 'Invalid request data');
    }

    throw error(500, 'Failed to run Ralph Loop');
  }
};

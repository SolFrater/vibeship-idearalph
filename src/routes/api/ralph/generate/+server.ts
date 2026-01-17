// POST /api/ralph/generate - Generate a new idea
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { generateIdea } from '$lib/ralph/engine';
import { z } from 'zod';

const GenerateSchema = z.object({
  prompt: z.string().optional(),
  chaosLevel: z.number().min(1).max(10).optional().default(5)
});

export const POST: RequestHandler = async ({ request, locals }) => {
  // Check authentication
  if (!locals.session || !locals.user) {
    throw error(401, 'Authentication required');
  }

  try {
    const body = await request.json();
    const { prompt, chaosLevel } = GenerateSchema.parse(body);

    // Generate idea using Ralph
    const result = await generateIdea({
      prompt,
      chaosLevel
    });

    return json({
      success: true,
      data: {
        name: result.name,
        idea: result.idea,
        ralphQuote: result.ralphQuote,
        dopeLevel: result.dopeLevel,
        pmfScores: result.pmfScores,
        feedback: result.feedback,
        shouldContinue: result.shouldContinue
      }
    });
  } catch (err) {
    console.error('Error generating idea:', err);

    if (err instanceof z.ZodError) {
      throw error(400, 'Invalid request data');
    }

    throw error(500, 'Failed to generate idea');
  }
};

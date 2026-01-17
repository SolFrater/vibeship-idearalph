// POST /api/prd/generate - Generate a PRD for an idea
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { generatePRD } from '$lib/ralph/engine';
import { z } from 'zod';

const PRDSchema = z.object({
  idea: z.string().min(1),
  name: z.string().min(1),
  pmfScores: z.object({
    marketSize: z.number().min(0).max(10),
    problemSeverity: z.number().min(0).max(10),
    solutionFit: z.number().min(0).max(10),
    competition: z.number().min(0).max(10),
    vibeCodeable: z.number().min(0).max(10),
    virality: z.number().min(0).max(10)
  })
});

export const POST: RequestHandler = async ({ request, locals }) => {
  // Check authentication
  if (!locals.session || !locals.user) {
    throw error(401, 'Authentication required');
  }

  try {
    const body = await request.json();
    const { idea, name, pmfScores } = PRDSchema.parse(body);

    // Generate PRD
    const markdown = await generatePRD(idea, name, pmfScores);

    return json({
      success: true,
      data: {
        markdown,
        name,
        generatedAt: new Date().toISOString()
      }
    });
  } catch (err) {
    console.error('Error generating PRD:', err);

    if (err instanceof z.ZodError) {
      throw error(400, 'Invalid request data');
    }

    throw error(500, 'Failed to generate PRD');
  }
};

// GET /api/ideas/[id] - Get single idea
// PATCH /api/ideas/[id] - Update idea
// DELETE /api/ideas/[id] - Delete idea
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { z } from 'zod';

const UpdateIdeaSchema = z.object({
  name: z.string().min(1).max(200).optional(),
  refinedIdea: z.string().optional(),
  ralphQuote: z.string().optional(),
  status: z.enum(['sandbox', 'validating', 'refining', 'completed', 'archived']).optional(),
  dopeLevel: z.number().min(0).max(5).optional(),
  iteration: z.number().min(0).optional(),
  chaosLevel: z.number().min(1).max(10).optional(),
  pmfScores: z
    .object({
      marketSize: z.number().min(0).max(10),
      problemSeverity: z.number().min(0).max(10),
      solutionFit: z.number().min(0).max(10),
      competition: z.number().min(0).max(10),
      vibeCodeable: z.number().min(0).max(10),
      virality: z.number().min(0).max(10)
    })
    .optional()
});

// GET - Single idea
export const GET: RequestHandler = async ({ params, locals }) => {
  if (!locals.session || !locals.user) {
    throw error(401, 'Authentication required');
  }

  const { data, error: dbError } = await locals.supabase
    .from('ideas')
    .select('*, idea_iterations(*)')
    .eq('id', params.id)
    .eq('user_id', locals.user.id)
    .single();

  if (dbError || !data) {
    throw error(404, 'Idea not found');
  }

  return json({ success: true, data });
};

// PATCH - Update idea
export const PATCH: RequestHandler = async ({ params, request, locals }) => {
  if (!locals.session || !locals.user) {
    throw error(401, 'Authentication required');
  }

  try {
    const body = await request.json();
    const validated = UpdateIdeaSchema.parse(body);

    // Build update object
    const updateData: Record<string, unknown> = {};

    if (validated.name !== undefined) updateData.name = validated.name;
    if (validated.refinedIdea !== undefined) updateData.refined_idea = validated.refinedIdea;
    if (validated.ralphQuote !== undefined) updateData.ralph_quote = validated.ralphQuote;
    if (validated.status !== undefined) updateData.status = validated.status;
    if (validated.dopeLevel !== undefined) updateData.dope_level = validated.dopeLevel;
    if (validated.iteration !== undefined) updateData.iteration = validated.iteration;
    if (validated.chaosLevel !== undefined) updateData.chaos_level = validated.chaosLevel;

    if (validated.pmfScores) {
      updateData.pmf_market_size = validated.pmfScores.marketSize;
      updateData.pmf_problem_severity = validated.pmfScores.problemSeverity;
      updateData.pmf_solution_fit = validated.pmfScores.solutionFit;
      updateData.pmf_competition = validated.pmfScores.competition;
      updateData.pmf_vibe_codeable = validated.pmfScores.vibeCodeable;
      updateData.pmf_virality = validated.pmfScores.virality;
    }

    const { data, error: dbError } = await (locals.supabase as any)
      .from('ideas')
      .update(updateData)
      .eq('id', params.id)
      .eq('user_id', locals.user.id)
      .select()
      .single();

    if (dbError || !data) {
      throw error(404, 'Idea not found');
    }

    return json({ success: true, data });
  } catch (err) {
    if (err instanceof z.ZodError) {
      throw error(400, 'Invalid update data');
    }
    throw err;
  }
};

// DELETE - Delete idea
export const DELETE: RequestHandler = async ({ params, locals }) => {
  if (!locals.session || !locals.user) {
    throw error(401, 'Authentication required');
  }

  const { error: dbError } = await locals.supabase
    .from('ideas')
    .delete()
    .eq('id', params.id)
    .eq('user_id', locals.user.id);

  if (dbError) {
    throw error(500, 'Failed to delete idea');
  }

  return json({ success: true });
};

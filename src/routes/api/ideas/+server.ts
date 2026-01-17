// GET /api/ideas - List user's ideas
// POST /api/ideas - Save a new idea
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { z } from 'zod';

const CreateIdeaSchema = z.object({
  name: z.string().min(1).max(200),
  rawIdea: z.string().min(1),
  refinedIdea: z.string().optional(),
  ralphQuote: z.string().optional(),
  status: z.enum(['sandbox', 'validating', 'refining', 'completed', 'archived']).optional(),
  dopeLevel: z.number().min(0).max(5).optional(),
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

// GET - List ideas
export const GET: RequestHandler = async ({ locals, url }) => {
  if (!locals.session || !locals.user) {
    throw error(401, 'Authentication required');
  }

  const limit = Math.min(50, parseInt(url.searchParams.get('limit') ?? '20'));
  const offset = parseInt(url.searchParams.get('offset') ?? '0');
  const status = url.searchParams.get('status');

  let query = locals.supabase
    .from('ideas')
    .select('*')
    .eq('user_id', locals.user.id)
    .order('created_at', { ascending: false })
    .range(offset, offset + limit - 1);

  if (status) {
    query = query.eq('status', status);
  }

  const { data, error: dbError } = await query;

  if (dbError) {
    console.error('Error fetching ideas:', dbError);
    throw error(500, 'Failed to fetch ideas');
  }

  return json({
    success: true,
    data: data ?? [],
    pagination: { limit, offset }
  });
};

// POST - Create idea
export const POST: RequestHandler = async ({ request, locals }) => {
  if (!locals.session || !locals.user) {
    throw error(401, 'Authentication required');
  }

  try {
    const body = await request.json();
    const validated = CreateIdeaSchema.parse(body);

    const insertData = {
      user_id: locals.user.id,
      name: validated.name,
      raw_idea: validated.rawIdea,
      refined_idea: validated.refinedIdea ?? null,
      ralph_quote: validated.ralphQuote ?? null,
      status: validated.status ?? 'sandbox',
      dope_level: validated.dopeLevel ?? 0,
      chaos_level: validated.chaosLevel ?? 5,
      pmf_market_size: validated.pmfScores?.marketSize ?? null,
      pmf_problem_severity: validated.pmfScores?.problemSeverity ?? null,
      pmf_solution_fit: validated.pmfScores?.solutionFit ?? null,
      pmf_competition: validated.pmfScores?.competition ?? null,
      pmf_vibe_codeable: validated.pmfScores?.vibeCodeable ?? null,
      pmf_virality: validated.pmfScores?.virality ?? null
    };

    const { data, error: dbError } = await locals.supabase
      .from('ideas')
      .insert(insertData as any)
      .select()
      .single();

    if (dbError) {
      console.error('Error creating idea:', dbError);
      throw error(500, 'Failed to save idea');
    }

    return json({
      success: true,
      data
    });
  } catch (err) {
    if (err instanceof z.ZodError) {
      throw error(400, 'Invalid idea data');
    }
    throw err;
  }
};

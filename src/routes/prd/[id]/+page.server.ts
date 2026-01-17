import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { Database } from '$lib/types/database';

type IdeaRow = Database['public']['Tables']['ideas']['Row'];

export const load: PageServerLoad = async ({ params, locals }) => {
  // Fetch the idea
  const { data: idea, error: dbError } = await locals.supabase
    .from('ideas')
    .select('*')
    .eq('id', params.id)
    .eq('user_id', locals.user!.id)
    .single();

  if (dbError || !idea) {
    throw error(404, 'Idea not found');
  }

  // Check if idea has gold star status
  if ((idea as IdeaRow).dope_level < 4) {
    throw error(403, 'Idea must reach Gold Star status to generate PRD');
  }

  return {
    idea: idea as IdeaRow
  };
};

import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  // User is already validated by hooks.server.ts authGuard
  // Load user's ideas
  const { data: ideas } = await locals.supabase
    .from('ideas')
    .select('*')
    .eq('user_id', locals.user!.id)
    .order('created_at', { ascending: false })
    .limit(20);

  return {
    ideas: ideas ?? []
  };
};

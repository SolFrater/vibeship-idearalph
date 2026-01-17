import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
  if (locals.session) {
    redirect(303, '/playground');
  }
};

export const actions: Actions = {
  default: async ({ request, locals: { supabase }, url }) => {
    const formData = await request.formData();
    const email = formData.get('email') as string;
    const password = formData.get('password') as string;
    const displayName = formData.get('displayName') as string;

    if (!email || !password) {
      return fail(400, { error: 'Email and password are required' });
    }

    if (password.length < 6) {
      return fail(400, { error: 'Password must be at least 6 characters' });
    }

    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${url.origin}/auth/callback`,
        data: {
          display_name: displayName || null
        }
      }
    });

    if (error) {
      return fail(400, { error: error.message });
    }

    return { success: true };
  }
};

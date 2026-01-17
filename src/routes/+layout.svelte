<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
  import { invalidate } from '$app/navigation';

  let { children, data } = $props();

  // Supabase auth state listener
  onMount(() => {
    const { data: { subscription } } = data.supabase.auth.onAuthStateChange(
      (event, session) => {
        if (session?.expires_at !== data.session?.expires_at) {
          invalidate('supabase:auth');
        }
      }
    );

    return () => subscription.unsubscribe();
  });
</script>

<svelte:head>
  <title>IdeaRalph - The Dumbest Genius You'll Ever Meet</title>
</svelte:head>

<div class="min-h-full">
  {@render children()}
</div>

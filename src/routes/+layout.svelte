<script lang="ts">
  import '../app.css';
  import { Navbar } from '$lib/components';

  let { children } = $props();
</script>

<svelte:head>
  <title>IdeaRalph - Stupid Smart</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
  <link
    href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Patrick+Hand&family=Inter:wght@400;500;600;700&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<Navbar />

<div class="min-h-full">
  {@render children()}
</div>

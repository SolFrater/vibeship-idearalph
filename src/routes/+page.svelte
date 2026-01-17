<script lang="ts">
  import { goto } from '$app/navigation';

  let { data } = $props();

  let bellRinging = $state(false);

  async function spawnRalph() {
    bellRinging = true;

    // Small delay for animation
    await new Promise((r) => setTimeout(r, 800));

    if (data.session) {
      goto('/playground');
    } else {
      goto('/auth/login');
    }
  }
</script>

<main class="min-h-screen bg-playground-sunset">
  <!-- Hero Section -->
  <div class="flex flex-col items-center justify-center min-h-screen px-4 text-center">
    <!-- Ralph Character Placeholder -->
    <div class="mb-8 animate-float">
      <div
        class="w-48 h-48 bg-ralph-yellow rounded-full border-4 border-chalkboard shadow-crayon-lg flex items-center justify-center"
      >
        <span class="text-6xl">🧒</span>
      </div>
    </div>

    <!-- Title -->
    <h1
      class="text-5xl md:text-7xl font-chalk text-chalkboard mb-4 text-shadow-crayon"
    >
      IdeaRalph
    </h1>

    <p class="ralph-voice text-2xl md:text-3xl text-chalkboard mb-2">
      "I'm a idea generator! And I'm helping!"
    </p>

    <p class="text-lg text-chalkboard/80 mb-8 max-w-md">
      The dumbest genius you'll ever meet. Generate startup ideas so weird
      they might actually work.
    </p>

    <!-- Spawn Button -->
    <button
      onclick={spawnRalph}
      class="btn-crayon text-2xl flex items-center gap-3 {bellRinging
        ? 'animate-wiggle'
        : ''}"
    >
      <span class="text-3xl">🔔</span>
      Ring the Bell
    </button>

    <!-- Tagline -->
    <p class="mt-8 text-sm text-chalkboard/60">
      {#if data.session}
        Ready to spawn Ralph!
      {:else}
        Sign up free to start generating ideas
      {/if}
    </p>
  </div>

  <!-- Features Section -->
  <section class="bg-paper py-16 px-4">
    <div class="max-w-4xl mx-auto">
      <h2 class="text-4xl font-chalk text-center text-chalkboard mb-12">
        How It Works
      </h2>

      <div class="grid md:grid-cols-3 gap-8">
        <!-- Step 1 -->
        <div class="text-center">
          <div
            class="w-20 h-20 bg-ralph-yellow rounded-full mx-auto mb-4 flex items-center justify-center border-4 border-chalkboard shadow-crayon"
          >
            <span class="text-3xl">🏖️</span>
          </div>
          <h3 class="font-chalk text-xl mb-2">1. Sandbox</h3>
          <p class="ralph-voice text-chalkboard/80">
            Ralph digs around in his brain and finds weird connections
          </p>
        </div>

        <!-- Step 2 -->
        <div class="text-center">
          <div
            class="w-20 h-20 bg-playground-green rounded-full mx-auto mb-4 flex items-center justify-center border-4 border-chalkboard shadow-crayon"
          >
            <span class="text-3xl">🎢</span>
          </div>
          <h3 class="font-chalk text-xl mb-2">2. Swing Set</h3>
          <p class="ralph-voice text-chalkboard/80">
            Ideas swing back and forth until they get momentum
          </p>
        </div>

        <!-- Step 3 -->
        <div class="text-center">
          <div
            class="w-20 h-20 bg-sky-blue rounded-full mx-auto mb-4 flex items-center justify-center border-4 border-chalkboard shadow-crayon"
          >
            <span class="text-3xl">⭐</span>
          </div>
          <h3 class="font-chalk text-xl mb-2">3. Gold Star</h3>
          <p class="ralph-voice text-chalkboard/80">
            You get a PRD that's actually genius (probably)
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Dope Ideas Section -->
  <section class="bg-chalkboard py-16 px-4">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-4xl font-chalk text-ralph-yellow mb-8">
        Ideas So Dumb They're Genius
      </h2>

      <div class="grid md:grid-cols-2 gap-6">
        <div class="thought-bubble bg-paper text-left">
          <p class="ralph-voice">
            "What if dogs had their own social media? My dog would post about
            butts a lot."
          </p>
          <p class="text-sm text-chalkboard/60 mt-2">— Actual Ralph idea</p>
        </div>

        <div class="thought-bubble bg-paper text-left">
          <p class="ralph-voice">
            "This idea tastes like purple and also like money!"
          </p>
          <p class="text-sm text-chalkboard/60 mt-2">— Dope level: 5/5</p>
        </div>
      </div>

      <p class="text-white/80 mt-8 ralph-voice">
        Airbnb sounded dumb. Uber sounded dumb. Twitter sounded dumb.
        <br />
        <span class="text-ralph-yellow">All of them worked.</span>
      </p>
    </div>
  </section>

  <!-- Footer -->
  <footer class="bg-paper py-8 px-4 text-center">
    <p class="text-chalkboard/60">
      Built with 🖍️ by
      <a href="https://vibeship.com" class="text-sky-blue hover:underline">
        Vibeship
      </a>
    </p>
    <p class="text-sm text-chalkboard/40 mt-2">
      "I'm helping!" — Ralph Wiggum
    </p>
  </footer>
</main>

<script lang="ts">
  import { goto } from '$app/navigation';
  import { RalphAvatar, HeroVideo } from '$lib/components';

  let { data } = $props();

  let bellRinging = $state(false);
  let mounted = $state(false);

  // Trigger entrance animations
  $effect(() => {
    mounted = true;
  });

  async function spawnRalph() {
    bellRinging = true;

    // Bell ring animation
    await new Promise((r) => setTimeout(r, 800));

    if (data.session) {
      goto('/playground');
    } else {
      goto('/auth/login');
    }
  }

  const stats = [
    { value: '∞', label: 'Ideas Generated', icon: '💡' },
    { value: '5⭐', label: 'Max Dope Level', icon: '🌟' },
    { value: '0', label: 'Bad Ideas*', icon: '🚀' }
  ];
</script>

<main class="bg-playground-sunset overflow-hidden">
  <!-- Hero Section - Half-screen Video Background -->
  <HeroVideo size="half">
    <!-- Overlay Content -->
    <div class="text-center max-w-4xl mx-auto">
      <!-- Handwritten "Hi I'm" label -->
      <div
        class="mb-4 transition-all duration-700 {mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}"
      >
        <span class="inline-block bg-white/90 backdrop-blur-sm rounded-full px-6 py-2
                     border-2 border-chalkboard shadow-crayon transform -rotate-2">
          <span class="ralph-voice text-lg md:text-xl text-chalkboard">Hi, I'm</span>
        </span>
      </div>

      <!-- Title -->
      <h1
        class="text-6xl md:text-8xl lg:text-9xl font-chalk mb-6
               transition-all duration-700 delay-100
               {mounted ? 'opacity-100 translate-y-0 scale-100' : 'opacity-0 translate-y-10 scale-95'}"
      >
        <span class="text-chalkboard drop-shadow-[0_4px_0_rgba(0,0,0,0.2)]">Idea</span><span
          class="text-playground-red drop-shadow-[0_4px_0_rgba(0,0,0,0.2)]">Ralph</span>
      </h1>

      <!-- Tagline in thought bubble style -->
      <div
        class="mb-8 transition-all duration-700 delay-200
               {mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}"
      >
        <div class="inline-block bg-white/95 backdrop-blur-sm rounded-2xl px-8 py-4
                    border-4 border-chalkboard shadow-crayon-lg relative">
          <p class="ralph-voice text-xl md:text-2xl lg:text-3xl text-chalkboard">
            "I'm a idea generator! And I'm helping!"
          </p>
          <!-- Speech bubble tail -->
          <div class="absolute -bottom-3 left-1/2 -translate-x-1/2 w-6 h-6 bg-white border-r-4 border-b-4
                      border-chalkboard transform rotate-45"></div>
        </div>
      </div>

      <!-- Subtitle -->
      <p
        class="text-lg md:text-xl text-chalkboard/90 mb-10 max-w-2xl mx-auto
               transition-all duration-700 delay-300 font-medium
               {mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}"
      >
        The dumbest genius you'll ever meet. Generate startup ideas so weird
        they might actually work.
      </p>

      <!-- CTA Button -->
      <div
        class="transition-all duration-700 delay-400
               {mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}"
      >
        <button
          onclick={spawnRalph}
          class="btn-crayon text-xl md:text-2xl px-10 py-5 flex items-center gap-4 mx-auto
                 transform hover:scale-105 transition-transform
                 {bellRinging ? 'animate-wiggle' : ''}"
        >
          <span class="text-3xl md:text-4xl group-hover:animate-wiggle">🔔</span>
          <span>Ring the Bell</span>
        </button>
      </div>

      <!-- Status tag -->
      <p
        class="mt-8 transition-all duration-700 delay-500
               {mounted ? 'opacity-100' : 'opacity-0'}"
      >
        {#if data.session}
          <span class="inline-flex items-center gap-2 bg-playground-green/20 backdrop-blur-sm
                       text-chalkboard px-4 py-2 rounded-full border-2 border-playground-green/50">
            <span class="text-playground-green">✓</span> Ready to spawn Ralph!
          </span>
        {:else}
          <span class="inline-flex items-center gap-2 bg-white/30 backdrop-blur-sm
                       text-chalkboard px-4 py-2 rounded-full">
            Sign up free • No credit card required
          </span>
        {/if}
      </p>
    </div>
  </HeroVideo>

  <!-- Stats Section -->
  <section class="bg-chalkboard py-12 px-4">
    <div class="max-w-4xl mx-auto">
      <div class="grid grid-cols-3 gap-4 md:gap-8">
        {#each stats as stat, i}
          <div class="text-center">
            <span class="text-3xl md:text-4xl mb-2 block">{stat.icon}</span>
            <p class="text-2xl md:text-4xl font-chalk text-ralph-yellow">{stat.value}</p>
            <p class="text-xs md:text-sm text-white/60">{stat.label}</p>
          </div>
        {/each}
      </div>
      <p class="text-center text-white/40 text-xs mt-4">*Subjectively speaking</p>
    </div>
  </section>

  <!-- Features Section -->
  <section class="bg-paper py-16 md:py-24 px-4">
    <div class="max-w-4xl mx-auto">
      <h2 class="text-3xl md:text-4xl font-chalk text-center text-chalkboard mb-4">
        How It Works
      </h2>
      <p class="text-center text-chalkboard/60 mb-12 max-w-md mx-auto">
        Three simple steps to genius (or at least entertaining) ideas
      </p>

      <div class="grid md:grid-cols-3 gap-8 md:gap-12">
        <!-- Step 1 -->
        <div class="text-center group">
          <div
            class="w-24 h-24 bg-ralph-yellow rounded-full mx-auto mb-4 flex items-center justify-center
                   border-4 border-chalkboard shadow-crayon
                   transition-transform group-hover:scale-110 group-hover:rotate-3"
          >
            <span class="text-4xl">🏖️</span>
          </div>
          <h3 class="font-chalk text-xl mb-2">1. Sandbox</h3>
          <p class="ralph-voice text-chalkboard/80">
            "Ralph digs around in his brain and finds weird connections"
          </p>
        </div>

        <!-- Arrow -->
        <div class="hidden md:flex items-center justify-center">
          <span class="text-4xl text-chalkboard/30">→</span>
        </div>

        <!-- Step 2 -->
        <div class="text-center group md:col-start-2 md:row-start-1">
          <div
            class="w-24 h-24 bg-playground-green rounded-full mx-auto mb-4 flex items-center justify-center
                   border-4 border-chalkboard shadow-crayon
                   transition-transform group-hover:scale-110 group-hover:-rotate-3"
          >
            <span class="text-4xl">🎢</span>
          </div>
          <h3 class="font-chalk text-xl mb-2">2. Swing Set</h3>
          <p class="ralph-voice text-chalkboard/80">
            "Ideas swing back and forth until they get momentum"
          </p>
        </div>

        <!-- Step 3 -->
        <div class="text-center group md:col-start-3">
          <div
            class="w-24 h-24 bg-sky-blue rounded-full mx-auto mb-4 flex items-center justify-center
                   border-4 border-chalkboard shadow-crayon
                   transition-transform group-hover:scale-110 group-hover:rotate-3"
          >
            <span class="text-4xl">⭐</span>
          </div>
          <h3 class="font-chalk text-xl mb-2">3. Gold Star</h3>
          <p class="ralph-voice text-chalkboard/80">
            "You get a PRD that's actually genius (probably)"
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Dope Ideas Section -->
  <section class="bg-gradient-to-b from-chalkboard to-chalkboard/90 py-16 md:py-24 px-4">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-3xl md:text-4xl font-chalk text-ralph-yellow mb-4">
        Ideas So Dumb They're Genius
      </h2>
      <p class="text-white/60 mb-12">Real examples from Ralph's beautiful brain</p>

      <div class="grid md:grid-cols-2 gap-6">
        <div
          class="thought-bubble bg-paper text-left hover:scale-[1.02] transition-transform cursor-default"
        >
          <p class="ralph-voice text-lg">
            "What if dogs had their own social media? My dog would post about
            butts a lot."
          </p>
          <div class="flex items-center justify-between mt-4">
            <p class="text-sm text-chalkboard/60">— Actual Ralph idea</p>
            <div class="flex gap-1">
              <span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span><span class="opacity-30">⭐</span>
            </div>
          </div>
        </div>

        <div
          class="thought-bubble bg-paper text-left hover:scale-[1.02] transition-transform cursor-default"
        >
          <p class="ralph-voice text-lg">
            "Uber but the cars are boats and the roads are rivers. Wait, that's just boats."
          </p>
          <div class="flex items-center justify-between mt-4">
            <p class="text-sm text-chalkboard/60">— Dope level: 3/5</p>
            <div class="flex gap-1">
              <span>⭐</span><span>⭐</span><span>⭐</span><span class="opacity-30">⭐</span><span class="opacity-30">⭐</span>
            </div>
          </div>
        </div>

        <div
          class="thought-bubble bg-paper text-left hover:scale-[1.02] transition-transform cursor-default"
        >
          <p class="ralph-voice text-lg">
            "AI that writes your excuses for being late. It learns your boss's personality!"
          </p>
          <div class="flex items-center justify-between mt-4">
            <p class="text-sm text-chalkboard/60">— Gold star material</p>
            <div class="flex gap-1">
              <span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span>
            </div>
          </div>
        </div>

        <div
          class="thought-bubble bg-paper text-left hover:scale-[1.02] transition-transform cursor-default"
        >
          <p class="ralph-voice text-lg">
            "This idea tastes like purple and also like money!"
          </p>
          <div class="flex items-center justify-between mt-4">
            <p class="text-sm text-chalkboard/60">— Classic Ralph</p>
            <div class="flex gap-1">
              <span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-12 p-6 bg-white/5 rounded-lg border border-white/10">
        <p class="text-white/80 ralph-voice text-lg">
          Airbnb sounded dumb. Uber sounded dumb. Twitter sounded dumb.
        </p>
        <p class="text-ralph-yellow font-chalk text-2xl mt-2">
          All of them worked.
        </p>
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="bg-playground-sunset py-16 md:py-24 px-4">
    <div class="max-w-2xl mx-auto text-center">
      <RalphAvatar size="lg" mood="excited" />
      <h2 class="font-chalk text-3xl md:text-4xl text-chalkboard mt-6 mb-4">
        Ready to Generate Some Genius?
      </h2>
      <p class="ralph-voice text-chalkboard/80 mb-8">
        "My brain has so many ideas it hurts! Let me share them with you!"
      </p>
      <button
        onclick={spawnRalph}
        class="btn-crayon text-xl md:text-2xl"
      >
        🔔 Ring the Bell
      </button>
    </div>
  </section>

  <!-- Footer -->
  <footer class="bg-paper py-8 px-4">
    <div class="max-w-4xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 bg-ralph-yellow rounded-full flex items-center justify-center border-2 border-chalkboard">
          <span class="text-sm">🧒</span>
        </div>
        <span class="font-chalk text-chalkboard">IdeaRalph</span>
      </div>

      <p class="text-chalkboard/60 text-sm">
        Built with 🖍️ by
        <a href="https://vibeship.com" class="text-sky-blue hover:underline">
          Vibeship
        </a>
      </p>

      <p class="text-chalkboard/40 text-sm ralph-voice">
        "I'm helping!" — Ralph Wiggum
      </p>
    </div>
  </footer>
</main>

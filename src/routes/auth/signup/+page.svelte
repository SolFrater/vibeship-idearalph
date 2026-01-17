<script lang="ts">
  import { enhance } from '$app/forms';

  let { form } = $props();
  let loading = $state(false);
</script>

<main class="min-h-screen bg-playground-sunset flex items-center justify-center px-4">
  <div class="bg-paper rounded-lg border-4 border-chalkboard shadow-crayon-lg p-8 max-w-md w-full">
    <div class="text-center mb-8">
      <div class="w-24 h-24 bg-playground-green rounded-full mx-auto mb-4 flex items-center justify-center border-4 border-chalkboard shadow-crayon">
        <span class="text-4xl">🎒</span>
      </div>
      <h1 class="font-chalk text-3xl text-chalkboard">Join the Playground!</h1>
      <p class="ralph-voice text-chalkboard/80 mt-2">"We have fun and also ideas!"</p>
    </div>

    {#if form?.error}
      <div class="bg-playground-red/20 border-2 border-playground-red rounded-lg p-4 mb-6">
        <p class="text-playground-red text-sm">{form.error}</p>
      </div>
    {/if}

    {#if form?.success}
      <div class="bg-playground-green/20 border-2 border-playground-green rounded-lg p-4 mb-6">
        <p class="text-playground-green text-sm">Check your email for the confirmation link!</p>
      </div>
    {/if}

    <form
      method="POST"
      use:enhance={() => {
        loading = true;
        return async ({ update }) => {
          loading = false;
          await update();
        };
      }}
      class="space-y-6"
    >
      <div>
        <label for="email" class="block font-chalk text-chalkboard mb-2">Email</label>
        <input
          type="email"
          id="email"
          name="email"
          required
          class="w-full px-4 py-3 rounded-lg border-2 border-chalkboard bg-white focus:outline-none focus:ring-2 focus:ring-sky-blue"
          placeholder="ralph@springfield.edu"
        />
      </div>

      <div>
        <label for="password" class="block font-chalk text-chalkboard mb-2">Password</label>
        <input
          type="password"
          id="password"
          name="password"
          required
          minlength="6"
          class="w-full px-4 py-3 rounded-lg border-2 border-chalkboard bg-white focus:outline-none focus:ring-2 focus:ring-sky-blue"
          placeholder="••••••••"
        />
      </div>

      <div>
        <label for="displayName" class="block font-chalk text-chalkboard mb-2">Display Name (optional)</label>
        <input
          type="text"
          id="displayName"
          name="displayName"
          class="w-full px-4 py-3 rounded-lg border-2 border-chalkboard bg-white focus:outline-none focus:ring-2 focus:ring-sky-blue"
          placeholder="Your playground name"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        class="btn-crayon w-full text-lg {loading ? 'opacity-50 cursor-not-allowed' : ''}"
      >
        {#if loading}
          <span class="animate-wiggle inline-block">🎢</span> Joining...
        {:else}
          Join the Fun! 🎢
        {/if}
      </button>
    </form>

    <p class="text-center mt-6 text-chalkboard/80">
      Already have an account?
      <a href="/auth/login" class="text-sky-blue hover:underline font-chalk">Sign in!</a>
    </p>
  </div>
</main>

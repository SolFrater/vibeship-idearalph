<script>
  const lastUpdated = "January 2026";
</script>

<svelte:head>
  <title>Privacy Policy | IdeaRalph</title>
  <meta name="description" content="Privacy Policy for IdeaRalph - AI-powered startup idea validation" />
</svelte:head>

<main class="min-h-screen bg-paper">
  <!-- Header -->
  <header class="bg-ralph-yellow/20 py-8 px-4 border-b border-chalkboard/10">
    <div class="max-w-3xl mx-auto">
      <a href="/" class="inline-flex items-center gap-2 text-chalkboard/60 hover:text-chalkboard mb-4 transition-colors">
        <span>&larr;</span>
        <span>Back to IdeaRalph</span>
      </a>
      <h1 class="font-chalk text-4xl text-chalkboard">Privacy Policy</h1>
      <p class="text-chalkboard/60 mt-2">Last updated: {lastUpdated}</p>
    </div>
  </header>

  <!-- Content -->
  <div class="max-w-3xl mx-auto py-12 px-4">
    <div class="space-y-10">

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">The Short Version</h2>
        <div class="bg-playground-green/10 border border-playground-green/30 rounded-lg p-6">
          <p class="text-chalkboard/80 leading-relaxed font-medium">
            IdeaRalph doesn't collect your data. Your ideas stay on your machine. We don't track you.
            The MCP runs locally and doesn't phone home. That's it.
          </p>
        </div>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">1. Information We Don't Collect</h2>
        <p class="text-chalkboard/80 leading-relaxed mb-4">
          Unlike most services, here's what we <strong>don't</strong> collect:
        </p>
        <ul class="list-disc pl-6 text-chalkboard/80 space-y-2">
          <li><strong>Your ideas:</strong> We never see, store, or process your startup ideas</li>
          <li><strong>Your projects:</strong> The MCP doesn't transmit project information</li>
          <li><strong>Your PRDs:</strong> Generated documents stay on your machine</li>
          <li><strong>Personal information:</strong> No accounts, no sign-ups, no profiles</li>
          <li><strong>Usage analytics:</strong> No tracking pixels, no session recording</li>
        </ul>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">2. How IdeaRalph Works</h2>
        <p class="text-chalkboard/80 leading-relaxed mb-4">
          Understanding how the tool works explains why we don't have your data:
        </p>
        <ul class="list-disc pl-6 text-chalkboard/80 space-y-2">
          <li><strong>MCP Server:</strong> Runs locally on your machine within Claude Code</li>
          <li><strong>Processing:</strong> All idea validation happens in your local Claude session</li>
          <li><strong>Storage:</strong> Any files created are saved locally by you</li>
          <li><strong>No Backend:</strong> There's no server receiving your requests</li>
        </ul>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">3. The Web Interface</h2>
        <p class="text-chalkboard/80 leading-relaxed mb-4">
          If you use the IdeaRalph web interface:
        </p>
        <ul class="list-disc pl-6 text-chalkboard/80 space-y-2">
          <li>It's a static site with no backend database</li>
          <li>We don't use cookies for tracking</li>
          <li>We don't use third-party analytics services</li>
          <li>Any ideas you enter are processed client-side only</li>
        </ul>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">4. Third-Party Services</h2>
        <p class="text-chalkboard/80 leading-relaxed mb-4">
          When you use IdeaRalph through Claude Code:
        </p>
        <ul class="list-disc pl-6 text-chalkboard/80 space-y-2">
          <li><strong>Anthropic:</strong> Your prompts are processed by Claude according to Anthropic's privacy policy</li>
          <li><strong>GitHub:</strong> If you clone/fork the repo, GitHub's policies apply to that interaction</li>
        </ul>
        <p class="text-chalkboard/80 leading-relaxed mt-4">
          We encourage you to review Anthropic's privacy policy for details on how Claude handles your conversations.
        </p>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">5. Your Rights (GDPR & CCPA)</h2>
        <p class="text-chalkboard/80 leading-relaxed mb-4">
          Since we don't collect personal data, traditional data rights requests don't apply. However:
        </p>
        <ul class="list-disc pl-6 text-chalkboard/80 space-y-2">
          <li><strong>Right to know:</strong> This policy tells you everything</li>
          <li><strong>Right to delete:</strong> Nothing to delete on our end</li>
          <li><strong>Right to portability:</strong> Your data is already on your machine</li>
          <li><strong>Right to opt-out:</strong> No tracking to opt out of</li>
        </ul>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">6. Children's Privacy</h2>
        <p class="text-chalkboard/80 leading-relaxed">
          IdeaRalph is intended for use by adults and business professionals. We don't knowingly
          collect information from children under 13. Since we don't collect data from anyone,
          this isn't a practical concern.
        </p>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">7. Changes to This Policy</h2>
        <p class="text-chalkboard/80 leading-relaxed">
          If we ever change how IdeaRalph handles data (for example, if we add cloud features),
          we'll update this policy and make it clear what changed. The "last updated" date at
          the top will reflect any changes.
        </p>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">8. Contact</h2>
        <p class="text-chalkboard/80 leading-relaxed">
          Questions about privacy? Visit
          <a href="https://vibeship.co" class="text-sky-blue hover:underline" target="_blank" rel="noopener noreferrer">vibeship.co</a>.
        </p>
      </section>

    </div>
  </div>

  <!-- Footer -->
  <footer class="bg-paper py-6 px-4 border-t border-chalkboard/10">
    <div class="max-w-3xl mx-auto flex items-center justify-between">
      <a href="/" class="flex items-center gap-2 text-chalkboard/60 hover:text-chalkboard transition-colors">
        <span class="font-chalk">IdeaRalph</span>
      </a>
      <div class="flex items-center gap-4 text-xs text-chalkboard/40">
        <a href="/terms" class="hover:text-chalkboard/70 transition-colors">Terms</a>
        <span>Privacy</span>
      </div>
    </div>
  </footer>
</main>

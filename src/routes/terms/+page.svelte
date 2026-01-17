<script>
  const lastUpdated = "January 2026";
</script>

<svelte:head>
  <title>Terms of Service | IdeaRalph</title>
  <meta name="description" content="Terms of Service for IdeaRalph - AI-powered startup idea validation" />
</svelte:head>

<main class="min-h-screen bg-paper">
  <!-- Header -->
  <header class="bg-ralph-yellow/20 py-8 px-4 border-b border-chalkboard/10">
    <div class="max-w-3xl mx-auto">
      <a href="/" class="inline-flex items-center gap-2 text-chalkboard/60 hover:text-chalkboard mb-4 transition-colors">
        <span>&larr;</span>
        <span>Back to IdeaRalph</span>
      </a>
      <h1 class="font-chalk text-4xl text-chalkboard">Terms of Service</h1>
      <p class="text-chalkboard/60 mt-2">Last updated: {lastUpdated}</p>
    </div>
  </header>

  <!-- Content -->
  <div class="max-w-3xl mx-auto py-12 px-4">
    <div class="space-y-10">

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">1. Acceptance of Terms</h2>
        <p class="text-chalkboard/80 leading-relaxed">
          By accessing and using IdeaRalph ("Service"), you agree to be bound by these Terms of Service.
          IdeaRalph is provided by Vibeship. If you do not agree to these terms, please do not use the Service.
        </p>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">2. Description of Service</h2>
        <p class="text-chalkboard/80 leading-relaxed mb-4">
          IdeaRalph is an AI-powered tool for brainstorming, validating, and refining startup ideas. The Service includes:
        </p>
        <ul class="list-disc pl-6 text-chalkboard/80 space-y-2">
          <li>A web interface for idea validation and scoring</li>
          <li>An MCP (Model Context Protocol) server for integration with Claude Code</li>
          <li>PRD (Product Requirements Document) generation</li>
          <li>Architecture planning tools</li>
        </ul>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">3. Local Processing & Data</h2>
        <p class="text-chalkboard/80 leading-relaxed mb-4">
          IdeaRalph operates differently from typical cloud services:
        </p>
        <ul class="list-disc pl-6 text-chalkboard/80 space-y-2">
          <li><strong>Local Execution:</strong> The MCP server runs locally on your machine within Claude Code</li>
          <li><strong>No Databases:</strong> We do not store your ideas, projects, or generated content</li>
          <li><strong>No Data Transmission:</strong> The MCP does not send your information to our servers</li>
          <li><strong>Your Ideas Stay Yours:</strong> All intellectual property in your ideas remains entirely yours</li>
        </ul>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">4. Intellectual Property</h2>
        <p class="text-chalkboard/80 leading-relaxed mb-4">
          <strong>Your Content:</strong> You retain all rights to your ideas, business concepts, PRDs, and any content you create using the Service.
          We claim no ownership over your intellectual property.
        </p>
        <p class="text-chalkboard/80 leading-relaxed">
          <strong>Our Content:</strong> The IdeaRalph name, branding, code, and interface design are owned by Vibeship.
          The Ralph Wiggum character is a trademark of 20th Century Studios/Disney and is used here for parody/fan purposes only.
        </p>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">5. Acceptable Use</h2>
        <p class="text-chalkboard/80 leading-relaxed mb-4">You agree not to use the Service to:</p>
        <ul class="list-disc pl-6 text-chalkboard/80 space-y-2">
          <li>Generate illegal, harmful, or deceptive content</li>
          <li>Infringe on others' intellectual property rights</li>
          <li>Attempt to reverse-engineer or exploit the Service</li>
          <li>Use automated systems to abuse the Service</li>
        </ul>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">6. Disclaimer of Warranties</h2>
        <p class="text-chalkboard/80 leading-relaxed">
          The Service is provided "as is" without warranties of any kind. IdeaRalph's scoring and feedback are for
          informational purposes only and should not be considered business, legal, or financial advice.
          A high PMF score does not guarantee startup success, and a low score does not mean an idea is without merit.
        </p>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">7. Limitation of Liability</h2>
        <p class="text-chalkboard/80 leading-relaxed">
          Vibeship and its contributors shall not be liable for any indirect, incidental, special, consequential,
          or punitive damages resulting from your use of the Service. This includes any business decisions made
          based on IdeaRalph's output.
        </p>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">8. Open Source</h2>
        <p class="text-chalkboard/80 leading-relaxed">
          IdeaRalph is open source software. The source code is available under the MIT License.
          You are free to fork, modify, and distribute the code in accordance with that license.
        </p>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">9. Changes to Terms</h2>
        <p class="text-chalkboard/80 leading-relaxed">
          We may update these Terms from time to time. Continued use of the Service after changes
          constitutes acceptance of the new Terms. We encourage you to review this page periodically.
        </p>
      </section>

      <section>
        <h2 class="font-chalk text-2xl text-chalkboard mb-4">10. Contact</h2>
        <p class="text-chalkboard/80 leading-relaxed">
          For questions about these Terms, please visit
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
        <span>Terms</span>
        <a href="/privacy" class="hover:text-chalkboard/70 transition-colors">Privacy</a>
      </div>
    </div>
  </footer>
</main>

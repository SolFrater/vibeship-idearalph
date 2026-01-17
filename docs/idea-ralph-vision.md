# IdeaRalph: The Dumbest Genius You'll Ever Meet

> "My cat's breath smells like cat food... and that's why we should build a pet subscription box with AI-powered smell matching."
> - Ralph Wiggum, accidentally discovering PMF

---

## The Origin: From SupaRalph to IdeaRalph

SupaRalph (the Supabase Penetration Scanner) hit 150k+ views and drove the highest single-day user influx to Vibeship. It proved the concept: take the [official Ralph Wiggum methodology](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) - iterative, self-referential AI loops - and apply it to a specific, useful problem.

Now we spawn another Ralph. This time for ideas.

---

## The Spirit

Ralph Wiggum isn't smart. That's his superpower.

He doesn't know what's "impossible." He doesn't have imposter syndrome. He doesn't self-censor before the idea fully forms. He just... says things. And sometimes, through the beautiful chaos of unfiltered thought, he stumbles onto gold.

IdeaRalph is the anti-thesis of every sterile "AI ideation tool" that spits out the same 10 SaaS ideas. He's chaotic. He's weird. He connects dots that shouldn't be connected - and occasionally creates constellations.

**The Philosophy:**
- Genius lives in the spaces between "normal" thoughts
- The best ideas sound stupid at first
- Validation isn't about killing ideas - it's about finding the gold inside the garbage
- Every founder needs permission to think dumb before they think big

---

## The World

### Setting: Ralph's Imagination Playground

Ralph doesn't work in an office. He works in his head - a place where:

- **The Sandbox** is where raw ideas first appear, messy and half-formed
- **The Swing Set** is where ideas get momentum, swinging between "this is stupid" and "wait, maybe..."
- **The Slide** is where ideas go through rapid iteration, picking up speed
- **The Monkey Bars** is where ideas get stress-tested, hanging by their strongest points
- **The Show & Tell Stage** is where validated ideas get presented, polished and ready

The playground exists in a perpetual golden-hour sunset. It's nostalgic. It's safe. It's the place where you weren't afraid to say dumb things because nobody judged you yet.

### The Journey

When you spawn Ralph, you're not just starting an AI process. You're entering his world.

1. **The Bell Rings** - Ralph appears at the playground, ready to play
2. **Sandbox Time** - He starts digging, making random connections, talking to himself
3. **Recess Energy** - Ideas multiply, mutate, combine in weird ways
4. **The Teacher Appears** - PMF validation begins (the teacher is also Ralph, but with glasses)
5. **Show & Tell** - The refined idea gets presented to an imaginary class
6. **Gold Star** - You receive your PRD, blessed by Ralph's accidental genius

---

## The Story

### Origin

You know that feeling at 2 AM when you're half-asleep and you think "wait, what if..." and then you wake up and it's either the best idea you've ever had or complete nonsense?

Ralph lives in that 2 AM space permanently.

He was born from the realization that the best founders aren't the smartest people in the room - they're the ones dumb enough to try things smart people "know" won't work.

Airbnb? "Let strangers sleep in your house." Dumb.
Uber? "Get in a stranger's car." Dumb.
Twitter? "Say things in 140 characters." Dumb.

All of them sounded stupid. All of them worked.

### The Mission

IdeaRalph exists to give vibe coders the one thing they can't build themselves: **permission to be stupid**.

He generates hundreds of ideas without judgment. He validates without crushing. He refines without sanitizing the weird edges that make ideas memorable.

By the time you get your PRD, it's not just a product spec. It's a story you believe in, with the Ralph-shaped fingerprints of genuine creativity still visible.

---

## The Art Style

### Visual Language

**Primary Aesthetic: "Crayon Genius"**

The art evolves with the idea's maturity:

| Stage | Visual Style |
|-------|--------------|
| Raw Ideas | Crayon scribbles, wobbly lines, paper texture |
| Developing | Colored pencil, more defined but still hand-drawn |
| Validating | Marker style, bold outlines, confidence emerging |
| Refined | Clean vector with hand-drawn personality preserved |
| Final PRD | Professional design with subtle crayon accents |

### Color Palette

```
Primary:    #FFD93D (Ralph Yellow - optimism, naivety)
Secondary:  #6BCB77 (Playground Green - growth, possibility)
Accent:     #FF6B6B (Crayon Red - excitement, energy)
Neutral:    #4D96FF (Sky Blue - imagination, dreams)
Dark:       #2D3436 (Chalkboard - grounding, structure)
```

### Typography

- **Headlines:** Chalkboard-style, slightly uneven, hand-written feel
- **Body:** Clean sans-serif (readability matters)
- **Ralph's Voice:** Comic Sans adjacent (yes, intentionally) - rounded, childlike
- **Data/PRD:** Professional monospace for contrast

### Character Design

Ralph in IdeaRalph isn't a Simpsons copy. He's an homage:

- Oversized head (big brain energy, empty brain reality)
- Perpetually confused but happy expression
- School clothes that are slightly too big
- Always holding something random (glue stick, a rock, a half-eaten crayon)
- Thought bubbles that are literally bubbles, floating and popping

### UI Elements

- Buttons look like playground equipment
- Progress bars are monkey bars Ralph swings across
- Loading states show Ralph thinking (smoke coming from ears)
- Success states are gold star stickers
- Error states are Ralph saying "I bent my Wookie" (never actually errors - just "happy accidents")

---

## The Technology

### The Ralph Wiggum Methodology

IdeaRalph is built on the official Ralph Wiggum technique from Anthropic's Claude Code plugin ecosystem. As the methodology states:

> "Ralph is a Bash loop - a simple while true that repeatedly feeds an AI agent a prompt, allowing it to iteratively improve its work until completion."

The philosophy:
- Don't aim for perfect on first try. Let the loop refine the work.
- "Deterministically bad" means failures are predictable and informative.
- Success depends on writing good prompts, not just having a good model.
- Keep trying until success. The loop handles retry logic automatically.

This is exactly what idea generation needs. Most "AI idea tools" run once and give you whatever comes out. IdeaRalph loops until the idea is actually good.

### Tech Stack

```
Frontend:     Svelte 5 + SvelteKit
Build:        Vite
Styling:      TailwindCSS + custom crayon design system
Animations:   Svelte transitions + Motion One
State:        Svelte stores + runes
Backend:      SvelteKit API routes / Edge functions
Database:     Supabase (Postgres + Auth + Realtime)
AI:           Anthropic Claude API (via Spawner integration)
Hosting:      Vercel / Cloudflare Pages
```

**Why Svelte + Vite:**
- Faster builds, smaller bundles (vibe coders ship fast)
- Less boilerplate than React (more building, less configuring)
- Native transitions perfect for Ralph's playful animations
- Runes make reactive state dead simple
- SvelteKit handles routing, SSR, API routes in one framework

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     IDEARALPH SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   SPAWNER   │───▶│  IDEATION   │───▶│ VALIDATION  │     │
│  │   (Entry)   │    │   ENGINE    │    │   ENGINE    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                  │                  │             │
│         │                  ▼                  ▼             │
│         │          ┌─────────────┐    ┌─────────────┐      │
│         │          │    MIND     │    │  PMF LENS   │      │
│         │          │  (Memory)   │    │ (Visualize) │      │
│         │          └─────────────┘    └─────────────┘      │
│         │                  │                  │             │
│         │                  ▼                  ▼             │
│         │          ┌─────────────────────────────┐         │
│         └─────────▶│   RALPH LOOP (while true)   │         │
│                    │   Iterate until DOPE        │         │
│                    └─────────────────────────────┘         │
│                                   │                         │
│                                   ▼                         │
│                         ┌─────────────────┐                │
│                         │   PRD FACTORY   │                │
│                         │  (Final Output) │                │
│                         └─────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Project Structure (SvelteKit)

```
idearalph/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── playground/
│   │   │   │   ├── Sandbox.svelte
│   │   │   │   ├── SwingSet.svelte
│   │   │   │   ├── MonkeyBars.svelte
│   │   │   │   └── ShowAndTell.svelte
│   │   │   ├── ralph/
│   │   │   │   ├── RalphCharacter.svelte
│   │   │   │   ├── ThoughtBubble.svelte
│   │   │   │   └── RalphQuotes.svelte
│   │   │   ├── pmf/
│   │   │   │   ├── ReportCard.svelte
│   │   │   │   ├── PlaygroundMap.svelte
│   │   │   │   └── CompetitionDodgeball.svelte
│   │   │   └── ui/
│   │   │       ├── CrayonButton.svelte
│   │   │       ├── GoldStar.svelte
│   │   │       └── ProgressBars.svelte
│   │   ├── stores/
│   │   │   ├── idea.svelte.ts        # Idea state (runes)
│   │   │   ├── ralph.svelte.ts       # Ralph loop state
│   │   │   └── session.svelte.ts     # User session
│   │   ├── ralph/
│   │   │   ├── loop.ts               # Core Ralph loop logic
│   │   │   ├── prompts.ts            # Prompt templates
│   │   │   └── validators.ts         # PMF validation functions
│   │   └── styles/
│   │       ├── crayon.css            # Custom design system
│   │       └── animations.css        # Playground animations
│   ├── routes/
│   │   ├── +page.svelte              # Landing
│   │   ├── +layout.svelte            # App shell
│   │   ├── spawn/
│   │   │   └── +page.svelte          # Spawn Ralph flow
│   │   ├── playground/
│   │   │   └── +page.svelte          # Main ideation space
│   │   ├── idea/[id]/
│   │   │   └── +page.svelte          # Individual idea view
│   │   └── api/
│   │       ├── ralph/
│   │       │   ├── +server.ts        # Ralph loop endpoint
│   │       │   └── stream/+server.ts # SSE for live updates
│   │       └── prd/
│   │           └── +server.ts        # PRD generation
│   └── app.html
├── static/
│   └── ralph/                        # Character assets
├── svelte.config.js
├── vite.config.ts
├── tailwind.config.js
└── package.json
```

### Core Components

#### 1. The Spawner Integration
- Hooks into existing Vibeship Spawner infrastructure
- Ralph is a specialized agent persona with unique prompt engineering
- Inherits multi-skill orchestration capabilities

#### 2. The Ralph Loop (Core Engine)

This is where the magic happens. Based on the official Ralph Wiggum methodology:

```typescript
// src/lib/ralph/loop.ts

interface RalphLoopConfig {
  maxIterations: number;
  completionPromise: string;
  dopenessThreshold: number;
}

interface IdeaState {
  raw: string;
  refined: string;
  dopeLevel: number;
  pmfScores: PMFScores;
  iteration: number;
}

async function* ralphLoop(
  initialPrompt: string,
  config: RalphLoopConfig
): AsyncGenerator<IdeaState> {

  let iteration = 0;
  let idea: IdeaState = await generateInitialIdea(initialPrompt);

  // The Ralph Loop - keep going until it's dope
  while (
    idea.dopeLevel < config.dopenessThreshold &&
    iteration < config.maxIterations
  ) {
    iteration++;

    // Feed the same core prompt back, but with current state
    const refinementPrompt = buildRefinementPrompt(initialPrompt, idea);

    // Ralph sees what he made and tries again
    idea = await refineIdea(refinementPrompt, idea);

    // Validate PMF on each iteration
    idea.pmfScores = await validatePMF(idea);
    idea.dopeLevel = calculateDopeness(idea.pmfScores);

    // Yield current state for UI updates
    yield idea;

    // Check for completion promise
    if (idea.refined.includes(config.completionPromise)) {
      break;
    }
  }

  return idea;
}
```

#### 3. Ideation Engine

**The "Random Genius" Algorithm:**

```typescript
// src/lib/ralph/prompts.ts

const IDEATION_PROMPT = `
You are Ralph Wiggum, idea generator extraordinaire.

Your brain works differently. You make connections others miss.
You say things that sound dumb but are secretly genius.

Generate 10 product/app ideas based on the user's context.
For each idea:
- One sentence that sounds silly
- The hidden genius underneath
- Why a vibe coder could build it

Rate each idea's "dumbness score" (1-10).
Higher = sounds dumber = potentially more genius.

User context: {context}
Domain hints: {domain}
Chaos level: {chaosLevel}/10

Remember: The best ideas taste like purple.
`;

const REFINEMENT_PROMPT = `
You are Ralph Wiggum, looking at an idea you made.

Current idea: {currentIdea}
Current dope level: {dopeLevel}/5
Iteration: {iteration}

What's wrong with it:
- Market too small? "What if we also sold it to... cats?"
- Too competitive? "What if we did it... backwards?"
- Too complex? "My brain hurts. Make it simpler."
- Not viral? "This needs more glitter!"

Make it doper. Don't start over. Improve what's there.

Output your improved idea and what you changed.
If it's now SUPER DUPER DOPE, say: "DOPE_ACHIEVED"
`;
```

**Idea Generation Modes:**
- **Paste Eater Mode:** Chaos level 10, temperature 1.0, no filters
- **Gold Star Mode:** Chaos level 5, balanced creativity with market awareness
- **Teacher's Pet Mode:** Chaos level 2, conservative, validated-first approach

#### 4. PMF Validation Engine

**The "Show & Tell" Validator:**

```typescript
// src/lib/ralph/validators.ts

interface PMFScores {
  marketSize: number;      // TAM/SAM/SOM estimation
  problemSeverity: number; // Pain point scoring (1-10)
  solutionFit: number;     // Technical feasibility
  competition: number;     // Competitive landscape
  vibeCodeable: number;    // Can a vibe coder build it?
  virality: number;        // Shareability factor
}

async function validatePMF(idea: IdeaState): Promise<PMFScores> {
  // Parallel validation for speed
  const [market, problem, solution, competition, buildability, virality] =
    await Promise.all([
      analyzeMarket(idea),      // Web search for TAM data
      scoreProblem(idea),       // Pain point analysis
      assessFit(idea),          // Solution-problem fit
      mapCompetition(idea),     // Competitor landscape
      assessBuildability(idea), // Vibe coder feasibility
      scoreVirality(idea)       // Meme-ability index
    ]);

  return {
    marketSize: market,
    problemSeverity: problem,
    solutionFit: solution,
    competition: competition,
    vibeCodeable: buildability,
    virality: virality
  };
}

function calculateDopeness(scores: PMFScores): number {
  // Weighted average, with virality and vibeCodeable getting bonus weight
  const weights = {
    marketSize: 1.0,
    problemSeverity: 1.2,
    solutionFit: 1.0,
    competition: 0.8,
    vibeCodeable: 1.5,  // Critical for our audience
    virality: 1.3       // We want shareable ideas
  };

  let total = 0;
  let weightSum = 0;

  for (const [key, weight] of Object.entries(weights)) {
    total += scores[key] * weight;
    weightSum += weight;
  }

  return Math.round((total / weightSum) * 5) / 5; // 0-5 scale
}
```

#### 5. PMF Visualizations (Svelte Components)

**The Report Card:**

```svelte
<!-- src/lib/components/pmf/ReportCard.svelte -->
<script lang="ts">
  import { fly, scale } from 'svelte/transition';
  import GoldStar from '../ui/GoldStar.svelte';

  let { scores, ideaName, ralphQuote } = $props();

  const grades = ['F', 'D', 'C', 'B', 'A', 'A+'];
  const getGrade = (score: number) => grades[Math.min(Math.floor(score * 1.2), 5)];

  const metrics = [
    { key: 'marketSize', label: 'Market Size', quip: '' },
    { key: 'problemSeverity', label: 'Problem Severity', quip: 'Ouchie!' },
    { key: 'solutionFit', label: 'Solution Fit', quip: 'It works!' },
    { key: 'competition', label: 'Competition', quip: 'Others try' },
    { key: 'vibeCodeable', label: 'Vibe-Codeable', quip: 'You can!' },
    { key: 'virality', label: 'Virality', quip: 'Shareable!' }
  ];
</script>

<div class="report-card" in:fly={{ y: 50, duration: 500 }}>
  <header class="report-header">
    <h2>Ralph's Report Card</h2>
    <p class="idea-name">{ideaName}</p>
  </header>

  <div class="grades">
    {#each metrics as metric, i}
      <div
        class="grade-row"
        in:fly={{ x: -20, delay: i * 100 }}
      >
        <span class="label">{metric.label}</span>
        <div class="bar-container">
          <div
            class="bar"
            style="width: {scores[metric.key] * 10}%"
          />
        </div>
        <span class="grade">{getGrade(scores[metric.key])}</span>
        {#if metric.quip && scores[metric.key] > 7}
          <span class="quip">"{metric.quip}"</span>
        {/if}
      </div>
    {/each}
  </div>

  <footer class="report-footer">
    <div class="overall" in:scale={{ delay: 600 }}>
      {#each Array(Math.floor(scores.overall)) as _, i}
        <GoldStar delay={700 + i * 100} />
      {/each}
      <span class="dope-label">
        {scores.overall >= 4.5 ? 'Super Duper Dope!' :
         scores.overall >= 3.5 ? 'Pretty Dope!' :
         scores.overall >= 2.5 ? 'Getting There!' : 'Needs Work'}
      </span>
    </div>
    <p class="ralph-says">Ralph says: "{ralphQuote}"</p>
  </footer>
</div>
```

**The Playground Map:**
Visual representation showing the idea's journey:
- Where it started (sandbox)
- Key pivots (swing set moments)
- Validation checkpoints (monkey bar challenges)
- Final position (show & tell readiness)

**The Competition Dodgeball:**
Visual showing competitive landscape as a dodgeball game:
- Your idea is Ralph
- Competitors are other kids
- Open spaces show market gaps
- Direct hits show overlap risks

#### 6. Dope Levels

```typescript
const DOPE_LEVELS = {
  1: { label: "My cat could do better", emoji: "😿", action: "Major rework needed" },
  2: { label: "Interesting...", emoji: "🤔", action: "Potential visible, keep iterating" },
  3: { label: "Hey, that's pretty good", emoji: "👍", action: "Solid foundation" },
  4: { label: "Dope", emoji: "🔥", action: "Ready for building" },
  5: { label: "Super Duper Dope", emoji: "⭐", action: "Ralph's seal of approval" }
};
```

#### 7. PRD Factory

**Output Structure:**
```markdown
# [IDEA NAME]
## "Ralph's one-liner description"

### The Problem (Why This Matters)
[Human-readable problem statement]
[Pain point evidence]
[Market context]

### The Solution (What We're Building)
[Core concept]
[Key features - prioritized]
[What makes it different]

### The Market (Who Wants This)
[Target users - specific personas]
[Market size visualization]
[Competition analysis]

### The Build Plan (How to Vibe Code It)
[MVP scope - what to build first]
[Tech stack recommendations]
[Estimated timeline for vibe coder]

### The Launch (How to Get Users)
[Go-to-market strategy]
[Viral hooks]
[Community building approach]

### Ralph's Notes
[Random observations that might be genius]
[Things that "taste like purple"]
[Unconventional angles to explore]

### Ready to Build?
[Next steps checklist]
[Resources needed]
[First line of code suggestion]
```

---

## The UI/UX

### Screen Flow

```
[Landing] → [Spawn Ralph] → [Playground Loading] → [Sandbox Mode]
                                                        │
                ┌───────────────────────────────────────┘
                │
                ▼
        [Idea Generation] → [Pick Favorites] → [Validation]
                │                                    │
                │ (or "Surprise Me")                 │
                ▼                                    ▼
        [Random Selection] ─────────────────▶ [PMF Dashboard]
                                                    │
                                                    ▼
                                            [Ralph Loop View]
                                            (watch iterations)
                                                    │
                                            (iterate until dope)
                                                    │
                                                    ▼
                                            [Show & Tell]
                                                    │
                                                    ▼
                                            [PRD Delivery]
                                                    │
                                                    ▼
                                            [Export / Share]
```

### Key Screens (Svelte Components)

#### 1. Landing Page (`src/routes/+page.svelte`)

```svelte
<script>
  import { goto } from '$app/navigation';
  import { fly, scale } from 'svelte/transition';
  import RalphCharacter from '$lib/components/ralph/RalphCharacter.svelte';
  import CrayonButton from '$lib/components/ui/CrayonButton.svelte';
  import RecentIdeas from '$lib/components/RecentIdeas.svelte';

  let bellRinging = $state(false);

  async function spawnRalph() {
    bellRinging = true;
    await new Promise(r => setTimeout(r, 800));
    goto('/spawn');
  }
</script>

<main class="landing">
  <div class="playground-gate" in:fly={{ y: -50 }}>
    <RalphCharacter pose="waiting" />

    <CrayonButton
      onclick={spawnRalph}
      class:ringing={bellRinging}
    >
      🔔 Ring the Bell
    </CrayonButton>

    <p class="tagline">
      "I'm a idea generator! And I'm helping!"
    </p>
  </div>

  <aside class="graffiti-wall">
    <RecentIdeas />
  </aside>
</main>
```

Features:
- Ralph standing at playground entrance
- "Ring the Bell" CTA (spawn button)
- Testimonials styled as playground graffiti
- Recent "Gold Star Ideas" ticker

#### 2. Spawn Animation (`src/routes/spawn/+page.svelte`)

```svelte
<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { fly, fade } from 'svelte/transition';
  import { elasticOut } from 'svelte/easing';

  let stage = $state(0);
  // 0: bell, 1: running, 2: landing, 3: ready

  onMount(() => {
    const sequence = [500, 1000, 800, 500];
    let total = 0;
    sequence.forEach((delay, i) => {
      total += delay;
      setTimeout(() => stage = i + 1, total);
    });
    setTimeout(() => goto('/playground'), total + 500);
  });
</script>

<div class="spawn-sequence">
  {#if stage >= 0}
    <div class="bell" in:scale={{ duration: 300 }}>🔔</div>
  {/if}

  {#if stage >= 1}
    <div
      class="ralph-running"
      in:fly={{ x: -200, duration: 800, easing: elasticOut }}
    >
      <!-- Ralph sprite animation -->
    </div>
  {/if}

  {#if stage >= 2}
    <div class="sandbox-poof" in:scale={{ duration: 400 }}>
      💨
    </div>
  {/if}

  {#if stage >= 3}
    <p class="ready-text" in:fade>
      "Hi! I'm helping!"
    </p>
  {/if}
</div>
```

Animation sequence:
- School bell rings
- Ralph runs in from off-screen
- Backpack bouncing
- Lands in sandbox with a poof
- "Hi! I'm helping!"

#### 3. Sandbox Mode (`src/routes/playground/+page.svelte`)

```svelte
<script>
  import { ralphStore } from '$lib/stores/ralph.svelte';
  import ThoughtBubble from '$lib/components/ralph/ThoughtBubble.svelte';
  import RalphCharacter from '$lib/components/ralph/RalphCharacter.svelte';
  import CrayonButton from '$lib/components/ui/CrayonButton.svelte';

  let { ideas, isGenerating, iteration } = $derived(ralphStore);

  function dismissIdea(id: string) {
    ralphStore.dismiss(id);
  }

  function combineIdeas(id1: string, id2: string) {
    ralphStore.combine(id1, id2);
  }

  function moreRandom() {
    ralphStore.shake();
  }
</script>

<div class="sandbox-mode">
  <section class="ralph-area">
    <RalphCharacter pose={isGenerating ? 'digging' : 'thinking'} />
    <span class="iteration-badge">Loop #{iteration}</span>
  </section>

  <section class="idea-bubbles">
    {#each ideas as idea (idea.id)}
      <ThoughtBubble
        {idea}
        ondismiss={() => dismissIdea(idea.id)}
        draggable
      />
    {/each}
  </section>

  <footer class="sandbox-controls">
    <CrayonButton onclick={moreRandom}>
      🎲 More Random!
    </CrayonButton>
    <CrayonButton onclick={() => ralphStore.validate()}>
      📋 Validate These
    </CrayonButton>
  </footer>
</div>
```

Features:
- Split screen: Ralph playing / Ideas appearing
- Ideas float up like thought bubbles
- User can pop bubbles to dismiss
- Drag bubbles together to combine
- "More Random!" button shakes the sandbox
- Loop iteration counter visible

#### 4. Ralph Loop View (`src/lib/components/RalphLoopView.svelte`)

```svelte
<script>
  import { ralphStore } from '$lib/stores/ralph.svelte';
  import SwingSet from './playground/SwingSet.svelte';
  import ProgressBars from './ui/ProgressBars.svelte';

  let { iteration, maxIterations, dopeLevel, currentIdea } = $derived(ralphStore);

  // Ralph swings faster as idea improves
  let swingSpeed = $derived(0.5 + (dopeLevel / 5) * 1.5);
</script>

<div class="ralph-loop-view">
  <SwingSet
    speed={swingSpeed}
    iteration={iteration}
  />

  <div class="loop-status">
    <ProgressBars
      current={iteration}
      max={maxIterations}
      label="Iterations"
    />
    <ProgressBars
      current={dopeLevel}
      max={5}
      label="Dopeness"
      style="gold-stars"
    />
  </div>

  <div class="current-refinement">
    <p class="ralph-thought">
      "{currentIdea.lastRefinement}"
    </p>
  </div>

  <div class="loop-controls">
    <CrayonButton onclick={() => ralphStore.stop()}>
      Good Enough!
    </CrayonButton>
    <CrayonButton onclick={() => ralphStore.boost()}>
      Keep Swinging!
    </CrayonButton>
  </div>
</div>
```

Features:
- Ralph on swing set
- Each swing = one iteration
- Visual showing idea evolving
- "Keep Swinging" or "Good Enough" options
- Swing speed increases as idea improves

#### 5. PRD Delivery (`src/routes/idea/[id]/+page.svelte`)

```svelte
<script>
  import { page } from '$app/stores';
  import { fly, scale } from 'svelte/transition';
  import GoldStar from '$lib/components/ui/GoldStar.svelte';
  import RalphCharacter from '$lib/components/ralph/RalphCharacter.svelte';

  let { data } = $props();
  let showConfetti = $state(false);

  onMount(() => {
    setTimeout(() => showConfetti = true, 1000);
  });
</script>

<div class="show-and-tell">
  <div class="stage">
    <RalphCharacter pose="presenting" />
    <div class="audience">
      <!-- Empty chairs with imaginary friends -->
    </div>
  </div>

  <div class="prd-book-report" in:fly={{ y: 50, delay: 500 }}>
    <header>
      <h1>{data.idea.name}</h1>
      <GoldStar size="large" animate />
    </header>

    <article class="prd-content">
      {@html data.prd}
    </article>
  </div>

  {#if showConfetti}
    <div class="confetti" in:scale>🎉</div>
  {/if}

  <footer class="delivery-actions">
    <CrayonButton onclick={() => downloadPRD(data.prd)}>
      📥 Download
    </CrayonButton>
    <CrayonButton onclick={() => copyToClipboard(data.prd)}>
      📋 Copy
    </CrayonButton>
    <CrayonButton onclick={() => share(data.idea)}>
      🔗 Share
    </CrayonButton>
  </footer>
</div>
```

Features:
- Show & Tell stage
- Ralph presents to empty chairs (imagination friends)
- PRD appears as a "book report"
- Gold star sticker slaps onto final version
- Confetti animation
- Download/Copy/Share options

### Micro-Interactions (Svelte Transitions)

```svelte
<!-- src/lib/components/ui/transitions.ts -->
<script context="module">
  import { cubicOut, elasticOut, bounceOut } from 'svelte/easing';

  export function crayonScribble(node, { duration = 300 }) {
    return {
      duration,
      css: (t) => `
        stroke-dasharray: ${t * 100};
        opacity: ${t};
      `
    };
  }

  export function goldStarPop(node, { delay = 0 }) {
    return {
      delay,
      duration: 400,
      easing: elasticOut,
      css: (t) => `
        transform: scale(${t}) rotate(${(1 - t) * 180}deg);
        opacity: ${t};
      `
    };
  }

  export function bubblePop(node, { duration = 200 }) {
    return {
      duration,
      easing: cubicOut,
      css: (t) => `
        transform: scale(${1 + (1 - t) * 0.3});
        opacity: ${t};
      `
    };
  }
</script>
```

| Action | Svelte Transition |
|--------|-------------------|
| Button hover | `use:crayonScribble` |
| Successful action | `in:goldStarPop` |
| Error state | Ralph says "I made a mistake" (never real error) |
| Loading | Ralph chases butterfly (`animate:flip`) |
| Progress | Monkey bars filling (`tweened` store) |
| Idea dismissed | `out:bubblePop` + Ralph giggles |
| Idea saved | Heart appears (`in:scale`), Ralph blushes |

---

## The Strategy

### Phase 1: MVP Launch (Week 1-2)
**Goal:** Prove the concept works, capture lightning

**Build:**
- Landing page with spawn mechanic
- Basic idea generation (10 ideas per spawn)
- Simple PMF scoring (not full visualization yet)
- PRD template output
- Share functionality

**Metrics:**
- Spawns per day
- Ideas marked as "dope"
- PRDs downloaded
- Social shares

### Phase 2: Viral Mechanics (Week 3-4)
**Goal:** Make it spread

**Add:**
- "Share your Ralph idea" cards (OG images)
- Leaderboard: "Dopest Ideas This Week"
- Community voting on ideas
- "Idea of the Day" feature
- Integration with SupaRalph (cross-promotion)

**Viral Loops:**
```
User spawns Ralph → Gets dope idea → Shares card
                                          │
        ┌─────────────────────────────────┘
        │
        ▼
New user sees card → Curious about their idea → Spawns Ralph
                                                      │
                    ┌─────────────────────────────────┘
                    │
                    ▼
             Repeat cycle
```

### Phase 3: Full Experience (Week 5-8)
**Goal:** Complete the playground

**Add:**
- Full PMF visualization suite
- Refinement loop with iterations
- User accounts / idea history
- "My Playground" dashboard
- Collaboration: share ideas with team
- Advanced modes (different Ralph personalities)

### Phase 4: Monetization (Week 9+)
**Goal:** Sustainable growth

**Free Tier:**
- 3 Ralph spawns per day
- Basic PMF scoring
- Standard PRD output

**Pro Tier ($19/mo):**
- Unlimited spawns
- Full PMF visualizations
- Priority refinement
- Custom PRD templates
- Idea history & organization
- Export to Notion/Docs

**Team Tier ($49/mo):**
- Everything in Pro
- Team collaboration
- Idea voting/commenting
- Shared playground
- Analytics dashboard

### Content Strategy

**Stream Integration:**
- Spawn Ralph live on stream
- Audience votes on which ideas to pursue
- Build the winning idea live
- Content: "From Ralph to Reality" series

**Social Clips:**
- "Ralph said WHAT?!" - wildest ideas
- "Wait, that's actually genius" - ideas that seem dumb but work
- "PRD in 60 seconds" - fast idea-to-plan demos
- "Ralph vs. ChatGPT" - personality comparison

**SEO Play:**
- "AI idea generator"
- "Startup idea validation"
- "Product idea for developers"
- "Vibe coding project ideas"

---

## The Gameplan

### Week 1: Foundation
- [ ] `npm create svelte@latest idearalph` with TypeScript
- [ ] Set up Tailwind + custom crayon design system CSS
- [ ] Design tokens: colors, typography, Ralph character assets
- [ ] Landing page with spawn animation (Svelte transitions)
- [ ] Basic agent prompt engineering for "Ralph voice"
- [ ] Supabase project setup (auth, database schema)

### Week 2: Core Loop
- [ ] Ralph loop engine (`src/lib/ralph/loop.ts`)
- [ ] Idea generation flow with streaming UI
- [ ] PMF scoring algorithm and validators
- [ ] Report Card component with animated grades
- [ ] PRD template and markdown generation
- [ ] Share card generation (OG images via SvelteKit endpoint)
- [ ] Basic analytics (Plausible or PostHog)

### Week 3: Stream Launch
- [ ] Polish Svelte transitions and micro-interactions
- [ ] Bug fixes from internal testing
- [ ] Stream: "Meet IdeaRalph" launch
- [ ] Social campaign: teaser clips
- [ ] Community feedback collection

### Week 4: Iterate
- [ ] Implement top feedback items
- [ ] Add viral mechanics (leaderboard, voting)
- [ ] Cross-promote with SupaRalph
- [ ] Content: "Best of Ralph" compilation
- [ ] A/B test landing page

### Month 2: Expand
- [ ] User accounts and idea history (Supabase auth)
- [ ] Full refinement loop with live iteration view
- [ ] Collaboration features (share playground)
- [ ] Pro tier launch (Stripe integration)
- [ ] Partnership outreach (vibe coding tools)

### Month 3: Scale
- [ ] Team tier launch
- [ ] API for integrations (SvelteKit API routes)
- [ ] Mobile responsive refinements
- [ ] Expanded Ralph personalities (chaos modes)
- [ ] Community features (idea marketplace?)

---

## The Promise

IdeaRalph isn't just another AI tool.

It's permission to be stupid.
It's a playground for your brain.
It's the friend who says "that's not dumb, that's interesting."

For every vibe coder staring at a blank IDE wondering "what should I build?", Ralph is there. Eating paste. Making weird connections. Accidentally discovering the next big thing.

Because the best ideas don't come from trying to be smart.
They come from being dumb enough to try.

---

*"I'm a idea! And I'm helping!"*
- Ralph Wiggum, Idea Generation Specialist

---

## Appendix: Ralph's Voice Guide

### How Ralph Talks

**Do:**
- Simple words, complex connections
- Non-sequiturs that accidentally make sense
- Enthusiastic about everything
- Speaks in present tense
- Uses "I" and "My" frequently
- Mixes childlike observations with business terms

**Don't:**
- Jargon-heavy language
- Cynical or negative framing
- Complex sentence structures
- Irony or sarcasm (Ralph is sincere)
- Adult humor or references

### Example Ralph Lines

**During Ideation:**
- "What if dogs had their own social media? My dog would post about butts a lot."
- "I found an idea in my nose! It's about subscription boxes!"
- "This idea tastes like purple and also like money!"

**During Validation:**
- "The market is this big! *holds arms wide* That's bigger than my bedroom!"
- "Other people tried this but they forgot to add the fun part."
- "My teacher says competition is good. Your competition looks tired."

**During Refinement:**
- "It's getting doper! I can feel it in my tummy!"
- "We should add more colors. Colors make everything better."
- "This part is confusing. Even my imaginary friend is confused."

**During PRD Delivery:**
- "I made you a book report! There's no pictures but I drew some in my head."
- "You should build this. I believe in you like I believe in Santa."
- "Go make the thing! I'll be here eating paste if you need me."

---

*Document Version: 1.0*
*Created for: Vibeship / IdeaRalph*
*Status: Ready to Vibe Code*

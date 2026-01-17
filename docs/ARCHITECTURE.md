# IdeaRalph Architecture Document

> Built with H70+ skill methodology for production-grade implementation

---

## System Overview

IdeaRalph is an AI-powered idea generation tool that uses iterative refinement loops (the "Ralph Loop") to generate, validate, and refine startup ideas until they reach a "dope" threshold.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         IDEARALPH SYSTEM                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                │
│  │   SvelteKit  │   │   Supabase   │   │  Claude API  │                │
│  │   Frontend   │◄─►│   Backend    │◄─►│   (Spawner)  │                │
│  └──────────────┘   └──────────────┘   └──────────────┘                │
│         │                  │                  │                         │
│         │    ┌─────────────┴─────────────┐   │                         │
│         │    │                           │   │                         │
│         ▼    ▼                           ▼   ▼                         │
│  ┌─────────────────────────────────────────────────────┐               │
│  │              RALPH LOOP ENGINE                       │               │
│  │  ┌─────────┐  ┌───────────┐  ┌─────────────┐       │               │
│  │  │ Ideate  │─►│  Validate │─►│   Refine    │──┐    │               │
│  │  └─────────┘  └───────────┘  └─────────────┘  │    │               │
│  │       ▲                                        │    │               │
│  │       └────────────────────────────────────────┘    │               │
│  │              (loop until dope_level >= 4)           │               │
│  └─────────────────────────────────────────────────────┘               │
│                              │                                          │
│                              ▼                                          │
│                    ┌─────────────────┐                                 │
│                    │   PRD Factory   │                                 │
│                    └─────────────────┘                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Frontend | Svelte 5 + SvelteKit | Runes system, native transitions, SSR |
| Build | Vite | Fast HMR, optimized builds |
| Styling | TailwindCSS | Utility-first, crayon design system |
| State | Svelte stores + runes | $state, $derived, $effect |
| Backend | SvelteKit API routes | Colocated, type-safe |
| Database | Supabase (Postgres) | RLS, Realtime, Auth |
| Auth | Supabase Auth | Email/OAuth, session management |
| AI | Anthropic Claude API | Via Spawner integration |
| Hosting | Vercel/Cloudflare | Edge-ready, global CDN |

---

## Database Schema (Supabase)

### Core Tables

```sql
-- Users (extends Supabase auth.users)
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name TEXT,
  avatar_url TEXT,
  tier TEXT DEFAULT 'free' CHECK (tier IN ('free', 'pro', 'team')),
  spawns_today INTEGER DEFAULT 0,
  spawns_reset_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Ideas (core entity)
CREATE TABLE public.ideas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,

  -- Content
  name TEXT NOT NULL,
  raw_idea TEXT NOT NULL,
  refined_idea TEXT,
  ralph_quote TEXT,

  -- State
  status TEXT DEFAULT 'sandbox' CHECK (status IN ('sandbox', 'validating', 'refining', 'completed', 'archived')),
  dope_level SMALLINT DEFAULT 1 CHECK (dope_level BETWEEN 1 AND 5),
  iteration INTEGER DEFAULT 0,
  max_iterations INTEGER DEFAULT 10,

  -- PMF Scores (0-10 scale)
  pmf_market_size NUMERIC(3,1),
  pmf_problem_severity NUMERIC(3,1),
  pmf_solution_fit NUMERIC(3,1),
  pmf_competition NUMERIC(3,1),
  pmf_vibe_codeable NUMERIC(3,1),
  pmf_virality NUMERIC(3,1),

  -- Metadata
  chaos_level SMALLINT DEFAULT 5 CHECK (chaos_level BETWEEN 1 AND 10),
  context JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Idea Iterations (history of refinements)
CREATE TABLE public.idea_iterations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  idea_id UUID NOT NULL REFERENCES public.ideas(id) ON DELETE CASCADE,
  iteration_number INTEGER NOT NULL,

  -- Snapshot
  idea_content TEXT NOT NULL,
  dope_level SMALLINT NOT NULL,
  pmf_scores JSONB,
  ralph_feedback TEXT,

  -- What changed
  changes_made TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- PRDs (Product Requirement Documents)
CREATE TABLE public.prds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  idea_id UUID NOT NULL REFERENCES public.ideas(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,

  -- Content
  content TEXT NOT NULL,
  markdown TEXT NOT NULL,

  -- Metadata
  version INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Sessions (track Ralph spawns)
CREATE TABLE public.sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,

  -- Session data
  initial_prompt TEXT,
  chaos_level SMALLINT DEFAULT 5,
  ideas_generated INTEGER DEFAULT 0,

  -- Timing
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

-- Votes (community features, phase 2)
CREATE TABLE public.votes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  idea_id UUID NOT NULL REFERENCES public.ideas(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  vote_type TEXT CHECK (vote_type IN ('dope', 'meh')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(idea_id, user_id)
);
```

### Row Level Security (RLS)

```sql
-- Enable RLS on all tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ideas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.idea_iterations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.prds ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.votes ENABLE ROW LEVEL SECURITY;

-- Profiles: users can only access their own
CREATE POLICY "Users can view own profile"
  ON public.profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id);

-- Ideas: users own their ideas, public ideas can be viewed
CREATE POLICY "Users can CRUD own ideas"
  ON public.ideas FOR ALL
  USING (auth.uid() = user_id);

CREATE POLICY "Public can view completed ideas"
  ON public.ideas FOR SELECT
  USING (status = 'completed');

-- Iterations: tied to idea ownership
CREATE POLICY "Users can view own idea iterations"
  ON public.idea_iterations FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.ideas
      WHERE ideas.id = idea_iterations.idea_id
      AND ideas.user_id = auth.uid()
    )
  );

-- PRDs: users own their PRDs
CREATE POLICY "Users can CRUD own PRDs"
  ON public.prds FOR ALL
  USING (auth.uid() = user_id);

-- Sessions: users own their sessions
CREATE POLICY "Users can CRUD own sessions"
  ON public.sessions FOR ALL
  USING (auth.uid() = user_id);

-- Votes: users can vote, view all votes
CREATE POLICY "Users can vote"
  ON public.votes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view all votes"
  ON public.votes FOR SELECT
  USING (true);
```

### Indexes

```sql
-- Performance indexes
CREATE INDEX idx_ideas_user_id ON public.ideas(user_id);
CREATE INDEX idx_ideas_status ON public.ideas(status);
CREATE INDEX idx_ideas_dope_level ON public.ideas(dope_level);
CREATE INDEX idx_ideas_created_at ON public.ideas(created_at DESC);

CREATE INDEX idx_iterations_idea_id ON public.idea_iterations(idea_id);
CREATE INDEX idx_prds_idea_id ON public.prds(idea_id);
CREATE INDEX idx_sessions_user_id ON public.sessions(user_id);
CREATE INDEX idx_votes_idea_id ON public.votes(idea_id);
```

---

## Project Structure

```
idearalph/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── playground/
│   │   │   │   ├── Sandbox.svelte          # Main idea generation area
│   │   │   │   ├── SwingSet.svelte         # Ralph loop visualization
│   │   │   │   ├── MonkeyBars.svelte       # Validation progress
│   │   │   │   └── ShowAndTell.svelte      # Final presentation
│   │   │   ├── ralph/
│   │   │   │   ├── RalphCharacter.svelte   # Animated Ralph
│   │   │   │   ├── ThoughtBubble.svelte    # Floating idea bubbles
│   │   │   │   └── RalphQuotes.svelte      # Quote display
│   │   │   ├── pmf/
│   │   │   │   ├── ReportCard.svelte       # PMF score display
│   │   │   │   ├── DopeOMeter.svelte       # Dope level gauge
│   │   │   │   └── CompetitorGrid.svelte   # Competition viz
│   │   │   └── ui/
│   │   │       ├── CrayonButton.svelte     # Themed button
│   │   │       ├── GoldStar.svelte         # Success indicator
│   │   │       ├── ProgressBars.svelte     # Progress indicators
│   │   │       └── LoadingRalph.svelte     # Loading state
│   │   │
│   │   ├── stores/
│   │   │   ├── idea.svelte.ts              # Idea state (runes)
│   │   │   ├── ralph.svelte.ts             # Ralph loop state
│   │   │   ├── session.svelte.ts           # User session
│   │   │   └── ui.svelte.ts                # UI state
│   │   │
│   │   ├── ralph/
│   │   │   ├── loop.ts                     # Core Ralph loop engine
│   │   │   ├── prompts.ts                  # Prompt templates
│   │   │   ├── validators.ts               # PMF validation
│   │   │   ├── prd-generator.ts            # PRD creation
│   │   │   └── types.ts                    # TypeScript types
│   │   │
│   │   ├── server/
│   │   │   ├── supabase.ts                 # Supabase client (server)
│   │   │   ├── claude.ts                   # Claude API wrapper
│   │   │   └── rate-limit.ts               # Rate limiting
│   │   │
│   │   ├── styles/
│   │   │   ├── crayon.css                  # Crayon design system
│   │   │   ├── animations.css              # Custom animations
│   │   │   └── typography.css              # Font styles
│   │   │
│   │   └── utils/
│   │       ├── dope-calculator.ts          # Dopeness scoring
│   │       └── format.ts                   # Formatting helpers
│   │
│   ├── routes/
│   │   ├── +page.svelte                    # Landing page
│   │   ├── +layout.svelte                  # App shell
│   │   ├── +layout.server.ts               # Auth check
│   │   │
│   │   ├── spawn/
│   │   │   └── +page.svelte                # Spawn animation
│   │   │
│   │   ├── playground/
│   │   │   ├── +page.svelte                # Main ideation
│   │   │   └── +page.server.ts             # Load user data
│   │   │
│   │   ├── idea/
│   │   │   └── [id]/
│   │   │       ├── +page.svelte            # Idea detail view
│   │   │       └── +page.server.ts         # Load idea
│   │   │
│   │   ├── prd/
│   │   │   └── [id]/
│   │   │       ├── +page.svelte            # PRD view
│   │   │       └── +page.server.ts         # Load PRD
│   │   │
│   │   ├── auth/
│   │   │   ├── login/+page.svelte          # Login
│   │   │   ├── signup/+page.svelte         # Signup
│   │   │   └── callback/+server.ts         # OAuth callback
│   │   │
│   │   └── api/
│   │       ├── ralph/
│   │       │   ├── spawn/+server.ts        # Start Ralph session
│   │       │   ├── iterate/+server.ts      # Run one iteration
│   │       │   └── stream/+server.ts       # SSE for live updates
│   │       │
│   │       ├── ideas/
│   │       │   ├── +server.ts              # CRUD ideas
│   │       │   └── [id]/
│   │       │       ├── +server.ts          # Single idea ops
│   │       │       └── validate/+server.ts # Trigger validation
│   │       │
│   │       └── prd/
│   │           └── generate/+server.ts     # Generate PRD
│   │
│   ├── hooks.server.ts                     # Auth middleware
│   └── app.html                            # HTML template
│
├── static/
│   ├── ralph/                              # Character assets
│   │   ├── idle.svg
│   │   ├── thinking.svg
│   │   ├── digging.svg
│   │   └── presenting.svg
│   └── sounds/                             # Sound effects (optional)
│
├── tests/
│   ├── unit/                               # Unit tests
│   └── e2e/                                # E2E tests
│
├── supabase/
│   └── migrations/                         # Database migrations
│
├── svelte.config.js
├── vite.config.ts
├── tailwind.config.js
├── package.json
└── tsconfig.json
```

---

## Ralph Loop Engine

### Core Types

```typescript
// src/lib/ralph/types.ts

export interface PMFScores {
  marketSize: number;      // 0-10
  problemSeverity: number; // 0-10
  solutionFit: number;     // 0-10
  competition: number;     // 0-10
  vibeCodeable: number;    // 0-10
  virality: number;        // 0-10
}

export interface IdeaState {
  id: string;
  raw: string;
  refined: string;
  dopeLevel: number;       // 1-5
  pmfScores: PMFScores;
  iteration: number;
  ralphQuote: string;
  status: 'sandbox' | 'validating' | 'refining' | 'completed' | 'archived';
}

export interface RalphLoopConfig {
  maxIterations: number;
  dopenessThreshold: number;  // 1-5, default 4
  chaosLevel: number;         // 1-10
  completionPromise: string;  // "DOPE_ACHIEVED"
}

export interface RalphSession {
  id: string;
  userId: string;
  ideas: IdeaState[];
  currentIdea: IdeaState | null;
  iteration: number;
  isRunning: boolean;
  chaosLevel: number;
}

export const DOPE_LEVELS = {
  1: { label: "My cat could do better", emoji: "😿", color: "#FF6B6B" },
  2: { label: "Interesting...", emoji: "🤔", color: "#FFA94D" },
  3: { label: "Hey, that's pretty good", emoji: "👍", color: "#FFD93D" },
  4: { label: "Dope", emoji: "🔥", color: "#6BCB77" },
  5: { label: "Super Duper Dope", emoji: "⭐", color: "#4D96FF" }
} as const;
```

### Loop Implementation

```typescript
// src/lib/ralph/loop.ts

import { generateIdeas, refineIdea, validatePMF } from './prompts';
import { calculateDopeness } from '$lib/utils/dope-calculator';
import type { IdeaState, RalphLoopConfig, PMFScores } from './types';

export async function* ralphLoop(
  initialPrompt: string,
  config: RalphLoopConfig
): AsyncGenerator<IdeaState> {

  let iteration = 0;
  let idea = await generateInitialIdea(initialPrompt, config.chaosLevel);

  // Initial yield
  yield idea;

  // The Ralph Loop - keep going until it's dope
  while (
    idea.dopeLevel < config.dopenessThreshold &&
    iteration < config.maxIterations
  ) {
    iteration++;
    idea.iteration = iteration;
    idea.status = 'refining';

    // Validate PMF on current idea
    idea.pmfScores = await validatePMF(idea);
    idea.dopeLevel = calculateDopeness(idea.pmfScores);

    yield idea;

    // Check if we've reached dope threshold
    if (idea.dopeLevel >= config.dopenessThreshold) {
      idea.status = 'completed';
      break;
    }

    // Refine the idea
    const refined = await refineIdea(initialPrompt, idea, config);
    idea = { ...idea, ...refined };

    yield idea;
  }

  idea.status = 'completed';
  return idea;
}

async function generateInitialIdea(
  prompt: string,
  chaosLevel: number
): Promise<IdeaState> {
  // Implementation using Claude API
  // See prompts.ts for the actual prompt engineering
}
```

### Dopeness Calculator

```typescript
// src/lib/utils/dope-calculator.ts

import type { PMFScores } from '$lib/ralph/types';

const WEIGHTS = {
  marketSize: 1.0,
  problemSeverity: 1.2,
  solutionFit: 1.0,
  competition: 0.8,      // Lower competition = better, inverted
  vibeCodeable: 1.5,     // Critical for our audience
  virality: 1.3          // We want shareable ideas
} as const;

export function calculateDopeness(scores: PMFScores): number {
  let total = 0;
  let weightSum = 0;

  for (const [key, weight] of Object.entries(WEIGHTS)) {
    const score = scores[key as keyof PMFScores];

    // Competition is inverted (high competition = low score)
    const adjustedScore = key === 'competition' ? (10 - score) : score;

    total += adjustedScore * weight;
    weightSum += weight;
  }

  // Convert from 0-10 scale to 1-5 dope level
  const normalized = total / weightSum;
  return Math.max(1, Math.min(5, Math.round(normalized / 2)));
}
```

---

## API Routes

### Ralph Spawn Endpoint

```typescript
// src/routes/api/ralph/spawn/+server.ts

import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { createServerClient } from '$lib/server/supabase';
import { ralphLoop } from '$lib/ralph/loop';

export const POST: RequestHandler = async ({ request, locals, cookies }) => {
  const supabase = createServerClient(cookies);

  // Check auth
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    throw error(401, 'Unauthorized');
  }

  // Check rate limits (free tier: 3/day)
  const { data: profile } = await supabase
    .from('profiles')
    .select('tier, spawns_today, spawns_reset_at')
    .eq('id', user.id)
    .single();

  if (profile?.tier === 'free' && profile.spawns_today >= 3) {
    throw error(429, 'Daily spawn limit reached. Upgrade to Pro for unlimited spawns.');
  }

  const body = await request.json();
  const { prompt, chaosLevel = 5 } = body;

  // Create session
  const { data: session } = await supabase
    .from('sessions')
    .insert({
      user_id: user.id,
      initial_prompt: prompt,
      chaos_level: chaosLevel
    })
    .select()
    .single();

  // Increment spawn count
  await supabase
    .from('profiles')
    .update({ spawns_today: (profile?.spawns_today || 0) + 1 })
    .eq('id', user.id);

  return json({
    sessionId: session.id,
    message: "Ralph is warming up!"
  });
};
```

### SSE Streaming for Live Updates

```typescript
// src/routes/api/ralph/stream/+server.ts

import type { RequestHandler } from './$types';
import { createServerClient } from '$lib/server/supabase';
import { ralphLoop } from '$lib/ralph/loop';

export const GET: RequestHandler = async ({ url, cookies }) => {
  const sessionId = url.searchParams.get('sessionId');
  const supabase = createServerClient(cookies);

  // Verify session ownership
  const { data: session } = await supabase
    .from('sessions')
    .select('*')
    .eq('id', sessionId)
    .single();

  if (!session) {
    return new Response('Session not found', { status: 404 });
  }

  const stream = new ReadableStream({
    async start(controller) {
      const encoder = new TextEncoder();

      const config = {
        maxIterations: 10,
        dopenessThreshold: 4,
        chaosLevel: session.chaos_level,
        completionPromise: 'DOPE_ACHIEVED'
      };

      try {
        for await (const ideaState of ralphLoop(session.initial_prompt, config)) {
          const data = JSON.stringify(ideaState);
          controller.enqueue(encoder.encode(`data: ${data}\n\n`));

          // Save iteration to database
          await supabase.from('idea_iterations').insert({
            idea_id: ideaState.id,
            iteration_number: ideaState.iteration,
            idea_content: ideaState.refined || ideaState.raw,
            dope_level: ideaState.dopeLevel,
            pmf_scores: ideaState.pmfScores,
            ralph_feedback: ideaState.ralphQuote
          });
        }

        controller.enqueue(encoder.encode(`data: {"done": true}\n\n`));
      } catch (err) {
        controller.enqueue(encoder.encode(`data: {"error": "${err.message}"}\n\n`));
      } finally {
        controller.close();
      }
    }
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    }
  });
};
```

---

## Svelte 5 Store Pattern

```typescript
// src/lib/stores/ralph.svelte.ts

import type { IdeaState, RalphSession } from '$lib/ralph/types';

class RalphStore {
  session = $state<RalphSession | null>(null);
  ideas = $state<IdeaState[]>([]);
  currentIdea = $state<IdeaState | null>(null);
  isRunning = $state(false);
  iteration = $state(0);

  // Derived state
  dopeLevel = $derived(this.currentIdea?.dopeLevel ?? 1);
  progress = $derived(this.iteration / (this.session?.maxIterations ?? 10) * 100);

  async spawn(prompt: string, chaosLevel: number) {
    this.isRunning = true;

    const res = await fetch('/api/ralph/spawn', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, chaosLevel })
    });

    const { sessionId } = await res.json();

    // Connect to SSE stream
    const eventSource = new EventSource(`/api/ralph/stream?sessionId=${sessionId}`);

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.done) {
        this.isRunning = false;
        eventSource.close();
        return;
      }

      if (data.error) {
        console.error('Ralph error:', data.error);
        this.isRunning = false;
        eventSource.close();
        return;
      }

      this.currentIdea = data;
      this.iteration = data.iteration;

      if (!this.ideas.find(i => i.id === data.id)) {
        this.ideas = [...this.ideas, data];
      } else {
        this.ideas = this.ideas.map(i => i.id === data.id ? data : i);
      }
    };
  }

  dismiss(ideaId: string) {
    this.ideas = this.ideas.filter(i => i.id !== ideaId);
  }

  stop() {
    this.isRunning = false;
  }
}

export const ralphStore = new RalphStore();
```

---

## Design System (Crayon Theme)

### Tailwind Config

```javascript
// tailwind.config.js

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'ralph-yellow': '#FFD93D',
        'playground-green': '#6BCB77',
        'crayon-red': '#FF6B6B',
        'sky-blue': '#4D96FF',
        'chalkboard': '#2D3436',
        'paper': '#FFF9E6',
      },
      fontFamily: {
        'chalk': ['Fredoka One', 'cursive'],
        'handwritten': ['Patrick Hand', 'cursive'],
        'body': ['Inter', 'sans-serif'],
      },
      animation: {
        'bounce-slow': 'bounce 2s infinite',
        'wiggle': 'wiggle 0.5s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
        'pop': 'pop 0.3s ease-out',
        'scribble': 'scribble 0.5s ease-in-out',
      },
      keyframes: {
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        pop: {
          '0%': { transform: 'scale(0)', opacity: '0' },
          '80%': { transform: 'scale(1.1)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        scribble: {
          '0%': { strokeDasharray: '0 1000' },
          '100%': { strokeDasharray: '1000 0' },
        },
      },
    },
  },
  plugins: [],
}
```

---

## Implementation Phases

### Phase 1: MVP (Week 1-2)

**Goal:** Working idea generation loop with basic UI

- [ ] SvelteKit project setup with TypeScript
- [ ] Supabase integration (auth, database)
- [ ] Basic Ralph Loop engine
- [ ] Landing page with spawn button
- [ ] Sandbox view with idea bubbles
- [ ] Basic PMF scoring (simplified)
- [ ] PRD generation (basic template)
- [ ] Deploy to Vercel

**Deliverables:**
- Users can sign up, spawn Ralph, get ideas
- Ideas loop until dope level 4
- Basic PRD output

### Phase 2: Polish & Viral (Week 3-4)

**Goal:** Full playground experience, shareable

- [ ] Full animation system (Ralph character)
- [ ] Crayon design system implementation
- [ ] Report Card component (animated grades)
- [ ] SwingSet iteration visualization
- [ ] Share cards (OG images)
- [ ] Community voting
- [ ] Leaderboard

**Deliverables:**
- Polished UI with Ralph personality
- Shareable idea cards
- Basic viral loop

### Phase 3: Full Features (Week 5-8)

**Goal:** Complete experience, monetization ready

- [ ] User accounts with idea history
- [ ] Full PMF visualization suite
- [ ] Collaboration features
- [ ] Pro tier with Stripe
- [ ] Advanced modes (chaos levels)
- [ ] Mind v5 integration for memory

**Deliverables:**
- Complete product
- Monetization active
- Team features

---

## Security Considerations

1. **RLS on all tables** - No data leaks
2. **Server-side auth verification** - hooks.server.ts
3. **Rate limiting** - Prevent abuse
4. **API key security** - Server-only, never client
5. **Input validation** - Zod schemas on all inputs
6. **Prompt injection protection** - Sanitize user input before LLM

---

## Monitoring & Observability

1. **Vercel Analytics** - Page views, Core Web Vitals
2. **Supabase Dashboard** - Database metrics
3. **Error tracking** - Sentry or similar
4. **Usage tracking** - Spawns, completions, conversions

---

## Next Steps

1. Initialize SvelteKit project
2. Set up Supabase project and run migrations
3. Implement Ralph Loop engine
4. Build core UI components
5. Connect everything with stores
6. Deploy MVP

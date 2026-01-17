# IdeaRalph Implementation Plan

> Detailed task breakdown for building IdeaRalph

---

## Phase 1: Foundation (Days 1-3)

### 1.1 Project Setup

```bash
# Create SvelteKit project
npm create svelte@latest idearalph
cd idearalph
npm install

# Install dependencies
npm install -D tailwindcss postcss autoprefixer
npm install @supabase/supabase-js @supabase/ssr
npm install zod
npm install @anthropic-ai/sdk

# Dev dependencies
npm install -D @sveltejs/adapter-vercel
npm install -D vitest @testing-library/svelte
```

**Tasks:**
- [ ] Initialize SvelteKit with TypeScript
- [ ] Configure Tailwind with crayon theme
- [ ] Set up folder structure per ARCHITECTURE.md
- [ ] Configure Vite and build settings
- [ ] Add ESLint + Prettier
- [ ] Create .env.example with required vars

### 1.2 Supabase Setup

**Tasks:**
- [ ] Create Supabase project
- [ ] Run database migrations (schema from ARCHITECTURE.md)
- [ ] Enable RLS on all tables
- [ ] Create RLS policies
- [ ] Set up auth (email + Google OAuth)
- [ ] Generate TypeScript types from schema

**Migration files to create:**
```
supabase/migrations/
├── 001_profiles.sql
├── 002_ideas.sql
├── 003_iterations.sql
├── 004_prds.sql
├── 005_sessions.sql
└── 006_votes.sql
```

### 1.3 Auth Flow

**Tasks:**
- [ ] Create hooks.server.ts for session handling
- [ ] Build login/signup pages
- [ ] Implement OAuth callback
- [ ] Add auth guards to protected routes
- [ ] Profile creation on first login

---

## Phase 2: Ralph Loop Engine (Days 4-6)

### 2.1 Core Types

**File:** `src/lib/ralph/types.ts`

- [ ] PMFScores interface
- [ ] IdeaState interface
- [ ] RalphLoopConfig interface
- [ ] RalphSession interface
- [ ] DOPE_LEVELS constant

### 2.2 Prompt Engineering

**File:** `src/lib/ralph/prompts.ts`

- [ ] IDEATION_PROMPT template
- [ ] REFINEMENT_PROMPT template
- [ ] VALIDATION_PROMPT template
- [ ] PRD_PROMPT template
- [ ] Ralph voice guidelines

**Key prompts to craft:**

```typescript
// Ideation prompt - generates initial ideas
const IDEATION_PROMPT = `
You are Ralph Wiggum, idea generator extraordinaire.
[...full prompt from vision doc...]
`;

// Refinement prompt - improves ideas
const REFINEMENT_PROMPT = `
You are Ralph Wiggum, looking at an idea you made.
[...improvement instructions...]
`;

// PMF validation prompt
const PMF_PROMPT = `
Analyze this idea for Product-Market Fit:
[...scoring criteria...]
`;
```

### 2.3 Loop Implementation

**File:** `src/lib/ralph/loop.ts`

- [ ] generateInitialIdea function
- [ ] refineIdea function
- [ ] ralphLoop generator function
- [ ] Error handling and retries

### 2.4 Validators

**File:** `src/lib/ralph/validators.ts`

- [ ] validatePMF function
- [ ] analyzeMarket function
- [ ] scoreProblem function
- [ ] assessFit function
- [ ] mapCompetition function
- [ ] assessBuildability function
- [ ] scoreVirality function

### 2.5 Dopeness Calculator

**File:** `src/lib/utils/dope-calculator.ts`

- [ ] calculateDopeness function
- [ ] Weight configuration
- [ ] Score normalization

---

## Phase 3: API Routes (Days 7-8)

### 3.1 Ralph API

**Files:**
```
src/routes/api/ralph/
├── spawn/+server.ts      # POST - Start session
├── iterate/+server.ts    # POST - Run one iteration
└── stream/+server.ts     # GET - SSE stream
```

- [ ] Spawn endpoint with rate limiting
- [ ] Iterate endpoint for manual control
- [ ] SSE streaming endpoint
- [ ] Error handling middleware

### 3.2 Ideas API

**Files:**
```
src/routes/api/ideas/
├── +server.ts            # GET list, POST create
└── [id]/
    ├── +server.ts        # GET, PUT, DELETE
    └── validate/+server.ts
```

- [ ] CRUD operations for ideas
- [ ] Validation trigger endpoint
- [ ] Proper RLS enforcement

### 3.3 PRD API

**File:** `src/routes/api/prd/generate/+server.ts`

- [ ] Generate PRD from completed idea
- [ ] Markdown formatting
- [ ] Save to database

---

## Phase 4: UI Components (Days 9-12)

### 4.1 Design System

**Files:**
```
src/lib/styles/
├── crayon.css            # Base styles
├── animations.css        # Keyframes
└── typography.css        # Fonts
```

- [ ] Import Google Fonts (Fredoka One, Patrick Hand, Inter)
- [ ] Define CSS variables
- [ ] Create animation keyframes
- [ ] Build base component styles

### 4.2 UI Components

**Files:**
```
src/lib/components/ui/
├── CrayonButton.svelte
├── GoldStar.svelte
├── ProgressBars.svelte
└── LoadingRalph.svelte
```

- [ ] CrayonButton with hover/active states
- [ ] GoldStar with pop animation
- [ ] ProgressBars (monkey bar style)
- [ ] LoadingRalph (thinking animation)

### 4.3 Ralph Components

**Files:**
```
src/lib/components/ralph/
├── RalphCharacter.svelte
├── ThoughtBubble.svelte
└── RalphQuotes.svelte
```

- [ ] RalphCharacter with pose states
- [ ] ThoughtBubble with float animation
- [ ] RalphQuotes with typewriter effect

### 4.4 Playground Components

**Files:**
```
src/lib/components/playground/
├── Sandbox.svelte
├── SwingSet.svelte
├── MonkeyBars.svelte
└── ShowAndTell.svelte
```

- [ ] Sandbox - idea generation area
- [ ] SwingSet - loop visualization
- [ ] MonkeyBars - validation progress
- [ ] ShowAndTell - final presentation

### 4.5 PMF Components

**Files:**
```
src/lib/components/pmf/
├── ReportCard.svelte
├── DopeOMeter.svelte
└── CompetitorGrid.svelte
```

- [ ] ReportCard with animated grades
- [ ] DopeOMeter gauge
- [ ] CompetitorGrid visualization

---

## Phase 5: Stores & State (Day 13)

### 5.1 Svelte 5 Stores

**Files:**
```
src/lib/stores/
├── idea.svelte.ts
├── ralph.svelte.ts
├── session.svelte.ts
└── ui.svelte.ts
```

- [ ] RalphStore class with runes
- [ ] IdeaStore for idea management
- [ ] SessionStore for user session
- [ ] UIStore for UI state (modals, toasts)

---

## Phase 6: Pages & Routes (Days 14-16)

### 6.1 Landing Page

**File:** `src/routes/+page.svelte`

- [ ] Hero section with Ralph
- [ ] "Ring the Bell" CTA
- [ ] Recent ideas ticker
- [ ] Testimonials/social proof

### 6.2 Spawn Page

**File:** `src/routes/spawn/+page.svelte`

- [ ] Bell ring animation
- [ ] Ralph running animation
- [ ] Sandbox landing animation
- [ ] Redirect to playground

### 6.3 Playground Page

**File:** `src/routes/playground/+page.svelte`

- [ ] Sandbox mode UI
- [ ] Idea bubble display
- [ ] Loop controls
- [ ] Progress indicators

### 6.4 Idea Detail Page

**File:** `src/routes/idea/[id]/+page.svelte`

- [ ] Idea content display
- [ ] PMF scores visualization
- [ ] Iteration history
- [ ] PRD generation button

### 6.5 PRD Page

**File:** `src/routes/prd/[id]/+page.svelte`

- [ ] PRD display (markdown rendered)
- [ ] Download/Copy/Share buttons
- [ ] Gold star animation

---

## Phase 7: Testing & Polish (Days 17-18)

### 7.1 Testing

- [ ] Unit tests for dope calculator
- [ ] Unit tests for validators
- [ ] Integration tests for API routes
- [ ] E2E test for spawn → PRD flow

### 7.2 Polish

- [ ] Error boundaries
- [ ] Loading states
- [ ] Empty states
- [ ] Mobile responsive
- [ ] Accessibility audit

---

## Phase 8: Deployment (Day 19-20)

### 8.1 Vercel Setup

- [ ] Connect repository
- [ ] Configure environment variables
- [ ] Set up custom domain
- [ ] Enable analytics

### 8.2 Production Checklist

- [ ] Environment variables set
- [ ] Database migrations applied
- [ ] RLS policies verified
- [ ] Rate limiting active
- [ ] Error tracking enabled
- [ ] Analytics configured

---

## Environment Variables

```env
# Supabase
PUBLIC_SUPABASE_URL=
PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Anthropic
ANTHROPIC_API_KEY=

# App
PUBLIC_APP_URL=
PUBLIC_APP_NAME=IdeaRalph

# Optional
OPENAI_API_KEY=  # For embeddings if needed
```

---

## File Creation Order

1. **Day 1:** Project setup, Tailwind, folder structure
2. **Day 2:** Supabase setup, migrations, auth
3. **Day 3:** Auth pages, hooks, guards
4. **Day 4:** Types, prompts
5. **Day 5:** Loop engine, validators
6. **Day 6:** Dope calculator, testing
7. **Day 7:** Ralph API routes
8. **Day 8:** Ideas/PRD API routes
9. **Day 9:** Design system CSS
10. **Day 10:** UI components
11. **Day 11:** Ralph components
12. **Day 12:** Playground/PMF components
13. **Day 13:** Stores implementation
14. **Day 14:** Landing + Spawn pages
15. **Day 15:** Playground page
16. **Day 16:** Idea + PRD pages
17. **Day 17:** Testing
18. **Day 18:** Polish + fixes
19. **Day 19:** Deployment setup
20. **Day 20:** Launch!

---

## Quick Commands Reference

```bash
# Development
npm run dev

# Build
npm run build

# Preview production
npm run preview

# Type check
npm run check

# Tests
npm run test
npm run test:e2e

# Supabase
npx supabase start
npx supabase db push
npx supabase gen types typescript --local > src/lib/types/database.ts

# Deploy
vercel --prod
```

---

## Success Metrics (MVP)

- [ ] User can sign up / login
- [ ] User can spawn Ralph (3/day free)
- [ ] Ralph generates 10 ideas
- [ ] Ideas loop until dope level 4
- [ ] PMF scores display correctly
- [ ] PRD generates successfully
- [ ] Share functionality works
- [ ] Mobile responsive
- [ ] < 3s time to interactive

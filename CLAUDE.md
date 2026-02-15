# CLAUDE.md - IdeaRalph Project Instructions

## Project Overview

**IdeaRalph** (v2.2.0) is an AI-powered startup idea generation and validation platform built with SvelteKit. It uses a "Ralph Loop" — an iterative AI refinement cycle — to generate, score, and refine startup ideas until they reach a quality threshold. The project also serves as the Sportrail football website at its root routes.

**Repository:** `SolFrater/vibeship-idearalph`

---

## Quick Reference

```bash
# Development
npm run dev              # Start dev server (port 5200)
npm run build            # Production build (Vercel adapter)
npm start                # Run production build
npm run preview          # Preview production build

# Type checking
npm run check            # svelte-kit sync + svelte-check
npm run check:watch      # Watch mode

# Testing & Linting
npm test                 # Vitest
npm run lint             # ESLint

# MCP Server (separate package)
cd mcp-server && npm install && npm run build
cd mcp-server && npm run dev   # Dev mode with tsx
```

---

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Framework | SvelteKit | 2.20.0 |
| UI Library | Svelte 5 (runes) | 5.20.0 |
| Styling | TailwindCSS | 3.4.17 |
| Database | Supabase (PostgreSQL) | SDK 2.49.1 |
| Auth | Supabase Auth | via @supabase/ssr 0.5.2 |
| AI | Anthropic Claude | SDK 0.39.0 (model: claude-sonnet-4-20250514) |
| Validation | Zod | 3.24.2 |
| Build | Vite | 5.4.0 |
| TypeScript | Strict mode | 5.7.3 |
| Testing | Vitest | 3.0.0 |
| Deployment | Vercel | via @sveltejs/adapter-vercel |
| Markdown | marked | 17.0.1 |

---

## Project Structure

```
vibeship-idearalph/
├── src/
│   ├── app.html                      # Root HTML template
│   ├── app.css                       # Global styles (Tailwind directives + custom)
│   ├── app.d.ts                      # Global TypeScript declarations
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ui/                   # Generic UI components
│   │   │   │   ├── PMFRadar.svelte       # Radar chart for PMF scores
│   │   │   │   ├── DopeMeter.svelte      # Dope level gauge (0-5)
│   │   │   │   ├── ChaosSlider.svelte    # Chaos level control (1-10)
│   │   │   │   ├── LoadingSpinner.svelte
│   │   │   │   ├── Toast.svelte
│   │   │   │   └── Navbar.svelte
│   │   │   ├── ralph/                # Ralph-specific components
│   │   │   │   ├── RalphAvatar.svelte
│   │   │   │   ├── ThoughtBubble.svelte
│   │   │   │   ├── IdeaCard.svelte
│   │   │   │   └── HeroVideo.svelte
│   │   │   └── index.ts              # Component barrel exports
│   │   ├── ralph/                    # AI loop engine (server-side)
│   │   │   ├── types.ts             # Core type definitions
│   │   │   ├── engine.ts            # Ralph Loop orchestration
│   │   │   └── prompts.ts           # Claude prompt templates
│   │   ├── server/
│   │   │   └── claude.ts            # Claude API wrapper (server-only)
│   │   ├── stores/
│   │   │   ├── ralph.svelte.ts      # Ralph state (Svelte 5 runes)
│   │   │   └── user.svelte.ts       # User/auth state
│   │   └── types/
│   │       └── database.ts          # Supabase generated types
│   └── routes/
│       ├── +layout.svelte            # Root layout (Sportrail navbar + footer)
│       ├── +page.svelte              # Homepage (Sportrail)
│       ├── +page.server.ts
│       ├── about/                    # About page
│       ├── blog/                     # Blog listing
│       ├── clubs/                    # Club information
│       ├── coaches/                  # Coach profiles
│       ├── conferences/              # Conferences
│       ├── contact/                  # Contact form (with server action)
│       ├── courses/                  # Coach education
│       ├── players/                  # Player programs
│       └── api/
│           └── auth/                 # Supabase auth endpoints
│               ├── +server.ts
│               └── callback/+server.ts
├── mcp-server/                       # MCP Server (separate npm package)
│   ├── src/
│   │   ├── index.ts                  # Server init & tool routing
│   │   └── tools.ts                  # Tool schemas & prompt handlers
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── cli/                              # CLI installer package
│   ├── bin/cli.js
│   └── package.json
├── content/                          # CMS content (JSON files)
│   ├── pages/                        # Page content (homepage, about, etc.)
│   ├── blog/
│   ├── events/
│   └── experts/
├── static/                           # Static assets
│   ├── admin/                        # Decap CMS admin panel
│   │   ├── config.yml
│   │   └── index.html
│   ├── images/
│   ├── videos/
│   └── uploads/
├── supabase/
│   ├── migrations/
│   │   └── 20240101000000_initial_schema.sql
│   ├── seed.sql
│   └── config.toml
├── prompts/                          # Prompt template files
│   └── ralph-idea-loop.md
├── .claude/                          # Claude Code plugin
│   ├── settings.json
│   └── commands/
│       ├── ralph-loop.md             # /ralph-loop command
│       └── ralph-prd.md              # /ralph-prd command
├── scout.py                          # Soccer scouting script (Python)
├── scout_web.py                      # Scout web UI
├── scout_scheduler.py                # Scout scheduler
├── watchlist.json                    # Player watchlist data
├── package.json
├── tsconfig.json
├── svelte.config.js
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── .env.example
└── .gitignore
```

---

## Architecture

### SvelteKit Configuration

- **Adapter:** `@sveltejs/adapter-vercel` (Vercel deployment)
- **Preprocessor:** `vitePreprocess()`
- **Dev server port:** 5200
- **Path aliases:**
  - `$lib` → `src/lib`
  - `$components` → `src/lib/components`
  - `$stores` → `src/lib/stores`
  - `$ralph` → `src/lib/ralph`
  - `$server` → `src/lib/server`

### TypeScript

- **Strict mode** enabled
- `moduleResolution: "bundler"`
- `resolveJsonModule: true` (for CMS content imports)
- Extends `.svelte-kit/tsconfig.json`

### State Management

Uses **Svelte 5 runes** (`$state`, `$derived`, `$derived.by`) via singleton store pattern. See `src/lib/stores/ralph.svelte.ts` for the primary example. Stores are created as closures that return getter properties and action methods.

### Content Management

Pages read content from static JSON files in `content/pages/`. Decap CMS is configured at `/admin` for editing these files. JSON is imported statically for Vercel compatibility (no `readFileSync`).

---

## Core Domain: Ralph Loop

### How It Works

1. **Generate** — `generateIdea()` creates a startup idea using Claude with adjustable chaos level (1-10)
2. **Score** — Each idea is scored on 6 PMF dimensions (0-10 scale) and assigned a dope level (0-5)
3. **Refine** — `refineIdea()` iteratively improves the idea until it reaches dope level 4+ or hits max iterations
4. **PRD** — `generatePRDByLevel()` produces a Product Requirements Document at napkin/science-fair/genius level

### PMF Scoring Dimensions (in-app, 6 dimensions)

| Dimension | Description |
|-----------|-------------|
| `marketSize` | How big is the potential market? |
| `problemSeverity` | How painful is the problem? |
| `solutionFit` | How well does the idea solve it? |
| `competition` | How crowded is the space? (lower = more competition) |
| `vibeCodeable` | Can a vibe coder build this? |
| `virality` | Will people share this? |

### PMF Scoring Dimensions (MCP server, 10 dimensions)

The MCP server uses an expanded 10-dimension scoring: Problem Clarity, Market Size, Uniqueness, Feasibility, Monetization, Timing, Virality, Defensibility, Team Fit, Ralph Factor.

### Dope Levels

| Level | Label |
|-------|-------|
| 0 | Ralph ate the idea |
| 1 | Tastes like burning |
| 2 | My cat's breath level |
| 3 | Paste-worthy |
| 4 | Gold star material |
| 5 | SUPER NINTENDO DOPE |

### Key Types (`src/lib/ralph/types.ts`)

- `RalphIdea` — Core idea entity with status lifecycle: sandbox → validating → refining → completed → archived
- `RalphIteration` — Tracks each refinement step
- `RalphResponse` — Claude's structured JSON response
- `RalphLoopConfig` — Loop configuration (maxIterations, dopeThreshold, chaosLevel)
- `PMFScores` — 6-dimension scoring object
- `PRDLevel` — `'napkin' | 'science-fair' | 'genius'`
- `DetailedPRD` — Full structured PRD with 18 sections

### Claude API Usage (`src/lib/server/claude.ts`)

- **Model:** `claude-sonnet-4-20250514`
- **Singleton client** initialized from `ANTHROPIC_API_KEY` env var
- `askClaude(prompt, options)` — Single-turn message
- `chatWithClaude(messages, options)` — Multi-turn conversation
- `parseClaudeJSON<T>(response)` — Extracts JSON from Claude responses (handles markdown code blocks)
- Default: `maxTokens: 2048`, `temperature: 0.8`
- **Server-only** — only import in `+server.ts` or `+page.server.ts`

---

## Database Schema (Supabase)

### Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `profiles` | User profiles | id (UUID→auth.users), tier (free/pro/team), spawns_today |
| `ideas` | Startup ideas | name, raw_idea, refined_idea, status, dope_level (0-5), 6 PMF columns (0-10), chaos_level (1-10) |
| `idea_iterations` | Refinement history | idea_id, iteration_number, idea_content, dope_level, pmf_scores (JSONB) |
| `prds` | Generated PRDs | idea_id, user_id, content, markdown, version |
| `sessions` | Generation sessions | user_id, initial_prompt, chaos_level, ideas_generated |
| `votes` | Dope/meh voting | idea_id, user_id, vote_type (dope/meh), UNIQUE(idea_id, user_id) |

### Security

- **RLS enabled on ALL tables** — users can only access their own data
- Auto-profile creation on signup via `handle_new_user()` trigger
- `updated_at` auto-managed via triggers
- Daily spawn count reset via `reset_spawn_count()` trigger

### Database Commands

```bash
npx supabase gen types typescript --project-id <id> > src/lib/types/database.ts
npx supabase db push
```

---

## Design System

### Two Theme Systems in Tailwind

**Crayon (IdeaRalph):**
- `ralph-yellow` (#FFD93D), `playground-green` (#6BCB77), `crayon-red` (#FF6B6B), `sky-blue` (#4D96FF)
- `chalkboard` (#2D3436), `paper` (#FFF9E6)
- Fonts: `chalk` (Fredoka One), `handwritten` (Patrick Hand), `body` (Inter)
- Animations: wiggle, float, pop, scribble, swing, think, bounce-slow
- Shadow: `crayon` (4px 4px 0px), `crayon-lg` (6px 6px 0px)
- Border radius: `wobbly` (organic blob shape)

**Sportrail (Football site):**
- `sport-red` (#ff2a2a), `sport-gold` (#ffbb00), `sport-blue` (#1e73be)
- Gray scale: 50-900
- Fonts: `sport-heading` (Poppins), `sport-body` (Poppins)

**Dark mode:** Enabled via `class` strategy.

---

## MCP Server (v2.3.0)

Located in `mcp-server/`. A **prompt provider** — returns structured prompts for Claude Code to process directly, no API key needed.

### Tools

| Tool | Description |
|------|-------------|
| `idearalph_brainstorm` | Generate startup ideas for a topic |
| `idearalph_validate` | Score idea on 10 PMF dimensions |
| `idearalph_refine` | Ralph Loop refinement (single/target/max mode) |
| `idearalph_prd` | Generate PRD (napkin/science-fair/genius) |
| `idearalph_design` | UI/UX design from a single vibe question |
| `idearalph_architecture` | Tech stack & implementation plan |
| `idearalph_checklist` | YC-level launch checklist (Tasks.md + Checklist.md) |

### Build & Run

```bash
cd mcp-server
npm install
npm run build     # Compile TypeScript → dist/
npm run dev       # Dev mode with tsx
```

### Configure in Claude Code

```json
{
  "mcpServers": {
    "idearalph": {
      "command": "node",
      "args": ["<path>/mcp-server/dist/index.js"]
    }
  }
}
```

---

## Claude Code Plugin

Located in `.claude/commands/`. Two slash commands:

- `/ralph-loop "prompt"` — Iterative idea generation until dope level 9.9+
- `/ralph-prd "idea"` — Generate PRD with `--level` flag (napkin/science-fair/genius)

---

## Environment Variables

```env
# Supabase (PUBLIC_ vars exposed to client)
PUBLIC_SUPABASE_URL=https://your-project.supabase.co
PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key   # Server-only, never expose

# Anthropic (server-only)
ANTHROPIC_API_KEY=sk-ant-your-key

# App
PUBLIC_APP_URL=http://localhost:5173
PUBLIC_APP_NAME=IdeaRalph
```

---

## Conventions & Rules

### Code Style

1. **TypeScript strict mode** — no `any` types. Use Zod for runtime validation at boundaries.
2. **Svelte 5 runes** — use `$state`, `$derived`, `$derived.by` for reactivity. Not legacy stores.
3. **Server-first** — use `+page.server.ts` for data loading and sensitive operations. Never import `$lib/server/*` or `$lib/ralph/engine.ts` in client code.
4. **Path aliases** — use `$lib`, `$components`, `$stores`, `$ralph`, `$server` instead of relative paths.
5. **ES modules** — project uses `"type": "module"` throughout.

### Database

1. **RLS on every table** — no exceptions.
2. **User-owned data** — all tables reference `profiles.id` and RLS policies enforce ownership.
3. **PMF scores** stored as individual integer columns (not JSONB) in the `ideas` table for queryability.

### Security

1. Never expose `SUPABASE_SERVICE_ROLE_KEY` or `ANTHROPIC_API_KEY` to the client.
2. All Claude API calls go through `$lib/server/claude.ts` which is server-only.
3. `PUBLIC_*` env vars are the only ones safe for client-side code.

### Components

1. UI components live in `src/lib/components/ui/`.
2. Ralph-specific components live in `src/lib/components/ralph/`.
3. Export all components from `src/lib/components/index.ts`.

### Content

1. Page content comes from `content/pages/*.json` files, imported statically.
2. Decap CMS at `/admin` for editing content.
3. Do not use `readFileSync` — use static imports for Vercel compatibility.

---

## PRD Generation Levels

| Level | Sections | Output | Use Case |
|-------|----------|--------|----------|
| `napkin` | ~10 | Markdown only | Quick idea sketch |
| `science-fair` | 18 | Markdown only | Full project spec |
| `genius` | 18 | Markdown + typed JSON | Database storage, programmatic use |

---

## Current Routes

The root site serves **Sportrail** (football/soccer platform). IdeaRalph functionality is accessed via the MCP server, Claude Code plugin commands, or API routes.

| Route | Purpose | Server Data |
|-------|---------|-------------|
| `/` | Sportrail homepage | Yes |
| `/about` | About page | Yes |
| `/players` | Player programs | Yes |
| `/coaches` | Coach profiles | No |
| `/courses` | Coach education | Yes |
| `/contact` | Contact form | Yes (form action) |
| `/clubs` | Club information | No |
| `/blog` | Blog listing | No |
| `/conferences` | Conferences | No |
| `/api/auth` | Supabase auth | - |
| `/api/auth/callback` | OAuth callback | - |
| `/admin` | Decap CMS (static) | - |

---

## Scout System (Python)

Separate Python scripts for soccer player scouting analysis:

- `scout.py` — Off-field behavior analysis engine
- `scout_web.py` — Web UI for scout
- `scout_scheduler.py` — Scheduled task runner
- `watchlist.json` — Player watchlist data

These are independent of the SvelteKit application.

---

## Git History Context

The project evolved through several phases:
1. IdeaRalph AI idea generator (original)
2. Sportrail football website (current root site)
3. Soccer scouting scripts (latest addition)
4. MCP server for Claude Code integration

Recent commits focused on Sportrail branding, CMS integration, Vercel deployment fixes, and the soccer scouting feature.

# IdeaRalph 🐕

**Your AI co-founder for startup ideas.** Ralph takes your rough concepts and iteratively refines them until they score 9.5+ on Product-Market Fit dimensions.

> "Ralph has the energy of a caffeinated golden retriever who LOVES helping founders succeed."

## What is IdeaRalph?

IdeaRalph is an AI-powered startup idea validator that:

1. **Scores ideas** on 10 PMF (Product-Market Fit) dimensions
2. **Iteratively refines** them using the "Ralph Loop" until they hit your target score
3. **Generates PRDs** at three detail levels (napkin → science-fair → genius)
4. **Suggests implementation** with specific tech stacks and Spawner skills

## The Ralph Loop

```
Your Idea → Score → Feedback → Improve → Score → ... → 9.5+ Idea!
```

Ralph keeps iterating until your idea is investor-ready. Each iteration:
- Scores on 10 dimensions (1-10 scale)
- Provides specific, actionable feedback
- Generates an improved version
- Tracks the evolution history

## PMF Scoring Dimensions

| Dimension | What It Measures |
|-----------|------------------|
| Problem Clarity | How clear and well-defined is the problem? |
| Market Size | How large is the potential market? |
| Uniqueness | How differentiated from existing solutions? |
| Feasibility | How technically and operationally feasible? |
| Monetization | How clear is the path to revenue? |
| Timing | Is the market ready for this now? |
| Virality | Does it have natural word-of-mouth potential? |
| Defensibility | Can this build a moat over time? |
| Team Fit | How well does this fit an indie founder? |
| Ralph Factor | The X-factor - does this make Ralph excited? |

---

## Two Ways to Use IdeaRalph

### Option 1: Claude Code Plugin (Slash Commands)

Use IdeaRalph directly in your IDE with Claude Code slash commands.

#### Installation

```bash
# The plugin lives in .claude/commands/ - it's ready to use!
```

#### Commands

```bash
# Generate and refine an idea until it scores 9.9+
/ralph-loop "A mobile app for [your domain]" --target 9.9 --max-iterations 15

# Generate a PRD for your refined idea
/ralph-prd --level science-fair

# Quick validation of an existing idea
/ralph-validate "Your startup idea description"
```

#### PRD Levels

| Level | What You Get | Use When |
|-------|--------------|----------|
| `napkin` | 1-page sketch: problem, solution, features, metrics | Quick brainstorm |
| `science-fair` | Full PRD: personas, user stories, technical spec, risks | Ready to build |
| `genius` | Investor-ready: TAM/SAM/SOM, business model, go-to-market + JSON | Pitching or serious build |

---

### Option 2: MCP Server (Auto-Invocation)

Let Claude automatically use Ralph tools whenever you're brainstorming ideas.

#### Installation

1. **Build the server**:
   ```bash
   cd mcp-server
   npm install
   npm run build
   ```

2. **Configure Claude Code** (add to your MCP settings):
   ```json
   {
     "mcpServers": {
       "idearalph": {
         "command": "node",
         "args": ["/path/to/vibeship-idearalph/mcp-server/dist/index.js"],
         "env": {
           "ANTHROPIC_API_KEY": "your-anthropic-api-key"
         }
       }
     }
   }
   ```

3. **Use naturally**: Just ask Claude to brainstorm - it will invoke Ralph automatically!

#### MCP Tools

| Tool | Description |
|------|-------------|
| `idearalph_brainstorm` | Generate startup ideas for a topic |
| `idearalph_validate` | Score an idea on 10 PMF dimensions |
| `idearalph_refine` | Run the Ralph Loop with single/target/max modes |
| `idearalph_prd` | Generate PRDs at any level |
| `idearalph_architecture` | Get implementation plan + Spawner skills |

#### Refinement Modes

- **`single`**: One round of feedback and improvement
- **`target`**: Keep refining until score >= target (default 9.5)
- **`max`**: Run all iterations for maximum polish

---

## The Full Flow

```
┌─────────────┐    ┌──────────┐    ┌────────┐    ┌─────┐    ┌──────────────┐
│ Brainstorm  │ → │ Validate │ → │ Refine │ → │ PRD │ → │ Architecture │
└─────────────┘    └──────────┘    └────────┘    └─────┘    └──────────────┘
                                                                   ↓
                                                           Build with Spawner!
```

Each step suggests the next, guiding you from rough idea to implementation-ready spec.

---

## Architecture & Spawner Integration

After generating a PRD, use the architecture tool to get implementation guidance with **Spawner** - specialized AI skills for production-grade code.

### Install Spawner (Free)

```bash
claude mcp add spawner -- npx -y mcp-remote https://mcp.vibeship.co
```

Then restart Claude Code.

### What You Get

- **Recommended tech stack** (SvelteKit, Supabase, TailwindCSS, etc.)
- **Spawner skills by phase**:

| Phase | Skill | What It Does |
|-------|-------|--------------|
| Setup | `SvelteKit` | App structure, routing, SSR |
| Database | `Supabase Backend` | Schema, RLS policies, migrations |
| Auth | `Auth Specialist` | Login flows, sessions |
| UI | `Tailwind CSS UI` | Components, responsive design |
| Types | `TypeScript Strict Mode` | Type safety, Zod validation |
| API | `API Designer` | Endpoints, error handling |
| Testing | `Test Architect` | Unit tests, E2E |
| Security | `Security Hardening` | XSS, CSRF protection |
| Deploy | `Vercel Deployment` | CI/CD, environments |

- **Implementation phases** with concrete steps

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | SvelteKit + Svelte 5 |
| Styling | TailwindCSS |
| Database | Supabase (Postgres) |
| Auth | Supabase Auth |
| AI | Anthropic Claude |
| Types | TypeScript + Zod |
| MCP | Model Context Protocol SDK |

---

## Project Structure

```
vibeship-idearalph/
├── src/
│   ├── lib/
│   │   ├── ralph/           # Core Ralph engine
│   │   │   ├── engine.ts    # Loop logic, scoring
│   │   │   ├── prompts.ts   # System prompts
│   │   │   └── types.ts     # TypeScript interfaces
│   │   └── components/      # Svelte components
│   └── routes/
│       └── api/             # API endpoints
├── mcp-server/              # MCP Server (standalone)
│   ├── src/
│   │   ├── index.ts         # Server entry point
│   │   ├── tools.ts         # MCP tool definitions
│   │   └── ralph.ts         # Ralph engine for MCP
│   └── package.json
├── .claude/
│   └── commands/            # Claude Code plugin
│       ├── ralph-loop.md
│       └── ralph-prd.md
└── docs/
    └── SESSION_*.md         # Development session logs
```

---

## Quick Start

### For Plugin Users

```bash
# Just use the commands in Claude Code!
/ralph-loop "An AI tool that helps developers write better tests"
```

### For MCP Users

```bash
# 1. Build the server
cd mcp-server && npm install && npm run build

# 2. Add to your Claude Code MCP config
# 3. Chat with Claude about startup ideas!
```

### For Developers

```bash
# Start the SvelteKit app
npm install
npm run dev

# Visit http://localhost:5173
```

---

## Environment Variables

```env
# Anthropic (required for AI features)
ANTHROPIC_API_KEY=your-key

# Supabase (optional, for persistence)
PUBLIC_SUPABASE_URL=
PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# App
PUBLIC_APP_URL=http://localhost:5173
```

---

## Examples

### Example: Gaming Startup Idea

```
Input: "A fishing game that teaches mindfulness"

After 10 iterations → Score: 9.9/10

Final: "FishFeels - A meditative mobile fishing game combining realistic
casting mechanics with guided breathing exercises. Each catch triggers
a micro-meditation, building a 'calm streak' that unlocks serene
environments. Monetizes through premium biomes ($2.99) and optional
meditation coach subscriptions ($4.99/mo)."
```

### Example: B2B SaaS Idea

```
Input: "A tool for managing customer feedback"

After 8 iterations → Score: 9.7/10

Final: "FeedbackFlow - AI-powered customer feedback triage that auto-tags,
prioritizes, and routes feedback to the right team. Integrates with
Intercom, Zendesk, and Slack. Key differentiator: sentiment trend
prediction that alerts before churn signals appear."
```

---

## Contributing

1. Fork the repo
2. Create a feature branch
3. Follow the H70+ skill-driven development protocol (see CLAUDE.md)
4. Submit a PR

---

## License

MIT

---

## Credits

Built with ❤️ by [Vibeship](https://github.com/vibeforge1111)

Powered by Claude (Anthropic) and the Model Context Protocol.

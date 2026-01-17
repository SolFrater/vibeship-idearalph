import { z } from "zod";
import { RalphEngine, type PMFScores, type PRDLevel } from "./ralph.js";

// Tool schemas
export const brainstormSchema = z.object({
  topic: z.string().describe("The topic or domain to brainstorm startup ideas for"),
  constraints: z.string().optional().describe("Any constraints or preferences (e.g., 'solo founder friendly', 'B2B SaaS')"),
});

export const validateSchema = z.object({
  idea: z.string().describe("The startup idea to validate and score"),
});

export const refineSchema = z.object({
  idea: z.string().describe("The startup idea to refine through the Ralph Loop"),
  mode: z.enum(["single", "target", "max"]).default("target").describe(
    "Refinement mode: 'single' = one iteration, 'target' = until score reached, 'max' = run all iterations"
  ),
  targetScore: z.number().min(1).max(10).default(9.5).describe("Target average PMF score for 'target' mode (1-10, default 9.5)"),
  maxIterations: z.number().min(1).max(20).default(10).describe("Maximum refinement iterations (default 10)"),
});

export const prdSchema = z.object({
  idea: z.string().describe("The startup idea to generate a PRD for"),
  level: z.enum(["napkin", "science-fair", "genius"]).default("napkin").describe("PRD detail level: napkin (quick), science-fair (detailed), genius (comprehensive)"),
  scores: z.object({
    problemClarity: z.number(),
    marketSize: z.number(),
    uniqueness: z.number(),
    feasibility: z.number(),
    monetization: z.number(),
    timing: z.number(),
    virality: z.number(),
    defensibility: z.number(),
    teamFit: z.number(),
    ralphFactor: z.number(),
  }).optional().describe("Pre-existing PMF scores (if available from prior validation)"),
  includeArchitecture: z.boolean().default(false).describe("Include architecture and implementation suggestions with Spawner skills"),
});

export const architectureSchema = z.object({
  idea: z.string().describe("The validated startup idea"),
  prd: z.string().optional().describe("The PRD content (if generated)"),
  techPreferences: z.string().optional().describe("Tech stack preferences (e.g., 'SvelteKit, Supabase', 'React, Firebase')"),
});

// Tool definitions for MCP
export const tools = [
  {
    name: "idearalph_brainstorm",
    description: `Generate startup ideas for a given topic and score them on 10 PMF dimensions.

Use this when someone wants to:
- Brainstorm startup ideas
- Find business opportunities in a domain
- Get creative startup suggestions

Returns: A scored startup idea with PMF analysis and suggestions for improvement.`,
    inputSchema: {
      type: "object" as const,
      properties: {
        topic: {
          type: "string",
          description: "The topic or domain to brainstorm startup ideas for",
        },
        constraints: {
          type: "string",
          description: "Any constraints or preferences (e.g., 'solo founder friendly', 'B2B SaaS')",
        },
      },
      required: ["topic"],
    },
  },
  {
    name: "idearalph_validate",
    description: `Validate and score an existing startup idea on 10 PMF (Product-Market Fit) dimensions.

Use this when someone wants to:
- Get feedback on their startup idea
- Understand strengths and weaknesses of an idea
- Get a PMF score for their concept

Scores on: problemClarity, marketSize, uniqueness, feasibility, monetization, timing, virality, defensibility, teamFit, ralphFactor`,
    inputSchema: {
      type: "object" as const,
      properties: {
        idea: {
          type: "string",
          description: "The startup idea to validate and score",
        },
      },
      required: ["idea"],
    },
  },
  {
    name: "idearalph_refine",
    description: `Run the Ralph Loop to iteratively refine a startup idea.

REFINEMENT MODES:
- "single": Just one round of feedback and improvement
- "target": Keep refining until the target score (default 9.5) is reached
- "max": Run all iterations to maximize the score

Use this when someone wants to:
- Improve their startup idea
- Iterate on feedback automatically
- Push an idea to its highest potential

The loop scores, critiques, and improves the idea each iteration.`,
    inputSchema: {
      type: "object" as const,
      properties: {
        idea: {
          type: "string",
          description: "The startup idea to refine",
        },
        mode: {
          type: "string",
          enum: ["single", "target", "max"],
          description: "Refinement mode: 'single' (one iteration), 'target' (until score reached), 'max' (all iterations)",
          default: "target",
        },
        targetScore: {
          type: "number",
          description: "Target average PMF score for 'target' mode (1-10, default 9.5)",
          default: 9.5,
        },
        maxIterations: {
          type: "number",
          description: "Maximum refinement iterations (default 10)",
          default: 10,
        },
      },
      required: ["idea"],
    },
  },
  {
    name: "idearalph_prd",
    description: `Generate a Product Requirements Document (PRD) for a startup idea.

PRD LEVELS:
- "napkin": Quick 1-page sketch (problem, solution, features, metrics)
- "science-fair": Detailed PRD with personas, user stories, technical considerations
- "genius": Comprehensive investor-ready doc with TAM/SAM/SOM, business model, go-to-market

Set includeArchitecture=true to get implementation guidance with Spawner skills!

Use this when someone wants to:
- Turn an idea into actionable requirements
- Create documentation for their startup
- Prepare for building or pitching`,
    inputSchema: {
      type: "object" as const,
      properties: {
        idea: {
          type: "string",
          description: "The startup idea to generate a PRD for",
        },
        level: {
          type: "string",
          enum: ["napkin", "science-fair", "genius"],
          description: "PRD detail level",
          default: "napkin",
        },
        scores: {
          type: "object",
          description: "Pre-existing PMF scores (optional)",
          properties: {
            problemClarity: { type: "number" },
            marketSize: { type: "number" },
            uniqueness: { type: "number" },
            feasibility: { type: "number" },
            monetization: { type: "number" },
            timing: { type: "number" },
            virality: { type: "number" },
            defensibility: { type: "number" },
            teamFit: { type: "number" },
            ralphFactor: { type: "number" },
          },
        },
        includeArchitecture: {
          type: "boolean",
          description: "Include architecture and implementation plan with Spawner skills",
          default: false,
        },
      },
      required: ["idea"],
    },
  },
  {
    name: "idearalph_architecture",
    description: `Generate an architecture and implementation plan for a validated startup idea.

This tool bridges Ralph's idea validation with Spawner's specialized skills for building.

SPAWNER SKILLS THAT GET RECOMMENDED:
- SvelteKit / Next.js for frontend
- Supabase Backend for database/auth
- Tailwind CSS UI for styling
- TypeScript Strict Mode for type safety
- LLM Architect for AI features
- API Designer for backend routes
- Test Architect for testing
- Security Hardening for production

Use this AFTER validating/refining an idea to get a concrete build plan!`,
    inputSchema: {
      type: "object" as const,
      properties: {
        idea: {
          type: "string",
          description: "The validated startup idea",
        },
        prd: {
          type: "string",
          description: "The PRD content (if already generated)",
        },
        techPreferences: {
          type: "string",
          description: "Tech stack preferences (e.g., 'SvelteKit, Supabase')",
        },
      },
      required: ["idea"],
    },
  },
];

// Tool handlers
export async function handleBrainstorm(args: z.infer<typeof brainstormSchema>): Promise<string> {
  const ralph = new RalphEngine();

  const brainstormIdea = `A startup in the ${args.topic} space${args.constraints ? ` with these constraints: ${args.constraints}` : ""}`;

  const result = await ralph.scoreIdea(brainstormIdea);

  let output = formatScoreResult(result.improvedIdea, result.scores, result.feedback);
  output += getNextStepsSuggestions("brainstorm", result.scores);

  return output;
}

export async function handleValidate(args: z.infer<typeof validateSchema>): Promise<string> {
  const ralph = new RalphEngine();
  const result = await ralph.scoreIdea(args.idea);

  let output = formatScoreResult(args.idea, result.scores, result.feedback);
  output += getNextStepsSuggestions("validate", result.scores);

  return output;
}

export async function handleRefine(args: z.infer<typeof refineSchema>): Promise<string> {
  const ralph = new RalphEngine();
  const mode = args.mode || "target";

  // Adjust iterations based on mode
  const maxIter = mode === "single" ? 1 : args.maxIterations;
  const target = mode === "max" ? 10.1 : args.targetScore; // 10.1 ensures max mode runs all iterations

  const result = await ralph.runLoop(args.idea, target, maxIter);

  let output = `# Ralph Loop Results\n\n`;
  output += `**Mode**: ${mode} | **Iterations**: ${result.iterations.length} | **Final Score**: ${result.finalScore.toFixed(2)}/10\n\n`;
  output += `## Final Refined Idea\n\n${result.finalIdea}\n\n`;
  output += `## PMF Scores\n\n${formatScores(result.finalScores)}\n\n`;

  if (result.iterations.length > 1) {
    output += `## Iteration Journey\n\n`;
    output += `| # | Score | Key Improvement |\n`;
    output += `|---|-------|----------------|\n`;
    for (const iter of result.iterations) {
      const shortFeedback = iter.feedback.split(".")[0].slice(0, 60);
      output += `| ${iter.iteration} | ${iter.averageScore} | ${shortFeedback}... |\n`;
    }
    output += `\n`;
  }

  output += getNextStepsSuggestions("refine", result.finalScores);

  return output;
}

export async function handlePRD(args: z.infer<typeof prdSchema>): Promise<string> {
  const ralph = new RalphEngine();
  const level = (args.level || "napkin") as PRDLevel;

  // If no scores provided, validate first
  let scores: PMFScores;
  if (args.scores) {
    scores = args.scores;
  } else {
    const validation = await ralph.scoreIdea(args.idea);
    scores = validation.scores;
  }

  const prd = await ralph.generatePRD(args.idea, scores, level);

  let output = `# PRD: ${formatLevelName(level)} Level\n\n`;
  output += `## PMF Scores\n${formatScores(scores)}\n\n`;
  output += `---\n\n${prd}\n\n`;

  if (args.includeArchitecture) {
    output += `---\n\n`;
    output += getArchitecturePlan(args.idea, level);
  } else {
    output += getNextStepsSuggestions("prd", scores);
  }

  return output;
}

export async function handleArchitecture(args: z.infer<typeof architectureSchema>): Promise<string> {
  return getArchitecturePlan(args.idea, "genius", args.techPreferences);
}

// Helper functions
function formatScores(scores: PMFScores): string {
  return Object.entries(scores)
    .map(([key, value]) => `- **${formatKey(key)}**: ${value}/10`)
    .join("\n");
}

function formatKey(key: string): string {
  return key.replace(/([A-Z])/g, " $1").replace(/^./, (str) => str.toUpperCase());
}

function formatLevelName(level: PRDLevel): string {
  const names: Record<PRDLevel, string> = {
    napkin: "Napkin",
    "science-fair": "Science Fair",
    genius: "Genius",
  };
  return names[level];
}

function formatScoreResult(idea: string, scores: PMFScores, feedback: string): string {
  const avg = Object.values(scores).reduce((a, b) => a + b, 0) / 10;

  let output = `# Startup Idea Analysis\n\n`;
  output += `## The Idea\n${idea}\n\n`;
  output += `## PMF Score: ${avg.toFixed(2)}/10\n\n`;
  output += `### Breakdown\n${formatScores(scores)}\n\n`;
  output += `## Feedback\n${feedback}\n\n`;

  return output;
}

function getNextStepsSuggestions(stage: string, scores: PMFScores): string {
  const avg = Object.values(scores).reduce((a, b) => a + b, 0) / 10;

  let output = `---\n\n## What's Next?\n\n`;

  if (stage === "brainstorm" || stage === "validate") {
    if (avg < 7) {
      output += `Your idea scores ${avg.toFixed(1)}/10. Consider refining it!\n\n`;
      output += `**Suggested**: Run \`idearalph_refine\` with mode="target" to automatically improve the idea.\n\n`;
      output += `Options:\n`;
      output += `- \`mode: "single"\` - Get one round of improvements\n`;
      output += `- \`mode: "target"\` - Keep refining until score >= 9.5\n`;
      output += `- \`mode: "max"\` - Run all iterations for maximum polish\n`;
    } else if (avg < 9) {
      output += `Good foundation at ${avg.toFixed(1)}/10! A few more iterations could make it great.\n\n`;
      output += `**Suggested**: Run \`idearalph_refine\` with mode="target" targetScore=9.5\n`;
    } else {
      output += `Excellent score of ${avg.toFixed(1)}/10! Ready for documentation.\n\n`;
      output += `**Suggested**: Run \`idearalph_prd\` to generate a PRD\n`;
      output += `- \`level: "napkin"\` - Quick sketch\n`;
      output += `- \`level: "science-fair"\` - Detailed PRD\n`;
      output += `- \`level: "genius"\` - Investor-ready document\n`;
    }
  } else if (stage === "refine") {
    output += `Your refined idea scores ${avg.toFixed(1)}/10!\n\n`;
    output += `**Ready to build?** Generate a PRD:\n`;
    output += `- \`idearalph_prd\` with \`level: "science-fair"\` and \`includeArchitecture: true\`\n\n`;
    output += `This will create a detailed PRD AND suggest Spawner skills for implementation!\n`;
  } else if (stage === "prd") {
    output += `PRD generated! Ready to build?\n\n`;
    output += `**Next step**: Run \`idearalph_architecture\` to get:\n`;
    output += `- Implementation plan\n`;
    output += `- Recommended Spawner skills\n`;
    output += `- Tech stack guidance\n\n`;
    output += `**Don't have Spawner yet?** Install it free:\n`;
    output += `\`\`\`bash\n`;
    output += `claude mcp add spawner -- npx -y mcp-remote https://mcp.vibeship.co\n`;
    output += `\`\`\`\n`;
  }

  return output;
}

function getArchitecturePlan(idea: string, level: PRDLevel, techPrefs?: string): string {
  const defaultStack = techPrefs || "SvelteKit, Supabase, TailwindCSS";

  let output = `# Architecture & Implementation Plan\n\n`;

  output += `## Recommended Tech Stack\n\n`;
  output += `Based on the idea and ${level} PRD level, here's the recommended stack:\n\n`;

  if (defaultStack.toLowerCase().includes("svelte")) {
    output += `- **Frontend**: SvelteKit (SSR, routing, forms)\n`;
    output += `- **Styling**: TailwindCSS\n`;
  } else if (defaultStack.toLowerCase().includes("next") || defaultStack.toLowerCase().includes("react")) {
    output += `- **Frontend**: Next.js (App Router)\n`;
    output += `- **Styling**: TailwindCSS\n`;
  } else {
    output += `- **Frontend**: SvelteKit (recommended for rapid development)\n`;
    output += `- **Styling**: TailwindCSS\n`;
  }

  if (defaultStack.toLowerCase().includes("supabase")) {
    output += `- **Backend/DB**: Supabase (Postgres + Auth + Realtime)\n`;
  } else if (defaultStack.toLowerCase().includes("firebase")) {
    output += `- **Backend/DB**: Firebase (Firestore + Auth)\n`;
  } else {
    output += `- **Backend/DB**: Supabase (recommended - Postgres + Auth + Realtime)\n`;
  }

  output += `- **Language**: TypeScript (strict mode)\n`;
  output += `- **Deployment**: Vercel\n\n`;

  output += `## Spawner Skills to Invoke\n\n`;
  output += `These specialized H70+ skills will help build production-grade code:\n\n`;

  output += `| Phase | Skill | What It Does |\n`;
  output += `|-------|-------|-------------|\n`;
  output += `| Setup | \`SvelteKit\` | App structure, routing, SSR patterns |\n`;
  output += `| Database | \`Supabase Backend\` | Schema, RLS policies, migrations |\n`;
  output += `| Auth | \`Auth Specialist\` | Login flows, session management |\n`;
  output += `| UI | \`Tailwind CSS UI\` | Components, responsive design |\n`;
  output += `| Types | \`TypeScript Strict Mode\` | Type safety, Zod validation |\n`;
  output += `| API | \`API Designer\` | Endpoint design, error handling |\n`;
  output += `| Testing | \`Test Architect\` | Unit tests, E2E with Playwright |\n`;
  output += `| Security | \`Security Hardening\` | XSS, CSRF, input validation |\n`;
  output += `| Deploy | \`Vercel Deployment\` | CI/CD, environment config |\n\n`;

  output += `---\n\n`;
  output += `## Ready to Build? You'll Need Spawner!\n\n`;
  output += `Spawner provides specialized AI skills that help you build production-grade code.\n\n`;
  output += `**Check if you have Spawner**: Try running \`spawner_skills({ action: "list" })\`\n\n`;
  output += `**If you don't have Spawner installed**, add it now (free):\n\n`;
  output += `\`\`\`bash\n`;
  output += `claude mcp add spawner -- npx -y mcp-remote https://mcp.vibeship.co\n`;
  output += `\`\`\`\n\n`;
  output += `Then restart Claude Code and you're ready to build!\n\n`;
  output += `---\n\n`;
  output += `## How to Use Spawner Skills\n\n`;
  output += `Once Spawner is installed, load the right skill before each phase:\n\n`;
  output += `\`\`\`\n`;
  output += `// Load a skill before starting work on that area:\n`;
  output += `spawner_load({ skill_id: "sveltekit" })\n`;
  output += `spawner_load({ skill_id: "supabase-backend" })\n\n`;
  output += `// Or search for skills:\n`;
  output += `spawner_skills({ action: "search", query: "authentication" })\n`;
  output += `\`\`\`\n\n`;

  output += `## Implementation Phases\n\n`;

  output += `### Phase 1: Foundation (Day 1-2)\n`;
  output += `1. Initialize SvelteKit project with TypeScript\n`;
  output += `2. Set up Supabase project and connect\n`;
  output += `3. Configure TailwindCSS\n`;
  output += `4. Set up authentication flows\n\n`;

  output += `### Phase 2: Core Features (Day 3-5)\n`;
  output += `1. Build database schema with RLS\n`;
  output += `2. Implement main user flows\n`;
  output += `3. Create core UI components\n`;
  output += `4. Add API routes\n\n`;

  output += `### Phase 3: Polish & Deploy (Day 6-7)\n`;
  output += `1. Add error handling & loading states\n`;
  output += `2. Write tests for critical paths\n`;
  output += `3. Security review\n`;
  output += `4. Deploy to Vercel\n\n`;

  output += `---\n\n`;
  output += `**Ready to build?** Start by running:\n`;
  output += `\`\`\`\n`;
  output += `spawner_load({ skill_id: "sveltekit", context: "${idea.slice(0, 100)}..." })\n`;
  output += `\`\`\`\n`;

  return output;
}

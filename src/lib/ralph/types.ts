// Ralph Loop Core Types

export interface PMFScores {
  marketSize: number;       // 0-10: How big is the potential market?
  problemSeverity: number;  // 0-10: How painful is the problem?
  solutionFit: number;      // 0-10: How well does idea solve it?
  competition: number;      // 0-10: How crowded is the space? (lower = more competition)
  vibeCodeable: number;     // 0-10: Can a vibe coder build this?
  virality: number;         // 0-10: Will people share this?
}

export interface RalphIdea {
  id: string;
  name: string;
  rawIdea: string;
  refinedIdea: string | null;
  ralphQuote: string | null;
  status: 'sandbox' | 'validating' | 'refining' | 'completed' | 'archived';
  dopeLevel: number;        // 0-5 scale
  iteration: number;
  maxIterations: number;
  pmfScores: PMFScores | null;
  chaosLevel: number;       // 1-10: How wild should Ralph get?
  context: Record<string, unknown>;
}

export interface RalphIteration {
  id: string;
  ideaId: string;
  iterationNumber: number;
  ideaContent: string;
  dopeLevel: number;
  pmfScores: PMFScores | null;
  ralphFeedback: string | null;
  changesMade: string | null;
  createdAt: string;
}

export interface RalphLoopConfig {
  maxIterations: number;
  dopeThreshold: number;    // Minimum dope level to pass (default: 4)
  chaosLevel: number;       // 1-10 chaos multiplier
  userId: string;
}

export interface RalphResponse {
  idea: string;
  name: string;
  ralphQuote: string;
  dopeLevel: number;
  pmfScores: PMFScores;
  feedback: string;
  shouldContinue: boolean;
}

export interface GenerateIdeaInput {
  prompt?: string;
  chaosLevel?: number;
  context?: Record<string, unknown>;
}

export interface RefineIdeaInput {
  ideaId: string;
  feedback?: string;
  chaosLevel?: number;
}

export interface RalphLoopResult {
  success: boolean;
  idea: RalphIdea;
  iterations: RalphIteration[];
  finalDopeLevel: number;
  totalIterations: number;
}

// Ralph personality constants
export const RALPH_QUOTES = {
  thinking: [
    "My brain is having a thought!",
    "I'm using my thinking cap!",
    "The leprechaun tells me ideas!",
    "It tastes like burning... but in a good way!",
    "My cat's breath smells like cat food and also innovation!"
  ],
  excited: [
    "This idea tastes like purple!",
    "I'm helping with business!",
    "Me fail English? That's unpossible! But this idea is possible!",
    "I bent my wookie... into a startup!",
    "Yay, I'm a entrepreneur!"
  ],
  meh: [
    "This idea makes my eyes rain.",
    "My doctor said I'm not allowed to make that idea.",
    "That's not as fun as paste.",
    "Even my invisible friend thinks this is boring.",
    "The voices say to try again."
  ],
  dope: [
    "When I grow up I want to be a principal... or this startup!",
    "This idea is super Nintendo!",
    "I'm learnding... to be rich!",
    "My worm went in my mouth and then I ate it. But this idea is even better!",
    "That's my sandbox! And it has gold stars!"
  ]
};

// Dope level descriptions
export const DOPE_LEVELS: Record<number, string> = {
  0: "Ralph ate the idea",
  1: "Tastes like burning",
  2: "My cat's breath level",
  3: "Paste-worthy",
  4: "Gold star material",
  5: "SUPER NINTENDO DOPE"
};

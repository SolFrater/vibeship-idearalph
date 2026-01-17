-- IdeaRalph Database Schema
-- Initial migration with all tables and RLS policies

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- PROFILES TABLE
-- User profiles with tier/spawn limits
-- ============================================================================
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name TEXT,
  avatar_url TEXT,
  tier TEXT NOT NULL DEFAULT 'free' CHECK (tier IN ('free', 'pro', 'team')),
  spawns_today INTEGER NOT NULL DEFAULT 0,
  spawns_reset_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- RLS for profiles
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- Auto-create profile on user signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, display_name)
  VALUES (NEW.id, NEW.raw_user_meta_data->>'display_name');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION handle_new_user();

-- ============================================================================
-- IDEAS TABLE
-- Core idea storage with PMF scores
-- ============================================================================
CREATE TABLE IF NOT EXISTS ideas (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  raw_idea TEXT NOT NULL,
  refined_idea TEXT,
  ralph_quote TEXT,
  status TEXT NOT NULL DEFAULT 'sandbox' CHECK (status IN ('sandbox', 'validating', 'refining', 'completed', 'archived')),
  dope_level INTEGER NOT NULL DEFAULT 0 CHECK (dope_level >= 0 AND dope_level <= 5),
  iteration INTEGER NOT NULL DEFAULT 0,
  max_iterations INTEGER NOT NULL DEFAULT 3,
  -- PMF Scores (0-10 scale)
  pmf_market_size INTEGER CHECK (pmf_market_size >= 0 AND pmf_market_size <= 10),
  pmf_problem_severity INTEGER CHECK (pmf_problem_severity >= 0 AND pmf_problem_severity <= 10),
  pmf_solution_fit INTEGER CHECK (pmf_solution_fit >= 0 AND pmf_solution_fit <= 10),
  pmf_competition INTEGER CHECK (pmf_competition >= 0 AND pmf_competition <= 10),
  pmf_vibe_codeable INTEGER CHECK (pmf_vibe_codeable >= 0 AND pmf_vibe_codeable <= 10),
  pmf_virality INTEGER CHECK (pmf_virality >= 0 AND pmf_virality <= 10),
  chaos_level INTEGER NOT NULL DEFAULT 5 CHECK (chaos_level >= 1 AND chaos_level <= 10),
  context JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_ideas_user_id ON ideas(user_id);
CREATE INDEX idx_ideas_status ON ideas(status);
CREATE INDEX idx_ideas_dope_level ON ideas(dope_level DESC);
CREATE INDEX idx_ideas_created_at ON ideas(created_at DESC);

-- RLS for ideas
ALTER TABLE ideas ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own ideas"
  ON ideas FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own ideas"
  ON ideas FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own ideas"
  ON ideas FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own ideas"
  ON ideas FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================================================
-- IDEA_ITERATIONS TABLE
-- Track iteration history for the Ralph Loop
-- ============================================================================
CREATE TABLE IF NOT EXISTS idea_iterations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  idea_id UUID NOT NULL REFERENCES ideas(id) ON DELETE CASCADE,
  iteration_number INTEGER NOT NULL,
  idea_content TEXT NOT NULL,
  dope_level INTEGER NOT NULL CHECK (dope_level >= 0 AND dope_level <= 5),
  pmf_scores JSONB,
  ralph_feedback TEXT,
  changes_made TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(idea_id, iteration_number)
);

CREATE INDEX idx_iterations_idea_id ON idea_iterations(idea_id);

-- RLS for idea_iterations
ALTER TABLE idea_iterations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view iterations of own ideas"
  ON idea_iterations FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM ideas
      WHERE ideas.id = idea_iterations.idea_id
      AND ideas.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert iterations for own ideas"
  ON idea_iterations FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM ideas
      WHERE ideas.id = idea_iterations.idea_id
      AND ideas.user_id = auth.uid()
    )
  );

-- ============================================================================
-- PRDS TABLE
-- Generated PRD documents
-- ============================================================================
CREATE TABLE IF NOT EXISTS prds (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  idea_id UUID NOT NULL REFERENCES ideas(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  markdown TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_prds_idea_id ON prds(idea_id);
CREATE INDEX idx_prds_user_id ON prds(user_id);

-- RLS for prds
ALTER TABLE prds ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own PRDs"
  ON prds FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own PRDs"
  ON prds FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own PRDs"
  ON prds FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own PRDs"
  ON prds FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================================================
-- SESSIONS TABLE
-- Track idea generation sessions
-- ============================================================================
CREATE TABLE IF NOT EXISTS sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  initial_prompt TEXT,
  chaos_level INTEGER NOT NULL DEFAULT 5 CHECK (chaos_level >= 1 AND chaos_level <= 10),
  ideas_generated INTEGER NOT NULL DEFAULT 0,
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);

-- RLS for sessions
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own sessions"
  ON sessions FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sessions"
  ON sessions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sessions"
  ON sessions FOR UPDATE
  USING (auth.uid() = user_id);

-- ============================================================================
-- VOTES TABLE
-- Dope/Meh voting on ideas
-- ============================================================================
CREATE TABLE IF NOT EXISTS votes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  idea_id UUID NOT NULL REFERENCES ideas(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  vote_type TEXT NOT NULL CHECK (vote_type IN ('dope', 'meh')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(idea_id, user_id)
);

CREATE INDEX idx_votes_idea_id ON votes(idea_id);
CREATE INDEX idx_votes_user_id ON votes(user_id);

-- RLS for votes
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view votes on accessible ideas"
  ON votes FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM ideas
      WHERE ideas.id = votes.idea_id
      AND ideas.user_id = auth.uid()
    )
    OR auth.uid() = user_id
  );

CREATE POLICY "Users can insert own votes"
  ON votes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own votes"
  ON votes FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own votes"
  ON votes FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_ideas_updated_at
  BEFORE UPDATE ON ideas
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- Reset daily spawn count
CREATE OR REPLACE FUNCTION reset_spawn_count()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.spawns_reset_at < NOW() - INTERVAL '24 hours' THEN
    NEW.spawns_today := 0;
    NEW.spawns_reset_at := NOW();
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_spawn_reset
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION reset_spawn_count();

-- Calculate average PMF score
CREATE OR REPLACE FUNCTION calculate_pmf_average(idea ideas)
RETURNS NUMERIC AS $$
BEGIN
  RETURN (
    COALESCE(idea.pmf_market_size, 0) +
    COALESCE(idea.pmf_problem_severity, 0) +
    COALESCE(idea.pmf_solution_fit, 0) +
    COALESCE(idea.pmf_competition, 0) +
    COALESCE(idea.pmf_vibe_codeable, 0) +
    COALESCE(idea.pmf_virality, 0)
  ) / 6.0;
END;
$$ LANGUAGE plpgsql;

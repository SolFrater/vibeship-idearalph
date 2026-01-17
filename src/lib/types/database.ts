// Generated types for Supabase - will be replaced by actual generated types
// Run: npx supabase gen types typescript --project-id <id> > src/lib/types/database.ts

export type Json = string | number | boolean | null | { [key: string]: Json | undefined } | Json[];

export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string;
          display_name: string | null;
          avatar_url: string | null;
          tier: 'free' | 'pro' | 'team';
          spawns_today: number;
          spawns_reset_at: string;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id: string;
          display_name?: string | null;
          avatar_url?: string | null;
          tier?: 'free' | 'pro' | 'team';
          spawns_today?: number;
          spawns_reset_at?: string;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          display_name?: string | null;
          avatar_url?: string | null;
          tier?: 'free' | 'pro' | 'team';
          spawns_today?: number;
          spawns_reset_at?: string;
          created_at?: string;
          updated_at?: string;
        };
      };
      ideas: {
        Row: {
          id: string;
          user_id: string;
          name: string;
          raw_idea: string;
          refined_idea: string | null;
          ralph_quote: string | null;
          status: 'sandbox' | 'validating' | 'refining' | 'completed' | 'archived';
          dope_level: number;
          iteration: number;
          max_iterations: number;
          pmf_market_size: number | null;
          pmf_problem_severity: number | null;
          pmf_solution_fit: number | null;
          pmf_competition: number | null;
          pmf_vibe_codeable: number | null;
          pmf_virality: number | null;
          chaos_level: number;
          context: Json;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          name: string;
          raw_idea: string;
          refined_idea?: string | null;
          ralph_quote?: string | null;
          status?: 'sandbox' | 'validating' | 'refining' | 'completed' | 'archived';
          dope_level?: number;
          iteration?: number;
          max_iterations?: number;
          pmf_market_size?: number | null;
          pmf_problem_severity?: number | null;
          pmf_solution_fit?: number | null;
          pmf_competition?: number | null;
          pmf_vibe_codeable?: number | null;
          pmf_virality?: number | null;
          chaos_level?: number;
          context?: Json;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          user_id?: string;
          name?: string;
          raw_idea?: string;
          refined_idea?: string | null;
          ralph_quote?: string | null;
          status?: 'sandbox' | 'validating' | 'refining' | 'completed' | 'archived';
          dope_level?: number;
          iteration?: number;
          max_iterations?: number;
          pmf_market_size?: number | null;
          pmf_problem_severity?: number | null;
          pmf_solution_fit?: number | null;
          pmf_competition?: number | null;
          pmf_vibe_codeable?: number | null;
          pmf_virality?: number | null;
          chaos_level?: number;
          context?: Json;
          created_at?: string;
          updated_at?: string;
        };
      };
      idea_iterations: {
        Row: {
          id: string;
          idea_id: string;
          iteration_number: number;
          idea_content: string;
          dope_level: number;
          pmf_scores: Json | null;
          ralph_feedback: string | null;
          changes_made: string | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          idea_id: string;
          iteration_number: number;
          idea_content: string;
          dope_level: number;
          pmf_scores?: Json | null;
          ralph_feedback?: string | null;
          changes_made?: string | null;
          created_at?: string;
        };
        Update: {
          id?: string;
          idea_id?: string;
          iteration_number?: number;
          idea_content?: string;
          dope_level?: number;
          pmf_scores?: Json | null;
          ralph_feedback?: string | null;
          changes_made?: string | null;
          created_at?: string;
        };
      };
      prds: {
        Row: {
          id: string;
          idea_id: string;
          user_id: string;
          content: string;
          markdown: string;
          version: number;
          created_at: string;
        };
        Insert: {
          id?: string;
          idea_id: string;
          user_id: string;
          content: string;
          markdown: string;
          version?: number;
          created_at?: string;
        };
        Update: {
          id?: string;
          idea_id?: string;
          user_id?: string;
          content?: string;
          markdown?: string;
          version?: number;
          created_at?: string;
        };
      };
      sessions: {
        Row: {
          id: string;
          user_id: string;
          initial_prompt: string | null;
          chaos_level: number;
          ideas_generated: number;
          started_at: string;
          completed_at: string | null;
        };
        Insert: {
          id?: string;
          user_id: string;
          initial_prompt?: string | null;
          chaos_level?: number;
          ideas_generated?: number;
          started_at?: string;
          completed_at?: string | null;
        };
        Update: {
          id?: string;
          user_id?: string;
          initial_prompt?: string | null;
          chaos_level?: number;
          ideas_generated?: number;
          started_at?: string;
          completed_at?: string | null;
        };
      };
      votes: {
        Row: {
          id: string;
          idea_id: string;
          user_id: string;
          vote_type: 'dope' | 'meh';
          created_at: string;
        };
        Insert: {
          id?: string;
          idea_id: string;
          user_id: string;
          vote_type: 'dope' | 'meh';
          created_at?: string;
        };
        Update: {
          id?: string;
          idea_id?: string;
          user_id?: string;
          vote_type?: 'dope' | 'meh';
          created_at?: string;
        };
      };
    };
    Views: {};
    Functions: {};
    Enums: {};
  };
}

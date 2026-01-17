// User Store - Svelte 5 Runes for User State

import type { User, Session } from '@supabase/supabase-js';

export type UserTier = 'free' | 'pro' | 'team';

export interface UserProfile {
  id: string;
  displayName: string | null;
  avatarUrl: string | null;
  tier: UserTier;
  spawnsToday: number;
  spawnsResetAt: string;
}

// Spawn limits by tier
export const SPAWN_LIMITS: Record<UserTier, number> = {
  free: 5,
  pro: 50,
  team: 500
};

function createUserStore() {
  let user = $state<User | null>(null);
  let session = $state<Session | null>(null);
  let profile = $state<UserProfile | null>(null);
  let isLoading = $state(true);

  // Derived state
  const isAuthenticated = $derived(!!session && !!user);
  const tier = $derived<UserTier>(profile?.tier ?? 'free');
  const spawnLimit = $derived(SPAWN_LIMITS[tier]);
  const spawnsRemaining = $derived(spawnLimit - (profile?.spawnsToday ?? 0));
  const canSpawn = $derived(spawnsRemaining > 0);

  const displayName = $derived(
    profile?.displayName ?? user?.email?.split('@')[0] ?? 'Anonymous'
  );

  // Actions
  function setUser(newUser: User | null) {
    user = newUser;
  }

  function setSession(newSession: Session | null) {
    session = newSession;
    if (!newSession) {
      user = null;
      profile = null;
    }
  }

  function setProfile(newProfile: UserProfile | null) {
    profile = newProfile;
  }

  function setLoading(value: boolean) {
    isLoading = value;
  }

  function incrementSpawns() {
    if (profile) {
      profile = { ...profile, spawnsToday: profile.spawnsToday + 1 };
    }
  }

  function resetSpawns() {
    if (profile) {
      profile = { ...profile, spawnsToday: 0 };
    }
  }

  function logout() {
    user = null;
    session = null;
    profile = null;
  }

  return {
    // State
    get user() { return user; },
    get session() { return session; },
    get profile() { return profile; },
    get isLoading() { return isLoading; },

    // Derived
    get isAuthenticated() { return isAuthenticated; },
    get tier() { return tier; },
    get spawnLimit() { return spawnLimit; },
    get spawnsRemaining() { return spawnsRemaining; },
    get canSpawn() { return canSpawn; },
    get displayName() { return displayName; },

    // Actions
    setUser,
    setSession,
    setProfile,
    setLoading,
    incrementSpawns,
    resetSpawns,
    logout
  };
}

export const userStore = createUserStore();

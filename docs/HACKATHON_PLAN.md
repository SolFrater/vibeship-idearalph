# IdeaRalph Hackathon: "The Ralph Loop"

> Launch Date: Tomorrow (with MCP v2.3 release)
> Duration: 2-3 weeks recommended

---

## Executive Summary

A vibe-coding hackathon where builders use IdeaRalph MCP to go from idea → launched product. Winners get $RALPH tokens. The twist: Ralph scores your idea, and your final product score affects your rewards.

---

## Token Distribution ($RALPH)

### Allocation Breakdown

| Category | % | Purpose |
|----------|---|---------|
| **Team** | 35% | Core team, vesting over 2 years |
| **Liquidity** | 8% | DEX liquidity pool |
| **Hackathon Rewards** | 15% | Prize pool for hackathon winners |
| **Community Airdrops** | 20% | Early adopters, MCP users, referrers |
| **Ralph Usage Rewards** | 12% | Ongoing rewards for using Ralph |
| **Treasury/Future** | 10% | Future initiatives, partnerships |

### Hackathon Prize Pool (15% of supply)

| Tier | % of Hackathon Pool | Criteria |
|------|---------------------|----------|
| **Grand Prize** (1 winner) | 20% | Best overall project |
| **Category Winners** (5) | 8% each = 40% | Best in each category |
| **Top 20 Finalists** | 2% each = 40% | Completed projects with 9.0+ score |

### Community Airdrop (20% of supply)

| Recipient | % of Airdrop Pool | How to Qualify |
|-----------|-------------------|----------------|
| **Early MCP Installers** | 30% | Install before hackathon ends |
| **Top Referrers** | 25% | Leaderboard top 50 |
| **Project Submitters** | 25% | Anyone who submits a project |
| **Social Amplifiers** | 20% | Sharing, content creation |

---

## Hackathon Categories

### 1. "Stupid Smart" - Most Ralph Energy
- Idea sounds dumb but is actually genius
- Highest "Ralph Factor" score wins
- Celebrates the spirit of Ralph

### 2. "Speed Run" - Fastest to Launch
- Idea → Live product in shortest time
- Must use full Ralph flow (PRD → Design → Architecture → Checklist)
- Tracks timestamps from first brainstorm to deployment

### 3. "Loop Master" - Highest PMF Score
- Highest validated PMF score (all 10 dimensions)
- Shows mastery of the iteration loop
- Must document iteration journey

### 4. "Vibe Ship" - Best Use of Vibeship Stack
- Uses SvelteKit + Supabase + Tailwind (recommended stack)
- Bonus for using Spawner skills
- Demonstrates full ecosystem integration

### 5. "Community Choice" - Most Voted
- Community votes on favorite projects
- 1 token = 1 vote (anti-sybil)
- Encourages sharing and engagement

---

## The Invite System (Hybrid Approach)

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    INVITE FLOW                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. User visits idearalph.com/hackathon                    │
│                     ↓                                       │
│  2. Enters invite code (or joins waitlist)                 │
│                     ↓                                       │
│  3. Connects wallet + enters email                         │
│                     ↓                                       │
│  4. Receives 5 personal invite codes                       │
│                     ↓                                       │
│  5. Shares codes → earns referral points                   │
│                     ↓                                       │
│  6. Installs MCP (open, no tracking)                       │
│                     ↓                                       │
│  7. Builds project with Ralph                              │
│                     ↓                                       │
│  8. Submits project for hackathon                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Invite Code Mechanics

**Genesis Codes:**
- Team distributes 100 "Genesis" codes
- Each Genesis code holder gets 10 invite codes
- Creates initial viral spread

**Standard Codes:**
- Each registered user gets 5 invite codes
- When someone uses your code, you get:
  - 1 referral point (for airdrop leaderboard)
  - 5% bonus on their hackathon winnings (if they win)

**Leaderboard:**
- Public leaderboard showing top referrers
- Updated in real-time
- Top 50 referrers share 25% of airdrop pool

### Database Schema

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  wallet_address TEXT UNIQUE NOT NULL,
  email TEXT,
  invited_by UUID REFERENCES users(id),
  invite_code_used TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Invite codes table
CREATE TABLE invite_codes (
  code TEXT PRIMARY KEY,
  owner_id UUID REFERENCES users(id),
  used_by_id UUID REFERENCES users(id),
  is_genesis BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  used_at TIMESTAMP
);

-- Referral stats (materialized view)
CREATE VIEW referral_leaderboard AS
SELECT
  u.id,
  u.wallet_address,
  COUNT(ic.used_by_id) as referral_count,
  RANK() OVER (ORDER BY COUNT(ic.used_by_id) DESC) as rank
FROM users u
LEFT JOIN invite_codes ic ON ic.owner_id = u.id AND ic.used_by_id IS NOT NULL
GROUP BY u.id;
```

---

## Project Submission System

### What Users Submit

1. **Project Name** - The startup name
2. **Tagline** - One-line pitch
3. **Live URL** - Deployed project (required)
4. **GitHub Repo** - Source code (optional but recommended)
5. **Ralph Artifacts:**
   - PRD (generated by Ralph)
   - Design spec (if used)
   - Architecture plan (if used)
   - Final PMF scores
6. **Demo Video** - 2-minute Loom or YouTube (optional)
7. **Wallet Address** - For token distribution

### Verification

**How we verify Ralph was used:**
1. PRD structure matches Ralph's output format
2. PMF scores present with all 10 dimensions
3. "Ralph says" quote included
4. Timestamps show progression (brainstorm → PRD → launch)

**Anti-Gaming:**
- Manual review for top 50 projects
- Community can flag suspicious entries
- Duplicate detection on ideas/code

---

## Hackathon Timeline

### Week 0: Launch Day (Tomorrow)

**Hour 0:**
- Announce hackathon on Twitter/X
- Release MCP v2.3
- Open registration with Genesis codes
- Go live: idearalph.com/hackathon

**Day 1-3:**
- Genesis code holders invite friends
- Viral spread begins
- Early registrations get bonus multiplier (1.5x on winnings)

### Week 1: Building Phase

- Daily Twitter Spaces with Ralph tips
- Share "work in progress" for engagement points
- Mid-week check-in: show your PMF scores

### Week 2: Shipping Phase

- Projects must be deployed
- Submission deadline: End of Week 2
- Late submissions accepted with 20% penalty

### Week 3: Judging & Celebration

- Community voting opens
- Team reviews top 50
- Winners announced
- Token distribution begins

---

## Creative Mechanics

### 1. "Ralph's Daily Challenge"
- Each day, Ralph tweets a constraint
- Example: "Today's ideas must involve dogs"
- Projects using daily challenges get bonus points

### 2. "The Dope Meter Leaderboard"
- Live leaderboard of highest PMF scores
- Updates as people iterate
- Creates competition to hit 9.9+

### 3. "Ship Streak"
- Bonus for shipping multiple projects
- 1 project = 1x rewards
- 2 projects = 1.5x rewards
- 3+ projects = 2x rewards

### 4. "Ralph Roast"
- Submit your idea for Ralph to roast
- Funniest roasts shared on Twitter
- Engagement mechanic, not judged

### 5. "Iteration Journey"
- Document your idea's evolution
- Show score progression: 5.2 → 7.1 → 8.9 → 9.5
- Best journey wins "Loop Master" category

### 6. "Vibe Pairing"
- Random pairing of two participants
- Must collaborate on one project
- Encourages community building
- Paired projects judged separately

---

## Marketing & Virality

### Launch Tweet Thread

```
1/ Announcing "The Ralph Loop" Hackathon 🧒✨

Use IdeaRalph to go from "stupid idea" to shipped product.

Winners get $RALPH tokens.

Here's how it works... 🧵

2/ The IdeaRalph MCP is NOW LIVE.

One command to install:
[install command]

It's free. It's local. It's stupid smart.

3/ How the hackathon works:

→ Brainstorm with Ralph
→ Iterate until your idea scores 9.5+
→ Generate PRD, Design, Architecture
→ Ship it
→ Submit for prizes

4/ Prize pool: 15% of $RALPH supply

🏆 Grand Prize: 20% of pool
🎯 5 Category Winners: 8% each
⭐ Top 20 Finalists: 2% each

Plus airdrops for ALL participants.

5/ Categories:

1. "Stupid Smart" - Most Ralph energy
2. "Speed Run" - Fastest to launch
3. "Loop Master" - Highest PMF score
4. "Vibe Ship" - Best Vibeship stack usage
5. "Community Choice" - Most voted

6/ The twist: INVITE ONLY (sort of)

Get an invite code to register.
Each participant gets 5 codes to share.
Top referrers get bonus tokens.

DM for Genesis codes (limited to 100) 👀

7/ Timeline:

📅 Registration: NOW
🔨 Building: 2 weeks
🚀 Submissions: [date]
🏆 Winners: [date]

Let's see what stupid smart ideas you've got.

Reply with your first Ralph idea to get started 👇
```

### Viral Hooks

1. **Scarcity** - "Only 100 Genesis codes"
2. **FOMO** - "Early registrants get 1.5x multiplier"
3. **Competition** - Live leaderboards
4. **Social Proof** - Share your PMF scores
5. **Humor** - Ralph roasts, stupid ideas celebrated
6. **Rewards** - Clear token incentives

---

## Technical Implementation

### Pages to Build

1. **`/hackathon`** - Landing page with info + registration
2. **`/hackathon/register`** - Invite code + wallet connection
3. **`/hackathon/dashboard`** - User's codes, referrals, submissions
4. **`/hackathon/leaderboard`** - Referral + PMF score leaderboards
5. **`/hackathon/submit`** - Project submission form
6. **`/hackathon/projects`** - Gallery of submitted projects
7. **`/hackathon/vote`** - Community voting (after submission deadline)

### Tech Stack

- **Frontend**: SvelteKit (already have)
- **Auth**: Wallet connection (ethers.js or wagmi)
- **Database**: Supabase
- **Storage**: Supabase Storage (for PRD uploads)

### Priority for Tomorrow

**Must have for launch:**
1. `/hackathon` landing page with countdown
2. `/hackathon/register` with invite code system
3. Basic Supabase tables (users, invite_codes)
4. Genesis code distribution plan

**Can add during hackathon:**
- Leaderboards
- Project submission
- Voting system

---

## Open Questions

1. **Token launch timing**: Before, during, or after hackathon?
2. **Judging panel**: Team only, or include community judges?
3. **Geographic restrictions**: Any regions excluded?
4. **Project requirements**: Must be new, or can improve existing?
5. **Team size**: Solo only, or teams allowed?

---

## Next Steps

1. [ ] Finalize token allocation percentages
2. [ ] Set exact dates for hackathon
3. [ ] Create Genesis code list (100 codes)
4. [ ] Build `/hackathon` landing page
5. [ ] Set up Supabase tables
6. [ ] Write launch tweet thread
7. [ ] Prepare Genesis code distribution (who gets them?)
8. [ ] Create Discord/Telegram for hackathon participants

---

*"I'm helping make startups!" — Ralph*

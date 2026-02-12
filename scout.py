#!/usr/bin/env python3
"""
Soccer Player Scout - Psychological & Off-Field Behavior Analysis
The dumbest version that works. No libraries. No frameworks. Just stdlib.

Usage:
    python3 scout.py "Kylian Mbappe"
    python3 scout.py "Marcus Rashford" --days 30
    python3 scout.py "Neymar Jr" --json

Web UI:
    python3 scout_web.py          # opens http://localhost:8888

Scheduler:
    python3 scout_scheduler.py    # runs watchlist once
    python3 scout_scheduler.py --daemon  # runs every morning
"""

import sys
import os
import json
import re
import uuid
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from html import unescape
from datetime import datetime, timedelta
from collections import Counter
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent.resolve()
LOG_DIR = SCRIPT_DIR / "scout_logs"
RUNS_DIR = LOG_DIR / "runs"
AUDIT_LOG = LOG_DIR / "audit.jsonl"
ERROR_LOG = LOG_DIR / "errors.log"
WATCHLIST_FILE = SCRIPT_DIR / "watchlist.json"


# ─── Logging ──────────────────────────────────────────────────────────────────
# Every run, every result, every failure. Full audit trail.

def _ensure_dirs():
    LOG_DIR.mkdir(exist_ok=True)
    RUNS_DIR.mkdir(exist_ok=True)


def log_run(entry):
    """Append one JSON line to audit.jsonl and save full run to runs/."""
    _ensure_dirs()

    # Append to audit trail (one line per run)
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")

    # Save full run file
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", entry.get("player", "unknown"))
    ts = entry.get("timestamp", datetime.now().isoformat()).replace(":", "-")
    run_file = RUNS_DIR / f"{ts}_{safe_name}.json"
    with open(run_file, "w") as f:
        json.dump(entry, f, indent=2, default=str)

    return str(run_file)


def log_error(error_msg, player="unknown", context=""):
    """Log errors to errors.log."""
    _ensure_dirs()
    ts = datetime.now().isoformat()
    with open(ERROR_LOG, "a") as f:
        f.write(f"[{ts}] player={player} | {error_msg} | {context}\n")


def get_recent_logs(limit=50):
    """Read last N entries from audit.jsonl."""
    if not AUDIT_LOG.exists():
        return []
    lines = AUDIT_LOG.read_text().strip().split("\n")
    entries = []
    for line in lines[-limit:]:
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return entries


# ─── Keyword Dictionaries ────────────────────────────────────────────────────
# These are the "AI". Just word matching. Dumb but works.

RED_FLAGS = {
    "legal_trouble": [
        "arrest", "arrested", "charged", "lawsuit", "court", "police",
        "investigation", "allegations", "accused", "indicted", "trial",
        "convicted", "sentence", "jail", "prison", "bail", "probation",
        "restraining order", "domestic", "assault", "battery", "dui", "dwi",
    ],
    "discipline_issues": [
        "suspended", "suspension", "red card", "banned", "fine", "fined",
        "misconduct", "expelled", "benched", "dropped", "axed",
        "missed training", "no-show", "AWOL", "breach",
        "code of conduct", "violation", "punishment",
    ],
    "attitude_problems": [
        "tantrum", "outburst", "confrontation", "argument",
        "refuse", "refused", "stormed off", "walked out", "angry",
        "furious", "frustrated", "unhappy", "disgruntled", "sulk",
        "diva", "ego", "arrogant", "selfish", "toxic", "petulant",
        "disrespect", "rant", "lash out", "blasted",
    ],
    "substance_issues": [
        "drunk", "alcohol", "drug", "drugs", "substance", "cocaine",
        "cannabis", "marijuana", "failed test", "doping",
        "rehabilitation", "rehab", "addiction", "nightclub",
        "partying", "gambling",
    ],
    "relationship_drama": [
        "divorce", "breakup", "affair", "cheating", "scandal",
        "controversy", "leaked", "sex tape", "paternity",
        "custody", "infidelity",
    ],
}

GREEN_FLAGS = {
    "leadership": [
        "captain", "leader", "mentor", "role model", "influence",
        "vocal", "inspires", "motivate", "rally", "team-first",
        "selfless", "example", "respected", "trust",
    ],
    "professionalism": [
        "professional", "dedicated", "committed", "work ethic", "discipline",
        "focused", "determined", "consistent", "reliable", "humble",
        "grounded", "mature", "composed", "calm", "level-headed",
    ],
    "community": [
        "charity", "foundation", "donate", "donation", "volunteer",
        "community", "school", "hospital", "children", "youth",
        "campaign", "ambassador", "awareness", "philanthrop",
        "gives back", "helping", "fundrais",
    ],
    "mental_strength": [
        "resilient", "comeback", "bounced back", "overcame", "adversity",
        "mental health", "therapy", "wellbeing", "mindset", "tough",
        "pressure", "clutch", "big game", "steps up",
    ],
    "growth_mindset": [
        "improve", "learning", "studying", "extra training", "development",
        "growth", "progress", "adapting", "evolving", "working on",
        "added to his game", "new skill", "versatile",
    ],
}

CONTEXT_CLUES = {
    "transfer_noise": [
        "transfer", "move", "linked", "bid", "offer", "target",
        "wants", "interested", "swap", "deal", "contract", "wages",
        "salary", "release clause", "free agent", "loan",
    ],
    "injury": [
        "injury", "injured", "sidelined", "surgery", "operation",
        "recovery", "fitness", "setback", "hamstring",
        "knee", "ankle", "muscle", "torn", "fracture", "out for",
    ],
}

# Words that mean an article is about a match, not off-field behavior.
# Used by the cheap tier to filter false positives.
MATCH_CONTEXT = [
    "match", "game", "fixture", "derby", "final", "semifinal",
    "semi-final", "quarter-final", "quarterfinal", "round of",
    "first leg", "second leg", "minute", "half-time", "halftime",
    "goal", "assist", "header", "penalty", "free kick", "corner",
    "offside", "var", "referee", "substitut", "lineup", "squad",
    "kickoff", "kick-off", "pre-season", "friendly", "vs", "versus",
    "copa del rey", "champions league", "premier league", "la liga",
    "serie a", "bundesliga", "ligue 1", "europa league", "world cup",
    "euro 2", "fa cup", "carabao", "league cup",
]

# Keywords that are high-confidence OFF-field (not match context)
CONFIRMED_OFF_FIELD = [
    "arrest", "arrested", "jail", "prison", "court appearance",
    "nightclub", "drunk driving", "dui", "dwi", "cocaine",
    "sex tape", "paternity", "divorce", "domestic violence",
    "restraining order", "gambling debt", "rehab", "addiction",
]


# ─── News Fetching ────────────────────────────────────────────────────────────

def fetch_news(player_name, days=14):
    """Fetch news from Google News RSS. Free. No API key. Works."""
    query = urllib.parse.quote(f'"{player_name}" soccer OR football')
    url = f"https://news.google.com/rss/search?q={query}&hl=en&gl=US&ceid=US:en"

    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; SoccerScout/1.0)"
    })

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read().decode("utf-8")
    except Exception as e:
        log_error(str(e), player_name, "fetch_news")
        return []

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        log_error(str(e), player_name, "parse_rss")
        return []

    articles = []
    cutoff = datetime.now() - timedelta(days=days)

    for item in root.iter("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        pubdate_el = item.find("pubDate")
        desc_el = item.find("description")

        title = unescape(title_el.text) if title_el is not None and title_el.text else ""
        link = link_el.text if link_el is not None and link_el.text else ""
        desc = unescape(desc_el.text) if desc_el is not None and desc_el.text else ""
        pubdate_str = pubdate_el.text if pubdate_el is not None and pubdate_el.text else ""

        desc = re.sub(r"<[^>]+>", " ", desc)
        desc = re.sub(r"\s+", " ", desc).strip()

        pub_date = None
        if pubdate_str:
            try:
                pub_date = datetime.strptime(
                    re.sub(r"\s+\w+$", "", pubdate_str),
                    "%a, %d %b %Y %H:%M:%S"
                )
            except ValueError:
                pub_date = None

        if pub_date and pub_date < cutoff:
            continue

        articles.append({
            "title": title,
            "link": link,
            "description": desc,
            "date": pub_date.strftime("%Y-%m-%d") if pub_date else "unknown",
        })

    return articles


# ─── Tiered Analysis ─────────────────────────────────────────────────────────
#
# COST MODEL:
#   FREE  tier = keyword matching. Runs on everything. Zero cost.
#   CHEAP tier = heuristic rules. Filters false positives. Still free compute.
#   EXPENSIVE tier = flags items for human review. Costs human attention.
#
# The idea: don't waste expensive judgment on things cheap logic can handle.

def free_tier_analyze(article):
    """
    FREE TIER: Raw keyword matching against all dictionaries.
    Runs on every single article. No filtering, just detection.
    """
    text = f"{article['title']} {article['description']}".lower()
    findings = {"red": {}, "green": {}, "context": {}}

    for category, keywords in RED_FLAGS.items():
        hits = [kw for kw in keywords if kw.lower() in text]
        if hits:
            findings["red"][category] = hits

    for category, keywords in GREEN_FLAGS.items():
        hits = [kw for kw in keywords if kw.lower() in text]
        if hits:
            findings["green"][category] = hits

    for category, keywords in CONTEXT_CLUES.items():
        hits = [kw for kw in keywords if kw.lower() in text]
        if hits:
            findings["context"][category] = hits

    return findings


def cheap_tier_filter(article, raw_findings):
    """
    CHEAP TIER: Heuristic rules that filter out false positives.
    Still zero-cost compute, but smarter than raw keyword matching.

    Fixes the problem where "clash" in "Copa del Rey clash" triggers
    attitude_problems, or "suspended" in "match suspended due to rain".
    """
    text = f"{article['title']} {article['description']}".lower()
    filtered = {"red": {}, "green": raw_findings["green"], "context": raw_findings["context"]}

    # Count how many match-context words appear
    match_words = sum(1 for mw in MATCH_CONTEXT if mw in text)
    is_match_article = match_words >= 2  # 2+ match words = probably about a game

    for category, hits in raw_findings["red"].items():
        surviving_hits = []
        for kw in hits:
            # Rule 1: If the keyword is a confirmed off-field term, always keep it
            if kw in CONFIRMED_OFF_FIELD:
                surviving_hits.append(kw)
                continue

            # Rule 2: If it's a match article, filter out ambiguous keywords
            if is_match_article and kw in (
                "clash", "clash with", "ban", "banned", "dropped", "axed",
                "benched", "suspended", "late", "frustrated", "unhappy",
                "angry", "blasted", "party", "united",
            ):
                continue  # likely match context, not off-field

            # Rule 3: "rehabilitation" / "rehab" near "injury" = medical, not substance
            if kw in ("rehab", "rehabilitation") and "injury" in raw_findings.get("context", {}):
                continue

            surviving_hits.append(kw)

        if surviving_hits:
            filtered["red"][category] = surviving_hits

    return filtered


def expensive_tier_flag(player_name, articles, all_findings, score):
    """
    EXPENSIVE TIER: Flags items that need human eyeballs.
    This doesn't cost compute — it costs human attention.
    Only triggered when cheap-tier confidence is low.

    Returns a list of items that need manual review.
    """
    review_items = []

    # Flag 1: High score but few articles — could be noise
    if score >= 5 and len(articles) < 5:
        review_items.append({
            "reason": "HIGH_SCORE_LOW_DATA",
            "detail": f"Risk score {score}/10 but only {len(articles)} articles. Small sample = unreliable.",
            "action": "Manually verify flagged articles. Increase --days to get more data.",
        })

    # Flag 2: Contradictory signals — red AND green in same run
    total_red = sum(len(h) for f in all_findings for h in f["red"].values())
    total_green = sum(len(h) for f in all_findings for h in f["green"].values())
    if total_red >= 3 and total_green >= 5:
        review_items.append({
            "reason": "CONTRADICTORY_SIGNALS",
            "detail": f"{total_red} red hits + {total_green} green hits. Mixed picture.",
            "action": "Read flagged articles yourself. Keyword matching can't judge nuance.",
        })

    # Flag 3: Single category dominating red flags
    cat_counts = Counter()
    for f in all_findings:
        for cat in f["red"]:
            cat_counts[cat] += 1
    if cat_counts:
        top_cat, top_count = cat_counts.most_common(1)[0]
        total_flagged = sum(cat_counts.values())
        if total_flagged >= 3 and top_count / total_flagged > 0.8:
            review_items.append({
                "reason": "SINGLE_CATEGORY_DOMINANCE",
                "detail": f"'{top_cat}' is {top_count}/{total_flagged} of all red flags. Could be one story repeated.",
                "action": "Check if multiple articles are about the same incident.",
            })

    # Flag 4: All dates are the same — news burst about one event
    dates = [a["date"] for a in articles if a["date"] != "unknown"]
    if dates:
        unique_dates = set(dates)
        if len(unique_dates) <= 2 and len(dates) >= 5:
            review_items.append({
                "reason": "NEWS_BURST",
                "detail": f"All {len(dates)} articles from {len(unique_dates)} date(s). Likely one event amplified.",
                "action": "Verify this is multiple incidents, not one story echoed across outlets.",
            })

    return review_items


# ─── Self-Check / Audit ──────────────────────────────────────────────────────
# After every run, audit the output. If something looks off, log it.

def self_check(player_name, articles, all_findings, score):
    """
    Post-run audit. Checks output quality and flags problems.
    Returns dict with issues found and suggested fixes.
    """
    issues = []
    suggestions = []
    confidence = 1.0  # starts at 100%, each issue reduces it

    # Check 1: No articles found
    if not articles:
        issues.append("ZERO_ARTICLES: No news found for this player.")
        suggestions.append("Try alternate name spellings, add nationality, or increase --days.")
        confidence -= 0.5

    # Check 2: Very few articles
    elif len(articles) < 3:
        issues.append(f"LOW_COVERAGE: Only {len(articles)} articles. Thin dataset.")
        suggestions.append("Increase --days to 60 or 90 for more data. Or player may be low-profile.")
        confidence -= 0.2

    # Check 3: Risk score at extremes
    if score == 0 and len(articles) > 10:
        issues.append("PERFECT_ZERO: Score is 0 with many articles. Possibly under-detecting.")
        suggestions.append("Review keyword dictionaries. Player may use different name in media.")
        confidence -= 0.1

    if score == 10:
        issues.append("MAX_SCORE: Risk pegged at 10/10. Could be noise or genuinely bad.")
        suggestions.append("Manual review critical. Check if multiple incidents or one amplified story.")
        confidence -= 0.15

    # Check 4: All articles from same source
    if articles:
        sources = set()
        for a in articles:
            # Extract domain-ish from title suffix (Google News format: "Title - Source")
            parts = a["title"].rsplit(" - ", 1)
            if len(parts) == 2:
                sources.add(parts[1].strip().lower())
        if len(sources) == 1 and len(articles) > 3:
            issues.append(f"SINGLE_SOURCE: All articles from one outlet ({sources.pop()}). Echo chamber risk.")
            suggestions.append("Cross-reference with other search queries or news sources.")
            confidence -= 0.2

    # Check 5: Stale data
    if articles:
        dates = [a["date"] for a in articles if a["date"] != "unknown"]
        if dates:
            newest = max(dates)
            try:
                newest_dt = datetime.strptime(newest, "%Y-%m-%d")
                days_old = (datetime.now() - newest_dt).days
                if days_old > 7:
                    issues.append(f"STALE_DATA: Newest article is {days_old} days old.")
                    suggestions.append("Recent news may not be indexed yet. Re-run in a day or two.")
                    confidence -= 0.1
            except ValueError:
                pass

    # Check 6: Keyword saturation (one keyword triggering everywhere)
    kw_counts = Counter()
    for f in all_findings:
        for hits in f["red"].values():
            for kw in hits:
                kw_counts[kw] += 1
    if kw_counts:
        top_kw, top_count = kw_counts.most_common(1)[0]
        if top_count > len(articles) * 0.5 and top_count >= 3:
            issues.append(f"KEYWORD_SATURATION: '{top_kw}' matched in {top_count}/{len(articles)} articles.")
            suggestions.append(f"'{top_kw}' may be too generic. Consider if it's genuinely off-field.")
            confidence -= 0.1

    # Check 7: Green flags unrealistically high
    total_green = sum(len(h) for f in all_findings for h in f["green"].values())
    if total_green > len(articles) * 3:
        issues.append(f"GREEN_INFLATION: {total_green} green hits from {len(articles)} articles. PR puff?")
        suggestions.append("High green flag count may indicate PR-driven coverage, not reality.")
        confidence -= 0.05

    confidence = max(0.0, min(1.0, confidence))

    return {
        "issues": issues,
        "suggestions": suggestions,
        "confidence": round(confidence, 2),
        "passed": len(issues) == 0,
    }


# ─── Scoring ──────────────────────────────────────────────────────────────────

def compute_risk_score(all_findings):
    red_count = sum(
        len(hits)
        for f in all_findings
        for hits in f["red"].values()
    )
    green_count = sum(
        len(hits)
        for f in all_findings
        for hits in f["green"].values()
    )
    raw = (red_count * 2) - (green_count * 1)
    return max(0, min(10, raw))


def categorize_risk(score):
    if score <= 2:
        return "LOW RISK"
    elif score <= 5:
        return "MODERATE RISK"
    elif score <= 7:
        return "ELEVATED RISK"
    else:
        return "HIGH RISK"


# ─── Report Generation ────────────────────────────────────────────────────────

def generate_report(player_name, articles, all_findings, score, audit, review_items):
    risk_label = categorize_risk(score)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append("=" * 70)
    lines.append("  SOCCER PLAYER SCOUTING REPORT - OFF-FIELD ANALYSIS")
    lines.append("=" * 70)
    lines.append(f"  Player:       {player_name}")
    lines.append(f"  Generated:    {now}")
    lines.append(f"  Articles:     {len(articles)} found")
    lines.append(f"  Risk Score:   {score}/10 ({risk_label})")
    lines.append(f"  Confidence:   {int(audit['confidence'] * 100)}%")
    lines.append("=" * 70)

    # Aggregate
    red_agg = Counter()
    green_agg = Counter()
    context_agg = Counter()
    flagged_articles = []

    for article, findings in zip(articles, all_findings):
        for cat in findings["red"]:
            red_agg[cat] += 1
        for cat in findings["green"]:
            green_agg[cat] += 1
        for cat in findings["context"]:
            context_agg[cat] += 1
        if findings["red"]:
            flagged_articles.append((article, findings))

    # Red Flags
    lines.append("")
    lines.append("RED FLAGS")
    lines.append("-" * 40)
    if red_agg:
        for cat, count in red_agg.most_common():
            label = cat.replace("_", " ").title()
            bar = "#" * count
            lines.append(f"  {label:.<30} {count:>3}x  {bar}")
    else:
        lines.append("  None found. Clean record in recent news.")

    # Green Flags
    lines.append("")
    lines.append("GREEN FLAGS")
    lines.append("-" * 40)
    if green_agg:
        for cat, count in green_agg.most_common():
            label = cat.replace("_", " ").title()
            bar = "+" * count
            lines.append(f"  {label:.<30} {count:>3}x  {bar}")
    else:
        lines.append("  No positive signals detected.")

    # Context
    lines.append("")
    lines.append("CONTEXT (not flags, just noise)")
    lines.append("-" * 40)
    if context_agg:
        for cat, count in context_agg.most_common():
            label = cat.replace("_", " ").title()
            lines.append(f"  {label:.<30} {count:>3}x")
    else:
        lines.append("  Quiet period.")

    # Flagged Articles
    lines.append("")
    lines.append("FLAGGED ARTICLES (red flags detected)")
    lines.append("-" * 40)
    if flagged_articles:
        for article, findings in flagged_articles[:15]:
            lines.append(f"  [{article['date']}] {article['title'][:80]}")
            for cat, hits in findings["red"].items():
                label = cat.replace("_", " ").title()
                lines.append(f"    >> {label}: {', '.join(hits)}")
            lines.append(f"    {article['link']}")
            lines.append("")
    else:
        lines.append("  No articles with red flags.")

    # Recent Headlines
    lines.append("")
    lines.append("RECENT HEADLINES (all)")
    lines.append("-" * 40)
    for i, article in enumerate(articles[:20]):
        marker = " "
        if all_findings[i]["red"]:
            marker = "!"
        elif all_findings[i]["green"]:
            marker = "+"
        lines.append(f"  [{marker}] [{article['date']}] {article['title'][:75]}")

    # Self-Check Results
    lines.append("")
    lines.append("=" * 70)
    lines.append("SELF-CHECK AUDIT")
    lines.append("=" * 70)
    if audit["passed"]:
        lines.append("  All checks passed. Output looks reliable.")
    else:
        for issue, suggestion in zip(audit["issues"], audit["suggestions"]):
            lines.append(f"  [ISSUE]  {issue}")
            lines.append(f"  [FIX]    {suggestion}")
            lines.append("")

    # Human Review Items (expensive tier)
    if review_items:
        lines.append("")
        lines.append("NEEDS HUMAN REVIEW (expensive tier)")
        lines.append("-" * 40)
        for item in review_items:
            lines.append(f"  [{item['reason']}]")
            lines.append(f"    {item['detail']}")
            lines.append(f"    -> {item['action']}")
            lines.append("")

    # Assessment
    lines.append("")
    lines.append("=" * 70)
    lines.append("ASSESSMENT")
    lines.append("=" * 70)

    if score <= 2:
        lines.append("  Clean profile. No significant off-field concerns detected")
        lines.append("  in recent coverage. Proceed with standard due diligence.")
    elif score <= 5:
        lines.append("  Some signals worth monitoring. Review flagged articles.")
        lines.append("  Recommend: background check + character references from")
        lines.append("  coaches and teammates before proceeding.")
    elif score <= 7:
        lines.append("  Multiple concerning signals detected. Elevated risk profile.")
        lines.append("  Recommend: thorough background investigation, interview with")
        lines.append("  player's inner circle, review of club disciplinary records.")
    else:
        lines.append("  Significant off-field concerns. High risk profile.")
        lines.append("  Recommend: full investigation before any transfer action.")
        lines.append("  Consider: morality clause, behavioral benchmarks in contract.")

    lines.append("")
    lines.append("-" * 70)
    lines.append("  NOTE: This is keyword-based analysis of public news only.")
    lines.append("  Not a substitute for professional background investigation.")
    lines.append("-" * 70)

    return "\n".join(lines)


# ─── Core Runner ──────────────────────────────────────────────────────────────
# This is what everything calls: CLI, web UI, scheduler.

def run_scout(player_name, days=14, trigger="manual"):
    """
    Run the full scouting pipeline. Returns a complete result dict.
    Everything is logged automatically.
    """
    run_id = str(uuid.uuid4())[:8]
    start = time.time()
    errors = []

    # Step 1: Fetch (FREE - uses Google News RSS, no API cost)
    articles = fetch_news(player_name, days=days)
    if not articles:
        errors.append("No articles found")

    # Step 2: FREE tier — raw keyword scan on every article
    raw_findings = [free_tier_analyze(a) for a in articles]

    # Step 3: CHEAP tier — filter false positives with heuristics
    filtered_findings = [
        cheap_tier_filter(a, raw)
        for a, raw in zip(articles, raw_findings)
    ]

    # Step 4: Score (FREE — just arithmetic)
    score = compute_risk_score(filtered_findings)

    # Step 5: Self-check (CHEAP — rule-based audit)
    audit = self_check(player_name, articles, filtered_findings, score)

    # Step 6: EXPENSIVE tier — flag items needing human review
    review_items = expensive_tier_flag(player_name, articles, filtered_findings, score)

    # Step 7: Generate report
    report = generate_report(player_name, articles, filtered_findings, score, audit, review_items)

    duration_ms = int((time.time() - start) * 1000)

    # Aggregate flags for log
    red_agg = {}
    green_agg = {}
    for f in filtered_findings:
        for cat, hits in f["red"].items():
            red_agg.setdefault(cat, []).extend(hits)
        for cat, hits in f["green"].items():
            green_agg.setdefault(cat, []).extend(hits)
    for cat in red_agg:
        red_agg[cat] = list(set(red_agg[cat]))
    for cat in green_agg:
        green_agg[cat] = list(set(green_agg[cat]))

    # Build log entry
    log_entry = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "player": player_name,
        "trigger": trigger,
        "days": days,
        "articles_found": len(articles),
        "risk_score": score,
        "risk_label": categorize_risk(score),
        "red_flags": red_agg,
        "green_flags": green_agg,
        "self_check": audit,
        "review_items": review_items,
        "duration_ms": duration_ms,
        "errors": errors,
        "tiers": {
            "free": "keyword_matching",
            "cheap": "false_positive_filter",
            "expensive": f"{len(review_items)} items flagged for human review",
        },
    }

    # Log it
    run_file = log_run(log_entry)

    return {
        "run_id": run_id,
        "report": report,
        "log": log_entry,
        "log_file": run_file,
    }


# ─── Watchlist ────────────────────────────────────────────────────────────────

def load_watchlist():
    if WATCHLIST_FILE.exists():
        return json.loads(WATCHLIST_FILE.read_text())
    return {"players": [], "settings": {"days": 14}}


def save_watchlist(data):
    WATCHLIST_FILE.write_text(json.dumps(data, indent=2))


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    player_name = sys.argv[1]
    days = 14
    output_json = False

    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == "--days" and i + 1 < len(sys.argv):
            try:
                days = int(sys.argv[i + 1])
            except ValueError:
                pass
        if arg == "--json":
            output_json = True

    print(f"[*] Scouting: {player_name}")
    print(f"[*] Looking back: {days} days")
    print(f"[*] Fetching news...")

    result = run_scout(player_name, days=days, trigger="cli")

    if not result["log"]["articles_found"]:
        print("[!] No articles found. Try a different name or longer --days.")
        sys.exit(1)

    if output_json:
        print(json.dumps(result["log"], indent=2, default=str))
    else:
        print()
        print(result["report"])

    print(f"\n[*] Logged to: {result['log_file']}")
    print(f"[*] Run ID: {result['run_id']}")


if __name__ == "__main__":
    main()

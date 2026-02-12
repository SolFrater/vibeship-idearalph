#!/usr/bin/env python3
"""
Soccer Player Scout - Psychological & Off-Field Behavior Analysis
The dumbest version that works. No libraries. No frameworks. Just stdlib.

Usage:
    python3 scout.py "Kylian Mbappe"
    python3 scout.py "Marcus Rashford" --days 30
    python3 scout.py "Neymar Jr" --json
"""

import sys
import json
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from html import unescape
from datetime import datetime, timedelta
from collections import Counter

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
        "late", "missed training", "no-show", "AWOL", "breach",
        "code of conduct", "violation", "punishment",
    ],
    "attitude_problems": [
        "tantrum", "outburst", "confrontation", "argument", "clash",
        "refuse", "refused", "stormed off", "walked out", "angry",
        "furious", "frustrated", "unhappy", "disgruntled", "sulk",
        "diva", "ego", "arrogant", "selfish", "toxic", "petulant",
        "disrespect", "rant", "lash out", "blasted",
    ],
    "substance_issues": [
        "drunk", "alcohol", "drug", "drugs", "substance", "cocaine",
        "cannabis", "marijuana", "failed test", "doping", "ban",
        "rehabilitation", "rehab", "addiction", "nightclub", "party",
        "partying", "gambling",
    ],
    "relationship_drama": [
        "divorce", "breakup", "affair", "cheating", "scandal",
        "controversy", "leaked", "sex tape", "paternity",
        "custody", "infidelity", "wag",
    ],
}

GREEN_FLAGS = {
    "leadership": [
        "captain", "leader", "mentor", "role model", "influence",
        "vocal", "inspires", "motivate", "rally", "united", "team-first",
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
        "recovery", "rehab", "fitness", "setback", "hamstring",
        "knee", "ankle", "muscle", "torn", "fracture", "out for",
    ],
}


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
        print(f"[!] Failed to fetch news: {e}")
        return []

    # Parse RSS XML
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"[!] Failed to parse RSS: {e}")
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

        # Strip HTML from description
        desc = re.sub(r"<[^>]+>", " ", desc)
        desc = re.sub(r"\s+", " ", desc).strip()

        # Parse date (RFC 2822 format from RSS)
        pub_date = None
        if pubdate_str:
            try:
                # "Mon, 10 Feb 2025 14:30:00 GMT"
                pub_date = datetime.strptime(
                    re.sub(r"\s+\w+$", "", pubdate_str),  # strip timezone
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


# ─── Analysis Engine ──────────────────────────────────────────────────────────

def analyze_article(article):
    """Scan one article for red flags, green flags, and context."""
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


def compute_risk_score(all_findings):
    """
    Simple risk score. Higher = more concerning.
    Scale: 0-10. Just counts weighted keyword hits.
    """
    red_count = sum(
        len(hits)
        for article_findings in all_findings
        for hits in article_findings["red"].values()
    )
    green_count = sum(
        len(hits)
        for article_findings in all_findings
        for hits in article_findings["green"].values()
    )

    # Weighted: red flags weigh more than green flags reduce
    raw = (red_count * 2) - (green_count * 1)
    # Clamp to 0-10
    score = max(0, min(10, raw))
    return score


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

def generate_report(player_name, articles, all_findings, score):
    """Generate a plain text scouting report."""
    risk_label = categorize_risk(score)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append("=" * 70)
    lines.append(f"  SOCCER PLAYER SCOUTING REPORT - OFF-FIELD ANALYSIS")
    lines.append("=" * 70)
    lines.append(f"  Player:       {player_name}")
    lines.append(f"  Generated:    {now}")
    lines.append(f"  Articles:     {len(articles)} found")
    lines.append(f"  Risk Score:   {score}/10 ({risk_label})")
    lines.append("=" * 70)

    # Aggregate all red flags
    red_agg = Counter()
    green_agg = Counter()
    context_agg = Counter()

    flagged_articles = []

    for i, (article, findings) in enumerate(zip(articles, all_findings)):
        for cat in findings["red"]:
            red_agg[cat] += 1
        for cat in findings["green"]:
            green_agg[cat] += 1
        for cat in findings["context"]:
            context_agg[cat] += 1
        if findings["red"]:
            flagged_articles.append((article, findings))

    # ── Red Flags Summary ──
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

    # ── Green Flags Summary ──
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

    # ── Context ──
    lines.append("")
    lines.append("CONTEXT (not flags, just noise)")
    lines.append("-" * 40)
    if context_agg:
        for cat, count in context_agg.most_common():
            label = cat.replace("_", " ").title()
            lines.append(f"  {label:.<30} {count:>3}x")
    else:
        lines.append("  Quiet period.")

    # ── Flagged Articles ──
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

    # ── Recent Headlines ──
    lines.append("")
    lines.append("RECENT HEADLINES (all)")
    lines.append("-" * 40)
    for article in articles[:20]:
        marker = " "
        findings = all_findings[articles.index(article)]
        if findings["red"]:
            marker = "!"
        elif findings["green"]:
            marker = "+"
        lines.append(f"  [{marker}] [{article['date']}] {article['title'][:75]}")

    # ── Assessment ──
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


def generate_json_report(player_name, articles, all_findings, score):
    """Generate structured JSON output."""
    red_agg = {}
    green_agg = {}

    for findings in all_findings:
        for cat, hits in findings["red"].items():
            red_agg.setdefault(cat, []).extend(hits)
        for cat, hits in findings["green"].items():
            green_agg.setdefault(cat, []).extend(hits)

    # Deduplicate keyword lists
    for cat in red_agg:
        red_agg[cat] = list(set(red_agg[cat]))
    for cat in green_agg:
        green_agg[cat] = list(set(green_agg[cat]))

    flagged = []
    for article, findings in zip(articles, all_findings):
        if findings["red"]:
            flagged.append({
                "title": article["title"],
                "date": article["date"],
                "link": article["link"],
                "red_flags": findings["red"],
            })

    return json.dumps({
        "player": player_name,
        "generated": datetime.now().isoformat(),
        "articles_found": len(articles),
        "risk_score": score,
        "risk_label": categorize_risk(score),
        "red_flags": red_agg,
        "green_flags": green_agg,
        "flagged_articles": flagged[:15],
    }, indent=2)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    player_name = sys.argv[1]
    days = 14
    output_json = False

    # Parse args the dumb way
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

    articles = fetch_news(player_name, days=days)
    print(f"[*] Found {len(articles)} articles")

    if not articles:
        print("[!] No articles found. Try a different player name or longer time window.")
        sys.exit(1)

    print(f"[*] Analyzing for behavioral signals...")

    all_findings = [analyze_article(a) for a in articles]
    score = compute_risk_score(all_findings)

    if output_json:
        print(generate_json_report(player_name, articles, all_findings, score))
    else:
        print()
        print(generate_report(player_name, articles, all_findings, score))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Soccer Player Scout - Web UI
Uses Python's built-in http.server. No Flask. No Django. No npm. Just stdlib.

Usage:
    python3 scout_web.py              # http://localhost:8888
    python3 scout_web.py --port 9000  # http://localhost:9000
"""

import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from scout import run_scout, load_watchlist, save_watchlist, get_recent_logs

PORT = 8888

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Soccer Player Scout</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Courier New', monospace;
    background: #0a0e17; color: #c8d6e5;
    min-height: 100vh;
}
.header {
    background: #131a2b; border-bottom: 2px solid #1e3a5f;
    padding: 20px 30px; display: flex; align-items: center; gap: 20px;
}
.header h1 { color: #00d4aa; font-size: 22px; }
.header span { color: #5a6e82; font-size: 13px; }
.container { display: flex; height: calc(100vh - 72px); }

/* Sidebar */
.sidebar {
    width: 280px; background: #0f1623; border-right: 1px solid #1e3a5f;
    display: flex; flex-direction: column; flex-shrink: 0;
}
.sidebar h2 {
    padding: 16px 20px 10px; font-size: 13px; color: #5a6e82;
    text-transform: uppercase; letter-spacing: 1px;
}
.add-player {
    display: flex; padding: 0 12px 12px; gap: 6px;
}
.add-player input {
    flex: 1; background: #131a2b; border: 1px solid #1e3a5f;
    color: #c8d6e5; padding: 8px 10px; border-radius: 4px;
    font-family: inherit; font-size: 13px;
}
.add-player button {
    background: #00d4aa; color: #0a0e17; border: none;
    padding: 8px 12px; border-radius: 4px; cursor: pointer;
    font-weight: bold; font-family: inherit;
}
.player-list { flex: 1; overflow-y: auto; }
.player-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 20px; cursor: pointer; border-bottom: 1px solid #131a2b;
    transition: background 0.15s;
}
.player-item:hover { background: #131a2b; }
.player-item.active { background: #1a2744; border-left: 3px solid #00d4aa; }
.player-item .name { font-size: 14px; }
.player-item .score {
    font-size: 12px; padding: 2px 8px; border-radius: 10px;
    font-weight: bold;
}
.score-low { background: #0a3622; color: #00d4aa; }
.score-mod { background: #3a3000; color: #ffd700; }
.score-high { background: #3a1010; color: #ff4444; }
.player-item .remove {
    color: #3a4050; cursor: pointer; font-size: 16px; margin-left: 8px;
}
.player-item .remove:hover { color: #ff4444; }

/* Main area */
.main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.search-bar {
    display: flex; padding: 16px 20px; gap: 10px;
    background: #0f1623; border-bottom: 1px solid #1e3a5f;
}
.search-bar input {
    flex: 1; background: #131a2b; border: 1px solid #1e3a5f;
    color: #c8d6e5; padding: 10px 14px; border-radius: 6px;
    font-family: inherit; font-size: 14px;
}
.search-bar input::placeholder { color: #3a4a5c; }
.search-bar select {
    background: #131a2b; border: 1px solid #1e3a5f;
    color: #c8d6e5; padding: 10px; border-radius: 6px;
    font-family: inherit;
}
.search-bar button {
    background: #00d4aa; color: #0a0e17; border: none;
    padding: 10px 24px; border-radius: 6px; cursor: pointer;
    font-weight: bold; font-family: inherit; font-size: 14px;
}
.search-bar button:hover { background: #00e8bb; }
.search-bar button:disabled { background: #1e3a5f; color: #3a4a5c; cursor: wait; }

/* Tabs */
.tabs {
    display: flex; background: #0f1623; border-bottom: 1px solid #1e3a5f;
}
.tab {
    padding: 10px 20px; cursor: pointer; font-size: 13px;
    color: #5a6e82; border-bottom: 2px solid transparent;
    transition: all 0.15s;
}
.tab:hover { color: #c8d6e5; }
.tab.active { color: #00d4aa; border-bottom-color: #00d4aa; }

/* Content */
.content { flex: 1; overflow-y: auto; padding: 20px; }
.report-output {
    white-space: pre-wrap; font-size: 13px; line-height: 1.6;
    color: #a0b0c0;
}
.empty-state {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; height: 100%; color: #2a3a4c;
}
.empty-state .icon { font-size: 48px; margin-bottom: 16px; }
.empty-state p { font-size: 15px; }

/* Logs */
.log-entry {
    padding: 12px 16px; border-bottom: 1px solid #131a2b;
    font-size: 13px; display: flex; gap: 16px; align-items: center;
}
.log-entry .ts { color: #3a4a5c; white-space: nowrap; }
.log-entry .player { color: #00d4aa; min-width: 140px; }
.log-entry .result { flex: 1; }
.log-entry .trigger {
    color: #5a6e82; font-size: 11px; background: #131a2b;
    padding: 2px 8px; border-radius: 8px;
}

/* Spinner */
.spinner {
    display: inline-block; width: 16px; height: 16px;
    border: 2px solid #1e3a5f; border-top-color: #00d4aa;
    border-radius: 50%; animation: spin 0.6s linear infinite;
    margin-right: 8px; vertical-align: middle;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e17; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
</style>
</head>
<body>

<div class="header">
    <h1>SOCCER SCOUT</h1>
    <span>Off-Field Behavior Analysis | Keyword + Heuristic Engine | All runs logged</span>
</div>

<div class="container">
    <!-- Sidebar: Watchlist -->
    <div class="sidebar">
        <h2>Watchlist</h2>
        <div class="add-player">
            <input type="text" id="addName" placeholder="Add player..." onkeydown="if(event.key==='Enter')addPlayer()">
            <button onclick="addPlayer()">+</button>
        </div>
        <div class="player-list" id="playerList"></div>
    </div>

    <!-- Main -->
    <div class="main">
        <div class="search-bar">
            <input type="text" id="scoutName" placeholder="Scout any player..." onkeydown="if(event.key==='Enter')scoutPlayer()">
            <select id="scoutDays">
                <option value="7">7 days</option>
                <option value="14" selected>14 days</option>
                <option value="30">30 days</option>
                <option value="60">60 days</option>
                <option value="90">90 days</option>
            </select>
            <button id="scoutBtn" onclick="scoutPlayer()">SCOUT</button>
        </div>

        <div class="tabs">
            <div class="tab active" data-tab="report" onclick="switchTab('report')">Report</div>
            <div class="tab" data-tab="audit" onclick="switchTab('audit')">Self-Check</div>
            <div class="tab" data-tab="logs" onclick="switchTab('logs')">Audit Logs</div>
        </div>

        <div class="content" id="content">
            <div class="empty-state" id="emptyState">
                <div class="icon">&#9917;</div>
                <p>Type a player name and hit SCOUT</p>
            </div>
            <div class="report-output" id="reportOutput" style="display:none"></div>
            <div id="auditOutput" style="display:none"></div>
            <div id="logsOutput" style="display:none"></div>
        </div>
    </div>
</div>

<script>
let currentResult = null;
let watchlist = { players: [], settings: { days: 14 } };

// ── API calls ──
async function api(method, path, body) {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    const r = await fetch(path, opts);
    return r.json();
}

// ── Scout a player ──
async function scoutPlayer() {
    const name = document.getElementById('scoutName').value.trim();
    if (!name) return;
    const days = parseInt(document.getElementById('scoutDays').value);
    const btn = document.getElementById('scoutBtn');

    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span>Scouting...';

    try {
        currentResult = await api('POST', '/api/scout', { player: name, days });
        showReport();
        switchTab('report');
    } catch(e) {
        document.getElementById('reportOutput').textContent = 'Error: ' + e.message;
        document.getElementById('reportOutput').style.display = 'block';
        document.getElementById('emptyState').style.display = 'none';
    }
    btn.disabled = false;
    btn.textContent = 'SCOUT';
}

// ── Display report ──
function showReport() {
    if (!currentResult) return;
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('reportOutput').textContent = currentResult.report;
    document.getElementById('reportOutput').style.display = 'block';
}

// ── Display audit ──
function showAudit() {
    const el = document.getElementById('auditOutput');
    if (!currentResult || !currentResult.log) {
        el.innerHTML = '<div class="empty-state"><p>Run a scout first to see self-check results</p></div>';
        el.style.display = 'block';
        return;
    }
    const sc = currentResult.log.self_check;
    const ri = currentResult.log.review_items || [];
    let html = '<div style="padding:8px">';
    html += '<h3 style="color:#00d4aa;margin-bottom:12px">Self-Check Audit</h3>';
    html += '<div style="margin-bottom:16px">';
    html += '<span style="font-size:36px;color:' + (sc.confidence >= 0.8 ? '#00d4aa' : sc.confidence >= 0.5 ? '#ffd700' : '#ff4444') + '">' + Math.round(sc.confidence * 100) + '%</span>';
    html += '<span style="color:#5a6e82;margin-left:8px">confidence</span>';
    html += '</div>';

    if (sc.passed) {
        html += '<div style="color:#00d4aa;padding:12px;background:#0a3622;border-radius:6px">All checks passed. Output looks reliable.</div>';
    } else {
        sc.issues.forEach((issue, i) => {
            html += '<div style="padding:12px;margin-bottom:8px;background:#1a1020;border-left:3px solid #ff4444;border-radius:4px">';
            html += '<div style="color:#ff4444;font-size:13px;margin-bottom:4px">' + issue + '</div>';
            html += '<div style="color:#5a6e82;font-size:12px">Fix: ' + sc.suggestions[i] + '</div>';
            html += '</div>';
        });
    }

    if (ri.length > 0) {
        html += '<h3 style="color:#ffd700;margin:20px 0 12px">Needs Human Review</h3>';
        ri.forEach(item => {
            html += '<div style="padding:12px;margin-bottom:8px;background:#2a2000;border-left:3px solid #ffd700;border-radius:4px">';
            html += '<div style="color:#ffd700;font-size:12px;margin-bottom:4px">' + item.reason + '</div>';
            html += '<div style="font-size:13px;margin-bottom:4px">' + item.detail + '</div>';
            html += '<div style="color:#5a6e82;font-size:12px">Action: ' + item.action + '</div>';
            html += '</div>';
        });
    }

    html += '<h3 style="color:#5a6e82;margin:20px 0 12px">Cost Tiers Used</h3>';
    const tiers = currentResult.log.tiers;
    html += '<div style="display:flex;gap:12px">';
    html += '<div style="flex:1;padding:12px;background:#131a2b;border-radius:6px;text-align:center">';
    html += '<div style="color:#00d4aa;font-size:11px">FREE</div><div style="font-size:12px;color:#5a6e82">' + tiers.free + '</div></div>';
    html += '<div style="flex:1;padding:12px;background:#131a2b;border-radius:6px;text-align:center">';
    html += '<div style="color:#ffd700;font-size:11px">CHEAP</div><div style="font-size:12px;color:#5a6e82">' + tiers.cheap + '</div></div>';
    html += '<div style="flex:1;padding:12px;background:#131a2b;border-radius:6px;text-align:center">';
    html += '<div style="color:#ff4444;font-size:11px">EXPENSIVE</div><div style="font-size:12px;color:#5a6e82">' + tiers.expensive + '</div></div>';
    html += '</div>';
    html += '</div>';
    el.innerHTML = html;
    el.style.display = 'block';
}

// ── Display logs ──
async function showLogs() {
    const el = document.getElementById('logsOutput');
    try {
        const logs = await api('GET', '/api/logs');
        if (!logs.length) {
            el.innerHTML = '<div class="empty-state"><p>No runs logged yet</p></div>';
            el.style.display = 'block';
            return;
        }
        let html = '';
        logs.reverse().forEach(log => {
            const ts = log.timestamp ? log.timestamp.substring(0, 16).replace('T', ' ') : '?';
            const sc = log.risk_score;
            const cls = sc <= 2 ? 'score-low' : sc <= 5 ? 'score-mod' : 'score-high';
            const conf = log.self_check ? Math.round(log.self_check.confidence * 100) + '%' : '?';
            html += '<div class="log-entry">';
            html += '<span class="ts">' + ts + '</span>';
            html += '<span class="player">' + (log.player || '?') + '</span>';
            html += '<span class="score ' + cls + '">' + sc + '/10</span>';
            html += '<span class="result">' + (log.risk_label || '') + ' | ' + (log.articles_found || 0) + ' articles | ' + conf + ' confidence | ' + (log.duration_ms || 0) + 'ms</span>';
            html += '<span class="trigger">' + (log.trigger || '?') + '</span>';
            html += '</div>';
        });
        el.innerHTML = html;
    } catch(e) {
        el.innerHTML = '<div style="color:#ff4444;padding:20px">Error loading logs: ' + e.message + '</div>';
    }
    el.style.display = 'block';
}

// ── Tab switching ──
function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('reportOutput').style.display = 'none';
    document.getElementById('auditOutput').style.display = 'none';
    document.getElementById('logsOutput').style.display = 'none';

    if (tab === 'report') { if (currentResult) showReport(); else document.getElementById('emptyState').style.display = 'flex'; }
    else if (tab === 'audit') showAudit();
    else if (tab === 'logs') showLogs();
}

// ── Watchlist ──
async function loadWatchlist() {
    watchlist = await api('GET', '/api/watchlist');
    renderWatchlist();
}

function renderWatchlist() {
    const el = document.getElementById('playerList');
    if (!watchlist.players || !watchlist.players.length) {
        el.innerHTML = '<div style="padding:20px;color:#2a3a4c;text-align:center;font-size:13px">No players yet.<br>Add one above.</div>';
        return;
    }
    el.innerHTML = watchlist.players.map((p, i) => {
        const name = typeof p === 'string' ? p : p.name;
        const score = typeof p === 'object' && p.last_score !== undefined ? p.last_score : null;
        const cls = score === null ? '' : score <= 2 ? 'score-low' : score <= 5 ? 'score-mod' : 'score-high';
        return '<div class="player-item" onclick="scoutFromList(\'' + name.replace(/'/g, "\\'") + '\')">' +
            '<span class="name">' + name + '</span>' +
            '<span>' + (score !== null ? '<span class="score ' + cls + '">' + score + '</span>' : '') +
            '<span class="remove" onclick="event.stopPropagation();removePlayer(' + i + ')">x</span></span>' +
            '</div>';
    }).join('');
}

async function addPlayer() {
    const input = document.getElementById('addName');
    const name = input.value.trim();
    if (!name) return;
    await api('POST', '/api/watchlist', { action: 'add', player: name });
    input.value = '';
    await loadWatchlist();
}

async function removePlayer(index) {
    await api('POST', '/api/watchlist', { action: 'remove', index });
    await loadWatchlist();
}

function scoutFromList(name) {
    document.getElementById('scoutName').value = name;
    scoutPlayer();
}

// ── Init ──
loadWatchlist();
</script>
</body>
</html>"""


class ScoutHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        # Quiet logs - just timestamp + path
        sys.stderr.write(f"[{self.log_date_time_string()}] {args[0]}\n")

    def _json(self, data, status=200):
        body = json.dumps(data, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, content):
        body = content.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length))

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path == "/" or path == "":
            self._html(HTML)

        elif path == "/api/watchlist":
            self._json(load_watchlist())

        elif path == "/api/logs":
            self._json(get_recent_logs(100))

        else:
            self.send_error(404)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path

        if path == "/api/scout":
            data = self._read_body()
            player = data.get("player", "").strip()
            days = int(data.get("days", 14))
            if not player:
                self._json({"error": "player name required"}, 400)
                return
            result = run_scout(player, days=days, trigger="web")
            # Update watchlist score if player is on it
            wl = load_watchlist()
            for i, p in enumerate(wl["players"]):
                name = p if isinstance(p, str) else p.get("name", "")
                if name.lower() == player.lower():
                    wl["players"][i] = {"name": name, "last_score": result["log"]["risk_score"]}
                    save_watchlist(wl)
                    break
            self._json(result)

        elif path == "/api/watchlist":
            data = self._read_body()
            wl = load_watchlist()
            action = data.get("action")

            if action == "add":
                name = data.get("player", "").strip()
                if name:
                    # Don't duplicate
                    existing = [
                        (p if isinstance(p, str) else p.get("name", "")).lower()
                        for p in wl["players"]
                    ]
                    if name.lower() not in existing:
                        wl["players"].append({"name": name, "last_score": None})
                        save_watchlist(wl)
            elif action == "remove":
                idx = data.get("index")
                if isinstance(idx, int) and 0 <= idx < len(wl["players"]):
                    wl["players"].pop(idx)
                    save_watchlist(wl)

            self._json(wl)

        else:
            self.send_error(404)


def main():
    port = PORT
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--port" and i + 1 < len(sys.argv):
            try:
                port = int(sys.argv[i + 1])
            except ValueError:
                pass

    server = HTTPServer(("0.0.0.0", port), ScoutHandler)
    print(f"[*] Soccer Scout Web UI running at http://localhost:{port}")
    print(f"[*] Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate the icon-based triage architecture SVG (diagram tooling only, not app code)."""
import html
import os
import json
import re
import sys

PKG = os.environ.get("SIMPLE_ICONS_DIR", "./simple-icons/package")
OUT = sys.argv[1]

# ---------- brand icons (Simple Icons, CC0) ----------
meta = json.load(open(f"{PKG}/_data/simple-icons.json"))
meta = meta["icons"] if isinstance(meta, dict) else meta
hex_by_title = {m["title"]: m["hex"] for m in meta}


def brand(slug):
    svg = open(f"{PKG}/icons/{slug}.svg", encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", svg).group(1)
    d = re.search(r' d="([^"]+)"', svg).group(1)
    return {"kind": "brand", "d": d, "hex": hex_by_title.get(title, "334155")}


def glyph(name):
    return {"kind": "glyph", "name": name}


GLYPHS = {
    "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M14 9l2 2"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "webhook": '<path d="M3 12h11M10 7l5 5-5 5M19 5v14"/>',
    "loop": '<path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5"/>',
    "switch": '<rect x="2" y="8" width="20" height="8" rx="4"/><circle cx="16" cy="12" r="2.5" fill="currentColor"/>',
    "list": '<path d="M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
    "db": '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "plug": '<path d="M9 3v5M15 3v5M6 8h12v4a6 6 0 0 1-12 0zM12 18v3"/>',
    "gate": '<rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
}

I = {
    "gitlab": brand("gitlab"), "docker": brand("docker"), "ollama": brand("ollama"),
    "nvidia": brand("nvidia"), "openai": brand("openai"), "claude": brand("claude"),
    "redis": brand("redis"), "postgres": brand("postgresql"), "grafana": brand("grafana"),
    "prometheus": brand("prometheus"), "jaeger": brand("jaeger"), "sonar": brand("sonarqube"),
    "sonatype": brand("sonatype"), "vault": brand("vault"), "trivy": brand("trivy"),
    "yaml": brand("yaml"),
}

TEXT = {"n": "#374151", "b": "#111827", "g": "#15803d", "a": "#b45309", "r": "#b91c1c", "m": "#64748b"}
warnings = []


def esc(s):
    return html.escape(s, quote=False)


def lum(hexcol):
    r, g, b = (int(hexcol[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def icon_svg(ic, cx, cy, size):
    """Icon centred on (cx, cy) with the given pixel size, no tile."""
    s = size / 24.0
    tx, ty = cx - size / 2, cy - size / 2
    if ic["kind"] == "brand":
        col = "#" + ic["hex"]
        if lum(ic["hex"]) > 0.7:
            col = "#111827"
        return f'<path transform="translate({tx:.1f},{ty:.1f}) scale({s:.3f})" d="{ic["d"]}" fill="{col}"/>'
    return (f'<g transform="translate({tx:.1f},{ty:.1f}) scale({s:.3f})" fill="none" stroke="#334155" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" color="#334155">{GLYPHS[ic["name"]]}</g>')


def tile(x, y, icons, size=44):
    """Rounded tile holding one icon, or a vertical stack of icons."""
    if not isinstance(icons, list):
        icons = [icons]
    n = len(icons)
    h = size if n == 1 else n * 22 + 10
    first = icons[0]
    light = first["kind"] == "brand" and lum(first["hex"]) > 0.7 and n == 1
    fill = "#" + first["hex"] if light else "#f1f5f9"
    out = [f'<rect x="{x}" y="{y}" width="{size}" height="{h}" rx="10" fill="{fill}" stroke="#e2e8f0"/>']
    if n == 1:
        out.append(icon_svg(first, x + size / 2, y + h / 2, size * 0.58))
    else:
        for i, ic in enumerate(icons):
            out.append(icon_svg(ic, x + size / 2, y + 17 + i * 22, 17))
    return "".join(out)


def card(x, y, w, h, icons, title, lines, stroke="#cbd5e1", fill="#ffffff", dashed=False, sw=1.5, tsize=44):
    out = []
    dash = ' stroke-dasharray="6 3"' if dashed else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')
    out.append(tile(x + 10, y + (10 if h > 60 else (h - tsize) / 2), icons, tsize))
    tx = x + 10 + tsize + 12
    avail = w - (tx - x) - 8
    ty = y + 24 if h > 60 else y + h / 2 - 4
    if len(title) * 7.4 > avail:
        warnings.append(f"TITLE too long: {title!r} ({len(title) * 7.4:.0f}>{avail})")
    out.append(f'<text x="{tx}" y="{ty}" font-size="13" font-weight="700" fill="{TEXT["b"]}">{esc(title)}</text>')
    for i, ln in enumerate(lines):
        style, txt = ln if isinstance(ln, tuple) else ("n", ln)
        if len(txt) * 5.9 > avail:
            warnings.append(f"LINE too long: {txt!r} ({len(txt) * 5.9:.0f}>{avail})")
        weight = ' font-weight="700"' if style == "b" else ""
        out.append(f'<text x="{tx}" y="{ty + 18 + i * 15.5:.1f}" font-size="11" fill="{TEXT[style] if style != "b" else TEXT["n"]}"{weight}>{esc(txt)}</text>')
    return "".join(out)


def group(x, y, w, h, title, icon, stroke, fill, tcol):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>']
    out.append(icon_svg(icon, x + 26, y + 22, 24))
    out.append(f'<text x="{x + 48}" y="{y + 28}" font-size="15" font-weight="700" fill="{tcol}">{esc(title)}</text>')
    return "".join(out)


def badge(cx, cy, n):
    r = 11 if n >= 10 else 10
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#111827" stroke="#fff" stroke-width="1.5"/>'
            f'<text x="{cx}" y="{cy + 3.5}" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">{n}</text>')


def t(x, y, s, size=10, fill="#475569", anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'


P = []  # parts in paint order
W, H = 1760, 1210
P.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
P.append('<text x="30" y="32" font-size="22" font-weight="700" fill="#111827">Pipeline Failure Triage: Agentic DevOps Architecture</text>')
P.append(t(30, 54, "GitLab + pluggable LLM (Ollama default, OpenAI or Claude via one config file) + MCP tools, all on Docker Desktop. "
          "Humans decide; every action is allow-listed and audited.", 12))

# ---- top row ----
P.append(card(30, 70, 290, 80, glyph("person"), "Engineer / Reviewer",
              ["push · review note · approve issue", "confirm: @triage-bot confirm-fix"], stroke="#94a3b8", fill="#f8fafc"))
P.append(card(395, 70, 290, 80, I["yaml"], "llm-providers.yaml",
              ["the ONLY file you edit to switch", "one boolean per provider", "keys: env: / vault: refs"],
              stroke="#ca8a04", fill="#fefce8", sw=2))
P.append(card(715, 70, 300, 80, [I["ollama"], I["nvidia"]], "Ollama (local) · DEFAULT",
              ["ollama :11434 · 2x RTX 5080", "gpt-oss:20b · qwen3-coder:30b", "llama3.1:8b for summaries"],
              stroke="#10b981", fill="#ecfdf5", sw=2))
P.append(card(1035, 70, 240, 80, I["openai"], "OpenAI API · optional",
              ["enabled: false by default", "key via env / Vault"], stroke="#f59e0b", fill="#fffbeb", dashed=True, sw=1.8))
P.append(card(1295, 70, 240, 80, I["claude"], "Claude API · optional",
              ["enabled: false by default", "key via env / Vault"], stroke="#f59e0b", fill="#fffbeb", dashed=True, sw=1.8))

# ---- groups ----
GY, GH = 200, 670
P.append(group(30, GY, 290, GH, "GitLab  (gitlab-server :8929)", I["gitlab"], "#fb923c", "#fff7ed", "#c2410c"))
P.append(group(380, GY, 630, GH, "Triage Agent Service", I["docker"], "#3b82f6", "#eff6ff", "#1d4ed8"))
P.append(group(1070, GY, 290, GH, "MCP Tool Gateway", glyph("plug"), "#a855f7", "#faf5ff", "#7e22ce"))
P.append(group(1420, GY, 310, GH, "Data sources (running containers)", glyph("db"), "#10b981", "#ecfdf5", "#047857"))

# ---- GitLab column ----
GX, GW = 45, 260
P.append(card(GX, 240, GW, 82, I["gitlab"], "CI Pipeline & Runner",
              ["gitlab-runner · 8 stages", ("r", "a job fails → webhook sent")], stroke="#fb923c"))
P.append(card(GX, 342, GW, 82, I["gitlab"], "Merge Request",
              ["diff · commits · discussion", ("g", "receives the AI analysis note")], stroke="#fb923c"))
P.append(card(GX, 444, GW, 82, I["gitlab"], "GitLab Issues",
              ["recurring-failure tickets", ("g", "label ai-triage (on approval)")], stroke="#fb923c"))
P.append(card(GX, 546, GW, 82, glyph("key"), "Agent identity (bot user)",
              ["Reporter role · api scope", ("r", "no push · no CI var · no runner"), "stored in Vault (AppRole)"],
              stroke="#f59e0b", fill="#fffbeb"))
P.append(card(GX, 648, GW, 82, glyph("shield"), "Existing controls",
              ["branch protection · approvals", "CODEOWNERS · protected envs", "the agent cannot bypass them"],
              stroke="#10b981", fill="#ecfdf5"))

# ---- Triage left column ----
LX, LW = 395, 290
P.append(card(LX, 240, LW, 82, glyph("webhook"), "Webhook Receiver",
              ["verify token · failed pipelines", "MR/branch pipelines, non-prod"], stroke="#3b82f6"))
P.append(card(LX, 342, LW, 82, I["redis"], "Job Queue + Dedup",
              ["one analysis per pipeline", "redis :6379"], stroke="#3b82f6"))
P.append(card(LX, 444, LW, 170, glyph("loop"), "Orchestrator (agent loop)",
              ["builds failure summary, then:", ("b", "observe → reason → act"),
               "step cap · token budget · timeout", "ends with an evidence report:",
               "root cause + confidence + steps"], stroke="#3b82f6", sw=2.2))
P.append(card(LX, 634, LW, 82, I["gitlab"], "Result Publisher",
              [("g", "MR note: automatic"), ("a", "issue: only after approval")], stroke="#3b82f6"))

# ---- Triage right column ----
RX, RW = 715, 280
P.append(card(RX, 240, RW, 100, glyph("switch"), "LLM Provider Layer",
              ["reads llm-providers.yaml", "adapters: ollama, openai, claude", "exactly 1 enabled or no start",
               "audit/MR footer names provider"], stroke="#ca8a04", fill="#fefce8", sw=2.2))
P.append(card(RX, 462, RW, 82, glyph("shield"), "Redactor",
              ["rules scrub secrets / PII", "gitleaks · Presidio"], stroke="#ef4444", fill="#fef2f2", sw=1.8))
P.append(card(RX, 564, RW, 82, glyph("gate"), "Policy Guard",
              ["tool allow-list", "autonomy gate · read-only tools"], stroke="#ef4444", fill="#fef2f2", sw=1.8))
P.append(card(RX, 666, RW, 82, I["postgres"], "Audit Logger",
              ["prompts · tool calls · decisions", "ai-postgres :5432"], stroke="#3b82f6"))

# guardrails
P.append('<rect x="395" y="762" width="600" height="100" rx="8" fill="#fff" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 3"/>')
P.append('<text x="409" y="781" font-size="13" font-weight="700" fill="#111827">Guardrails</text>')
for i, s in enumerate([
    "• Read-only investigation; the only writes are the MR note and (approved) issue",
    "• Never retries prod jobs, merges, or edits CI variables, runners, secrets, RBAC",
    "• Rules scrub secrets/PII BEFORE any model sees logs; cloud providers get scrubbed text only",
    "• On timeout or low confidence: comment \"needs human triage\" instead of guessing"]):
    P.append(t(409, 799 + i * 16, s, 11, "#374151"))

# ---- MCP column ----
MX, MW = 1085, 260
P.append(card(MX, 240, MW, 90, I["gitlab"], "GitLab MCP (read)",
              ["get_job_trace · get_mr_diff", "list_pipelines · get_commits"], stroke="#a855f7"))
P.append(card(MX, 350, MW, 90, I["grafana"], "Observability MCP (read)",
              ["loki_query · prom_query", "jaeger_trace · time-windowed"], stroke="#a855f7"))
P.append(card(MX, 460, MW, 90, I["sonar"], "Quality & Security MCP",
              ["sonar_gate · trivy_report", "nexus_artifact_status"], stroke="#a855f7"))
P.append(card(MX, 570, MW, 90, glyph("db"), "Knowledge MCP (RAG)",
              ["search_similar_failures", ("a", "add_fix (human-confirmed)")], stroke="#a855f7"))
for i, s in enumerate(["• Each server: scoped credentials", "  and its own timeouts",
                       "• Allow-listed tools only; no shell,", "  docker or write tools",
                       "• Results pass the Redactor"]):
    P.append(t(1085, 700 + i * 16, s, 11, "#374151"))

# ---- Data column ----
DX, DW = 1435, 280
P.append(card(DX, 240, DW, 90, I["gitlab"], "gitlab-server :8929",
              ["REST API v4: traces, diffs", "pipelines · commits · history"], stroke="#10b981"))
P.append(card(DX, 350, DW, 90, [I["grafana"], I["prometheus"], I["jaeger"]], "Observability",
              ["loki :3100 · prometheus :9090", "jaeger :16686 · promtail"], stroke="#10b981"))
P.append(card(DX, 460, DW, 90, [I["sonar"], I["trivy"], I["sonatype"]], "Quality & Security",
              ["ai-sonarqube :9002 (gate)", "trivy-server :8183 (CVEs)", "ai-nexus :8181 · reg :5001"], stroke="#10b981"))
P.append(card(DX, 570, DW, 90, glyph("db"), "chromadb :8005 (vector DB)",
              ["past failures + verified fixes", "similarity search (RAG)", ("m", "alternative: qdrant :6333")], stroke="#10b981"))
for i, s in enumerate(["Alternatives you already run:", "• qdrant :6333 (vector DB)", "• ai-splunk :8088 (logs)",
                       "• jira :8180 / redmine :8090", "  (instead of GitLab Issues)"]):
    P.append(t(1435, 700 + i * 16, s, 11, "#374151"))

# ---- platform strip ----
P.append('<rect x="380" y="900" width="980" height="100" rx="12" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>')
P.append('<text x="396" y="920" font-size="13" font-weight="700" fill="#334155">Platform services used by the Triage Agent Service</text>')
P.append(card(395, 932, 225, 56, I["redis"], "redis :6379", ["queue + dedup keys"], stroke="#94a3b8", tsize=36))
P.append(card(635, 932, 225, 56, I["postgres"], "ai-postgres :5432", ["audit trail + feedback"], stroke="#94a3b8", tsize=36))
P.append(card(875, 932, 225, 56, I["vault"], "vault :8200", ["GitLab token, LLM API keys"], stroke="#94a3b8", tsize=36))
P.append(card(1115, 932, 230, 56, I["docker"], "ai-platform-net", ["agent joins this Docker net"],
              stroke="#94a3b8", tsize=36))

# ---- arrow key ----
P.append('<rect x="30" y="900" width="290" height="100" rx="10" fill="#fff" stroke="#cbd5e1"/>')
P.append('<text x="44" y="922" font-size="13" font-weight="700" fill="#111827">Arrow key</text>')
P.append('<path d="M46,940 L110,940" class="ar"/>' + t(124, 944, "data / control flow", 11, "#374151"))
P.append('<path d="M46,958 L110,958" class="ar2"/>' + t(124, 962, "request ⇄ response", 11, "#374151"))
P.append('<path d="M46,976 L110,976" class="ds"/>' + t(124, 980, "optional / dependency", 11, "#374151"))

# ---- arrows (after groups/cards so they stay visible) ----
A = []
A.append('<path d="M175,150 L175,200" class="ar2"/>')                          # humans <-> gitlab
A.append('<path d="M305,281 L395,281" class="ar"/>' + t(350, 273, "webhook", 10, "#475569", "middle"))
A.append('<path d="M540,322 L540,342" class="ar"/><path d="M540,424 L540,444" class="ar"/><path d="M540,614 L540,634" class="ar"/>')
A.append('<path d="M395,675 L350,675 L350,383 L305,383" class="ar"/><path d="M350,485 L305,485" class="ar"/>')
A.append(t(338, 580, "AI note · issue", 10, "#475569", "middle", 'transform="rotate(-90 338 580)"'))
A.append('<path d="M715,503 L685,503" class="ar"/><path d="M685,605 L715,605" class="ar"/>')
A.append('<path d="M995,605 L1070,605" class="ar"/>' + t(1032, 597, "tool call", 10, "#475569", "middle"))
A.append('<path d="M1070,503 L995,503" class="ar"/>' + t(1032, 495, "results", 10, "#475569", "middle"))
for y in (285, 395, 505, 615):
    A.append(f'<path d="M1345,{y} L1435,{y}" class="ar"/>')
# provider layer <-> backends bus
A.append('<path d="M865,240 L865,175 L1415,175" stroke="#475569" stroke-width="1.8" fill="none"/>')
for x in (865, 1155, 1415):
    A.append(f'<path d="M{x},175 L{x},152" class="ar"/>')
A.append(t(880, 192, "only the provider with enabled: true is called", 10))
A.append('<path d="M685,110 L700,110 L700,262 L715,262" class="ds"/>')           # yaml read at startup
A.append('<path d="M685,458 L700,458 L700,315 L715,315" class="ar2"/>')          # orchestrator <-> provider
A.append('<path d="M855,462 L855,340" class="ds"/>' + t(865, 404, "optional local summarize", 10))
A.append('<path d="M695,870 L695,900" class="ds"/>')

# badges
B = [badge(293, 240, 1), badge(673, 240, 2), badge(651, 444, 3), badge(673, 444, 7), badge(983, 564, 4),
     badge(1346, 200, 5), badge(983, 462, 6), badge(673, 634, 8), badge(308, 70, 9), badge(983, 666, 10)]

# ---- numbered flow ----
F = ['<text x="30" y="1046" font-size="15" font-weight="700" fill="#111827">Numbered flow</text>']
left = ["1  Pipeline job fails, so gitlab-server sends a pipeline webhook.",
        "2  Receiver verifies the token, filters scope, enqueues one analysis per pipeline (redis).",
        "3  Orchestrator starts the loop via the LLM Provider Layer (provider set in llm-providers.yaml).",
        "4  The model asks for a tool; the Policy Guard checks it against the allow-list.",
        "5  MCP servers run read-only queries: GitLab, Loki/Prometheus/Jaeger, Sonar/Trivy/Nexus, ChromaDB."]
right = ["6  Results pass the Redactor: rules scrub secrets/PII; only scrubbed text reaches the active model (steps 4-6 repeat).",
         "7  The model returns root cause + confidence + suggested next steps.",
         "8  Publisher posts the MR note automatically; an issue only after human approval.",
         "9  Engineer decides on the fix; @triage-bot confirm-fix later stores the verified fix in the vector DB.",
         "10 Audit Logger records every prompt, tool call and decision to ai-postgres."]
for i, s in enumerate(left):
    F.append(t(30, 1072 + i * 22, s, 12, "#1f2937"))
for i, s in enumerate(right):
    F.append(t(900, 1072 + i * 22, s, 12, "#1f2937"))
F.append(t(30, 1198, "Logos are trademarks of their respective owners; brand icons from Simple Icons (CC0). Generic glyphs are used where no logo exists "
           "(MCP, ChromaDB/Qdrant, queue, policy).", 10, "#64748b"))

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Arial, Helvetica, sans-serif">
<title>Pipeline Failure Triage - Agentic DevOps Architecture (GitLab + pluggable LLM + MCP on Docker Desktop)</title>
<defs>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#475569"/></marker>
<style>
.ar{{stroke:#475569;stroke-width:1.8;fill:none;marker-end:url(#arr)}}
.ar2{{stroke:#475569;stroke-width:1.8;fill:none;marker-end:url(#arr);marker-start:url(#arr)}}
.ds{{stroke:#64748b;stroke-width:1.6;fill:none;stroke-dasharray:6 4;marker-end:url(#arr)}}
</style>
</defs>
{chr(10).join(P)}
{chr(10).join(A)}
{chr(10).join(B)}
{chr(10).join(F)}
</svg>
'''
open(OUT, "w", encoding="utf-8").write(svg)
print("written", OUT, len(svg), "bytes")
for w in warnings:
    print("WARN", w)

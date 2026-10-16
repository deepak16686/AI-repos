#!/usr/bin/env python3
"""Generate sequence / container / CI-CD / state diagrams for the triage design docs."""
import sys

import dlib
from dlib import I, card, glyph, region, svg_doc, t, badge, sequence

OUT = sys.argv[1]  # output directory (ai-setup-diagrams)
G = glyph


def write(name, W, H, title, body):
    with open(f"{OUT}/{name}", "w", encoding="utf-8") as f:
        f.write(svg_doc(W, H, title, body))
    print("wrote", name, W, H)


# ======================================================================= sequence 1
cols = [
    ("Engineer", "MR author / reviewer", G("person")),
    ("GitLab", "gitlab-server + runner", I["gitlab"]),
    ("triage-api", "webhook receiver", I["fastapi"]),
    ("Redis", "Streams queue", I["redis"]),
    ("triage-worker", "orchestrator · guard · redactor", G("loop")),
    ("LLM provider", "Ollama default (switchable)", I["ollama"]),
    ("MCP servers", "4 read-only containers", G("plug")),
    ("Data sources", "GitLab · Loki · Sonar · Chroma", G("db")),
    ("ai-postgres", "audit trail", I["postgres"]),
]
rows = [
    ("phase", "A · Trigger and ingest"),
    ("msg", 0, 1, "push commit / open MR", False),
    ("self", 1, "pipeline runs; a job FAILS"),
    ("msg", 1, 2, "Pipeline Hook + token", False),
    ("self", 2, "verify token · filter scope"),
    ("msg", 2, 3, "XADD event · SETNX dedup", False),
    ("msg", 2, 1, "200 OK (under 1 s)", True),
    ("phase", "B · Collect evidence (deterministic, no LLM)"),
    ("msg", 3, 4, "XREADGROUP (workers)", False),
    ("msg", 4, 8, "INSERT run + config snapshot", False),
    ("msg", 4, 6, "gitlab: failed jobs, traces, MR diff, job history", False),
    ("msg", 6, 7, "read-only REST calls", False),
    ("msg", 7, 6, "JSON (size-limited)", True),
    ("msg", 6, 4, "tool results", True),
    ("self", 4, "slice logs · Drain3 · fingerprint · classify"),
    ("self", 4, "Redactor scrubs secrets / PII"),
    ("msg", 4, 6, "knowledge: search_similar_failures", False),
    ("msg", 6, 7, "vector search (ChromaDB)", False),
    ("msg", 7, 6, "top-k past fixes", True),
    ("msg", 6, 4, "similar failures", True),
    ("phase", "C · Reason: observe → reason → act (max 12 steps, token and time budget)"),
    ("frame_start", "loop: until evidence is sufficient or a budget is hit", 4, 8),
    ("msg", 4, 5, "prompt + summary + tools", False),
    ("msg", 5, 4, "tool_call request", True),
    ("self", 4, "Policy Guard: tool on the allow-list?"),
    ("msg", 4, 6, "call tool (args validated)", False),
    ("msg", 6, 7, "query Loki/Sonar/Nexus", False),
    ("msg", 7, 6, "data", True),
    ("msg", 6, 4, "result (size-limited)", True),
    ("self", 4, "Redactor scrubs the result"),
    ("msg", 4, 8, "INSERT tool_call + llm_call", False),
    ("frame_end",),
    ("msg", 5, 4, "final JSON answer", True),
    ("note", 4, 6, ["Output schema: root_cause, confidence (high / medium / low),",
                    "evidence[] (tool_call_id + line range), next_steps[], not_checked[]"], "b"),
    ("phase", "D · Validate and publish"),
    ("self", 4, "validate: each claim cites a tool_call"),
    ("note", 4, 6, ["Invalid citations or low confidence ⇒ publish 'needs human triage'",
                    "instead of a guess (state NEEDS_HUMAN)."], "y"),
    ("self", 4, "Policy Guard: publish_note allowed"),
    ("msg", 4, 1, "PUT MR note (upsert by marker)", False),
    ("msg", 1, 4, "201 + note id", True),
    ("msg", 4, 8, "UPDATE run: PUBLISHED + cost", False),
    ("msg", 1, 0, "notify: AI analysis posted", True),
    ("self", 0, "reads note; decides on the fix"),
    ("note", 0, 3, ["The engineer applies the fix. The agent never pushes code, edits CI variables,",
                    "changes runners, or retries production jobs (autonomy ceiling = comment)."], "g"),
]
W, H, body = sequence(1800, cols, rows, "Sequence: from a failed pipeline to an evidence-backed MR note",
                      "Main flow (UC-17.1). Solid = request, dashed = response. The LLM provider is whichever one is enabled in llm-providers.yaml.")
write("pipeline-failure-triage-sequence-main.svg", W, H, "Sequence - triage a failed pipeline", body)

# ======================================================================= sequence 2
cols2 = [
    ("Developer+", "engineer / maintainer", G("person")),
    ("GitLab", "Note Hook · REST", I["gitlab"]),
    ("triage-api", "webhook receiver", I["fastapi"]),
    ("triage-worker", "guard · approvals", G("loop")),
    ("ai-postgres", "approvals · feedback", I["postgres"]),
    ("mcp-knowledge", "add_fix gate", G("plug")),
    ("Ollama", "embedding model (pinned)", I["ollama"]),
    ("ChromaDB", "vector store", G("db")),
]
rows2 = [
    ("phase", "A · Recurring failure → issue (execute on approval)"),
    ("self", 3, "recurrence ≥ 3 in 7 days (same fingerprint)"),
    ("msg", 3, 1, "MR note: 'reply @triage-bot create-issue'", False),
    ("msg", 1, 0, "notification", True),
    ("msg", 0, 1, "@triage-bot create-issue", False),
    ("msg", 1, 2, "Note Hook + token", False),
    ("self", 2, "verify token · parse command"),
    ("msg", 2, 3, "command event (Redis)", False),
    ("msg", 3, 1, "GET commenter's project role", False),
    ("msg", 1, 3, "role = Developer or higher", True),
    ("msg", 3, 4, "INSERT approval (single-use)", False),
    ("self", 3, "Policy Guard: create_issue approved"),
    ("msg", 3, 1, "POST issue (label ai-triage)", False),
    ("msg", 1, 3, "issue iid", True),
    ("msg", 3, 1, "edit note: 'Issue #n created'", False),
    ("msg", 3, 4, "audit: action + approver", False),
    ("phase", "B · Confirm fix → learn (execute on approval)"),
    ("msg", 0, 1, "@triage-bot confirm-fix …", False),
    ("msg", 1, 2, "Note Hook + token", False),
    ("self", 2, "verify token · parse command"),
    ("msg", 2, 3, "command event (Redis)", False),
    ("msg", 3, 1, "role check + find the fixing MR", False),
    ("msg", 1, 3, "Developer+ ✓ · MR link", True),
    ("msg", 3, 4, "INSERT approval (add_fix)", False),
    ("msg", 3, 5, "add_fix(run_id, approval_id)", False),
    ("msg", 5, 4, "verify approval record", False),
    ("msg", 4, 5, "valid, unexpired, unused", True),
    ("msg", 5, 6, "embed(signature+cause+fix)", False),
    ("msg", 6, 5, "vector (pinned dims)", True),
    ("msg", 5, 7, "upsert vector + payload", False),
    ("msg", 7, 5, "point id", True),
    ("msg", 5, 3, "stored", True),
    ("msg", 3, 1, "reply: 'Saved to knowledge base'", False),
    ("msg", 3, 4, "feedback = useful; audit", False),
    ("note", 2, 5, ["Approval rules: commenter must be Developer or higher; approvals are single-use,",
                    "expire after 7 days, and are checked again by mcp-knowledge (defence in depth)."], "y"),
    ("phase", "C · Negative feedback"),
    ("msg", 0, 1, "@triage-bot wrong <why>", False),
    ("msg", 1, 2, "Note Hook + token", False),
    ("msg", 2, 3, "command event (Redis)", False),
    ("msg", 3, 4, "INSERT feedback = wrong", False),
    ("note", 3, 6, ["The run is excluded from the knowledge base and added to the next eval review list."], "r"),
]
W, H, body = sequence(1700, cols2, rows2, "Sequence: human approval and the learning loop",
                      "UC-17.2 (issue on approval), UC-17.3 (confirm fix) and UC-17.4 (negative feedback). Nothing is written without a recorded human approval.")
write("pipeline-failure-triage-sequence-approval-learning.svg", W, H, "Sequence - approval and learning loop", body)

# ======================================================================= containers
P = []
Wc, Hc = 1760, 1250
P.append(t(30, 30, "Container and network view: everything runs in Docker", 22, "#111827", extra='font-weight="700"'))
P.append(t(30, 50, "New compose project `pipeline-triage` (blue) joins your existing ai-platform-net stack (green). No new host ports except 127.0.0.1:8140.", 12, "#475569"))
P.append(region(20, 62, 1720, 1170, "Windows PC · Docker Desktop (WSL2) · 2× NVIDIA RTX 5080 (2×16 GB VRAM)", [I["docker"]][0], "#94a3b8", "#fafafa", "#334155", dashed=True))
# left: new project
P.append(region(40, 130, 540, 1080, "NEW compose project: pipeline-triage", I["docker"], "#3b82f6", "#eff6ff", "#1d4ed8"))
P.append(t(56, 180, "networks: triage-internal (internal: true) + ai-platform-net (external)", 11, "#1d4ed8"))
LX1, LX2, CW = 55, 320, 250
rowsL = [
    (190, [(I["python"], "triage-worker ×2", ["orchestrator·guard·redactor", "consumer group, concurrency 2"]),
           (I["fastapi"], "triage-api", ["webhooks · health · metrics", "127.0.0.1:8140 only"])]),
    (288, [(I["gitlab"], "mcp-gitlab", ["read-only GitLab tools", "internal only · bearer auth"]),
           (I["grafana"], "mcp-observability", ["Loki · Prometheus · Jaeger", "templated, time-boxed queries"])]),
    (386, [(I["sonar"], "mcp-quality", ["Sonar · Trivy · Nexus status", "read-only credentials"]),
           (G("db"), "mcp-knowledge", ["vector search + gated add_fix", "checks approvals table"])]),
    (484, [(I["postgres"], "triage-migrate", ["one-shot Alembic job", "runs before api/worker start"]),
           (G("clock"), "triage-housekeeper", ["retention · nightly backups", "audit export to MinIO"])]),
]
for y, pair in rowsL:
    for (ic, ttl, lines), x in zip(pair, (LX1, LX2)):
        P.append(card(x, y, CW, 84, ic, ttl, lines, stroke="#3b82f6"))
extra = [
    (596, G("doc"), "Config + prompts", ["./config/*.yaml and ./prompts (bind mount, read-only)", "llm-providers.yaml · triage.yaml · policy.yaml · redaction.yaml"], "#ca8a04", "#fefce8"),
    (694, G("key"), "Secrets", ["docker secrets: Vault role_id + secret_id files", "API keys resolved from Vault at start, never baked into images"], "#f59e0b", "#fffbeb"),
    (792, G("gate"), "Hardening (every container)", ["non-root · read-only rootfs · cap_drop ALL · no-new-privileges", "cpu/memory limits · healthchecks · pinned image digests"], "#ef4444", "#fef2f2"),
    (890, I["sonatype"], "Images", ["built in CI, pushed to ai-nexus:5001 as version + sha tags", "prod-local pulls pinned tags, never :latest"], "#94a3b8", "#ffffff"),
    (988, G("bell"), "Observability", ["JSON logs → Docker → promtail (existing) → Loki", "/metrics → Prometheus · OTLP traces → Jaeger"], "#94a3b8", "#ffffff"),
]
for y, ic, ttl, lines, st, fl in extra:
    P.append(card(55, y, 515, 84, ic, ttl, lines, stroke=st, fill=fl))
P.append(t(56, 1098, "Published ports: only 127.0.0.1:8140 → triage-api (admin/health).", 11, "#1d4ed8"))
P.append(t(56, 1114, "GitLab reaches the webhook over the Docker network: http://triage-api:8140", 11, "#1d4ed8"))
P.append(t(56, 1130, "MCP servers have no published ports and bind to the internal interface.", 11, "#1d4ed8"))

# middle: existing stack
P.append(region(620, 130, 800, 1080, "EXISTING stack on ai-platform-net (unchanged)", I["docker"], "#10b981", "#ecfdf5", "#047857"))
MX = [635, 900, 1165]
MW = 245
grid = [
    [(I["gitlab"], "gitlab-server", [":8929 · webhook source"]), (I["gitlab"], "gitlab-runner", ["docker executor"]), ([I["ollama"], I["nvidia"]], "ollama", [":11434 · LLM + embeddings"])],
    [(I["redis"], "redis", [":6379 · stream + dedup"]), (I["postgres"], "ai-postgres", [":5432 · DB `triage`"]), (I["vault"], "vault", [":8200 · AppRole"])],
    [(I["minio"], "minio", [":9000 · evidence bucket"]), (G("db"), "chromadb", [":8005 · failure memory"]), (G("db"), "qdrant", [":6333 · alternative"])],
    [(I["grafana"], "loki", [":3100 · logs"]), (I["prometheus"], "prometheus", [":9090 · metrics"]), (I["jaeger"], "jaeger", [":16686 · traces"])],
    [(I["grafana"], "promtail", ["ships container logs"]), (I["grafana"], "grafana", [":3000 · monitoring-network"]), (I["trivy"], "trivy-server", [":8183 · CVE scans"])],
    [(I["sonar"], "ai-sonarqube", [":9002 · quality gates"]), (I["sonatype"], "ai-nexus", [":8181 · registry :5001"]), (G("cloud"), "ai-splunk", [":8088 · alt log store"])],
]
y = 170
for r in grid:
    for (ic, ttl, lines), x in zip(r, MX):
        P.append(card(x, y, MW, 62, ic, ttl, lines, stroke="#10b981", tsize=36))
    y += 76
P.append('<rect x="635" y="640" width="775" height="555" rx="10" fill="#ffffff" stroke="#94a3b8" stroke-dasharray="5 4"/>')
P.append(t(650, 664, "How the new containers use the existing stack (numbers match the arrows)", 13, "#111827", extra='font-weight="700"'))
notes = [
    ("1", "triage-api / triage-worker → redis (Streams + dedup keys), ai-postgres (audit), vault (secrets), minio (evidence)."),
    ("2", "triage-worker → ollama (chat model + pinned embedding model) over http://ollama:11434."),
    ("3", "mcp-* servers → gitlab-server, loki, prometheus, jaeger, ai-sonarqube, trivy-server, ai-nexus, chromadb (read-only)."),
    ("4", "gitlab-server → triage-api: project webhooks (Pipeline events + Comments) with a secret token."),
    ("5", "Existing promtail already ships every container's logs to loki; prometheus gets one new scrape job."),
]
for i, (n, s) in enumerate(notes):
    P.append(badge(655, 690 + i * 26, n))
    P.append(t(674, 694 + i * 26, s, 11.5))
P.append(t(650, 840, "Touch-points on the existing stack (one-time changes, tracked as tasks T0.x)", 13, "#111827", extra='font-weight="700"'))
tp = ["• ai-postgres: create database `triage` + a dedicated role with a Vault-managed password",
      "• vault: policy + AppRole `pipeline-triage`; secrets under secret/triage/*",
      "• minio: bucket `triage-evidence` with a 14-day lifecycle rule",
      "• ollama: pull the embedding model; set OLLAMA_MAX_LOADED_MODELS=2 (shared with Open WebUI)",
      "• prometheus: add a scrape job for triage-api:8140/metrics",
      "• grafana: attach to ai-platform-net (or query by URL) and import the triage dashboard",
      "• gitlab-server: allow webhooks to the local network; create bot user + per-project webhooks",
      "• ai-nexus: create hosted docker repo path devops-ai/* with a deploy role for CI"]
for i, s in enumerate(tp):
    P.append(t(650, 864 + i * 20, s, 11.5))

# right: internet
P.append(region(1450, 130, 270, 330, "Internet (optional)", G("cloud"), "#f59e0b", "#fffbeb", "#b45309", dashed=True))
P.append(card(1465, 180, 240, 84, I["openai"], "OpenAI API", ["enabled: false by default", "HTTPS egress, scrubbed text"], stroke="#f59e0b", dashed=True, fill="#ffffff"))
P.append(card(1465, 280, 240, 84, I["claude"], "Claude API", ["enabled: false by default", "HTTPS egress, scrubbed text"], stroke="#f59e0b", dashed=True, fill="#ffffff"))
P.append(t(1465, 392, "Used only when the matching", 11)); P.append(t(1465, 408, "provider is enabled in", 11)); P.append(t(1465, 424, "llm-providers.yaml.", 11))
P.append(t(1465, 446, "No other egress is needed.", 11, "#b45309"))
# arrows
A = []
A.append('<path d="M635,232 L575,232" class="ar"/>' + t(605, 224, "webhook", 10, "#475569", "middle") + badge(605, 246, "4"))
A.append('<path d="M580,330 L620,330" class="ar"/>' + badge(600, 318, "3"))
A.append('<path d="M580,420 L620,420" class="ar"/>' + badge(600, 408, "1"))
A.append('<path d="M580,510 L620,510" class="ar"/>' + badge(600, 498, "2"))
A.append('<path d="M580,600 L620,600" class="ar"/>' + badge(600, 588, "5"))
A.append('<path d="M450,130 L450,108 L1585,108 L1585,130" class="ds"/>' + t(1000, 102, "optional HTTPS egress (only if the provider is enabled)", 10, "#475569", "middle"))
B = "\n".join(P) + "\n" + "\n".join(A)
write("pipeline-failure-triage-containers.svg", Wc, Hc, "Container and network view", B)

# ======================================================================= CI/CD + code management
P = []
Wd, Hd = 1760, 1000
P.append(t(30, 30, "Code management and CI/CD: how the solution is built, shipped and rolled back", 22, "#111827", extra='font-weight="700"'))
P.append(t(30, 50, "GitLab project devops-ai/pipeline-triage on gitlab-server · pipelines run on gitlab-runner · images in ai-nexus:5001 · deploy to Docker Desktop.", 12, "#475569"))
P.append(region(20, 66, 1720, 170, "Source control flow (trunk-based)", I["git"], "#fb923c", "#fff7ed", "#c2410c"))
flow = [
    (G("person"), "Developer + AI assist", ["pre-commit: ruff · mypy ·", "gitleaks · hadolint"]),
    (G("branch"), "Feature branch", ["feat/<ticket>-<slug>", "fix/ · docs/ · chore/"]),
    (I["gitlab"], "Merge Request", ["CI green + 1 approval", "CODEOWNERS on policy/prompts"]),
    (I["git"], "main (protected)", ["squash merge", "Conventional Commits"]),
    (G("tag"), "Tag vX.Y.Z", ["protected tag = release", "changelog + image tags"]),
]
x = 40
for ic, ttl, lines in flow:
    P.append(card(x, 120, 300, 88, ic, ttl, lines, stroke="#fb923c"))
    x += 340
P.append(region(20, 256, 1720, 290, "GitLab CI pipeline (gitlab-runner, docker executor)", I["gitlab"], "#3b82f6", "#eff6ff", "#1d4ed8"))
stages = [
    (G("list"), "1 Lint + static", ["ruff · mypy · yamllint", "hadolint · gitleaks"], ["MR", "main", "tag"]),
    (I["python"], "2 Tests", ["pytest unit tests", "MCP contract tests"], ["MR", "main", "tag"]),
    (I["docker"], "3 Build images", ["5 images, multi-stage", "non-root, pinned bases"], ["MR", "main", "tag"]),
    (I["trivy"], "4 Security scan", ["trivy image scan", "SBOM per image"], ["MR", "main", "tag"]),
    (I["docker"], "5 Integration", ["replay golden webhooks", "mock GitLab + LLM"], ["MR", "main", "tag"]),
    (I["ollama"], "6 Eval gate", ["golden set, local model", "no regression allowed"], ["MR", "main", "tag"]),
    (I["sonatype"], "7 Publish", ["push to ai-nexus:5001", "version + sha tags"], ["main", "tag"]),
    (G("rocket"), "8 Deploy", ["manual · protected tag", "compose pull + up -d"], ["tag"]),
]
x = 30
for i, (ic, ttl, lines, chips) in enumerate(stages):
    P.append(card(x, 300, 200, 120, ic, ttl, lines, stroke="#3b82f6", tsize=34))
    cx = x + 12
    for c in chips:
        col = {"MR": ("#dbeafe", "#1d4ed8"), "main": ("#dcfce7", "#15803d"), "tag": ("#fef3c7", "#b45309")}[c]
        P.append(f'<rect x="{cx}" y="388" width="{len(c) * 7 + 14}" height="18" rx="9" fill="{col[0]}" stroke="{col[1]}"/>')
        P.append(t(cx + (len(c) * 7 + 14) / 2, 401, c, 10, col[1], "middle", 'font-weight="700"'))
        cx += len(c) * 7 + 20
    if i < len(stages) - 1:
        P.append(f'<path d="M{x + 200},360 L{x + 215},360" class="ar"/>')
    x += 215
P.append(t(40, 450, "Chips show where each stage runs: MR pipelines run stages 1-6 (build without push), main adds 7, a release tag adds 8.", 11.5, "#1d4ed8"))
P.append(t(40, 470, "Any failing stage blocks the merge or release. Stage 6 also runs on a nightly schedule to catch model or prompt drift.", 11.5, "#1d4ed8"))
P.append(t(40, 490, "Deploy uses a protected runner and a protected tag only; the deploy job is the only job allowed to touch Docker Desktop.", 11.5, "#b91c1c"))
P.append(t(40, 510, "Rollback = re-run the deploy job on the previous tag (images are immutable, compose pins versions).", 11.5, "#15803d"))
P.append(region(20, 566, 1720, 190, "Environments", I["docker"], "#10b981", "#ecfdf5", "#047857"))
envs = [
    (I["docker"], "dev (laptop)", ["compose.dev.yaml, bind mounts", "Ollama or a mock LLM", "tools run via `docker compose run`"]),
    (I["gitlab"], "ci (ephemeral)", ["compose.ci.yaml per pipeline", "mock GitLab + mock LLM", "destroyed after the job"]),
    (I["docker"], "prod-local", ["compose.yaml, images pinned", "config mounted read-only", "shadow mode first, then comment"]),
]
x = 40
for ic, ttl, lines in envs:
    P.append(card(x, 616, 540, 120, ic, ttl, lines, stroke="#10b981"))
    x += 560
P.append(region(20, 776, 1720, 200, "Change control", G("shield"), "#a855f7", "#faf5ff", "#7e22ce"))
cc = [
    (G("doc"), "Config + prompts", ["CODEOWNERS on policy.yaml,", "llm-providers.yaml, prompts/", "eval gate must pass"]),
    (G("key"), "Secrets", ["none in git; gitleaks in", "pre-commit + CI; Vault at", "runtime via AppRole"]),
    (G("box"), "Dependencies", ["lockfiles + pinned bases;", "weekly scheduled rebuild", "+ trivy re-scan"]),
    (G("tag"), "Releases", ["semver tags; changelog from", "Conventional Commits;", "release notes per tag"]),
    (G("branch"), "Docs as code", ["ADRs in docs/adr; diagrams", "as SVG; PDFs rebuilt in CI", "from the markdown sources"]),
]
x = 36
for ic, ttl, lines in cc:
    P.append(card(x, 826, 330, 128, ic, ttl, lines, stroke="#a855f7"))
    x += 342
A = []
A.append('<path d="M340,164 L380,164" class="ar"/><path d="M680,164 L720,164" class="ar"/><path d="M1020,164 L1060,164" class="ar"/><path d="M1360,164 L1400,164" class="ar"/>')
A.append('<path d="M1480,208 L1480,300" class="ds"/>')
write("pipeline-failure-triage-repo-cicd.svg", Wd, Hd, "Code management and CI/CD", "\n".join(P) + "\n" + "\n".join(A))

# ======================================================================= state machine
P = []
Ws, Hs = 1760, 780
P.append(t(30, 30, "State machine of one analysis run", 22, "#111827", extra='font-weight="700"'))
P.append(t(30, 50, "Persisted in ai-postgres (analysis_runs.status). Every transition writes an audit row. Retries re-enter the queue; nothing loops forever.", 12, "#475569"))
BW, STEP = 150, 225


def state(x, y, name, sub, kind="n"):
    st = {"n": ("#eff6ff", "#3b82f6"), "ok": ("#dcfce7", "#16a34a"), "skip": ("#f1f5f9", "#64748b"),
          "warn": ("#fef3c7", "#d97706"), "bad": ("#fee2e2", "#dc2626")}[kind]
    return (f'<rect x="{x}" y="{y}" width="{BW}" height="64" rx="12" fill="{st[0]}" stroke="{st[1]}" stroke-width="2"/>'
            f'<text x="{x + BW / 2}" y="{y + 27}" font-size="12.5" font-weight="700" fill="#111827" text-anchor="middle">{name}</text>'
            f'<text x="{x + BW / 2}" y="{y + 46}" font-size="10" fill="#475569" text-anchor="middle">{sub}</text>')


xs = [20 + i * STEP for i in range(8)]
c = [x + BW / 2 for x in xs]
Y1, Y2, Y3 = 130, 330, 520
names = [("RECEIVED", "webhook accepted", "n"), ("QUEUED", "in Redis stream", "n"), ("COLLECTING", "tools + log slicing", "n"),
         ("REASONING", "LLM loop", "n"), ("VALIDATING", "citations + schema", "n"), ("DRAFTED", "note rendered", "n"),
         ("PUBLISHED", "MR note posted", "ok"), ("CLOSED", "feedback or TTL", "ok")]
for x, (n, s_, k) in zip(xs, names):
    P.append(state(x, Y1, n, s_, k))
xr = int((c[2] + c[3]) / 2 - BW / 2)
cr = xr + BW / 2
P.append(state(xs[0], Y2, "SKIPPED", "filtered out", "skip"))
P.append(state(xr, Y2, "FAILED_RETRYABLE", "timeout / error", "bad"))
P.append(state(xs[4], Y2, "NEEDS_HUMAN", "low confidence", "warn"))
P.append(state(xr, Y3, "FAILED_FINAL", "retries exhausted", "bad"))
P.append(state(xs[5], Y3, "SHADOW_DONE", "shadow: no publish", "skip"))
A = []
labels = [("accepted", ""), ("worker", "claims"), ("evidence", "ready"), ("final", "answer"),
          ("citations", "valid"), ("mode =", "comment"), ("feedback /", "14 days")]
for i, (l1, l2) in enumerate(labels):
    xm = xs[i] + BW + (STEP - BW) / 2
    A.append(f'<path d="M{xs[i] + BW},{Y1 + 44} L{xs[i + 1]},{Y1 + 44}" class="ar"/>')
    A.append(t(xm, Y1 + 22 if l2 else Y1 + 34, l1, 10, "#475569", "middle"))
    if l2:
        A.append(t(xm, Y1 + 34, l2, 10, "#475569", "middle"))
# RECEIVED -> SKIPPED
A.append(f'<path d="M{c[0]},{Y1 + 64} L{c[0]},{Y2}" class="ar"/>' + t(c[0] + 8, 245, "not failed · not onboarded", 10, "#475569") + t(c[0] + 8, 259, "duplicate · prod pipeline", 10, "#475569"))
# COLLECTING / REASONING -> RETRYABLE
A.append(f'<path d="M{xr + 40},{Y1 + 64} L{xr + 40},{Y2}" class="ar"/>')
A.append(t(xr + 34, 245, "tool error", 10, "#475569", "end") + t(xr + 34, 259, "or timeout", 10, "#475569", "end"))
A.append(f'<path d="M{xr + 110},{Y1 + 64} L{xr + 110},{Y2}" class="ar"/>' + t(xr + 118, 245, "LLM timeout or", 10, "#475569") + t(xr + 118, 259, "provider error", 10, "#475569"))
# RETRYABLE -> QUEUED
A.append(f'<path d="M{xr},{Y2 + 32} L{c[1]},{Y2 + 32} L{c[1]},{Y1 + 64}" class="ar"/>' + t(c[1] + 10, Y2 + 24, "retry ≤ 2 with backoff", 10, "#475569", extra='class="halo"'))
# RETRYABLE -> FAILED_FINAL
A.append(f'<path d="M{cr},{Y2 + 64} L{cr},{Y3}" class="ar"/>' + t(cr + 8, 450, "retries exhausted / fatal error", 10, "#475569"))
# VALIDATING -> NEEDS_HUMAN
A.append(f'<path d="M{c[4]},{Y1 + 64} L{c[4]},{Y2}" class="ar"/>' + t(c[4] + 8, 245, "invalid citations or", 10, "#475569") + t(c[4] + 8, 259, "low confidence", 10, "#475569"))
# NEEDS_HUMAN -> PUBLISHED
A.append(f'<path d="M{xs[4] + BW},{Y2 + 32} L{c[6] - 40},{Y2 + 32} L{c[6] - 40},{Y1 + 64}" class="ar"/>' + t(1316, Y2 + 24, "publish 'needs human' note", 10, "#475569", "middle", 'class="halo"'))
# DRAFTED -> SHADOW_DONE
A.append(f'<path d="M{c[5]},{Y1 + 64} L{c[5]},{Y3}" class="ar"/>' + t(c[5] + 8, 470, "mode = shadow:", 10, "#475569") + t(c[5] + 8, 484, "analysis kept, nothing posted", 10, "#475569"))
# FAILED_FINAL -> PUBLISHED (optional)
A.append(f'<path d="M{cr},{Y3 + 64} L{cr},{Y3 + 100} L{c[6] + 40},{Y3 + 100} L{c[6] + 40},{Y1 + 64}" class="ds"/>' + t(1000, Y3 + 92, "optional: short 'analysis failed, please triage manually' note", 10, "#475569", "middle", 'class="halo"'))
P.append(t(30, 700, "Terminal states: CLOSED, SKIPPED, SHADOW_DONE, FAILED_FINAL.", 12, "#1f2937"))
P.append(t(30, 720, "Re-analysis (pipeline retried and fails again) creates a NEW run that updates the same MR note through its hidden marker.", 12, "#1f2937"))
write("pipeline-failure-triage-run-state.svg", Ws, Hs, "Analysis run state machine", "\n".join(P) + "\n" + "\n".join(A))

for w in dlib.warnings:
    print("WARN", w)

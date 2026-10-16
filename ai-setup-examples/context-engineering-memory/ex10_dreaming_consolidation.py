"""Example 10 - "Dreaming": offline consolidation of memory (illustrative).

NOTE: the talk was cut off before this section, so this is a reconstruction of the
idea, not a copy of Anthropic's implementation. Between sessions a background pass
reads transcripts, finds lessons that recur, drops stale/contradicted memory, and
PROPOSES an updated memory file that goes through the review gate.
"""
import re
import tempfile
from collections import defaultdict
from datetime import date
from memlib import MemoryStore

TODAY = date(2026, 10, 16)
store = MemoryStore(tempfile.mkdtemp())
store.write("project/lessons.md",
            "- [topic=registry] [verified 2026-02-01] Push images to ai-nexus:5000\n"
            "- [topic=sonar] [verified 2026-09-10] SonarQube gate must pass before push\n"
            "- [topic=old-runner] [verified 2026-01-05] Use runner tag legacy-docker\n",
            "human:alice", "curation", reason="seed")

# transcripts: (session, kind, topic, text)
events = [
    ("s1", "error", "registry", "push denied on ai-nexus:5000"), ("s1", "fix", "registry", "Push images to ai-nexus:5001"),
    ("s2", "error", "registry", "push denied on ai-nexus:5000"), ("s2", "fix", "registry", "Push images to ai-nexus:5001"),
    ("s3", "error", "maven", "central unreachable"),            ("s3", "fix", "maven", "Use nexus-mirror setting for Maven"),
    ("s4", "error", "maven", "central unreachable"),            ("s4", "fix", "maven", "Use nexus-mirror setting for Maven"),
    ("s5", "error", "trivy", "scan timeout"),                   ("s5", "fix", "trivy", "Raise trivy timeout to 10m"),
    ("s6", "info", "sonar", "gate passed as expected"),
]
print(f"input: {len({e[0] for e in events})} session transcripts, {len(events)} events\n")

seen = defaultdict(lambda: defaultdict(set))                 # topic -> fix text -> sessions
for sess, kind, topic, text in events:
    if kind == "fix":
        seen[topic][text].add(sess)

existing = {}
for line in store.read("project/lessons.md")[0].splitlines():
    m = re.match(r"- \[topic=(\S+)\] \[verified (\S+)\] (.*)", line)
    existing[m.group(1)] = (date.fromisoformat(m.group(2)), m.group(3))

new_lines, report = [], []
for topic, (d, text) in existing.items():
    if topic in seen and text not in seen[topic]:
        fix = max(seen[topic], key=lambda t: len(seen[topic][t]))
        report.append(f"REPLACE  topic={topic}: contradicted by {len(seen[topic][fix])} sessions")
        new_lines.append(f"- [topic={topic}] [verified {TODAY}] {fix}")
    elif (TODAY - d).days > 90 and topic not in seen:
        report.append(f"PRUNE    topic={topic}: unverified for {(TODAY - d).days} days")
    else:
        new_lines.append(f"- [topic={topic}] [verified {d}] {text}")
for topic, fixes in seen.items():
    for text, sessions in fixes.items():
        if topic in existing:
            continue
        if len(sessions) >= 2:
            report.append(f"PROMOTE  topic={topic}: seen in {len(sessions)} sessions")
            new_lines.append(f"- [topic={topic}] [verified {TODAY}] {text}")
        else:
            report.append(f"WATCH    topic={topic}: only 1 session, not promoted yet")

print("dreaming report:")
print("\n".join("  " + r for r in report))
proposal = "\n".join(new_lines) + "\n"
p = store.propose("agent:dreamer", "project/lessons.md", proposal, "dream-2026-10-16", reason="nightly consolidation")
print(f"\nproposal written to {p}; waiting at the review gate ...")
store.approve("human:alice", p, "review-2026-10-16")

print("\nmemory before (v1):\n" + store.versions("project/lessons.md")[0]["content"].rstrip())
print("\nmemory after (v2, approved by human):\n" + store.read("project/lessons.md")[0].rstrip())
last = store.versions("project/lessons.md")[-1]
print(f"\nprovenance: v{last['v']} by {last['actor']} - {last['reason']}")

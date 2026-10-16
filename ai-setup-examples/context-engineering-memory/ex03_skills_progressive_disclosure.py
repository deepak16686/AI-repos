"""Example 3 - Skills: progressive disclosure.

Talk: the agent only sees each skill's front matter (title + description). It loads
the full body only when the task matches - like scanning book titles on a shelf and
pulling off the French dictionary when someone speaks French.
"""
import re
import tempfile
from pathlib import Path
from memlib import tokens

SKILLS = {
    "gitlab-pipeline": ("Generate an 8-stage GitLab CI pipeline: compile, build, test, sast, quality, security, push, notify",
                        "pipeline gitlab ci stages"),
    "dockerfile": ("Create a multi-stage Dockerfile after analysing the repository",
                   "dockerfile docker image multi-stage"),
    "incident-triage": ("Diagnose a failed pipeline and propose a fix",
                        "failed failure triage diagnose"),
}

root = Path(tempfile.mkdtemp())
for name, (desc, _) in SKILLS.items():
    body = "".join(f"{i}. Detailed procedural step {i} for {name}: check inputs, apply golden rules, validate output.\n"
                   for i in range(1, 61))
    (root / f"{name}.md").write_text(f"---\nname: {name}\ndescription: {desc}\n---\n{body}")


def front_matter(path):
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(), re.S)
    return dict(line.split(": ", 1) for line in m.group(1).splitlines())


index = {p.stem: front_matter(p) for p in root.glob("*.md")}
all_bodies = sum(tokens(p.read_text()) for p in root.glob("*.md"))
titles = sum(tokens(f"{v['name']}: {v['description']}") for v in index.values())

print(f"skills on shelf: {len(index)}")
print(f"if ALL skills were loaded into context : {all_bodies:,} tokens")
print(f"progressive disclosure, titles only    : {titles:,} tokens\n")

for request in ("please generate a gitlab ci pipeline for this java repo",
                "write a multi-stage dockerfile for the service",
                "tell me a joke"):
    words = set(request.lower().split())
    scored = sorted(((len(words & set((v["name"] + " " + v["description"]).lower().replace("-", " ").split())), n)
                     for n, v in index.items()), reverse=True)
    score, best = scored[0]
    if score < 2:
        print(f"request: {request!r}\n  -> no skill matched, context cost = {titles:,} tokens")
        continue
    body = (root / f"{best}.md").read_text()
    print(f"request: {request!r}\n  -> matched skill '{best}' (score {score}), "
          f"loaded body: context cost = {titles + tokens(body):,} tokens "
          f"(vs {all_bodies:,} if everything were preloaded)")

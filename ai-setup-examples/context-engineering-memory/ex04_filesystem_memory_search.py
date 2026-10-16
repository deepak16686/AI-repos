"""Example 4 - Memory as a file system: plain Markdown + ls/grep.

Talk (best practice): model memory as files; let the agent use ordinary bash tools
instead of bespoke retrieval; let memory grow large but make it searchable.
Uses the REAL `grep` binary to show agents need nothing special.
"""
import subprocess
import tempfile
from memlib import MemoryStore, tokens

store = MemoryStore(tempfile.mkdtemp())
H = "human:curator"
store.write("org/index.md", "# Index\n- standards.md: stage order, registry rules\n- projects/: per-project notes\n", H, "s0")
store.write("org/standards.md",
            "# Golden rules\n- Pipeline stages: compile, build, test, sast, quality, security, push, notify\n"
            "- Docker registry: ai-nexus:5001 (never push to latest)\n- Quality gate: SonarQube must pass\n", H, "s0")
for i in range(1, 41):
    store.write(f"projects/svc-{i:02d}/notes.md",
                f"# svc-{i:02d}\n- language: {'java' if i % 3 else 'python'}\n- owner: team-{i % 5}\n"
                + ("- known issue: nexus login expires, re-auth before push\n" if i == 17 else ""),
                H, "s0")

total = sum(tokens((store.root / p).read_text()) for p in store.ls())
print(f"memory size: {len(store.ls())} files, {total:,} tokens if loaded in full\n")

for question, cmd in (("Which registry do we push images to?", ["grep", "-rIin", "--include=*.md", "registry", "org"]),
                      ("Any known issue with nexus login?", ["grep", "-rIin", "--include=*.md", "known issue", "."])):
    print(f"Q: {question}\n$ {' '.join(cmd)}")
    out = subprocess.run(cmd, cwd=store.root, capture_output=True, text=True).stdout.strip()
    print(out)
    files = {line.split(":")[0] for line in out.splitlines()}
    read = sum(tokens((store.root / f).read_text()) for f in files)
    print(f"-> agent reads {len(files)} file(s) = {read} tokens instead of {total:,} "
          f"({100 * (1 - read / total):.0f}% saved)\n")

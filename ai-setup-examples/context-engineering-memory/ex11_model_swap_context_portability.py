"""Example 11 - Swapping the model: context is the durable asset.

Talk: a newer, smarter model still knows nothing about YOUR environment, because
that knowledge is orthogonal to model intelligence. If your context lives outside the
model (memory files, skills, CLAUDE.md), a new model plugs into it and is instantly
useful; without it, it re-learns every local fact the hard way.

Toy model: 4 local facts must be right (registry, maven, sonar, runner) plus 1
generic hard step. The old model (v1) is weaker at the generic step; the new model
(v2) is stronger at it. Neither knows the local facts until it reads memory.
"""
import tempfile
from memlib import MemoryStore

TRUTH = {"registry": "ai-nexus:5001", "maven": "nexus-mirror", "sonar": "gate-required", "runner": "docker-prod"}
GUESS = {"registry": "docker.io", "maven": "maven-central", "sonar": "optional", "runner": "shared-default"}
MEM = "shared/platform-lessons.md"                # context lives OUTSIDE any model


def run(model, generic_ok, store, session):
    actor = f"agent:{model}"
    original, h = store.read(MEM, actor, missing_ok=True)
    text, failures = original, []
    for topic in TRUTH:
        hits = store.grep(rf"^- {topic}:", "shared")                 # agent greps its memory
        value = hits[0][2].split(": ", 1)[1] if hits else GUESS[topic]
        if value != TRUTH[topic]:
            failures.append(f"{topic}: guessed {value!r}, real value {TRUTH[topic]!r}")
            text += f"- {topic}: {TRUTH[topic]}\n"                    # learns from the error
    if not generic_ok:
        failures.append("generic: cache conflict in multi-stage build (weaker model needs a retry)")
    if text != original:
        store.write(MEM, text, actor, session, expected_hash=h, reason="lessons from failed attempts")
    return failures


def report(label, failures):
    print(f"{label}\n  failed attempts before success: {len(failures)}")
    for f in failures:
        print(f"    - {f}")
    return len(failures)


old_env = MemoryStore(tempfile.mkdtemp())
print("== OLD model (v1) living in this environment ==")
n1 = report("v1, session 1 (empty memory)", run("model-v1", False, old_env, "v1-s1"))
n2 = report("v1, session 2 (memory built by session 1)", run("model-v1", False, old_env, "v1-s2"))

print("\n== NEW smarter model (v2) arrives ==")
n3 = report("v2 COLD: new model, no context attached", run("model-v2", True, MemoryStore(tempfile.mkdtemp()), "v2-cold"))
n4 = report("v2 + SAME context layer (memory from the old model's sessions)", run("model-v2", True, old_env, "v2-ctx"))

print("\nsummary (failed attempts before success): "
      f"v1 first session={n1}, v1 learned={n2}, v2 cold={n3}, v2 + existing context={n4}")
print("-> the model changed; the context layer did not. Intelligence x context.")

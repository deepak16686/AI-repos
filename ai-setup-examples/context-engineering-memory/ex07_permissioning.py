"""Example 7 - Permissioning (production principle #3).

Talk: org-wide curated memory should be read-only for agents; an agent's own
scratchpad is read/write. A wrong org-wide write would reach every agent, so agents
PROPOSE and a human approves.
"""
import tempfile
from memlib import MemoryStore, PermissionDenied

store = MemoryStore(tempfile.mkdtemp())
store.write("org/standards.md", "- push images to ai-nexus:5001\n- SonarQube gate must pass\n", "human:alice", "curation", reason="curated")
A = "agent:pipeline-agent"


def attempt(label, fn):
    try:
        fn()
        print(f"  ALLOWED  {label}")
    except PermissionDenied as e:
        print(f"  DENIED   {label}  ({e})")


print("agent access matrix:")
attempt("read   org/standards.md", lambda: store.read("org/standards.md", A))
attempt("write  org/standards.md", lambda: store.write("org/standards.md", "x", A, "s1"))
attempt("write  agents/pipeline-agent/scratch.md (own)", lambda: store.write("agents/pipeline-agent/scratch.md", "wip", A, "s1"))
attempt("write  agents/other-agent/scratch.md (other)", lambda: store.write("agents/other-agent/scratch.md", "hijack", A, "s1"))
attempt("write  shared/notes.md (team scratch)", lambda: store.write("shared/notes.md", "hello", A, "s1"))

print("\nagent wants to improve org standards -> proposes, human approves:")
p = store.propose(A, "org/standards.md",
                  store.read("org/standards.md")[0] + "- Maven builds must use the nexus-mirror setting\n",
                  "sess-205", reason="repeated Maven failures")
print(f"  proposal stored at {p} (org/standards.md unchanged: {len(store.read('org/standards.md')[0].splitlines())} lines)")
try:
    store.approve(A, p, "sess-205")
except PermissionDenied as e:
    print(f"  agent tries to self-approve -> DENIED ({e})")
target, _ = store.approve("human:alice", p, "review-1")
print(f"  human:alice approved -> {target} now has {len(store.read(target)[0].splitlines())} lines")
last = store.versions(target)[-1]
print(f"  provenance: v{last['v']} by {last['actor']} - {last['reason']}")

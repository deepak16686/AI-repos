"""Example 5 - Versioning + provenance (production principle #1).

Talk: keep every version so you can roll back, and record which session/transcript
and which actor (agent or human) caused each change. Here an agent writes a bad
update, we find who/what caused it from the history, and roll back.
"""
import tempfile
from memlib import MemoryStore

store = MemoryStore(tempfile.mkdtemp())
P = "shared/standards.md"
store.write(P, "- run all 8 stages\n- SonarQube quality gate must pass\n", "human:alice", "onboarding", reason="initial standards")
t, h = store.read(P)
store.write(P, t + "- push images to ai-nexus:5001\n", "agent:pipeline-agent", "sess-101", expected_hash=h, reason="learned registry port")
t, h = store.read(P)
store.write(P, "- run 8 stages\n- skip SonarQube gate to speed up builds\n", "agent:troubleshooter", "sess-102", expected_hash=h,
            reason="'speed up builds'")


def show():
    print(f"{'v':<3} {'hash':<9} {'actor':<22} {'session':<11} reason")
    for r in store.versions(P):
        print(f"{r['v']:<3} {r['hash']:<9} {r['actor']:<22} {r['session']:<11} {r['reason']}")


print("history after the bad update:")
show()
print("\ncurrent content:\n" + store.read(P)[0])
bad = store.versions(P)[-1]
print(f"investigation: v{bad['v']} came from {bad['actor']} in {bad['session']} -> weakens the quality gate")

store.rollback(P, 2, "human:alice", "review-2026-10-16")
print("\nafter rollback to v2:")
show()
print("\ncurrent content:\n" + store.read(P)[0])
assert store.read(P)[1] == store.versions(P)[1]["hash"]
print("verified: content hash equals v2 hash; the bad version is still in history for audit")

"""Example 2 - Memory tools: the agent reads and writes memory in-band.

Talk: let the agent decide, DURING the session, when to look things up and when to
write a lesson down. Session 1 hits a Maven failure and records the fix; session 2
greps memory first and succeeds on the first attempt (the "continual learning" feel).
The agent here is a deterministic stand-in for an LLM; the memory behaviour is real.
"""
import tempfile
from memlib import MemoryStore

FIX = "nexus-mirror"
ME = "agent:pipeline-agent"
LESSONS = "agents/pipeline-agent/lessons.md"


def run_pipeline(settings):
    if FIX in settings:
        return True, "BUILD SUCCESS"
    return False, "ERROR: mvn dependency resolution failed: repo.maven.apache.org unreachable"


def agent_session(store, session):
    print(f"[{session}] task: generate + run pipeline for a Java repo")
    settings = set()
    hits = store.grep("maven", prefix="agents/pipeline-agent")          # in-band READ
    if hits:
        print(f"[{session}] memory hit: {hits[0][0]}:{hits[0][1]}  {hits[0][2]!r}")
        settings.add(FIX)
    else:
        print(f"[{session}] memory hit: none")
    attempts = 0
    while True:
        attempts += 1
        ok, msg = run_pipeline(settings)
        print(f"[{session}]   attempt {attempts}: {msg}")
        if ok:
            break
        settings.add(FIX)                                                # reason from error
        text, h = store.read(LESSONS, ME, missing_ok=True)               # in-band WRITE
        text += "- maven: builds must use the nexus-mirror setting (central is unreachable)\n"
        store.write(LESSONS, text, ME, session, expected_hash=h, reason="learned from failed build")
        print(f"[{session}]   wrote lesson to {LESSONS}")
    print(f"[{session}] done in {attempts} attempt(s)\n")
    return attempts


store = MemoryStore(tempfile.mkdtemp())
a1 = agent_session(store, "session-1")
a2 = agent_session(store, "session-2")
print(f"attempts: session-1={a1}, session-2={a2}  ->  improvement without any retraining")

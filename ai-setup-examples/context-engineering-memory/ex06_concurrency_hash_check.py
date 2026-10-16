"""Example 6 - Concurrency with a hash check (production principle #2).

Talk: before editing, take a hash; draft the edit; take another hash right before
writing; if they differ somebody else changed the file -> re-read and retry.
Eight agents append a note to the same file at the same moment, without and with
the check.
"""
import tempfile
import threading
from memlib import MemoryStore, ConflictError

N = 8
PATH = "shared/notes.md"


def run(use_check):
    store = MemoryStore(tempfile.mkdtemp())
    barrier = threading.Barrier(N)
    retries = [0] * N

    def worker(i):
        actor = f"agent:a{i}"
        text, h = store.read(PATH, actor, missing_ok=True)
        barrier.wait()                       # all agents have read the SAME version
        while True:
            try:
                store.write(PATH, text + f"- note from a{i}\n", actor, f"s{i}",
                            expected_hash=h if use_check else None)
                return
            except ConflictError:            # somebody wrote first: re-read, re-draft, retry
                retries[i] += 1
                text, h = store.read(PATH, actor)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    lines = len(store.read(PATH)[0].splitlines())
    return lines, sum(retries)


for label, check in (("WITHOUT hash check (last writer wins)", False), ("WITH hash check + retry", True)):
    lines, retries = run(check)
    print(f"{label}")
    print(f"  agents: {N}   notes in final file: {lines}   lost updates: {N - lines}   conflicts detected and retried: {'>= ' + str(N - 1) if retries >= N - 1 else retries}")

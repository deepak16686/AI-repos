# Context Engineering & Agent Memory - Runnable Examples

Self-contained, stdlib-only Python examples (Python 3.9+) for every concept in the AI DevCon talk (plus the model-swap scenario) on context engineering and agent memory. Each script prints its own result; `RESULTS.md` holds the captured source and output of all of them.

The agents are deterministic stand-ins for an LLM so results are reproducible. The memory behaviour (files, hashes, versions, permissions) is real. See `../../ai-setup-diagrams/context-engineering-memory-architecture.svg` (overall architecture) and `../../ai-setup-diagrams/model-swap-context-architecture.svg` (old model vs new model, with and without context).

## Run

```bash
python3 ex06_concurrency_hash_check.py   # any single example
python3 run_all.py                       # all examples, regenerates RESULTS.md
```

## Examples

| # | Script | Talk concept | What the output shows |
|---|--------|--------------|------------------------|
| 1 | `ex01_claude_md_bloat.py` | CLAUDE.md works but bloats | Token cost of 10 vs 1000 rules per session |
| 2 | `ex02_memory_tool_loop.py` | In-band memory tools | Session 1 needs 2 attempts and saves a lesson; session 2 needs 1 |
| 3 | `ex03_skills_progressive_disclosure.py` | Skills | 62 tokens of titles vs 4,673 tokens preloaded; body loaded only on match |
| 4 | `ex04_filesystem_memory_search.py` | Memory as a file system | Real `grep` finds the answer reading 1-2 files instead of all 42 |
| 5 | `ex05_versioning_provenance.py` | Versioning + provenance | Who/which session caused a bad write; rollback keeps audit trail |
| 6 | `ex06_concurrency_hash_check.py` | Concurrency (hash check) | 7 of 8 updates lost without the check; 0 lost with it |
| 7 | `ex07_permissioning.py` | Permissioning | Agents read org memory, cannot write it; propose, human approves |
| 8 | `ex08_portability.py` | Portability | JSON export/import preserves hashes and history; plain `cat`/`grep` works |
| 9 | `ex09_stale_and_injected_memory.py` | Stale / injected memory | Stale entry flagged; injection and gate-weakening proposals quarantined |
| 10 | `ex10_dreaming_consolidation.py` | Dreaming (illustrative) | Transcripts become a reviewed memory update (replace, prune, promote, watch) |
| 11 | `ex11_model_swap_context_portability.py` | New model, same context | Old model 5 -> 1 failed attempts as it learns; new model cold = 4; new model + existing context = 0 |

`memlib.py` is the shared governed memory store (versioning, hash-checked writes, permissions, proposals, grep, export/import).

## Notes

- Example 10 is a reconstruction: the source talk was cut off before the dreaming section.
- The permission policy in `memlib.py` (`org/`, `team/`, `project/` read-only for agents; `agents/<name>/`, `shared/`, `proposals/<name>/` writable) is a demonstration policy, not a standard.
- The in-process lock in `MemoryStore.write` stands in for an atomic compare-and-swap; a real multi-process store needs file locks or a database transaction.

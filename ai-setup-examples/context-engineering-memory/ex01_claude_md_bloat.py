"""Example 1 - CLAUDE.md: unreasonably effective, but it bloats.

Talk: a static markdown file injected at session start steers the agent very well,
but every rule you add is paid for in EVERY session. Shows the token cost of a
growing CLAUDE.md versus a slim one that points to on-demand memory.
"""
from memlib import tokens

RULE = "- Rule {i}: use the approved base image, registry host and stage order for project type {i}.\n"


def claude_md(n_rules):
    return "# CLAUDE.md\n" + "".join(RULE.format(i=i) for i in range(n_rules))


SESSIONS_PER_DAY = 100
print(f"{'rules':>6} {'tokens/session':>15} {'tokens/day (100 sessions)':>27}")
for n in (10, 50, 200, 1000):
    t = tokens(claude_md(n))
    print(f"{n:>6} {t:>15,} {t * SESSIONS_PER_DAY:>27,}")

slim = claude_md(10) + "- For anything else: grep memory/index.md, then read only the file you need.\n"
fat = claude_md(1000)
print()
print(f"slim CLAUDE.md (10 rules + pointer) : {tokens(slim):,} tokens/session")
print(f"fat  CLAUDE.md (1000 rules)         : {tokens(fat):,} tokens/session")
print(f"saving per session                  : {tokens(fat) - tokens(slim):,} tokens "
      f"({100 * (1 - tokens(slim) / tokens(fat)):.0f}%)")

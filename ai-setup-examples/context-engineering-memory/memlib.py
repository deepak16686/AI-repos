"""Minimal governed file-system memory used by every example (stdlib only).

Implements the production principles from the talk on top of plain Markdown files:
  * versioning + provenance  -> .history/<path>.jsonl (who, which session, why)
  * concurrency              -> write(expected_hash=...) is an optimistic lock
  * permissioning            -> can(): org/team/project are read-only for agents
  * portability              -> plain files + export_bundle()/import_bundle()
"""
import hashlib
import json
import re
import threading
from pathlib import Path


class ConflictError(Exception):
    """File changed between read and write (hash mismatch)."""


class PermissionDenied(Exception):
    """Actor may not perform this operation on this path."""


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()[:8]


def tokens(text):
    """Rough token estimate (~4 chars per token)."""
    return max(1, len(text) // 4)


class MemoryStore:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.hist = self.root / ".history"
        self._lock = threading.Lock()

    # ---- permissioning -------------------------------------------------
    def can(self, actor, path, op):
        kind, _, name = actor.partition(":")
        if op == "read" or kind == "human":
            return True
        top = path.split("/")[0]
        if top == "shared":                      # collaborative scratch area
            return True
        if top in ("agents", "proposals"):       # own sandbox only
            parts = path.split("/")
            return len(parts) > 1 and parts[1] == name
        return False                             # org/ team/ project/ -> read-only

    # ---- read / write --------------------------------------------------
    def read(self, path, actor="human:system", missing_ok=False):
        if not self.can(actor, path, "read"):
            raise PermissionDenied(f"{actor} cannot read {path}")
        p = self.root / path
        if not p.exists():
            if missing_ok:
                return "", digest("")
            raise FileNotFoundError(path)
        text = p.read_text()
        return text, digest(text)

    def write(self, path, text, actor, session, expected_hash=None, reason=""):
        if not self.can(actor, path, "write"):
            raise PermissionDenied(f"{actor} cannot write {path}")
        with self._lock:                         # makes check+write atomic in-process
            p = self.root / path
            current = p.read_text() if p.exists() else ""
            if expected_hash is not None and digest(current) != expected_hash:
                raise ConflictError(
                    f"{path}: expected {expected_hash}, found {digest(current)}")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
            hp = self.hist / (path.replace("/", "__") + ".jsonl")
            hp.parent.mkdir(parents=True, exist_ok=True)
            n = len(hp.read_text().splitlines()) + 1 if hp.exists() else 1
            rec = {"v": n, "hash": digest(text), "actor": actor,
                   "session": session, "reason": reason, "content": text}
            with hp.open("a") as fh:
                fh.write(json.dumps(rec) + "\n")
            return digest(text)

    def versions(self, path):
        hp = self.hist / (path.replace("/", "__") + ".jsonl")
        if not hp.exists():
            return []
        return [json.loads(line) for line in hp.read_text().splitlines()]

    def rollback(self, path, version, actor, session):
        rec = next(r for r in self.versions(path) if r["v"] == version)
        return self.write(path, rec["content"], actor, session,
                          reason=f"rollback to v{version}")

    # ---- proposals (agents -> review gate -> shared memory) -------------
    def propose(self, actor, target, text, session, reason=""):
        name = actor.partition(":")[2]
        p = f"proposals/{name}/{target.replace('/', '__')}"
        self.write(p, text, actor, session, reason=f"proposal for {target}: {reason}")
        return p

    def approve(self, reviewer, proposal_path, session):
        if not reviewer.startswith("human:"):
            raise PermissionDenied("only humans approve proposals")
        text, _ = self.read(proposal_path, reviewer)
        _, name, flat = proposal_path.split("/")
        target = flat.replace("__", "/")
        h = self.write(target, text, reviewer, session,
                       reason=f"approved proposal from agent:{name}")
        (self.root / proposal_path).unlink()
        return target, h

    # ---- search (what agents do with bash/grep/ls) ------------------------
    def ls(self, prefix=""):
        base = self.root / prefix
        return sorted(str(p.relative_to(self.root)) for p in base.rglob("*.md")
                      if ".history" not in p.parts)

    def grep(self, pattern, prefix=""):
        rx = re.compile(pattern, re.I)
        hits = []
        for path in self.ls(prefix):
            for i, line in enumerate((self.root / path).read_text().splitlines(), 1):
                if rx.search(line):
                    hits.append((path, i, line.strip()))
        return hits

    # ---- portability -----------------------------------------------------
    def export_bundle(self):
        return {p: {"content": (self.root / p).read_text(), "history": self.versions(p)}
                for p in self.ls()}

    def import_bundle(self, bundle):
        for path, item in bundle.items():
            p = self.root / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(item["content"])
            hp = self.hist / (path.replace("/", "__") + ".jsonl")
            hp.parent.mkdir(parents=True, exist_ok=True)
            hp.write_text("".join(json.dumps(r) + "\n" for r in item["history"]))

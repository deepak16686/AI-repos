"""Example 8 - Portability (production principle #4).

Talk: curated memory is valuable long-term, so keep it in a plain format behind a
clean API that other surfaces and systems can use. Here a store is exported to a
JSON bundle, imported into a completely separate store, and also read by a "second
surface" that uses nothing but the shell (cat/grep).
"""
import json
import subprocess
import tempfile
from memlib import MemoryStore

src = MemoryStore(tempfile.mkdtemp())
src.write("org/standards.md", "- push images to ai-nexus:5001\n", "human:alice", "s1", reason="initial")
t, h = src.read("org/standards.md")
src.write("org/standards.md", t + "- Maven uses nexus-mirror\n", "human:alice", "s2", expected_hash=h, reason="add maven rule")
src.write("projects/svc-17/notes.md", "- nexus login expires\n", "human:bob", "s3", reason="note")

bundle = src.export_bundle()
blob = json.dumps(bundle)
print(f"exported {len(bundle)} files + history to a JSON bundle ({len(blob)} bytes)")

dst = MemoryStore(tempfile.mkdtemp())                      # e.g. another product surface
dst.import_bundle(json.loads(blob))
for path in src.ls():
    same = src.read(path)[1] == dst.read(path)[1]
    print(f"  {path:<28} hash {src.read(path)[1]} == {dst.read(path)[1]}: {same}   versions: {len(src.versions(path))} -> {len(dst.versions(path))}")

print("\nsecond surface using only the shell, no library:")
for cmd in (["cat", "org/standards.md"], ["grep", "-rn", "nexus", "--include=*.md", "."]):
    print(f"$ {' '.join(cmd)}")
    print(subprocess.run(cmd, cwd=dst.root, capture_output=True, text=True).stdout.rstrip())

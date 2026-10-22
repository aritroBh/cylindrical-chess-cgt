"""Apply EDITS.md files (written by delegated tasks K1a/K1b/K1c) to a copy of the theory note.

Each edit's OLD text must occur exactly once in the current text, or the edit is rejected.
Usage (from the project root):
  python3 kings/delegate/apply_edits.py kings/theory/LOOPY.md OUT.md kings/delegate/out/K1a/EDITS.md [...]
Prints one line per edit: applied, or rejected with the reason.
"""
import re
import sys

src, dst, *edit_files = sys.argv[1:]
text = open(src).read()
pat = re.compile(r"^### EDIT ([^\n]*)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW", re.S | re.M)
ok = bad = 0
for ef in edit_files:
    for m in pat.finditer(open(ef).read()):
        label, old, new = m.group(1), m.group(2), m.group(3)
        n = text.count(old)
        if n == 1:
            text = text.replace(old, new)
            ok += 1
            print(f"applied  {ef.split('/')[-2]} EDIT {label}")
        else:
            bad += 1
            print(f"REJECTED {ef.split('/')[-2]} EDIT {label}: OLD occurs {n} times")
open(dst, "w").write(text)
print(f"{ok} applied, {bad} rejected -> {dst}")

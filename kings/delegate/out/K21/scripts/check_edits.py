"""K21: check that every OLD block of EDITS.md occurs exactly once in LOOPY.md (LOOPY.md is not modified)."""
import re, sys
loopy = open("/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md").read()
edits = open("/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K21/EDITS.md").read()
blocks = re.findall(r"### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW", edits, re.S)
print(len(blocks), "blocks")
cur = loopy
for label, old, new in blocks:
    n = cur.count(old)
    print("%-60s OLD occurrences: %d" % (label[:60], n))
    assert n == 1
    cur = cur.replace(old, new)
print("all apply; new length", len(cur), "old", len(loopy))

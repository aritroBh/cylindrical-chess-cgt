import re
L = open("/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md").read()
E = open("/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K21/EDITS.md").read()
blocks = re.findall(r"### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW", E, re.S)
print(len(blocks), "blocks; headings in file:", E.count("### EDIT "), " OLD markers:", E.count("<<<<<<< OLD"), " NEW markers:", E.count(">>>>>>> NEW"))
cur = L
for lab, old, new in blocks:
    print("%-55s OLD in original: %d, in progressively edited: %d" % (lab[:55], L.count(old), cur.count(old)))
    cur = cur.replace(old, new, 1)
print("final length", len(cur), "orig", len(L))
# internal cross refs in NEW text
refs = set(re.findall(r"(Theorem|Proposition|Corollary|Lemma|Definition) (\d+\.\d+[a-z]?[′']?)", "\n".join(b[2] for b in blocks)))
import collections
for k, v in sorted(refs):
    present = (f"**{k} {v}" in cur) or (f"{k} {v} (" in cur)
    print(k, v, "defined in new LOOPY:", present)

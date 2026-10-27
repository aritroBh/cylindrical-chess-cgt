# Step 3: from c78_cuts.tsv build the typed core library.  A "typed core" is (block, f, par, v): the block closed with
# an alternating wall starting with f ('W' = W2 first, 'B' = B4 first) of length L of parity par has the same nimber v
# for every tested L of that parity (even: 2,4,6; odd: 3,5,7).
import json
from collections import defaultdict
from lib import *
d = defaultdict(dict)   # (blockstr, f) -> {L: sig}
names = defaultdict(set)
for line in open("c78_cuts.tsv"):
    name, A, c, f, L, sig = line.rstrip("\n").split("\t")
    d[(A, f)][int(L)] = sig
    names[A].add(name)
lib = []
for (A, f), m in sorted(d.items()):
    for par, Ls in (("even", (2, 4, 6)), ("odd", (3, 5, 7))):
        sigs = [m[L] for L in Ls]
        if "ILLEGAL" in sigs: continue
        vs = [nimber(s) for s in sigs]
        if all(isinstance(v, int) for v in vs) and len(set(vs)) == 1:
            lib.append(dict(block=A, f=f, par=par, v=vs[0], src=sorted(names[A])[:3]))
# dedupe: the same (block, f, par)
print(len(lib), "typed stable cores from C7/C8/X cuts")
from collections import Counter
print(Counter((x['v'], x['f'], x['par']) for x in lib))
json.dump(lib, open("lib_big.json", "w"), indent=0)
for x in lib:
    if x['v'] >= 2 and len(x['block'].split()) <= 8 and x['src'][0].startswith(("P8", "Q8", "X")): print(x)

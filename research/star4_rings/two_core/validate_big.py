# Re-check every big typed core at longer walls (L = 8 even / 9 odd, plus 10 / 11) and keep only those still stable.
import json
from lib import *
ev = Evaluator("results.tsv", tbits=23, nodelim=20000000)
big = json.load(open("lib_big.json"))
ok = []; bad = []
for x in big:
    A = R(x['block']); Ls = (8, 10) if x['par'] == 'even' else (9, 11)
    vs = []
    for L in Ls:
        full = A + wall(L, x['f'])
        vs.append(nimber(ev.sig(full)) if legal_start(full) else 'ILL')
    x['v_long'] = vs
    (ok if all(v == x['v'] for v in vs) else bad).append(x)
print("kept", len(ok), "dropped", len(bad))
from collections import Counter
print("kept by v:", Counter(x['v'] for x in ok), "dropped by v:", Counter(x['v'] for x in bad))
json.dump(ok, open("lib_big_ok.json", "w"))
json.dump(bad, open("lib_big_unstable.json", "w"))

# k-core rings (k = 3, 4) with matched walls: ring value vs nim-sum.  Cores: stable typed cores of the library.
import sys, json, random
from lib import *
random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 3)
NR = int(sys.argv[1]) if len(sys.argv) > 1 else 60
lib = json.load(open("lib_all.json"))
pool = lib['big'] + lib['small1'] + lib['small0']
opp = lambda f: 'B' if f == 'W' else 'W'
lastof = lambda x: x['f'] if x['par'] == 'odd' else opp(x['f'])
ev = Evaluator("results_triple.tsv", tbits=23, nodelim=3000000, extra=("results.tsv", "results_blocks.tsv"))
out = open("triple.tsv", "w")
out.write("k\tsame_f\tcores\tvals\tn\tring\tsig\tval\tpred\n")
done = 0; tries = 0
while done < NR and tries < 5000:
    tries += 1
    k = random.choice((3, 3, 4))
    same = random.random() < 0.6
    if same:
        f0 = random.choice("WB"); par0 = random.choice(("even", "odd"))
        cand = [x for x in pool if x['f'] == f0 and x['par'] == 'even']     # same handedness, even type
    else:
        cand = [x for x in pool if x['par'] == 'even']
    cores = [random.choice(cand) for _ in range(k)]
    # make sure at least one core has value >= 1 and sizes small enough
    if sum(len(c['block'].split()) for c in cores) > 14: continue
    ring = []; lens = []
    for i in range(k):
        c, d = cores[i], cores[(i + 1) % k]
        first, last = c['f'], lastof(d)
        odd = first == last
        L = random.choice((3, 5) if odd else (2, 4))
        ring += R(c['block']) + wall(L, first)
    if len(ring) > 24 or not legal_start(ring): continue
    sig = ev.sig(ring)
    pred = 0
    for c in cores: pred ^= c['v']
    out.write("\t".join(map(str, [k, int(len(set(c['f'] for c in cores)) == 1), "|".join(c['block'] + ":" + c['f'] + c['par'][0] for c in cores),
                                  ",".join(str(c['v']) for c in cores), len(ring), S(ring), sig, nimber(sig), pred])) + "\n"); out.flush()
    done += 1
print("done", done)

"""Extra checks: (a) all 5290 candidates, e.p. off: textbook vs e.p.-aware root+children identical;
(b) per-rule values of the 20 v1 halves under the e.p.-aware test."""
import sys, threading, json
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/verify/bench/C1-refute')
import indep as I
def run():
    cands = I.candidates()
    models = {}
    diff_off = 0; diff_on = 0
    for rule in I.RULES:
        for w, p in cands:
            a = I.evaluate(w, p, False, rule, False, models); b = I.evaluate(w, p, True, rule, False, models)
            if a[0] is not b[0] or any(a[1][k] is not b[1][k] for k in a[1]): diff_off += 1
            a = I.evaluate(w, p, False, rule, True, models); b = I.evaluate(w, p, True, rule, True, models)
            if a[0] is not b[0] or any(a[1][k] is not b[1][k] for k in a[1]): diff_on += 1
    print("all candidates x 3 rules: (cand,rule) pairs differing, e.p. off:", diff_off, " e.p. on:", diff_on)
    out = json.load(open('/Users/aritro/Downloads/Research/Chessendgames/verify/bench/C1-refute/indep_out.json'))
    for t in out['halves']:
        r = next(x for x in out['changed'] if x['pos'] == t)
        ps = r['per_setting']
        print(t, '| tb', ps['count,ep=True']['tb'], '| aware count:', ps['count,ep=True']['aw'][:40], '| mover:', ps['mover,ep=True']['aw'][:40], '| opp:', ps['opponent,ep=True']['aw'][:40])
threading.stack_size(512*1024*1024)
th = threading.Thread(target=run); th.start(); th.join()

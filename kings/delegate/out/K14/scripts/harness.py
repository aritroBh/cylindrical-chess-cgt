#!/usr/bin/env python3
"""K14 harness: embed a candidate group + a context in flat/cyl boards, run kpp (P model, real kings) and/or kp
(chess, cap 1) through the shared heavy lock, and compare with the D-model prediction for G (+) dud_D (dmodel.py).

usage: harness.py CANDS.jsonl CONTEXTS.jsonl OUT.jsonl MODEL(p|c|pc) [first N contexts] [max candidates]
Every output row: group, context, state (a,b), stm, prediction, result(s), match flag."""
import sys, json, subprocess, os
sys.path.insert(0, os.path.dirname(__file__))
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAVY = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh'
# K14_DIRECT=1: run under plain nice (only for runs that are far below one CPU-minute, e.g. contexts of <= 3 pawns)
HCMD = ['nice', '-n', '15'] if os.environ.get('K14_DIRECT') else [HEAVY]
cands_f, ctx_f, out_f, model = sys.argv[1:5]
nctx = int(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 9
ncand = int(sys.argv[6]) if len(sys.argv) > 6 else 10 ** 9
W = 7


def nm(s, W=7): return chr(97 + s % W) + str(s // W + 1)


def run(binname, board, extra, posl):
    p = subprocess.run(HCMD + [os.path.join(D, 'bin', binname), '--board', board, '--ep', 'on', '--promote', 'QRBN', '--cap', '1'] + extra,
                       input='\n'.join(posl) + '\n', capture_output=True, text=True)
    res = {}
    for line in p.stdout.splitlines():
        if ' | ' not in line: continue
        pos, r = line.split(' | ')[:2]
        res[pos.strip()] = r.split()[:2]
    return res


seen, cands = set(), []
for l in open(cands_f):
    r = json.loads(l); key = json.dumps([r['board'], r['K'], r['k'], r['P'], r['p']])
    if key in seen: continue
    seen.add(key); cands.append(r)
cands.sort(key=lambda r: r['score'])
cands = cands[:ncand]
ctxs = [json.loads(l) for l in open(ctx_f)][:nctx]
out = open(out_f, 'a')
for c in cands:
    zs = [(nm(a), nm(b)) for a in c['K'] for b in c['k']]
    base = ' '.join(['P' + nm(s) for s in c['P']] + ['p' + nm(s) for s in c['p']])
    posl, meta = [], []
    for cx in ctxs:
        pw = ' '.join('P' + n for n in cx['w']); pb = ' '.join('p' + n for n in cx['b'])
        for (a, b) in zs:
            for stm in 'wb':
                pos = 'K%s k%s %s %s %s %s -' % (a, b, base, pw, pb, stm)
                pos = ' '.join(pos.split())
                posl.append(pos); meta.append((cx, a, b, stm))
    rp = run('kpp', c['board'], ['--pmodel'], posl) if 'p' in model else {}
    rc = run('kp', c['board'], [], posl) if 'c' in model else {}
    bad = 0
    for pos, (cx, a, b, stm) in zip(posl, meta):
        pred = cx['dud'][0 if stm == 'w' else 1]
        row = {'group': c, 'ctx': cx, 'state': [a, b], 'stm': stm, 'pos': pos, 'pred': pred, 'P': rp.get(pos), 'C': rc.get(pos)}
        ok = True
        if 'p' in model: ok &= (rp.get(pos) == [pred, pred])
        if 'c' in model: ok &= (rc.get(pos) == [pred, pred])
        row['ok'] = ok; bad += (not ok)
        out.write(json.dumps(row) + '\n')
    out.flush()
    print(nm(c['K'][0]), nm(c['K'][1]), nm(c['k'][0]), nm(c['k'][1]), base, 'score', c['score'], 'mismatches', bad, '/', len(posl), flush=True)

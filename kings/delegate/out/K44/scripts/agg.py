#!/usr/bin/env python3
"""K44 aggregator over logs/fsig_*.txt.  Line formats (written by kg44 --fsig):
 board|region|faithful|config|class|roots|short|stopper|signature     (roots = distinct full-pawn-set roots of the configuration)
 EX|config|signature|example roots
Prints class tables and the set of signatures new relative to the K20-convention baseline."""
import glob, os, sys, collections, re, json
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
order = ["0","*","+1","-1","+2","-2","+3","-3","1/2","-1/2","up","down","up*","down*","*2","on","off","dud","over","under","tis","tisn","{+|}","{|-}","{+|-}","{+|0}","{0|-}","{1|0}","{0|-1}","{2|0}","{0|-2}","{+|on}","{off|-}","{on|off}"]
HOT = {'{+|}', '{|-}', '{+|-}', '{+|0}', '{0|-}', '{+|on}', '{off|-}'}
iD = order.index('dud')
def cls_of(nm, sig):
    if nm == 'UNMATCHED':
        return 'loopy, not classified (quiet)' if sig[2*iD:2*iD+2] == '11' else 'loopy, not classified (decisive)'
    return ('decisive ' + nm) if nm in HOT else nm
def load(kind):
    rows = []; ex = {}
    for f in sorted(glob.glob(D + '/logs/fsig_%s_*.txt' % kind)):
        m = re.match(r'fsig_%s_(\d+)_(\w+)\.txt' % kind, os.path.basename(f))
        W, reg = int(m.group(1)), m.group(2)
        for l in open(f):
            l = l.rstrip('\n')
            if l.startswith('EX|'):
                _, cfg, sig, e = l.split('|', 3); ex[(W, reg, cfg, sig)] = e; continue
            head, cnt, sh, st, sig = l.rsplit('|', 4); b, rg, fa, cfg, nm = head.split('|', 4)
            rows.append(dict(W=W, reg=reg, faith=int(fa), cfg=cfg, nm=nm, cnt=int(cnt), sh=int(sh), st=int(st), sig=sig, rg=rg))
    return rows, ex
if __name__ == '__main__':
    new, exn = load('new'); base, exb = load('base')
    def sigset(rows, faith=None, Ws=None):
        return {r['sig'] for r in rows if (faith is None or r['faith'] == faith) and (Ws is None or r['W'] in Ws)}
    S0 = sigset(base); S0f = sigset(base, 1); S068 = sigset(base, None, {6, 7, 8})
    print('baseline distinct signatures: all %d, faithful %d, boards 6-8 %d' % (len(S0), len(S0f), len(S068)))
    # per board/region class table (new runs, faithful vs all)
    for kind, rows in (('base', base), ('new', new)):
        print('\n== %s ==' % kind)
        tab = collections.defaultdict(lambda: collections.Counter()); tabf = collections.defaultdict(lambda: collections.Counter()); ncfg = collections.defaultdict(set)
        for r in rows:
            k = (r['W'], r['reg']); c = cls_of(r['nm'], r['sig'])
            tab[k][c] += r['cnt']; ncfg[k].add((r['cfg'], r['faith']))
            if r['faith']: tabf[k][c] += r['cnt']
        for k in sorted(tab):
            print(k, 'configs', len(ncfg[k]), 'faithful', sum(f for _, f in ncfg[k]), 'roots', sum(tab[k].values()), {a: b for a, b in sorted(tab[k].items())})
    # new signatures
    newsig = collections.defaultdict(list)
    for r in new:
        if r['sig'] not in S0: newsig[r['sig']].append(r)
    print('\nsignatures in the new runs not in baseline (any board, any region):', len(newsig))
    named = [s for s, v in newsig.items() if v[0]['nm'] != 'UNMATCHED']
    print('  of which carry a B34 name:', len(named))
    for s in named: print('   NAMED', newsig[s][0]['nm'], s)
    json.dump({s: [dict(W=r['W'], reg=r['reg'], faith=r['faith'], cfg=r['cfg'], cnt=r['cnt']) for r in v] for s, v in newsig.items()}, open(D + '/logs/new_signatures.json', 'w'))

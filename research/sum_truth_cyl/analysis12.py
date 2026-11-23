import json, os, sys
D = os.path.dirname(os.path.abspath(__file__))
PRED = {"L": ("W", "W"), "R": ("L", "L"), "N": ("W", "L"), "P": ("L", "W")}
RK = {'L': 0, 'D': 1, 'W': 2}
def load(name):
    f = f'{D}/jobs12/{name}_cap1.json'
    return json.load(open(f)) if os.path.exists(f) else None
def res(r, i):
    """returns (hi, lo) tokens for line i"""
    t = r['stdout'][i].split('|')[1].split(); return t[0], t[1]
def judge(r, pred):
    """per side: 'exact-match','exact-MISMATCH','consistent(bounds)','CONTRADICTS(bounds)'"""
    out = []
    for i in (0, 1):
        hi, lo = res(r, i); p = pred[i]
        if hi == lo: out.append('exact-match' if p == hi else 'exact-MISMATCH')
        else: out.append('bounds-consistent' if RK[lo] <= RK[p] <= RK[hi] else 'bounds-CONTRADICT')
    return out
def solo(line0):
    # match on the stored position, not the file name: names differing only in case collide on macOS
    import glob
    for f in glob.glob(f'{D}/jobs12/solo*_cap1.json'):
        r = json.load(open(f))
        if r['lines'][0] == line0 and r.get('stdout'): return r
    return None
def rows(items, prefix, idxs):
    for i in idxs:
        it = items[i]; r = load(f'{prefix}{i:02d}')
        if r is None: yield i, it, None; continue
        yield i, it, r
if __name__ == '__main__':
    which = sys.argv[1]
    items = json.load(open(D + ('/pairs.json' if which == '1' else '/pairs2.json')))
    prefix = 'pair' if which == '1' else 'p2_'
    idxs = [1, 9, 21, 22, 26, 29, 35, 40, 48] if which == '1' else range(len(items))
    for i, it, r in rows(items, prefix, idxs):
        if r is None: print(i, 'NOT DONE'); continue
        o = it['ep-aware']['outcome']; tb = it['textbook']['outcome']
        sw = [x.split('|')[1].strip() for x in r['stdout']]
        print(i, it['A'], '+', it['B'], '| vals', it['ep-aware_A']['value'], it['ep-aware_B']['value'], '=', it['ep-aware']['value'], o, 'tb', tb,
              '| real w:', sw[0], 'b:', sw[1], '|', judge(r, PRED[o]), '| rss %.1fGB' % (r['maxrss_bytes'] / 1e9), r['secs'], 'killed' if r['killed_over_limit'] else '')
        for t in 'AB':
            s = solo(it['solo' + t][0]); c = it['ep-aware_' + t]
            print('    solo', t, c['value'], c['outcome'], [x.split('|')[1].strip() for x in s['stdout']], judge(s, PRED[c['outcome']]) if c['outcome'] in PRED else '')

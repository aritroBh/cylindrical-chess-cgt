#!/usr/bin/env python3
"""compare census JSON docs (several concatenated per file) between an old run and a rerun; match by (root_passers, ignore_leak)"""
import sys, json
dec = json.JSONDecoder()
def docs(f):
    s = open(f).read(); i = 0; out = []
    while i < len(s):
        while i < len(s) and s[i].isspace(): i += 1
        if i >= len(s): break
        o, i = dec.raw_decode(s, i); out.append(o)
    return out
old = {(d['root_passers'], d['ignore_leak']): d for d in docs(sys.argv[1])}
new = {(d['root_passers'], d['ignore_leak']): d for d in docs(sys.argv[2])}
ok = True
for k, n in new.items():
    o = old.get(k)
    if o is None: print('  no old doc for', k, '(new only)'); continue
    diffs = [f for f in ('board', 'files', 'wmax', 'bmax', 'roots', 'total', 'distinct_groups', 'by_ij', 'selfcheck_violations') if o.get(f) != n.get(f)]
    print('  %s: %s' % (k, 'IDENTICAL on board/files/wmax/bmax/roots/total/distinct/by_ij/selfcheck' if not diffs else 'DIFFERS in ' + ','.join(diffs)))
    ok = ok and not diffs
print('RESULT', 'identical' if ok else 'DIFFERENT')

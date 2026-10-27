"""K19: compare own P (own_P_*.json), kp_p (P, logs/kpp_*.txt) and kp (chess, logs/kp_*.txt) for every position set."""
import json, os, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sets = ['s51', 's52', 's52f', 's52a', 's52h', 's55']
summary = {}
allok = True
for s in sets:
    own = json.load(open(os.path.join(D, 'own_P_%s.json' % s)))
    kpp = [l for l in open(os.path.join(D, 'logs', 'kpp_%s.txt' % s)).read().splitlines() if '|' in l]
    kpf = os.path.join(D, 'logs', 'kp_%s.txt' % s)
    kp = [l for l in open(kpf).read().splitlines() if '|' in l] if os.path.exists(kpf) else None
    print('==', s, own['board'])
    for i, row in enumerate(own['rows']):
        a, b = kpp[i].split('|')[1].split()[:2]
        pv = a if a == b else a + '/' + b
        c = ''
        if kp is not None:
            ca, cb = kp[i].split('|')[1].split()[:2]
            c = ca if ca == cb else ca + '/' + cb
        ok = (pv == row['P_white_pov'])
        allok &= ok
        print('  %-40s own_P=%s kp_p=%s %s chess(kp)=%s' % (row['pos'], row['P_white_pov'], pv, 'OK' if ok else 'MISMATCH', c))
        summary.setdefault(s, []).append({'pos': row['pos'], 'own_P': row['P_white_pov'], 'kp_p': pv, 'chess_kp': c or None})
print('own P vs kp_p all agree:', allok)
json.dump(summary, open(os.path.join(D, 'fullboard_summary.json'), 'w'), indent=1)

#!/usr/bin/env python3
# summ.py LOGS... : summarise GRP lines: per log, groups, solver disagreements, survivors (Phi==Psi on all contexts), failing
import sys, re
for fn in sys.argv[1:]:
    g = s = f = d = 0; surv = []; fail = 0; psi = ''
    for l in open(fn):
        if l.startswith('PSI'): psi = l.strip()
        m = re.match(r'GRP \S+ \| (.*?) \| contexts (\d+) \| Phi solver disagreements (\d+) \| Phi!=Psi: kp (\d+) ref3 (\d+) either (\d+)', l)
        if not m: continue
        g += 1; d += int(m.group(3))
        if int(m.group(6)) == 0: surv.append(m.group(1))
        else: f += 1
        if int(m.group(4)) != int(m.group(5)): print('  kp/ref3 differ in #contexts:', m.group(1))
    print('%s: groups %d, Phi solver disagreements %d, survivors %d, failing %d | %s' % (fn, g, d, len(surv), f, psi[:140]))
    for z in surv: print('   survivor:', z)

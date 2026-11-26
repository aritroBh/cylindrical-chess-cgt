"""K65: one line block per checked group: position, shuttle, freezes, q's (from def48's ref3m log), Definition 4.8 by
ref3m and kp_p, (B1) by vgsum59 and pr57.  usage: report.py <groups file> ..."""
import os, re, sys
def rd(p): return open(p).read() if os.path.exists(p) else ''
for gf in sys.argv[1:]:
    for line in open(gf):
        if '|' not in line or line.startswith('#'): continue
        tag, G, z1 = [x.strip() for x in line.split('|')]
        r = rd('logs/grp/%s_def48_ref3m.txt' % tag); k = rd('logs/grp/%s_def48_kpp.txt' % tag)
        d = '%s/%s' % (r.split()[0] if r else '?', k.split()[0] if k else '?')
        fz = re.findall(r"'(P\w+) at K\w+ k(\w\d)'", r)
        qs = re.findall(r'q S to move (.*?) : ', r)
        c = rd('logs/grp/%s_cmp.txt' % tag)
        vg = rd('logs/grp/%s_vgsum.out' % tag); pr = rd('logs/grp/%s_pr57.out' % tag)
        nv = len(re.findall(r'B1\(sum rule', vg)); bad = re.findall(r'^\s+(\S+)\s+->.*B1\(sum rule, -1\)=not W', vg, re.M)
        nbad_pr = len(re.findall(r'\(N1\) no', pr)); npr = len(re.findall(r'\(N1\) (?:yes|no)', pr))
        if nv == 0 and npr == 0: b1 = '(B1) NOT CHECKED (vgsum59 and pr57 over 2.2 GB)'
        elif npr == 0: b1 = ('(B1) holds at all %d non-shuttle Black root moves by vgsum59 only (pr57 over 2.2 GB): COMPUTED-1' % nv) if not bad else ('(B1) FAILS at %s (of %d moves) by vgsum59 only (pr57 over 2.2 GB): COMPUTED-1' % (', '.join(bad), nv))
        elif 'AGREE' in c: b1 = '(B1) holds at all %d non-shuttle Black root moves (vgsum59 and pr57): CHECKED-2' % nv
        else: b1 = '(B1) FAILS at %s (of %d moves; vgsum59 sum rule, and pr57 (N1) no; see findings for pr57 beside -1)' % (', '.join(bad), nv)
        print('%s  %s /%s  Def 4.8 ref3m/kp_p %s' % (tag, G, z1, d))
        print('    freezes: %s; q (Black to move): %s' % ('; '.join('%s at k%s' % f for f in fz), ' | '.join(qs)))
        print('    ' + b1)

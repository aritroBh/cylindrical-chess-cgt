# K65 referee: compare the freezes and q's of findings.txt section 3 with ax65's Definition 4.8 logs, all 38 groups.
import re
F = open('../findings.txt').read()
bad = 0
for l in open('src/groups38.txt'):
    nm, pcs, z0, z1 = l.strip().split('|')
    blk = F[F.index('\n' + nm + '  '):]; fr = re.search(r'freezes: (.*?); q \(Black to move\): (.*)', blk)
    want = sorted(re.findall(r'P(\w\d\w\d) at k(\w\d)', fr.group(1)))
    qs = sorted(' '.join(sorted(q.split()[:-2])) for q in fr.group(2).split(' | '))
    log = open(f'logs/g/{nm}.out').read()
    got = sorted((a, z) for a, z in re.findall(r'freeze P(\w\d\w\d) at (\w\d) ->', log))
    gq = sorted(' '.join(sorted(q.split())) for q in re.findall(r'-> q = (.*?) [bw] ', log))
    ok = want == got and qs == gq and 'exact (0 failures)' in log
    bad += not ok
    print(nm, 'freezes and q agree, exact' if ok else f'DIFFER findings {want} {qs} ax65 {got} {gq}')
print('groups differing:', bad)

#!/usr/bin/env python3
# K31 task 2: class of every placement of both kings on the antipodal file, single pair a<r>, cyl:WxH (kg_wide roots file).
import subprocess, sys, os
BIN = os.path.dirname(os.path.abspath(__file__)) + '/../bin'
def matrix(W, H, r):
    rf = '/tmp/k31_mx_%d_%d_%d.roots' % (W, H, r)
    subprocess.run(['nice','-n','15',BIN+'/kgw','--board','cyl:%dx%d'%(W,H),'--only','a%d'%r,'--maxpairs','1','--roots',rf],capture_output=True)
    M = {}
    for line in open(rf):
        parts = line.rstrip('\n').split('|'); p = parts[1]; nm = '|'.join(parts[2:-2]).split('=')[0]
        if 'P' not in p: continue
        d = {}
        for tok in p.split(): d[tok[0]] = (ord(tok[1])-97, int(tok[2:]))
        if W % 2 == 0 and d['K'][0] == W//2 and d['k'][0] == W//2:
            M[(d['K'][1], d['k'][1])] = nm
    os.remove(rf)
    return M
if __name__ == '__main__':
    W, H, r = map(int, sys.argv[1:4])
    M = matrix(W, H, r)
    ab = {'+1':'+','-1':'-','0':'0','*':'*','dud':'d','on':'n','off':'f','tis':'t','tisn':'u','{1|0}':'A','{0|-1}':'B','{on|off}':'X','UNMATCHED':'.'}
    print('cyl:%dx%d pair a%d/a%d, kings on file %s; rows = White king rank, cols = Black king rank' % (W,H,r,r+1,chr(97+W//2)))
    print('     ' + ' '.join('%2d'%b for b in range(1,H+1)))
    for a in range(1,H+1):
        print('  %2d ' % a + ' '.join(' ' + ab.get(M.get((a,b),'?'), '?') if (a,b) in M else ' _' for b in range(1,H+1)))
    print('legend: + is +1, - is -1, 0 zero, * star, d dud, n on, f off, t tis, u tisn, A {1|0}, B {0|-1}, X {on|off}, . other (decisive or loopy unclassified), _ illegal')

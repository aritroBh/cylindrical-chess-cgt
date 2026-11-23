"""K49: write test-game files for kn.c.  Usage: python tgames.py std > std.t"""
import sys
nodes, roots = [], []
def node():
    nodes.append(([], [])); return len(nodes) - 1
def std():
    z = node(); pos = {0: z}; neg = {0: z}
    for i in range(1, 13):
        a = node(); nodes[a][0].append(pos[i-1]); pos[i] = a
        b = node(); nodes[b][1].append(neg[i-1]); neg[i] = b
    roots.extend([(str(-i), neg[i]) for i in range(12, 0, -1)] + [('0', z)] + [(str(i), pos[i]) for i in range(1, 13)])
    on = node(); nodes[on][0].append(on)
    off = node(); nodes[off][1].append(off)
    dud = node(); nodes[dud][0].append(dud); nodes[dud][1].append(dud)
    ov = node(); nodes[ov][0].append(z); nodes[ov][1].append(ov)
    un = node(); nodes[un][0].append(un); nodes[un][1].append(z)
    st = node(); nodes[st][0].append(z); nodes[st][1].append(z)
    up = node(); nodes[up][0].append(z); nodes[up][1].append(st)
    dn = node(); nodes[dn][0].append(st); nodes[dn][1].append(z)
    p1 = pos[1]; m1 = neg[1]; pm = node(); nodes[pm][0].append(p1); nodes[pm][1].append(m1)
    roots.extend([('on', on), ('off', off), ('dud', dud), ('over', ov), ('under', un), ('*', st), ('up', up), ('down', dn), ('+-1', pm)])
    return z, on, off
if sys.argv[1] == 'std':
    std()
elif sys.argv[1] == 'zoff':   # {0 | off}, and {| {0|off}}
    z = node(); off = node(); nodes[off][1].append(off)
    a = node(); nodes[a][0].append(z); nodes[a][1].append(off)
    b = node(); nodes[b][1].append(a)
    roots.extend([('0', z), ('off', off), ('0|off', a), ('|{0|off}', b)])
print(len(nodes))
for L, R in nodes:
    print('L:', *L, '; R:', *R)
for n, r in roots:
    print(n, r)

"""K77 referee: compare p74 (-m) and s77 (-t p -m) outputs: the value of every position and of every legal move.
usage: python cmp77.py <p74 out> <s77 out>"""
import sys


def rd(p):
    res, cur = {}, None
    for line in open(p):
        if not line.strip():
            continue
        if not line.startswith("   "):
            t, v = line.rstrip("\n").rsplit("  ", 1)
            cur = t.strip()
            res[cur] = (v.split("=")[1], {})
        else:
            m, v = line.split()
            res[cur][1][m] = v
    return res


a, b = rd(sys.argv[1]), rd(sys.argv[2])
npos = nmv = bad = 0
for k in a:
    if k not in b:
        print("missing in s77:", k); bad += 1; continue
    npos += 1
    if a[k][0] != b[k][0]:
        print("value differs:", k, a[k][0], b[k][0]); bad += 1
    if set(a[k][1]) != set(b[k][1]):
        print("move lists differ:", k, sorted(set(a[k][1]) ^ set(b[k][1]))); bad += 1
    for m in a[k][1]:
        nmv += 1
        if m in b[k][1] and a[k][1][m] != b[k][1][m]:
            print("move value differs:", k, m, a[k][1][m], b[k][1][m]); bad += 1
print("%d positions, %d moves compared, %d differences" % (npos, nmv, bad))

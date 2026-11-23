# writes test-game files for vk.c; node 0 is the root
import os
G = {}
def w(name, nodes):
    with open(f"t/{name}.t", "w") as f:
        f.write(f"{len(nodes)}\n")
        for nm, L, R in nodes:
            f.write(f"{nm} {len(L)} {' '.join(map(str,L))} {len(R)} {' '.join(map(str,R))}\n")
w("zero", [("0", [], [])])
w("on", [("on", [0], [])])
w("off", [("off", [], [0])])
w("dud", [("dud", [0], [0])])
w("over", [("over", [1], [0]), ("0", [], [])])
w("under", [("under", [0], [1]), ("0", [], [])])
w("star", [("*", [1], [1]), ("0", [], [])])
w("up", [("up", [1], [2]), ("0", [], []), ("*", [1], [1])])
w("down", [("down", [2], [1]), ("0", [], []), ("*", [1], [1])])
w("pm1", [("pm1", [1], [2]), ("1", [3], []), ("-1", [], [3]), ("0", [], [])])
w("onstar", [("on*", [0, 1], [1]), ("on", [1], [])])
w("zoff", [("{0|off}", [1], [2]), ("0", [], []), ("off", [], [2])])
for n in range(1, 4):
    # +n: node i = i-1 tokens? root = n, chain n->n-1->..->0
    w(f"p{n}", [(str(n - i), [i + 1] if i < n else [], []) for i in range(n + 1)])
    w(f"m{n}", [(str(-(n - i)), [], [i + 1] if i < n else []) for i in range(n + 1)])
w("zdud", [("{0|dud}", [1], [2]), ("0", [], []), ("dud", [2], [2])])

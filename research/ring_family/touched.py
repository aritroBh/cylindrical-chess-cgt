import sys, re
sys.path.insert(0, "research/ring_family")
from ringlib import *
from pump_check import fam, dump
sq = re.compile(r"([a-u])(\d)")
def parse_state(s):
    head, _, ep = s.partition(" ep")
    w, b = head.split(" / B:")
    return frozenset(w[2:].split()), frozenset(b.split())
def touched(edges):
    t = set(); movers = set()
    for a, side, mv, b in edges:
        A = parse_state(a)
        # file of the moving pawn = first letter of the move description
        movers.add(ord(mv[0]) - 97)
        if b == "TERMINAL-WIN": 
            m = re.match(r"([a-u])(\d)(?:-|x)([a-u])(\d)", mv)
            t.add(ord(m.group(1)) - 97); t.add(ord(m.group(3)) - 97)
            continue
        B_ = parse_state(b)
        for x in (A[0] ^ B_[0]) | (A[1] ^ B_[1]): t.add(ord(x[0]) - 97)
    return t, movers
if __name__ == "__main__":
    name = sys.argv[1]
    for k in [int(x) for x in sys.argv[2:]]:
        ring = fam(name, k); edges = dump(ring, f"research/ring_family/dumps/{name}_k{k}.tsv")
        t, m = touched(edges)
        n = len(ring)
        print(f"{name} k={k} C{n}: files {cstr(ring)}")
        print("   touched files (content changes or terminal-win moves):", "".join(chr(97+f) for f in sorted(t)), " | files from which kept moves originate:", "".join(chr(97+f) for f in sorted(m)))

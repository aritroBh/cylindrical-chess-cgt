import sys
sys.path.insert(0, "research/ring_family")
from ringlib import *
def chains(core, unit_a, unit_b, Lmax):
    """core + alternating chain unit_a unit_b unit_a ... of length L, both orientations"""
    out = []
    for L in range(0, Lmax + 1):
        for first, second in ((unit_a, unit_b), (unit_b, unit_a)):
            ch = tuple((first, second)[i % 2] for i in range(L))
            out.append((L, first == unit_a, ch))
    return out
if __name__ == "__main__":
    core = from_cstr(sys.argv[1]); a = from_cstr(sys.argv[2])[0]; b = from_cstr(sys.argv[3])[0]
    Lmax = int(sys.argv[4])
    for L, fa, ch in chains(core, a, b, Lmax):
        r = core + ch
        if len(r) < 3: continue
        res = evaluate([r])
        print(f"L={L} {'a-first' if fa else 'b-first'} C{len(r)} pawns={nparts(r)} {cstr(r)} -> {res[0]}", flush=True)

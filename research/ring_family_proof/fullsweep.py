"""Reduction-free full-game search (rg solve, no deletion of any move) of G + *h, h = 0..3, for every member of the three
families with 5 <= n <= 61 (the engine's limit is 64 files).  *2 means: outcomes N N P N for h = 0,1,2,3.
Usage: python fullsweep.py [nmax]"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam

def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 61
    bad = 0; tot = 0
    for famname, ns in (("odd", [n for n in range(5, nmax + 1) if n % 2]), ("even", [n for n in range(6, nmax + 1) if n % 2 == 0]),
                        ("F", [n for n in range(5, nmax + 1) if n == 5 or n >= 7])):
        t0 = time.time(); nodes = 0; res = set()
        for n in ns:
            toks = fam.FAMILIES[famname](n)
            assert fam.ntoks_pawns(toks) == n + 3
            out = fam.run_rg("solve", " ".join(toks) + "\n", extra=("3",)).split()
            sig = out[0]; nodes += int(out[1].split("=")[1]); res.add(sig); tot += 1
            if sig != "NNPN": bad += 1; print("NOT *2:", famname, n, sig)
        print(f"{famname}: n = {ns[0]}..{ns[-1]} ({len(ns)} rings, n+3 pawns each): outcome strings {sorted(res)}; search nodes {nodes}; {time.time()-t0:.1f}s")
    print(f"total {tot} rings, not *2: {bad}")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main() else 0)

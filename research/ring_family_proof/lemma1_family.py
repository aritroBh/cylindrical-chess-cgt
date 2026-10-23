"""Lemma 1 on the family members: outcome strings of G + *h (h = 0..7) from the unreduced search and from the reduced graph agree,
and equal NNPNNNNN (the outcome string of *2), for odd/even/F rings with n <= 33.  Usage: python lemma1_family.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam, graph

def main():
    bad = 0; tot = 0
    for famname, ns in (("odd", range(5, 34, 2)), ("even", range(6, 34, 2)), ("F", [5] + list(range(7, 34)))):
        for n in ns:
            S = fam.FAMILIES[famname](n)
            full = fam.run_rg("solve", " ".join(S) + "\n", extra=("7",)).split()[0]
            red = graph.solve(graph.build(S), 7)
            tot += 1
            if full != red or full != "NNPNNNNN": bad += 1; print("difference", famname, n, full, red)
    print(f"full (unreduced) vs reduced outcome strings of G+*h, h=0..7, odd/even/F rings up to n=33: {tot} rings, differences {bad}")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main() else 0)

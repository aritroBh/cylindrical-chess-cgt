"""Hit check for the 7 reported C9 rings and their colour reversals."""
import time
from engine import parse_ring, colour_reverse_tokens, make_engine

RINGS = [
 "B4 B7 W3 W2B5 B7 W3 W2 B7 W2",
 "B6 B7 W2B7 W4 B6 W2 W5 B7 W2",
 "B4 W2 B6 W2 W3 B6 B7 W3 W6B7",
 "B6 B7 W3 B7 W5 W2B3 B6 W2 W3",
 "B6 B7 W3 B7 W5B4 W2 B6 W2 W3",
 "B4 B7 W3 B5 W2B7 W2 W3 B7 W2",
 "B6 B7 W2 B7 W5 W2 B6 W4B7 W2",
]

def solve_tokens(tokens):
    pos = parse_ring(tokens, 9)
    # root check
    eng = make_engine(9, True)  # keep ep across heap (sum convention)
    sig = eng["signature"](pos, 4)
    return sig, eng

def main():
    t0 = time.time()
    for i, ring in enumerate(RINGS, 1):
        toks = ring.split()
        sig, _ = solve_tokens(toks)
        rev_toks = colour_reverse_tokens(toks)
        rev_sig, _ = solve_tokens(rev_toks)
        print(f"ring {i}: {ring}")
        print(f"  sig={sig}  rev_sig={rev_sig}  rev_tokens={' '.join(rev_toks)}")
    print(f"elapsed {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()

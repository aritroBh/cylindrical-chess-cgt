"""Build EDITS.md from the CURRENT LOOPY.md (OLD blocks are copied from it and checked to occur exactly once)."""
import re, sys
LOOPY = open("/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md").read()
OUT = "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32/EDITS.md"
DATA = open("/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32/scripts/edit_data.txt").read().strip()

old1 = "(The same table was computed by K21's solver and by the referee's `ref.py`, B = 4: CHECKED-2. For over and under these are also Λ and P, the node 0 inside them having reserves (0, 0).)"
new1 = old1 + "\n\n" + open("/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32/scripts/edit_prop39p.txt").read().strip().replace("@@DATA@@", DATA)

old2 = "(d) the relation between (λ, ρ) and\n     Siegel's stops (CONJECTURE, untested: λ(S) = ⌈−RS(S)⌉ or one more, for a terminal-free stopper with finite reserve)."
new2 = ("(d) the relation between (λ, ρ) and\n"
        "     Siegel's stops: ANSWERED (new, K32, 2026-10-27; Proposition 3.9′). The conjecture was true only after a clamp at 0: λ(S) = max(0, ⌈−RS(S)⌉) or one more,\n"
        "     and \"one more\" only if −RS(S) is an integer ≥ 0; λ(S) = ∞ iff RS(S) = −∞; ρ is the mirror with LS. The literal form fails whenever RS(S) ≥ 2 (the integer 2 has λ = 0).\n"
        "     PROVED from the standard comparison of the stops of a stopper with numbers (KNOWN, not re-derived here); the corrected relation holds on every rooted stopper with at most 4 nodes\n"
        "     and on 105,000 random stoppers of 5–8 nodes (CHECKED-2). Still open: a derivation of the comparison itself from the recursive definition of the stops inside this document.")

old3 = "the sampled states (K21: 142,798; referee: 6,150 instances) COMPUTED-1, 0 violations |"
new3 = (old3 + "\n| T3.9′ | Reserves against Siegel's stops: for a node y of a finite terminal-free stopper, λ(y) = ∞ iff RS(y) = −∞, otherwise max(0, ⌈−RS(y)⌉) ≤ λ(y) ≤ max(0, ⌊−RS(y)⌋ + 1) "
        "(one more only when −RS(y) is an integer ≥ 0); ρ is the mirror with LS. The conjecture of §8 item 4(d) holds after the clamp at 0 and fails literally for RS ≥ 2 | "
        "PROVED from the standard comparison of stops with numbers (new, K32, 2026-10-27; the comparison is KNOWN, not re-derived here); the corrected relation holds on all 2,173,754 rooted stoppers with at most 4 nodes and on 105,000 random stoppers of 5–8 nodes, CHECKED-2 (two C implementations; no violation) |")

blocks = [("Proposition 3.9prime: reserves against Siegel's stops (after Proposition 3.9)", old1, new1),
          ("Section 8 item 4(d): answered", old2, new2),
          ("Status table: new row T3.9prime after T3.11", old3, new3)]
out = []
for label, old, new in blocks:
    n = LOOPY.count(old)
    print("%-70s OLD occurrences: %d" % (label[:70], n))
    assert n == 1, label
    out.append("### EDIT %s\n<<<<<<< OLD\n%s\n=======\n%s\n>>>>>>> NEW\n" % (label, old, new))
open(OUT, "w").write("\n".join(out))
cur = LOOPY
for label, old, new in blocks: cur = cur.replace(old, new)
print("EDITS.md written; applies; new length", len(cur), "old length", len(LOOPY))

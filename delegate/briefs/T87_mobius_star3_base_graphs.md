# T87 — Independent base computations for two *3 families on the Möbius strip

Output directory: `delegate/out/T87/` (create it). Write `REPORT.md` there and your programs. Do not edit anything
else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs you started
and recorded yourself. At most 1 process at a time, under 3 GB RSS (bound any memo cache), `nice -n 15`; total
compute budget about 40 minutes. Other people's jobs run on this machine: leave them alone. Do not copy raw
terminal transcripts into your report, and do not write anything from your own memory of other projects or any
personal identifier (names, email addresses, home paths outside this repository) into it.

## Why
`research/mobius_star3_family/REPORT.md` claims two families of rings of value *3 with n+1 pawns on the Möbius
strip M_n, covering every n >= 11:
- TT(m) = `B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2 (B4 W2)^m`, n = 2m+10, m >= 1;
- SS(m) = `B6 W3 (W2 B4)^m W6B7 W3 B7 B6 W3 W2 B6 W2 B4`, n = 2m+11, m >= 0.
The proof will be the insertion proof of `research/mobius_rings_proof/PROOF.md` (rules in its section 1; the
reduced game, classes T, L, P, K and Lemmas 1 to 3 in its sections 1 and 3; the criteria in section 4). Its finite
inputs were computed by ONE program. We need a second, independently written computation. You wrote
`delegate/out/T82/referee.py` earlier (your own rules implementation and reduced-graph traversal for the families
F1 to F3); you may extend YOUR code, but do not import or run `research/mobius_rings_proof/*.py`,
`research/mobius_star3_family/*.py`, `cylcgt`, or the `mob1`/`mob2` binaries.

## Compute (ring notation: one token per file from file 0; `W6B7` = two pawns on one file; signature = outcome of
ring + nim-heap h for h = 0,1,2,3,(4): N first player wins, P second player wins; NNNP(N) means *3)
1. **C1 for TT at m = 5 (n = 20):** reduced graph. Report nodes, K-edges, T-moves, number of nodes with an e.p.
   flag, number of nodes with a passed pawn, the zone (files whose contents differ from the root at some node), and
   the reduced signature for h = 0..4. Claimed: 1305, 4018, 1212, 0, 0, {0,1,3,4,5,6,7,8}, NNNPN.
2. **C1 for SS at m = 6 (n = 23):** the same. Claimed: 22755, 72730, 49694, 0, 0,
   {0,1,12,13,15,16,17,18,19,20,21,22}, NNNPN.
3. **Insertion step at the base:** TT with cut c = 14 from m = 5 to m = 6 (insert after file 14 copies of files 15
   and 14, as ins_c is defined in PROOF.md): the image of the root is the root of m = 6, and the map is an
   isomorphism of reduced graphs (nodes, K-children per side, T-flags per side). SS with c = 6 from m = 6 to m = 7.
4. **C2, whole-board search with heaps 0..3 (your own unreduced search):** TT for m = 1..4 (n = 12..18) and SS for
   m = 0..5 (n = 11..21) as far as your budget allows, smallest first. Claimed NNNP each. Also TT at m = 0 (claimed
   LLLL, not in the family).
5. Check the stated setting of the proof plan: for TT, files 10..19 are wall files (B4 on even, W2 on odd) in every
   node of the m = 5 graph and none is in the zone; file 19 is the seam file n-1 and its neighbour across the seam,
   file 0, IS in the zone. Say whether any move in the graph crosses the seam between files 19 and 0 (a capture
   from or onto file 19, or an e.p. capture there), and list the classes of the moves of the pawn on file 19 over
   all nodes. For SS, the same for arc 2..11 (files 0 and 1 are in the zone and file 0 is the seam file).

## Report
`delegate/out/T87/REPORT.md`: first line AGREE / DISAGREE per item 1 to 4. Then the numbers, the answer to item 5,
the commands to rerun, peak memory and time, and what you did not do.

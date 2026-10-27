# Four-man endings on twisted boards: solver B

## Summary

1. Solver B reproduces `tablebase/replica/REPORT.md` exactly on the plane, cylinder and torus. Legal count, won count and longest mate agree for all 10 materials (30 rows), including the KBBK colour split. The replica's counts of non-won positions where White loses a man or is stalemated at once also match. KQK, KRK and KBNK match as required.
2. **Möbius:** forced win from every legal position for KQK (longest mate 7 moves), KRK (12), KBBK (11), KQRK (4), KRRK (4) and KQQK (2). KBNK wins 99.9769% (longest mate 19). KNNK wins 0.0077% (mate in 1 only).
3. **Klein bottle:** forced win from every legal position for KQK (3), KBNK (11), KBBK (5), KQRK (2), KRRK (4) and KQQK (1). KRK wins only 0.66% (mate in 1 only). KNNK never wins.
4. **RP²:** forced win from every legal position for KQK (4), KRK (12), KBNK (10), KBBK (4), KQRK (2), KRRK (3) and KQQK (2). KNNK wins 0.0091% (mate in 1 only). A lone bishop (KBK) wins 4.7% of positions, through the corner squares, which are cone points with only 6 neighbours.
5. **Square colours are lost on all three boards.**
   - No chessboard 2-colouring exists, because the four-neighbour graph has odd cycles. Example on the Möbius strip: a4 b4 c4 d4 e4 f4 g4 h4 a5 and back to a4 is 9 steps.
   - A diagonal step across the seam changes the nominal (f+r) parity, so one bishop reaches all 64 squares. On the plane, cylinder and torus there are 2 orbits of 32.
   - "Same colour" and "opposite colour" bishops no longer exist. KBBK is won from every legal position on all three boards, whatever nominal colours the bishops stand on (for example Möbius, same parity 4,086,912 of 4,086,912 won).
   - Knight graphs are not bipartite either.

## Results (white to move)

"Legal" means distinct squares, kings not adjacent through gluings, Black not in check. Identical men are counted in both orders, as in the replica. "Longest mate" is in White moves. The example is the first maximal position in index order.

| Board | Material | Legal | Won | Won % | Longest mate | Forced win from every legal position? | A longest-mate position |
|---|---|---|---|---|---|---|---|
| Möbius | KQK | 106,368 | 106,368 | 100.0000% | 7 | **yes** | Ka1 Qb1 kh2 |
| Möbius | KRK | 147,776 | 147,776 | 100.0000% | 12 | **yes** | Ka1 Rb1 ka4 |
| Möbius | KBNK | 9,568,672 | 9,566,464 | 99.9769% | 19 | no (2,208 not won) | Ka1 Bf1 Ne3 kf2 |
| Möbius | KBBK | 8,222,848 | 8,222,848 | 100.0000% | 11 | **yes** | Ka1 Bb1 Ba2 kh3 |
| Möbius | KNNK | 10,861,312 | 832 | 0.0077% | 1 | no | Ka1 Nb2 Ne6 kg8 |
| Möbius | KQRK | 4,365,248 | 4,365,248 | 100.0000% | 4 | **yes** | Ka2 Qb1 Ra1 kc7 |
| Möbius | KRRK | 5,974,912 | 5,974,912 | 100.0000% | 4 | **yes** | Ka1 Rb1 Rd1 kc7 |
| Möbius | KQQK | 3,069,312 | 3,069,312 | 100.0000% | 2 | **yes** | Ka1 Qb1 Qc1 kg2 |
| Klein | KQK | 69,120 | 69,120 | 100.0000% | 3 | **yes** | Ka1 Qe1 ka7 |
| Klein | KRK | 145,344 | 960 | 0.6605% | 1 | no | Ka2 Rc1 ka4 |
| Klein | KBNK | 6,693,856 | 6,693,856 | 100.0000% | 11 | **yes** | Ka1 Bb1 Na4 kb4 |
| Klein | KBBK | 4,285,120 | 4,285,120 | 100.0000% | 5 | **yes** | Ka1 Bb1 Bc1 kb5 |
| Klein | KNNK | 10,129,536 | 0 | 0.0000% | none | no | none |
| Klein | KQRK | 2,827,968 | 2,827,968 | 100.0000% | 2 | **yes** | Ka1 Qb1 Rc1 kf2 |
| Klein | KRRK | 5,856,768 | 5,856,768 | 100.0000% | 4 | **yes** | Ka1 Rb1 Rc1 kd2 |
| Klein | KQQK | 1,288,960 | 1,288,960 | 100.0000% | 1 | **yes** | Ka1 Qb1 Qc1 kf2 |
| RP² | KQK | 62,472 | 62,472 | 100.0000% | 4 | **yes** | Ka1 Qg2 ke5 |
| RP² | KRK | 124,848 | 124,848 | 100.0000% | 12 | **yes** | Ka1 Rb1 ke3 |
| RP² | KBNK | 7,031,412 | 7,031,412 | 100.0000% | 10 | **yes** | Ka1 Be1 Nf3 ke2 |
| RP² | KBBK | 4,700,680 | 4,700,680 | 100.0000% | 4 | **yes** | Ka1 Bb1 Bh1 kd1 |
| RP² | KNNK | 10,245,072 | 936 | 0.0091% | 1 | no | Kb1 Na1 Nc1 kh7 |
| RP² | KQRK | 2,183,940 | 2,183,940 | 100.0000% | 2 | **yes** | Ka1 Qb1 Rg1 kd4 |
| RP² | KRRK | 4,294,080 | 4,294,080 | 100.0000% | 3 | **yes** | Ka1 Rd1 Re1 kc2 |
| RP² | KQQK | 1,052,072 | 1,052,072 | 100.0000% | 2 | **yes** | Ka1 Qh1 Qa8 kc3 |

Extra rows from the same run:
- KRBK is won from every legal position on all three boards (longest mate 11 Möbius, 5 Klein, 5 RP²).
- KBK and KNK win nothing on the Möbius strip or the Klein bottle.
- On RP², KBK wins 6,132 of 130,208 (4.71%, longest mate 7), and KNK wins nothing.
- Möbius KBNK: of the 2,208 positions not won, 2,112 lose a man or stalemate at once and 96 are genuine draws.

## Square colours

| Board | Chessboard 2-colouring exists | Bishop orbits | Diagonal steps that change (f+r) parity | Knight graph bipartite |
|---|---|---|---|---|
| plane | yes | 2 (32+32) | 0 of 196 | yes |
| cylinder | yes | 2 (32+32) | 0 of 224 | yes |
| torus | yes | 2 (32+32) | 0 of 256 | yes |
| Möbius | no | 1 (64) | 28 of 224 | no |
| Klein | no | 1 (64) | 32 of 256 | no |
| RP² | no | 1 (64) | 56 of 252 | no |

Crossing the a/h seam sends (7, r) to (0, 7-r). That keeps the parity of f+r, so two squares that share an edge across the seam have the same nominal colour. A diagonal step across the seam changes it. For example, a Möbius bishop on h4 moving up-right lands on a4.

## Rules and modelling decisions

- Every step is the offset in the covering plane, reduced to the board by undoing the gluings. This applies to king steps, knight jumps and slider steps.
- A slider ray is a straight line in the covering plane. It continues straight through a seam, with its local direction reflected there. Example, Möbius: a bishop on e1 going up-right visits f2 g3 h4 a4 b3 c2 d1, then meets the rank wall.
- Rays stop at the first occupied square and stop if they revisit a square, their own included.
- RP² corners are cone points. A diagonal step through a corner returns to the same square, so it is not a move. The corner h1, for example, touches a8 twice (east and south), plus g1, g2, h2, a7 and b8.
- There is no castling and no 50-move rule. Stalemate and bare kings are draws. When Black captures, play continues in the K+one piece vs K sub-table, solved by the same program.
- Solving is plain value iteration on mate-in-n, with no retrograde shortcuts.

**Ray convention sensitivity.** The task says sliders "continue through gluings", and I read that as continuing straight. I also ran two naive variants that keep the local direction label after a seam crossing: variant 1 adds the step and then flips the rank, variant 2 flips the rank first and then adds the step.
- Rook-only endings and KNNK are identical in all three conventions.
- Bishop and queen endings change. Möbius KBBK has longest mate 11 under straight rays against 7 and 6 under the variants. Klein KBNK has 11 against 6 and 6.
- The variants break reversibility of rays (644 non-reversible ray squares on the Möbius strip, 2,912 on Klein, 4,312 and 1,848 on RP²) and let a lone bishop win KBK on the Möbius strip and the Klein bottle. That is why I used straight rays.
- If solver A uses a naive convention, expect differences only in bishop and queen endings. The full comparison is in the `{board}_ray1.txt` and `{board}_ray2.txt` files under `results/`.

**Smaller conventions.** The longest mate is counted in White moves. The RP² corner rule above could also differ in A.

## Checks

- **Geometry.** `verify.py` rebuilds every king, knight and ray table by parallel transport over edge neighbours, a different construction from the one in `twist.c`. It matches on all 6 boards with 0 differences.
- **Tables.** `verify.py` applies the rules by brute force and checks the Bellman equations on random positions, half of them on edge squares. It sampled 150,000 positions for each of the 66 tables and 600,000 for each of the 21 four-man tables on the new boards, with 0 mismatches. A deliberately corrupted table is caught.
- **Symmetry.** Every board symmetry of the move structure leaves all tables unchanged, with 0 differences. These are the symmetries that exist for that board (for example file shift on the Möbius strip, transpose on RP²).
- **Self-test.** Reduction to the board does not depend on gluing order, and rays are reversible on all six boards under the straight-ray rule.
- **Resources.** One thread per run, `nice -n 15`, at most 2 processes at a time. Peak memory was 454 MB. A full board with all 11 materials took 21 to 107 seconds.

## Commands

Run from `/Users/aritro/Downloads/Research/Chessendgames/research/twisted_tablebases/B`:

```bash
cc -O2 -Wall -o twist twist.c
mkdir -p results work/geo
nice -n 15 ./twist mobius all -g -s -d work -G work/geo/mobius.txt > results/mobius.txt
nice -n 15 ./twist rp2 BN -q -p "Ka1 Be1 Nf3 ke2"     # one material, prints a fastest line
nice -n 15 ./twist mobius all -r 1                      # naive ray variant (also -r 2)
python3 -I verify.py mobius geometry work/geo/mobius.txt
python3 -I verify.py mobius BN work 150000 7
python3 -I mkreport.py                                 # prints all tables to stdout
./run_all.sh                                           # everything, about 10 minutes
```

The longest-mate lines for the new boards are in `results/{mobius,klein,rp2}.txt` (the `PV` rows); `mkreport.py` prints them as well.

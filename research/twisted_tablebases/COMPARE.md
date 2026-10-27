# Twisted-board tablebases: A (T60, OpenCode) against B (Sonnet workflow, written blind)

Boards: Möbius strip (files a and h glued with the ranks reversed, ranks 1 and 8 are walls), Klein bottle (the same,
plus ranks 1 and 8 glued plainly) and RP² (both pairs glued with a flip). White to move throughout.

## Result

- **Plane, cylinder, torus.** B reproduces `tablebase/replica/REPORT.md` exactly in all 30 rows.
- **Same ray rule.** A's slider rays keep their local direction label after crossing a seam. That is B's naive ray
  variant 1 (`B/results/*_ray1.txt`), and under it A and B agree exactly on all 33 shared rows on the three twisted
  boards: legal count, won count and longest mate. For example, Möbius KBNK is 8,883,740 legal, all won, mate in 20.
  So the two programs are CHECKED-2 for that convention.
- **Rook and knight endings.** KRK, KRRK, KNNK, KNK and the Klein KRK draw do not depend on the ray rule. A, B and
  both variants are identical there, so these are CHECKED-2 outright:
  - KRK is won from every legal position on the Möbius strip (147,776, mate in at most 12) and on RP² (124,848,
    mate in at most 12).
  - KRK is won from only 960 of 145,344 positions (0.66%, all mate in 1) on the Klein bottle.
  - KNNK wins only mates in 1, and never on the Klein bottle.
- **Bishop and queen endings.** These change with the ray rule.
  - B's default rule continues a ray straight in the covering plane and reflects its direction at the seam. It is
    the geometric one: rays are reversible and the geometry was rebuilt independently by parallel transport.
  - Variant 1, which is A's rule, has 644 non-reversible ray squares on the Möbius strip and lets a lone bishop
    "win" KBK there.
  - So the straight-ray bishop and queen values are B alone (COMPUTED-1), and A's values are tied to a
    non-geometric rule.
- **Square colours.** On all three twisted boards there is no chessboard 2-colouring: the Möbius four-neighbour
  graph has a 9-cycle. One bishop reaches all 64 squares, so "opposite-colour bishops" does not exist there
  (COMPUTED-1, B; A notes the same).

## For the paper

Only the rook results are robust enough to state, as [C2]: KRK wins every Möbius position, against 0.66% on the
Klein bottle.

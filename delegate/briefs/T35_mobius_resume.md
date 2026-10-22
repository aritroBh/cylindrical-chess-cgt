# T35: Möbius strip and Klein bottle, resume and verify (moderate compute)

**Output directory:** `research/mobius/`. It exists, from T9. Add files; do not delete T9's.

**Steps.**
1. Read `research/mobius/REPORT.md` and `RULES.md`. Say whether T9 finished and what it claims.
2. Re-run its smallest reproduce command and check that the numbers match.
3. Extend the work in this order. Stop any step projected over 40 minutes.
   - **KPK on the 8×8 Möbius board.** The a- and h-files are glued with the ranks reversed, so a pawn that
     crosses the seam reverses direction. Report:
     - the White-to-move win rate against the cylinder's 78.89%;
     - the rook-pawn position Ka6 Pa5 vs Ka8;
     - the number of mutual zugzwangs.
   - **Pawn-only CGT values on narrow Möbius boards**, widths 3–4 with up to 4 pawns. Does any value occur
     that occurs on neither the ordinary board nor the cylinder?
4. Label everything; give reproduce commands.

**REPORT_T35.md:** the claims table, with labels.

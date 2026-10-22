# T32: legality and capture histories of the 21 five-file \*2 positions (light compute)

**Output directory:** `research/five_file_legal/`.

**Input:** the 21 positions in `delegate/REVIEW.md` (section "The 21 five-file \*2 positions"), or the
C/aware rows of `research/star2_width5/hits.tsv`.

**For each position:**
1. Can it arise in a real game? Give a pawn-capture history from the starting position, using pawn captures
   only, in the style of the paper's Theorem 16 (e.g. "c2×d3"):
   - count the captures each side needs;
   - check that the number of missing enemy pieces covers them.
2. Placed on files a–e of the 8×8 board beside the trébuchet (W Kf5 Pg4, B Kh4 Pg5), is the position legal?
   - No pawn may give check: a black pawn on e6 attacks f5, and a white pawn on g3 attacks h4.
   - No king may be adjacent to an enemy pawn it could capture, and the kings themselves must not be in check.
   - Is any e-file pawn touching the king group? List the conflicts.
3. Mirror the position onto files d–h with the trébuchet on files a–c, if that helps.

**REPORT.md:**
- a 21-row table: position | captures needed | history (or IMPOSSIBLE) | legal beside T? | notes;
- the list of positions that are both reachable and legal beside T;
- a reproduce script.

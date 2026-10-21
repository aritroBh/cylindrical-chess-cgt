# T10: king-and-pawn tablebases on the cylinder (KPK, KPKP, KPPK)

Output directory: `research/kp_tablebases/`.

**Context:** on the cylinder there are no edges, so the classic KPK theory (rook-pawn draws, the corner, key squares) must change. `kings/kpsolve.c` already solves king-and-pawn positions exactly on small flat and cylinder boards (`kings/SPEC.md`, `kings/REPORT.md`). Use it read-only or copy it into your directory.

1. Solve full 8×8 KPK on the cylinder and on the flat board. Also do KPKP and KPPK if memory and time allow; aim for each run under 45 minutes. Promotion must allow all four pieces.
2. Validate first: flat KPK must match the known result. Check 20 random positions against the Lichess cache via `realchess/probe.py` (offline mode first).
3. Characterise cylinder KPK:
   - the share of positions won with White to move;
   - which classic flat draws become wins, and the reverse;
   - a cylinder "square rule";
   - the key squares;
   - mutual zugzwangs (count them and give examples).
   State each rule as a theorem, labelled COMPUTED-1, CHECKED-2 or PROVED.
4. For KPKP: the share won and drawn, the maximal depth to promotion, and positions where the cylinder result differs from the flat result with the files rotated.

Write `research/kp_tablebases/REPORT.md`.

# K48 review (2026-11-23)

Question: is the exact group of K45 (cyl:8×6, `Kf5 kd4/kd5 Pb2 Pb4 Pe2 pa4 pb5 pe5`) still exact in chess, and do exact
groups of Definition 4.8 exist on flat boards and on taller boards?

Investigator: an Opus agent (`findings.txt`, `EDITS.md`, `p1_table.txt`, `flat_table.txt`). Referee: a second Opus
agent with its own Definition 4.8 checker and fresh builds of the chess tools (`VERIFY.md`, `verify/`). AI work, no
human re-derivation. A machine reboot interrupted the investigation; only unfinished runs were restarted.

## Verdict (all CHECKED-2 unless stated)

- **Chess, cyl:8×6, promotion cap 1.** The d4 root with White to move is exactly a White win by e2–e4, and the position
  after it is an exact mutual zugzwang in chess (both bounds agree in two code families; fresh runs by the referee).
  The other three roots, the d5 freeze and its zero stay at bounds (W, L). Of 49 move values 28 are exact and all
  agree with P. Whether the group is exact in chess is open; cap 2 was not completed.
- **Flat boards.** The wrap is not needed. On flat 8×6 the full search (20 file classes, 2,515,002,479 placements per
  orientation) finds exactly 3 exact groups up to left-right reflection: the group and its two translates. On flat
  9×6 and 10×6 the translates are exact (4 and 5); the other file classes there were not searched.
- **Taller board.** On cyl:8×7, files a, b, e, there are 4 exact groups, all new; the cyl:8×6 group is not exact there
  ((O1) and (O2) fail).
- Every group here is exact in the sense of Definition 4.8 only. No value in sums was computed, and K47 showed that
  the cyl:8×6 group is not equal to over.

## Integration

The referee's replacement set `verify/EDITS.md` was applied to `kings/theory/LOOPY.md`: 4 applied, 0 rejected, table
cell counts unchanged. It corrects the investigator's set in three ways: "up to left-right reflection" on the flat
8×6 count; "of Definition 4.8" with a note that no sum value was computed; two scope notes (chess on flat boards not
run, other file classes of cyl:8×7 not searched).

## Process notes

- The referee's checker first read the pawn letter b as a bishop and failed two groups; after the fix both pass with
  ref3m and kp_p.
- Peak memory: kpsolve 2.81 GiB (at the 3 GB limit; the investigator had measured 1.9 GB for the same run), own39
  0.95 GB, ref3m and kp_p at most 55 MB. Only recorded own PIDs were stopped; binaries removed.

## Not done

Cap 2 in chess; chess on flat boards; the other file classes on flat 9×6 and 10×6 and on cyl:8×7; cyl:8×8.

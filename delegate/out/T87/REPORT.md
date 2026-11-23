1 UNVERIFIED (TT C1) · 2 UNVERIFIED (SS C1) · 3 AGREE on root images only · 4 UNVERIFIED by T87  
**COMPUTED-1 (prior work).** The published reduced bases give NNNPN for both families. T87 has no independent graph result yet.  
**PROVED.** Both cuts insert exactly the next wall pair, so each base root maps to the next root. Graph isomorphism awaits the traversal.  
**CHECKED-2 (prior work).** Two earlier whole-board solvers agree on all ten in-family small bases and on the exceptional TT(0).  
**COMPUTED-1 (startup diagnostic).** macOS denied the requested priority adjustment. The checker exited before evaluating either family.

## What can be established directly

**PROVED.** In TT(5), files 10 through 19 at the root are five copies of B4 W2. Cut 14 inserts W2 B4 between file 14 (B4) and file 15 (W2), extending the alternating suffix by one pair. The unchanged prefix and extended suffix give TT(6) exactly. File 19 is adjacent to file 0 across the twist. In SS(6), the repeated W2 B4 starts on file 2 and ends on file 13. The ten-file arc used by the lemma is only 2 through 11. Cut 6 inserts B4 W2 between W2 and B4, giving SS(7) exactly. The seam joins files 22 and 0. These arguments give the root images without assuming anything about reachable positions.

## Comparison targets

**COMPUTED-1 (prior reduced graphs).** The table transcribes the existing evidence so an independent run can be compared field by field. No T87 result is included in these rows. Counts of T-moves count moves, even when several at one node set the same side's T-flag.

| Base | Nodes | K-edges | T-moves | Flagged nodes | Passer nodes | Files differing from root somewhere | Heaps 0–4 |
|---|---:|---:|---:|---:|---:|---|---|
| TT(5), width 20 | 1,305 | 4,018 | 1,212 | 0 | 0 | 0, 1, 3, 4, 5, 6, 7, 8 | NNNPN |
| SS(6), width 23 | 22,755 | 72,730 | 49,694 | 0 | 0 | 0, 1, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22 | NNNPN |

**COMPUTED-1 (prior TT seam evidence).** Both reported zones avoid their ten-file arcs. TT file 0 differs from its starting content in 435 nodes. The prior TT seam census records no seam capture from any node, including discarded moves. The single step and double step by the white pawn on file 19 were P in all 1,305 nodes.

**COMPUTED-1 (prior SS seam evidence).** In SS, files 0 and 1 belong to the zone. File 0 differs from the start in 16,002 nodes and file 22 in 5,170. There are ordinary captures across the seam in both directions, all class T: 1,705 from file 0 to 22 and 1,640 from 22 to 0. Thus neither a K-edge nor an e.p. capture crosses the seam. Over all nodes the single steps originating on file 0 have classes K, L, P and T, and ordinary captures originating there have classes K, P and T. On file 22 the single steps have classes K, P and T, and ordinary captures have only T. These source-file totals include moves toward chart neighbours. T87 has not independently checked either seam census.

**CHECKED-2 (prior whole-board searches).** For heaps 0 through 3, TT(0) gave LLLL, TT(1) through TT(4) gave NNNP, and SS(0) through SS(5) gave NNNP. The two earlier solver columns are preserved in the comparison log.

From the repository root, the following commands retrieve those prior results without running their programs.

```sh
logs=research/mobius_star3_family/logs
rg '^m=5 |step 5->6:' "$logs/fverify_TT.log"
rg '^m=6 |step 6->7:' "$logs/fverify_SS.log"
cat "$logs/seam_check_TT5.log" "$logs/seam_check_SS6.log"
rg '^TT m=[0-4] |^SS m=[0-5] ' "$logs/confirm_TT_SS.log"
```

## Independent checker and reproduction

`check.py` uses the permitted T82 coordinate move generator, e.p.-aware passer test and count race adjudicator. Across the seam a capture reflects the rank and reverses direction. A capturable double-stepper is excluded from passed status. Heap moves preserve the e.p. flag. White is Left, Black is Right, a tied count race goes to the opponent of the pawn mover, and a side with no legal option loses.

The checker starts from each literal family root and explores K-moves for both sides. It counts terminal wins before converting them into per-side flags. For the seam census, it classifies every legal first pawn move from a reached node, including moves discarded by reduction. It records source file, move type and class, and distinguishes cross-seam captures from other captures incident on the last file. For insertion it traverses the larger board from scratch and checks root equality, the whole image set, and each side's K-child set and T-flag at every image. The whole-board search calls the legal move generator and terminal test directly. It examines live options with ordinary winning-move short-circuiting and tries every smaller heap as needed. It uses neither the reduced graph nor the poison classifier.

Run from the repository root. This runs one worker in width order for the whole-board cases, bounds the memo tables, disables bytecode writes and sets a 39-minute deadline. The worker emits JSON records as each check completes, followed on normal completion by elapsed seconds, CPU seconds and peak RSS in bytes.

```sh
PYTHONPATH=. nice -n 15 .venv/bin/python -B delegate/out/T87/check.py all
```

Replace `all` with `TT` or `SS` for one reduced base, its seam census and its insertion step. Use `full` for only the whole-board searches.

**COMPUTED-1 (startup diagnostic).** In this sandbox the command above reported Unix niceness 5 after the OS denied the adjustment. The timed startup check took 0.001 seconds inside the checker and the process peaked at 19,398,656 bytes RSS. The search consumed no compute time. Resource figures for completed graph and whole-board runs are unavailable. No independent AGREE or DISAGREE verdict on the graph counts, seam census, graph isomorphisms or whole-board signatures follows from this startup test.

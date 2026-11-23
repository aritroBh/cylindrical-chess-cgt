# Moebius pawn rings, larger n (n files, 8 ranks, whole-board game, h = 0..3)

Rules, ring notation, symmetry group (order 4), signature convention: exactly as `research/mobius_rings/REPORT.md`.
Nothing under `paper/`, `dist/`, `research/mobius_rings/`, `research/mobius_rings_check/` was edited; no git writes.
Programs here: `mob1.c`, `mob2.c`, `mring.h`, `mring.c` (copies, MAXN made a compile-time `-DMAXN=`, `mseq`/buffers
enlarged, nothing else changed; builds `bin/mob{1,2}_{8,12,32}`), `check.c` (copy of the T77 checker with 128-bit boards,
width up to 21, alarm 8 h), `fam*.py`, `famconfirm.py`, `summarise.py`, `compare.sh`, `run_jobs.sh`.

## Headline

1. **One pawn per file.** Exhaustive, two solvers byte-identical: n = 8: 1 *2 orbit; **n = 9: 0**; n = 10: 2; n = 11: 1;
   no *3 anywhere. So n = 8 is not special, but n = 9 has none. n = 12 is not finished (partial below).
2. **From n = 10 on, *2 with one pawn per file exists for every n tested (10..32)**, via two pair-pumping families
   (below), each confirmed with mob1, mob2 and (n <= 21) check. n = 9 (0 rings) and n = 8 (isolated ring) are the only
   exceptions seen. Odd n >= 11 and even n >= 10 are both covered.
3. n = 9 with 10 pawns (exhaustive, C2): 9 *2 orbits and **1 *3 orbit** (`B5 W3 W4 B7 B7 W3 W2 W2B7 B7`).
4. Old counts reproduced exactly (n = 7: 65613 and 2570131 rings; n = 8: 427178; per-ring signature files and `.out`
   files byte-identical to the old results, for both solvers, built with MAXN = 12).

## Coverage (orbits under the order-4 group; label C2 = mob1 and mob2 per-ring signature files and histograms identical for every chunk)

| n | pawns | rings | *2 orbits | *3 orbits | label | time mob1 / mob2 (s, sum of chunks, nice 15, 2-3 jobs at once) |
|---|---|---|---|---|---|---|
| 7 | 7 | 65613 | 0 | 0 | C2 (reproduction) | 1 / 1 |
| 7 | 8 | 2570131 | 1 | 0 | C2 (reproduction) | 43 / 21 |
| 8 | 8 | 427178 | 1 | 0 | C2 (reproduction) | 4 / 3 |
| 9 | 9 | 2729517 | **0** | 0 | C2 | 51 / 25 |
| 10 | 10 | 17146529 | 2 | 0 | C2 (8 chunks) | 707 / 498 |
| 11 | 11 | 109358578 | 1 | 0 | C2 (24 chunks) | 5972 / 4221 |
| 9 | 10 | 133597405 | 9 | 1 | C2 (32 chunks) | 8193 / 6345 |
| 12 | 12 | PARTIAL, see below | | | | |
| 7 | 9 | 47881379 (old mob2 scan, 12 chunks, copied) | 9 | 0 | C1 for now; mob1 rerun started, see below | mob2 ~164 s/chunk |

Ring counts equal `mring N P --count` (n = 11: 109358578). Per-chunk agreement logs: `logs/compare_n10.log`,
`logs/compare_n11.log`, `logs/compare_n9p10.log`, `logs/validate_4a.log`. Per-ring signature files: `results/*.sig.zst`
(zstd -t tested by the runner), full outputs `results/*.out`, histograms inside them (`HIST` lines).
Not scanned: n = 10 with 11 pawns (about 1e9 rings, count aborted), n = 11 with 12 pawns, n >= 13 exhaustively.

## Hits (ring notation; one ring per orbit; every one also checked by `check`, C3)

- n = 8, 8 pawns: `B7 W3 W3 B6 W3 B6 B6 W2`
- n = 10, 10 pawns: `B4 W2 B6 W2 W3 B6 B7 W3 B7 W5` ; `B6 W3 B7 W2 W3 B6 B7 W2 B6 W3`
- n = 11, 11 pawns: `B4 W2 B6 W2 W3 B6 B7 W3 B7 W5 B7`
- n = 7, 8 pawns (old): `B6 W2 W3 B6 B7 W3 W6B7`
- n = 9, 10 pawns, *2 (9): `B6 W2 W3 B6 B7 W3 B7 W5 W6B7` ; `B4 W2 B6 W2 W3 B6 B7 W3B7 W5` ;
  `B6 W3 B5 W2 B6 W3 B5 W2 W3B7` ; `B5 W2 B5 W3 W5 B7 W2 B7 W4B6` ; `B5 W3 W2 B4 B7 W3 W2 W2B7 B7` ;
  `B5 W3 W5 B7 B7 W3 W2 W2B7 B7` ; `B5 W3 W4 B6 B7 W3 W2 W2B7 B7` ; `B4 W2 B7 W2B5 W2 B7 W3 W2 B7` ;
  `B6 W2 B5 W3 B6 W3 B5 W2 W3B7`
- n = 9, 10 pawns, **\*3**: `B5 W3 W4 B7 B7 W3 W2 W2B7 B7`
- n = 7, 9 pawns (old mob2 scan): 9 *2 hits listed in `hits_n7p9.txt`; all three programs agree on each (`logs/check_hits_n9p10_n7p9.log`).
All 5 hits of the n-pawn rows x 4 images (mirror, kappa, mirror*kappa) x 3 programs: signature unchanged, 0 mismatches
(`logs/symhit.log`). Third-solver check (`bin/check mobius n solve`) on the n = 9 (10 pawns) and n = 7 (9 pawns) hits:
all agree (`logs/check_hits_n9p10_n7p9.log`).

## Families (`famconfirm.py`, `logs/famconfirm.log`, `results/fam4_*.json`, `logs/fam4_*.log`)

Generators, all rings checked with mob1, mob2 and (n <= 21) check, all identical, signature NNPN each time:

- **F1(m) = (B4 W2)^m B6 W2 W3 B6 B7 W3 B7 W5**, n = 2m + 8, n pawns. m = 1..12 (n = 10..32): *2. m = 0 (n = 8) is RNRR, not a hit.
  mob1 nodes: 3350, 4655, 5906, 7157, 8408, 9659, ... 17165 (m = 1..12): +1251 per step after m = 2 (linear).
- **F2(m) = (B4 W2)^m B6 W2 W3 B6 B7 W3 B7 W5 B7**, n = 2m + 9, n pawns. m = 1..11 (n = 11..31): *2. m = 0 (n = 9) is NNRR.
  mob1 nodes 4056, 5388, 6627, ... 16539: +1239 per step.
- **F3(m) = B6 W2 W3 B6 B7 W3 (B7 W5)^m W6B7**, n = 2m + 7, n + 1 pawns (one doubled file). m = 0..12 (n = 7..31): *2,
  including m = 1 = n 9 hit above. mob1 nodes 1972, 2668, 3387, ... 10577: +719 per step.
So node counts stabilise into linear growth; the pump block never changes the signature for the tested range.
Other pump blocks that keep *2 for m = 1..11 (stage logs): at cut 0 of the n = 10 ring: `W4 B6`, `W5 B7`, `B6 W4`, `B7 W5`;
at the end `B7 W5`, `W3 B5`, `B5 W3`, `W2 B4`; for `B6 W3 B7 W2 W3 B6 B7 W2 B6 W3`: `B6 W4` at the front, `W3 B5` / `B5 W3` at the end;
for the n = 11 ring 16 block/cut combinations. The seam matters: blocks are pumped at the listed cuts only; rotations are not symmetries.
Search scope: blocks of 1 or 2 single-pawn files (and 3 for the n = 8, 10 rings) at every cut, m = 1, 2, then extended to n <= 32.
Result: **no single-file or three-file pump survives m = 1, 2** for the n = 7, 8, 10 rings (one n = 10 length-3 stage had 17 of 24420 candidates
time out at 15 s and unclassified); the n = 8 ring has no surviving pump at all (n = 8 is isolated); `n5p6` ring: none.
Stages over the 66 old hits with many pawns per file were abandoned (hard rings, memory); not done.

## n = 12, 12 pawns: PARTIAL, not a result

Still running in the background (nice 15): mob2 on `jobs_C` chunks of 128 (pid file `logs/worker_c2.pid`, shell 68444) and mob1
(`logs/worker_c1.pid`, shell 68445; it is first doing the n = 7, 9-pawn rerun, 12 chunks, then n = 9... already done, then n = 12). At
writing: mob2 9 of 128 chunks done (46,120,715 rings, 0 hits in them), mob1 0. Estimate 7+ h more for mob2 alone, 14+ h for mob1.
Summary when done (or at any time): `cd research/mobius_rings_n && python3 summarise.py | grep -E '^(12|7) '` (counts only chunks
finished by BOTH solvers; mob2-only chunks: `grep -h HIT results/n12*.mob2.out`). Existence at n = 12 is already settled by F1(2)
(and other blocks above), which is `NNPN` in all three programs; what the scan will add is the exact count of orbits.

## Not done

n = 12 exhaustive; n = 10 with 11 pawns; n >= 11 with n + 1 pawns; n = 7 with 9 pawns second-solver rerun is running but not
finished (the old rows are mob2-only = C1); families for the many-pawn-per-file hits; any proof; *3 families (the one *3 ring has
no tested pump; not searched); nimbers above *3; hits of n = 9 (10 pawns) are not re-checked by Part B (check = third program only).
Resource note: at most 2 scan workers; short family/check Python runs were a third process for minutes, a family run that
reached 3.8 GB RSS (batched solve) was stopped by me (recorded pid, `logs/orphan_fam3_child.pid`), later batches are time-limited.

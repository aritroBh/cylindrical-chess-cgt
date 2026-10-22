# BUGFIX: frontier_split1 SIGSEGV (stale memo-table slot pointer)

Date: 2026-10-22. Fixed copy: `frontier_split1_fixed.c` (binary `frontier_split1_fixed`). The originals
(`frontier_split1.c`, `frontier_split.c`, `../star2_width5/`, `../star3_hunt/`) are untouched.

## 0. Summary

* Cause: in `solve()` the memo slot `e` is looked up BEFORE the recursive `gen()` calls and written AFTER
  them. A nested `solve()` may call `tab_grow()`, which `free()`s the old table, so `e` then points into
  freed memory (or into a slot a nested call has filled). The store `e->wm = ...` is the faulting
  instruction (`frontier_split1+508`, `frontier_split+412`: the first `stp x22,x21,[x8]` of the entry store).
  It segfaults when the freed table has been returned to the OS, which happens for very large tables and,
  depending on malloc state, for smaller ones too. When it does not fault, the store lands in dead memory
  and the memo entry is silently lost.
* Fix: look the slot up again after the recursion (one extra `tab_find` per stored state).
* Chunk 0 of `--width 6 --min 9 --max 9 --nw 4 --nb 5 --only-setting 2 --chunk 0 4` now completes:
  2,822,072 roots, **0 \*2 hits and no \*k with k >= 3** in the default setting (count, e.p. on, e.p.-aware);
  the largest nimber in the chunk is \*1.
* Earlier scans: the same bug is in every copy of the memo table. It can crash (it has: see section 6) but
  it cannot give wrong values; outputs checked byte for byte are identical. A second, unrelated array
  overflow (`iw[8]/ib[8]`) did corrupt the root enumeration of the stored `cyl_w3_p10_1_9` scan
  (2560 roots instead of 2681; no hits either way).
* Several stored outputs in this directory are crash artifacts that look like "0 hits"
  (section 6.3). One of them hides a real result: **C3, 10 pawns, split 5+5 has 2 \*2 hits in the default
  setting** (section 6.3).

## 1. The bug

File `frontier_split1.c` (original), function `solve()`:

```c
264  static Value solve(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6) {
265      Entry *e = tab_find(wm, bm, ep3, ep6);          // slot pointer taken here
266      if (e->used) return e->val;
267      uint64_t AL = gen(wm, bm, ep3, ep6, 1), AR = gen(wm, bm, ep3, ep6, 0);   // recursion: solve() -> child_mask() -> gen() -> solve()
...
279      if ((tcount + 1) * 2 > tcap) { tab_grow(); e = tab_find(wm, bm, ep3, ep6); }   // refreshed only if THIS frame grew
280      if (e == tab_dummy) return v;
281      if (tcount + 1 >= (tcap / 16) * 15) return v;
282      e->wm = wm; e->bm = bm; e->ep3 = ep3; e->ep6 = ep6; e->val = v; e->used = 1; tcount++;   // store through a possibly stale e
```

`tab_grow()` (line 153) allocates a table of twice the size, re-inserts, and `free(old)` (line 160). It can
run in any nested `solve()` (line 279 of the nested frame). Every ancestor frame still inside its `gen()`
call then holds an `e` that points into the freed table, and the refresh at line 279 only protects the frame
that itself grew. The same happens (without a free) when a nested call fills the very slot `e` points to:
the outer store then overwrites that entry.

Same code, same line pattern, in: `frontier_split.c` (here, 240/254/255), `../star2_width5/frontier_split.c`,
`../star3_hunt/frontier_split.c` (240/254/255), `../star2_frontier/frontier.c`, `../star2_frontier/nimscan.c`,
`../star2_frontier_b/nimscan.c`, `../../atlas/flat8/rerun/nimscan.c`.

### Why it only shows on big runs, and how it was pinned down

* The crash reports (`frontier_split1-2026-10-22-0207xx/0209xx/0210xx.ips`) are `EXC_BAD_ACCESS
  KERN_INVALID_ADDRESS` in `solve+508` (the store), through `child_mask -> gen -> solve` recursion, with the
  stack nowhere near (so not a stack overflow; the 64 MB stack limit changed nothing). Registers:
  `tcap` = 2^28 = 268,435,456, `tcount+1` = 2^26+2, `(tcap/16)*15` = 251,658,240 (x11, x9, x10). The faulting
  address lies in an unmapped hole of exactly `0x1c0000000` = 7,516,192,768 bytes = 2^27 x 56 B, which is the
  2^27-entry table that `tab_grow()` had just freed (`Entry` is 56 bytes). So the grow 2^27 -> 2^28 happened
  in a nested frame and an ancestor then stored into the old table. All three chunk-0 crashes are identical.
* Whether the store faults depends on whether the freed block has already been returned to the kernel (inferred, not
  measured). Very large blocks (this run: 7.5 GB) evidently go back at once; smaller ones presumably sit in
  malloc's large-block cache for a while, and then the store silently succeeds into dead memory. But the earlier
  `frontier_split` crash reports (5 on this machine) show that smaller tables fault too: a hole of `0x7000000` =
  2^21 x 56 B = 112 MB in four of them (the freed 2^21-entry table), reached after only about 1M states.
  The stack-overflow reports of `frontier` (Oct 21 17:52) and the `nimscan` one (Oct 16) are a different problem.
* ASAN on the original, small case (`--cylinder --width 4 --min 8 --max 8 --nw 4 --nb 4 --only-setting 2`):
  `heap-use-after-free ... WRITE of size 8 at solve (frontier_split1.c:282)`, `freed by ... tab_grow
  (frontier_split1.c:160) <- solve (279)`, allocated by `tab_init`. In that trace the grow happens in the direct child of the frame that then stores through the stale `e` (5 vs 6 nested `solve` frames).
* lldb: a copy of the original in which `tab_grow()` uses `mmap/munmap` (i.e. the freed table really leaves
  the address space, as libmalloc does for multi-GB blocks) stops at the first grow with
  `EXC_BAD_ACCESS (code=1, address=...)` in `solve` at line 282, backtrace `solve <- child_mask <- gen <- solve ...`:
  the same signature as the real crash. The same emulation on the fixed code runs to completion with
  byte-identical output (section 3).
* Side effect visible in old logs: a stale store still does `tcount++`, so the `states=` figure of the original
  is slightly too large (orig vs fixed: 3,451,082 vs 3,451,036 on the w4 case; 46,998,867 vs 46,998,794 on chunk 1;
  3,863,469 vs 3,863,426 on chunk 2). That difference is the number of lost entries.

### Second defect found on the way: `iw[8], ib[8]` (line 332) overflow for a side with 9 pawns

`enum_roots()` declares `int iw[8], ib[8];` but is allowed `--max 10`, so `--nw 9` or `--nb 9` writes one `int`
past the array (lines 333, 345, 360, 367). ASAN (original): `stack-buffer-overflow ... WRITE of size 4 at
enum_roots (line 345 for nb=9, line 333 for nw=9)`. Undefined behaviour; in the stored `cyl_w3_p10_1_9`
run it produced 2560 roots instead of the true 2681 (the mirror split `9_1` has 2681). `frontier_split.c` in this
directory has the same arrays and limit; `../star2_width5` is capped at 8 pawns and is not affected.
Chunk 0 itself (4+5) is not affected by this.

## 2. The fix (`frontier_split1_fixed.c`, diff against `frontier_split1.c`)

1. `solve()`: tab_grow if needed, then ALWAYS look the slot up again right before the store (also skip the store
   if the key is somehow already there; a state cannot be its own descendant, so this never triggers):

   ```c
   if ((tcount + 1) * 2 > tcap) tab_grow();
   e = tab_find(wm, bm, ep3, ep6);
   if (e == tab_dummy || e->used) return v;
   if (tcount + 1 >= (tcap / 16) * 15) return v;
   e->wm = wm; ... tcount++;
   ```
2. `enum_roots()`: `int iw[16], ib[16];`.
3. `enum_roots()`: white combinations outside the chunk skip the black loop (`while (in_chunk)`); a pure speed-up
   (a sub-chunk now enumerates in about 0.5 s instead of 16-19 s; sub-chunking becomes cheap). The root set and order are unchanged.

Nothing else differs (`diff frontier_split1.c frontier_split1_fixed.c` is the header comment plus these three hunks).
Build: `cc -O2 -o frontier_split1_fixed frontier_split1_fixed.c`.

## 3. Verification (all outputs in `fixed_rerun/`)

Raw output = the unfiltered TSV (one line per root, all nimber/outcome columns), compared by md5 of the stream.

| test | result |
|---|---|
| w4, p8, 4+4, `--only-setting 2`, 487,623 roots: raw TSV, original `frontier_split1` vs fixed | identical (md5 963fd211...) |
| same: fixed default column vs the stored nine-setting run `cyl_w4_p8_4_4` | 3 \*2 hits identical; `rows`, `default_*`, outcome histogram `L:74134 N:333515 P:5840 R:74134` identical |
| chunk 1 (6,121,447 roots): fixed `.hits.tsv` and `.summary.txt` vs stored `cyl_w6_p9_4_5_s2_c1of4.*` | byte-identical; the 3 hits `W: a4 c4 d2 e2 / B: b6 b7 d6 e5 f6`, `W: a5 b3 d4 e2 / B: c6 d7 e6 e7 f7`, `W: a5 c4 d4 e3 / B: b7 d7 e4 e6 f7` |
| chunk 1: raw TSV, original vs fixed | identical (6,121,448 lines, md5 8f177b59...) |
| chunk 2 (456,170 roots): hits and summary vs stored | byte-identical (0 hits) |
| chunk 2: raw TSV, original vs fixed | identical (456,171 lines, md5 dc5033cd...) |
| fixed code under the `munmap` emulation (every freed table truly unmapped), w4 case | completes, raw md5 identical; the original under the same emulation exits 139 (SIGSEGV) |
| ASAN+UBSAN on the fixed copy: w4 case, and `--max 10` with 1+9 and 9+1 on C3 | no reports (original: heap-use-after-free / stack-buffer-overflow) |
| second implementation (`cylcgt`, Python, exact CGT values, `Board(W,8,True,True)`, count rule, e.p. aware): chunk-1 hit `W: a4 c4 d2 e2 / B: b6 b7 d6 e5 f6`, and the two new C3 p10 hits of section 6.3 | all three `*2`, outcome N (163 s, 427 s, 442 s) |
| earlier-scan code with the same one-line fix, `../star3_hunt` `cylinder_w4p8_4_4.tsv` (487,623 rows, all nine settings) | fixed build reproduces the stored file byte for byte (md5 15b42686...) |
| earlier-scan code with the same fix, `../star2_width5` `split_4_4.tsv` (5,979,141 rows, 483 MB) | fixed build reproduces the stored file byte for byte (md5 504d52a3...) |

Chunks 1 and 2 passed through 9 and 5 table doublings respectively, so the stale-store path was exercised in the
original runs (the `states=` differences above) and made no difference to any output line.

## 4. Chunk 0 results

Command (the original `scan.sh` line cannot be used as is: it only adds `--only-setting/--chunk` when `BIN` is
exactly `frontier_split1`. Also, the single chunk-0 process had more than 67M states when it died at the 2^27 -> 2^28 doubling; even fixed
it would need a table of at least 2^28 entries = 15 GB, 22 GB while doubling.)
Chunk 0 of 4 was run as the 32 sub-chunks 0..31 of 128, one process at a time under `nice -n 10`, each with its own table,
capped at 2^26 entries = 3.76 GB (`--max-entries 67108864`). Only sub-chunk 22 exceeded 33.5M states (37.7M) and ran at the
cap, at load 0.56, far below the 15/16 limit at which stores are dropped, so no state was dropped anywhere:

```
for i in 0..31: nice -n 10 ./frontier_split1_fixed --cylinder --width 6 --min 9 --max 9 --nw 4 --nb 5 \
    --only-setting 2 --chunk $i 128 --max-entries 67108864 2> c${i}of128.log | awk -v sumfile=c${i}of128.summary.txt -f filter.awk > c${i}of128.hits.tsv
python3 -I merge_subchunks.py c0_sub128
```

`--chunk I 128` for I = 0..31 partitions exactly the white combinations of `--chunk 0 4` (floor(4*total/16)-style
boundaries coincide: 27405 combinations, chunk-0 range [0, 6851)). Merged files: `cyl_w6_p9_4_5_s2_c0of4_fixed.{summary.txt,hits.tsv,log}`.

| | chunk 0 (fixed) |
|---|---|
| roots | **2,822,072** (equals `roots_ready` of the crashed run) |
| default setting (count, e.p. on, e.p.-aware) \*2 hits | **0** |
| \*k with k >= 3 | **0** (largest nimber in the chunk is \*1) |
| outcome histogram, default setting | L:100,937 N:1,507,287 P:3,737 R:1,210,111 |
| sub-chunk states (sum; each sub-chunk has its own table) | 185,137,464; CPU/elapsed about 182 s in total |

Partition check: a second, different partition (64 sub-chunks 0..63 of 256, `c0_sub256/`) gives the same rows,
the same outcome histogram, the same (empty) hit list and max nimber \*1.

Whole 4+5 split on C6 (9 pawns), default setting: chunks 0 + 1 + 2 + 3 = 2,822,072 + 6,121,447 + 456,170 + 0
= 9,399,689 roots (equals the unchunked `roots_ready` in `cyl_w6_p9_4_5_s2.log`); **3 \*2 positions in total, all in
chunk 1; no \*3 or higher**; outcomes N 5,680,877, R 3,286,677, L 414,936, P 17,199. The mirror split 5+4 is the
colour-reversal image of 4+5 (its stored run `cyl_w6_p9_5_4_s2` also crashed); it was not re-run.

## 5. How to run the fixed binary

Same arguments as `frontier_split1`. For anything above a few million roots, split into sub-chunks (each process then
needs only a 1-4 GB table) and merge with `fixed_rerun/merge_subchunks.py DIR` (sums rows/roots/states/outcome
histogram/hit lists of `c*ofN.{summary.txt,hits.tsv,log}`).

## 6. Could the same bug have affected earlier scans?

### 6.1 Crashes: yes, and it did
Every scanner that has this memo table (list in section 1) can fault at any table doubling. On this machine there
are 11 SIGSEGV reports in `~/Library/Logs/DiagnosticReports` whose faulting frame is `solve` (`+412` or `+508`):
`frontier_split` (Oct 21 21:38, 21:42; Oct 22 00:32 x2, 00:33) and `frontier_split1` (Oct 22 00:31 x2, 00:40, 02:07,
02:09, 02:10). For the current builds `+412` (`frontier_split`) and `+508` (`frontier_split1`) are the first instruction of
the entry store (`stp x22,x21,[x8]`, `x8` = `e`); the 00:31 and 00:40 builds of `frontier_split1` are gone, but they fault
at the same `solve+412` as `frontier_split` and show the same unmapped-table hole. A crash leaves a truncated log and an
empty summary, so it does not look like a result to anyone who checks `rows`; runs that finished were fault-free, not
necessarily free of lost stores (see 6.2).

### 6.2 Wrong values without a crash: no
A stale store writes one complete, correct (key, value) record into memory nobody reads again (the freed old table),
or overwrites one other memo entry in the live table. Either way the only effect is that a state is later recomputed;
`solve()` is a pure function of its arguments, so values cannot change. A stale pointer should not reach the live table:
table sizes double, so a freed block is too small to be reused by a later, larger table (the sum of all earlier sizes is
smaller than the next one), and the new table is allocated before the old one is freed. Corruption of malloc
metadata is not expected either (macOS libmalloc keeps large-block metadata outside the block). This is an argument
plus the byte-identity tests, not a proof. Measured evidence: every comparison above that exercised many doublings is
byte-identical (w4: 487,623 rows; chunk 1: 6,121,447 rows; chunk 2: 456,170 rows; `star3_hunt` w4 p8 4+4: 487,623 rows x 9 settings;
`star2_width5` split 4+4: 5,979,141 rows x 9 settings). The only visible trace in finished scans is a `states=` figure larger than
the true number of distinct states by the number of lost stores (tens to hundreds).

So `research/star2_width5` (largest table: 15.5M states per setting -> 2^25 entries, 1.9 GB) and `research/star3_hunt`
(largest 35.9M states, `flat_w6p8_4_4`, 2^27 entries) completed and their values are unaffected. A scan that
crashed produced no output to trust; a scan that finished is correct.

### 6.3 Stored outputs in this directory that are crash artifacts
These have `rows` blank in the summary (the pipeline's awk got no data) and a truncated log, so they read as "0 hits"
but are not results. Fixed re-runs are in `fixed_rerun/` (nine-setting runs where the original was nine-setting):

| stored scan | what happened | fixed re-run |
|---|---|---|
| `cyl_w3_p10_5_5` | crashed in setting 3 | 205,280 roots; **default setting 2 \*2 hits**: `W: a2 a5 b2 b4 c2 / B: a7 b5 b6 c4 c7` and `W: a2 a5 b3 b4 c2 / B: a7 b5 b7 c4 c7` (both also computed as `*2` by the independent Python `cylcgt`, 427 s and 442 s); no \*3+ in the default setting; 11 rows with nimber >= 2 in some setting (count/epoff has 3 \*2 and 2 \*3+, max \*3) |
| `cyl_w3_p10_6_4` | crashed in setting 2 | 163,114 roots, no hit in any setting; `rows`, `default_*` and the `count/epon/aware` line equal the stored mirror `cyl_w3_p10_4_6` |
| `cyl_w3_p9_4_5` | crashed in setting 2 | 129,746 roots, no hit; equals the stored mirror `cyl_w3_p9_5_4` with L and R swapped |
| `cyl_w3_p10_1_9` | finished but wrong root count (`ib[8]` overflow) | 2,681 roots (not 2,560), still no hit; stored `hits.tsv` is correct, stored `rows` is not |
| `cyl_w6_p9_4_5_s2`, `_s2_c0of4` | crashed | superseded by chunks 0/1/2 above |
| `cyl_w6_p9_5_4_s2` | crashed | mirror of 4+5, not re-run |

`cyl_w3_p10_9_1` and the other stored p10 splits (2_8, 3_7, 4_6, 7_3, 8_2) re-run identically (hits and summary byte-identical).
The `*_1_8`, `*_8_1` empty summaries are genuine (0 roots).

## 7. Files

* `frontier_split1_fixed.c`, `frontier_split1_fixed` (binary)
* `fixed_rerun/cyl_w6_p9_4_5_s2_c0of4_fixed.*` merged chunk 0; `fixed_rerun/c0_sub128/`, `c0_sub256/` per-sub-chunk logs
* `fixed_rerun/verify/` chunk 1/2 and w4 outputs and md5s; `fixed_rerun/cyl_w3_*_fixed.*` re-runs; `fixed_rerun/merge_subchunks.py`

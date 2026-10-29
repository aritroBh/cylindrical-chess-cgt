## 8. What was reused, what was re-run, what was audited

**What I found in the directory.** Earlier attempts (the task says three were stopped, the last by the reboot) had left `scripts/`, `logs/` (files dated 2026-10-27 16:14 to 2026-10-28 03:44), a `summary.json` and an `EDITS.md` (both written 2026-10-28 02:28 to 02:31),
and `verify/` (a from-scratch enumerator that uses ref3m only; 2026-10-28 02:34 to 03:44), but **no FINDINGS.md**. The machine's uptime shows the reboot was at about 2026-10-27 20:43, so those files come from runs after it; I did not rely on any process or PID from them.
This attempt audited those files and did the following.

**Reused after audit (read, and every number below that comes from them was either re-computed fresh or is marked "reused").**
- Scripts: `scripts/k26lib.py` (geometry, enumeration, classifier; read in full), `search.py` (t2 and t1 searches; read in full), `over3.py` (exact under/over; read in full, the king-freeze filter is Lemma 4.9, re-proved below),
  `enum2.py` (second enumerator, read in full), `audit_s1.py`, `audit_t1.py`, `confirm.py`, `confirm_all.py`, `ctxtest.py`, `ctx_exh.py`, `dmodel.py`, `final_ctx.py`, `build_edits.py`, and the referee's `verify/scripts/my_t2.py` (third enumerator, read in full).
- Logs of the earlier attempt that were **not** re-run here (marked "reused" where they appear): the four-file search (`logs/cyl_8x6_22_t1_nf4_*`, `logs/over3_cyl_8x6_22_nf4_*`, and the earlier `over2_*` runs without the king filter), the sampled context tables for the other 26 − 20 group ids and the older runs of the exhaustive contexts (`logs/exh/`, `logs/ctx_*`), `logs/zc_boards*` (widths beyond 10), the first audit (`logs/audit_*`, `logs/audit1_*`), `verify/logs/`.
- The old `EDITS.md` was re-checked: all ten OLD blocks occur exactly once in the current LOOPY.md (`scripts/build_edits.py --check-only`), and the new one is built from this attempt's numbers.

**Rebuilt by me:** all four binaries (`bin/kp`, `bin/kpp`, `bin/ref3`, `bin/ref3m`), from the sources whose md5 are: kpsolve.c 8ff499658aa67448c89ad0955dfcbcfe, kp_p.c f668d4d4861e1d89792245632e01516c,
ref3.cpp a9cd9ed267e3016c789138d86974d658, ref3m.cpp 1b0c8cd670ab54a9e3b385e14717cd63 (the same as in the earlier attempt's `summary.json`). Binaries are deleted at the end.

**Re-run fresh with the rebuilt binaries (tag prefix `k26f_`; `logs/f/`):** the two-shuttle (t2) and one-shuttle (t1) searches for at most 2 + 2 pawns on flat 7×6, cyl:7×6, cyl:8×6, flat 8×6 and flat 7×7; the t2 searches for 3 + 2 and 2 + 3 on cyl:8×6,
for 2 + 3 on flat 7×6 and for 3 + 2 on cyl:7×6; the t1 searches for 3 + 2 and 2 + 3 on cyl:7×6; the second-enumerator audits of both types (≤ 2 + 2); the ref3m confirmation of every exact group; the sampled contexts of the 20 selected groups. `audit/compare_fresh.txt` compares each fresh result with the earlier attempt's merged result:
candidate counts, stage-1 histograms, class counts and the *sets* of exact groups are identical on every line that was re-run.
**Not re-run (the shared lock was held by other jobs for most of the time; the chains `scripts/queueF*.sh` were killed by me at the end by their recorded PIDs, so nothing is left running):**
the t2 searches cyl:7×6 2 + 3 and flat 7×6 3 + 2 (colour mirrors of searches that were re-run, with equal counts in the earlier attempt); the t1 searches for 3 + 2 and 2 + 3 on cyl:8×6 and flat 7×6 (their counts are quoted in section 4 as reused);
the exact under/over searches (`over3.py`, `over2.py`); the collapsed-promotion searches; the exhaustive ≤ 3-pawn contexts; the third-enumerator run for flat 7×7. All of these are reused from the earlier attempt and are labelled so where they appear.

**Independent audits of this attempt.**
- A from-scratch candidate counter (`audit/count_cands.py`, no solver, no K26 code): 817,270 (2+2, H = 6), 1,886,421 (3+2 and 2+3, H = 6), 4,040,080 (2+2, H = 7) two-shuttle placements; 631,179, 1,602,414, 1,517,293 and 2,790,987 one-shuttle placements.
  All equal the counts of the searches (`audit/count_cands.log`).
- Three implementations of the two-shuttle search agree on every count of total leaks 0, 1, 2 for 2 + 2 on flat 7×6 and cyl:8×6: `search.py` (k26lib + kpp), `enum2.py` + `audit_s1.py` (kpp and ref3m on the same roots, full move lists compared), and the referee's `my_t2.py` (own enumerator, ref3m only).
- Negative control: `confirm_all.py` run on two groups that are *not* exact (Z_A, and Z_B placed on flat 7×7) reports 9 failures (`logs/f/confirm/negcontrol.json`); on the 113 found groups it reports 0.
- The passer flags of `k26lib` equal `cylcgt.pawns.passed` on all 2 + 2 placements of H = 6 and 7 (`logs/check_passer.log`).

**Fresh second-enumerator and second-solver audit (`audit/audit_fresh.txt`; both solvers run on the same roots, complete move lists compared, promotions normalised to one entry per push or capture, 8 shards per board):**

```
@@AUDIT@@
```

The older audit (`logs/audit_merged.json`) has exactly the same counts. The third implementation (the referee's `verify/scripts/my_t2.py`, ref3m only, own enumerator and leak classifier; `verify/logs/my_*.json`, reused) gives, for 2 + 2:
flat 7×6: 817,270 placements, totals 0 / 1 / 2 = 2 / 12 / 6; cyl:8×6: 817,270 placements, totals 0 / 1 / 2 = 4 / 0 / 4 (promotions once). The same as the other two.


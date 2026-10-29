## 9. Labels

- PROVED: Lemma 4.9 (section 3; hand proof, re-derived by me against the definitions; its use in `over3.py` is also checked by the unfiltered runs). Nothing else in this note is proved by hand.
- CHECKED-2: the 8 roots and complete move lists of every exact group (kpp and ref3m, 113 groups, 492 roots; 20 groups in both orientations, 240 roots with full move lists); the exhaustive two-shuttle search for ≤ 2 + 2 pawns on flat 7×6, flat 8×6, cyl:7×6, cyl:8×6 (enum2 + kpp + ref3m: 0 differences on every value and move list).
- COMPUTED-1: all other search counts (3 + 2, 2 + 3, flat 7×7, the one-shuttle and under/over searches, the four-file search; partly reused, section 8), and every context result (the D-model prediction is an independent implementation, but the P values come from kpp, partly re-solved with ref3m).
- CONJECTURE: that Z_B is exactly two-shuttle in P in every context; that Z_B is exact on the cylinder in the sense of a hand proof; "over is realisable on the cylinder with wider groups".
- Solver results are never PROVED.

## 10. Reproduce (all paths under `kings/delegate/out/K26/`; `PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames`, python `/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python`)

- Build: `cc -O2 -o bin/kpp ../K7/scripts/draft/kp_p.c -lpthread`, `c++ -O2 -std=c++17 -o bin/ref3m ../K23/verify/ref3m.cpp`, also `bin/kp` from `kings/kpsolve.c` and `bin/ref3` from `ref3.cpp`.
- Z_B / Z_C roots: `printf 'Kb2 ka4 Pa3 Pb4 pb3 pc4 w -\nKb2 ka4 Pa3 Pb4 pb3 pc4 b -\n' | bin/kpp --board cyl:7x6 --ep on --promote QRBN --cap 1 --pmodel --moves` and `... | bin/ref3m --board cyl:7x6 --moves` (for flat boards `--board flat7x6` with ref3m); Z_C: `Kc2 ka4 Pa2 Pc4 pa3 pc5 w -` on `cyl:8x6`.
  All eight roots of the four named groups on three boards: `audit/movelists.sh`; on 32 boards: `audit/named_groups.py`.
- Two-shuttle search (class a, d): `scripts/search.py --board cyl:8x6 --nw 2 --nb 2 --type t2 --tmax 12 [--shard i/n] --tag NAME` (through `../../heavy.sh`), output `logs/NAME_summary.json`, `logs/NAME_groups.jsonl`. `--type t1` is the one-shuttle search (classes c and loose). `K26_COLLAPSE_PROMO=1` counts promotions once.
  The whole fresh set: `scripts/queueF.sh`, `scripts/queueF_over.sh`, `scripts/queueF_collapse.sh`, `scripts/queueF_ctx.sh`, `audit/queue_audit.sh`, `audit/queue_audit1.sh`.
- Exact under/over (class b): `scripts/over3.py --board cyl:8x6 --nw 2 --nb 2 [--nf 4] [--shard i/n] --tag NAME` (output `logs/NAME.json`).
- Counts without a solver: `audit/count_cands.py H nW nB`. Comparison of fresh and reused runs: `audit/compare_fresh.py`. Audits: `audit/audit_s1_fresh.py`, `audit/audit_t1_fresh.py`, merged by `audit/audit_merge_fresh.py`.
- Confirmation of exact groups with ref3m: `scripts/confirm_all.py`, `scripts/confirm.py logs/groups_final.json OUT.json`. Contexts: `scripts/ctxtest.py groups.json OUT.json --nbase 66 --nflip 6 --ncheck 12 --seed 3`, `scripts/ctx_exh.py ZB cyl:8x6 efg 3 i/12 OUT.json`.
- Tables: `audit/make_tables.py`, `audit/final_ctx_fresh.py`. `summary.json`: `audit/make_summary.py`. `EDITS.md`: `scripts/build_edits.py`.

## 11. Not done

- A hand proof of Z_B on the cylinder or of Z_C; chess results for Z_C beyond the cap-1 probe; the five open chess deviations of Z_B (K28).
- F_Z elsewhere on a flat board, more than four files, more than 3 + 2 pawns, king groups with a king outside F_Z, groups with both kings on single squares (zero-type), 7 or more ranks for duds beyond flat 7×7.
- A diagnosis of the six roots where Proposition 4.6 fails for loose groups and of the on-group context mismatches (section 4).
- Flat 8×6 gives the same counts as flat 7×6, flat 7×7 was searched for 2 + 2 only.

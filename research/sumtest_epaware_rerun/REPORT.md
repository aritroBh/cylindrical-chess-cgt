# Rerun of the sumtest comparison with e.p.-aware engine (2026-11-23)

1. With both sides e.p.-aware (engine `PASSED_RESPECTS_EP=True`, solver `aware`), all 2,483,775 pairs match, in every solver scope/mode option.
2. Controls reproduce 0: textbook vs textbook, and e.p. off, each 2,483,775 pairs.
3. Mixed-convention rows reproduce the old 13,176 cases / 109,157 pairs, so the old disagreement was the convention mismatch only.

## Selection of options
- Solver (`sumsolver.py`, via `enum_positions.EPV`): `off` = e.p. off; `plain` = e.p. on, textbook test (`ep_aware=False`); `aware` = e.p. on, aware test; `*-global` = e.p. right lasts until any move anywhere (`ep_scope="global"`, whole mode only). `mode` is `whole` (first passed pawn anywhere ends the sum) or `comp` (components split, integers add; component scope only).
- Engine: `pawns.PASSED_RESPECTS_EP` (module flag, set before `pawns._value.cache_clear()`), `pawns.RACE_RULE`, and `pawns.Board(files, 8, wrap, ep)` for e.p. on/off. The engine has NO whole/comp or local/global switch; `sum_safe` is only reported by the old driver, not used for the prediction. So "scope options" are solver-side only; the engine value is compared against each solver option.
- The old driver ran the engine only with the default flag and compared with all solver variants. As written it cannot set the flag, so I copied it.

## Table (55,195 positions x 3 race rules = 165,585 cases; x 15 X = 2,483,775 pairs per row)
| row (engine / solver) | solver mode | cases | pairs | cases differing | pairs differing |
|---|---|---|---|---|---|
| aware / aware | whole | 165,585 | 2,483,775 | 0 | 0 |
| aware / aware | comp | 165,585 | 2,483,775 | 0 | 0 |
| aware / aware-global | whole | 165,585 | 2,483,775 | 0 | 0 |
| textbook / plain (control) | whole | 165,585 | 2,483,775 | 0 | 0 |
| textbook / plain (control) | comp | 165,585 | 2,483,775 | 0 | 0 |
| textbook / plain-global (control) | whole | 165,585 | 2,483,775 | 0 | 0 |
| e.p. off / off (control) | whole | 165,585 | 2,483,775 | 0 | 0 |
| e.p. off / off (control) | comp | 165,585 | 2,483,775 | 0 | 0 |
| aware engine / plain solver (mixed, expected mismatch) | whole | 165,585 | 2,483,775 | 13,176 | 109,157 |
| textbook engine / aware solver (mixed, expected mismatch) | whole | 165,585 | 2,483,775 | 13,176 | 109,157 |

The aware row is zero, so no differing position needs diagnosis.

## What I changed in the copies
`enum_positions.py`, `compare_cylcgt.py`: only the imports (`sumtest.x` -> `x`) and `OUT` now points to `./data`. `sumsolver.py`: unchanged copy (same SHA-256). New `rerun.py`: runs the engine under three settings (aware, textbook via flag False, off), runs the solver variants, compares, prints the table. Originals and `sumtest/data` untouched.

## Commands
```
cd /Users/aritro/Downloads/Research/Chessendgames
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:research/sumtest_epaware_rerun nice -n 15 /usr/bin/time -l .venv/bin/python research/sumtest_epaware_rerun/rerun.py > logs/run.log 2> logs/time.log
```
2 worker processes. Wall 259.9 s (user 501 s), max RSS 295 MB (parent; peak footprint 55 MB). No kill commands used; no `.pid` files (no signals sent).
Git HEAD (read-only): 2be1c6eabc86b1ac806cd97fbd50604fd64070dc (working tree has uncommitted changes elsewhere).
SHA-256: `cylcgt/pawns.py` 962c3bf6e467cc6766eff1b9be9aee414a330ea9b48f16768b3db427738f7483; `cylcgt/cgt.py` e15ae5b8ca4deff7f21b3722b41bc53995921edcbf082de67a3c562d67e40ff2; `sumtest/sumsolver.py` 2cf688912330783c11ba0f7f9f0c2db8f2413c658283ec79368c4627f451fbfa (also in `logs/sha256.txt`). `data.tar.zst` holds the per-position outcome files (zstd -t tested); `logs/run.log` has the table.
Note: the SHA of `pawns.py` is of the working tree file at run time; check `git diff --stat cylcgt/` if the committed version is what the paper cites (not checked).

## Sentence for the paper
"All 4,967,550 outcomes of G+X match under the textbook test, e.p. on and off, and all 2,483,775 under the e.p.-aware test." This is true as written: 2,483,775 (textbook, e.p. on) + 2,483,775 (e.p. off) = 4,967,550, and 2,483,775 under the e.p.-aware test (for each of the whole, comp and global-scope solver options).

# Summary

- **COMPUTED-1** The C8 reference example `W5 B7 W4 W4B7 B6 W3B6 W2 B4` solves as `NNPN`; the search driver classifies it as `NNPN` when given that ring.
- **COMPUTED-1** All 20 rows in the C8 ten-pawn hit list pass the offset-2 wall and no-passer predicates; canonical widths are 4 for 4 rows and 6 for 16 rows.
- **COMPUTED-1** The pre-existing C9 slice `(w=4,d=2,r=2,p=0)` emitted and solved 208,633 records with zero `*2` and zero `*3`; this is a pre-fix count and is not a trusted count for legal rings.
- **COMPUTED-1** The enumerator can generate a same-square W/B overlap that passes its no-passer and symmetry predicates, so its C9 counts need to be rerun after correcting candidate generation.
- **COMPUTED-1** The C9 answer for the requested expanded space remains undetermined: required `nice -n 15` launches fail with `setpriority: Operation not permitted`, and no C11 extensions were checked.

## Scope and conventions

The requested model is the whole-board pawn game with White = Left, Black = Right, normal play, `RACE_RULE="count"`, en passant on, and the e.p.-aware passed-pawn test. A signature `NNPN` is `*2`; `NNNP` is `*3`.

Claims below are labeled **COMPUTED-1** because they come from one implementation or a direct execution of the task's C solver. No new result is **CHECKED-2**.

## C8 validation

**COMPUTED-1.** The listed C8 ten-pawn hits contain 20 rows. A direct pass over the list found all 20 have an offset-2 single-pawn wall in some symmetry and have no passed pawn. Their canonical descriptor widths are `{4: 4, 6: 16}`. Reference: `research/star26_rings/c8/p10_5_5_hits.tsv`.

**COMPUTED-1.** The specified example is row 17 of that list. The unchanged `rg` binary returned `NNPN nodes=1479`. Calling the existing `search.py` batch and classification functions on the same record returned `driver_classification=NNPN`.

**COMPUTED-1.** At 17:50:55, the full C8 enumerator-to-driver validation was still running. Its external log was at `emitted=3,356,000`, `solved=3,356,000`, `nim2=0`, `nim3=0`, with no final summary. This is incomplete and does **not** establish that the enumerator emitted the example. The log is `/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/val_c8_w6_p0.log`.

### C8 reproduction commands

Reference list predicates and canonical width counts:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python - <<'PY'
import importlib.util
from collections import Counter
s = importlib.util.spec_from_file_location("c", "research/odd_n_plus_2/check_c8.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
rows = [x.split("\t")[0] for x in open("research/star26_rings/c8/p10_5_5_hits.tsv") if x.strip() and not x.startswith("#")]
c = Counter()
for pos in rows:
    b = m.parse(pos); assert m.no_passer(b)
    assert any(m.descriptors(t, (2,)) for t in m.transforms(b))
    c[m.canonical(b)[1][0]] += 1
print(len(rows), dict(sorted(c.items())))
PY
```

Direct solver check for the named example:

```sh
printf '%s\n' 'W5 B7 W4 W4B7 B6 W3B6 W2 B4' | research/odd_n_plus_2/rg solve 3
```

Driver classification check (this tests `search.py`'s batch and classifier on the named record; it does not test enumeration):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python - <<'PY'
import importlib.util
s = importlib.util.spec_from_file_location("search", "research/odd_n_plus_2/search.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
r = {"position":"W5 B7 W4 W4B7 B6 W3B6 W2 B4", "width":6, "offset":2, "rank":2, "phase":0}
lines = m.solve_batch([r]); hits = m.classify([r], lines)
assert lines[0].split()[0] == "NNPN" and len(hits) == 1
print(r["signature"])
PY
```

## Enumerator integrity finding

**COMPUTED-1.** `enumerate.c` builds each core-file option from any one-to-three of the 12 W/B rank slots but does not reject `c.w & c.b`. The following C8 ten-pawn ring has W and B both on a4; the Python predicate reports no passer, and the symmetry helper gives descriptor `(4,2,2,0)`:

```text
W: a4 c3 d4 f2 h2 / B: a4 b5 d5 e4 g4
```

**COMPUTED-1.** This is enough to make the existing enumerator suspect for exact counts. The minimal candidate-generation correction is to skip any option with `c.w & c.b` in `make_opts()`. It has not been applied because the required regression run could not be started under the mandated priority setting.

**COMPUTED-1.** The regression assertion is now present in [check_c8.py](check_c8.py): it rejects the canonical same-square sample if the C8 width-4 enumerator emits it. It has **not** been run to red or green in this turn.

Reproduce the sample predicate and descriptor:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python - <<'PY'
import importlib.util
s = importlib.util.spec_from_file_location("c", "research/odd_n_plus_2/check_c8.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
b = m.parse("W: a4 c3 d4 f2 h2 / B: a4 b5 d5 e4 g4", 8)
print("pawns", sum(w.bit_count()+bb.bit_count() for w,bb in b), "overlap", [(f,w&bb) for f,(w,bb) in enumerate(b) if w&bb], "no_passer", m.no_passer(b), "canonical", m.canonical(b)[1])
PY
```

## C9 slice status

| Core width | Offset | White rank | Phase | Emitted | Solved | Unsolved | `*2` | `*3` | Status |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 4 | 2 | 2 | 0 | 208,633 | 208,633 | 0 | 0 | 0 | **COMPUTED-1** pre-existing complete run; pre-fix enumerator, recount required |
| 4 | 2 | 2 | 1 | 78,000 observed | 78,000 observed | — | 0 observed | 0 observed | **COMPUTED-1** partial run only; stopped before completion |
| 4–7 | all other requested offset/rank/phase combinations | — | — | — | — | — | — | — | Not run |
| 8 | one-file wall | W2 or B4 | — | — | — | — | — | — | Not supported by current enumerator; not run |
| inserted C8 hits | one W2 or B4 wall file | — | — | — | — | — | — | — | Not run |

The earlier complete slice's exact summary is `summary_c9_w4_d2_r2_p0.json`. Its reproduction command was:

```sh
PYTHONPATH=. .venv/bin/python -u research/odd_n_plus_2/search.py 9 4 2 2 0 --batch 40 --bits 22
```

The partial phase-1 run used:

```sh
PYTHONPATH=. .venv/bin/python -u research/odd_n_plus_2/search.py 9 4 2 2 1 --batch 40 --bits 22
```

**COMPUTED-1.** Neither count is accepted as a final legal-ring count until the same-square option bug is fixed and the slice is rerun. No C9 `*2` or `*3` was found in the portion already computed, but this does not answer whether one exists in the requested space. No C11 extensions were evaluated.

## Blocker and remaining work

The task requires each search process to start under `nice -n 15`. The attempted launch failed before Python started:

```text
nice: setpriority: Operation not permitted
```

The failed launch is recorded in `logs/check_c8_red.log` and its attempted PID in `logs/check_c8_red.pid`. No unprioritized C9 search was started. To finish: run the regression with a shell that permits `nice -n 15`, add the overlap guard, rerun C8 validation, then run the C9 width-4–7 matrix plus the requested one-file-wall and inserted-hit cases, and confirm any hits with whole-board `cylcgt` before evaluating their C11 extensions.

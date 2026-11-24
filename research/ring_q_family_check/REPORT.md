# T55 report: Q-family coverage

## 5-line summary

1. **PROVED —** A separate insertion argument gives `Q_n = *3` for every even `n >= 8`, conditional on the finite reduced-game computations.
2. **COMPUTED-1 —** cylcgt canonical-form arithmetic returned `*3` for the reduced-game bases `n=8,10,...,22`.
3. **CHECKED-2 —** C and cylcgt graph/outcome checks agree: `NNNPNNNN` for the reduced games, and identical graphs for every even `n=8..24`.
4. **CHECKED-2 —** Direct whole-board cylcgt values for `Q_8` and `Q_10` are `*3`; the C solver independently matches their signatures.
5. **PROVED —** Q is a distinct `*3` family, not an omitted `*2` case in the P theorem; this result is whole-board only.

## Source-path audit

**COMPUTED-1 —** The prompt's `research/ring_family_proof/PROOF.md` is absent in this checkout. That folder contains T50's `proof.tex` and a runner for the O/E/F families. The T53-named files are `research/ring_n_plus_2_proof/PROOF.md` and `research/ring_n_plus_2_proof/run_all.sh`; I treated those as the intended P proof and current Q runner. The Q commands are the final four commands in that `run_all.sh`.

## Verdict among (a), (b), and (c)

**COMPUTED-1 — Verdict: (c).** The Q outcomes are not `*2`: the C solver prints `NNNP` for `h=0..3`, whereas `*2` would print `NNPN`. The current runner defines Q separately and computes its `*3` signature; the P proof does not cover Q. The closure here is an additional Q-family `*3` proof in [`PROOF_Q.md`](PROOF_Q.md). Its induction uses the common wall/insertion argument but has a different finite base and cut (`n=22`, `c=9`), so it is not an application of the P theorem without those checks.

## Exact Q configurations in `run_all.sh`

The runner defines

```text
Q_n = W4 B7 (B4 W2)^((n-8)/2) W3B6 W3 W2B5 B5 W2 B4,
```

for even `n=8..60`; each position has `n+2` pawns. I reproduced the Q commands into this folder with [`run_q_family.sh`](run_q_family.sh):

| Q command from the current runner | Configurations | Output from this run |
|---|---|---|
| `pump_verify.py Q 8 60` | Every even `n=8..60`; reduced graph and `G+*h`, `h=0..7` | `NNNPNNNN` for every row. From `n=18` onward: 7,968 nodes, 21,063 kept edges, 17,784 T-options, no e.p. flag. |
| `FIXC=9 pump_verify.py Q 22 60` | Every even `n=22..60`; fixed insertion cut `c=9` | `NNNPNNNN` on every row; each `n -> n+2` step reports start, node, and edge correspondence `True`. |
| `reduced_cyl.py Q 8 10 ... 24` | Even `n=8..24` | cylcgt-based and C reduced graphs are identical at every size. Node/edge-triple counts are below. |
| Feed Q positions for even `n=8..60` to `rg solve 3` | Full unreduced game, `h=0..3` | `NNNP` for every position. |

The Q pump output also reports `NNNPNNNN` at `n=8,10,12,14,16`; no insertion cut is selected there. The fixed `c=9` induction begins at `n=22`; the larger `n=18` graph plateau alone does not establish that induction.

**CHECKED-2 — Reduced-graph comparison.** The `reduced_cyl.py` output was:

| `n` | Nodes | Distinct `(source, side, target)` edges | C/cylcgt match |
|---:|---:|---:|---|
| 8 | 1,894 | 5,661 | yes |
| 10 | 7,141 | 24,716 | yes |
| 12 | 8,556 | 29,659 | yes |
| 14 | 8,756 | 30,069 | yes |
| 16 | 8,112 | 27,803 | yes |
| 18 | 7,968 | 27,359 | yes |
| 20 | 7,968 | 27,359 | yes |
| 22 | 7,968 | 27,359 | yes |
| 24 | 7,968 | 27,359 | yes |

These are distinct graph edge triples; the pump log's K-edge and T-option totals count move options and need not add to that deduplicated total.

## Base values and direct whole-board checks

**COMPUTED-1 — Reduced canonical forms.** [`run_q_base_values.sh`](run_q_base_values.sh) ran cylcgt canonical-form arithmetic for every finite base through `n=22`:

| `n` | Pawns | Reduced nodes | cylcgt reduced value | C signature `h=0..7` |
|---:|---:|---:|---:|---|
| 8 | 10 | 1,894 | `*3` | `NNNPNNNN` |
| 10 | 12 | 7,141 | `*3` | `NNNPNNNN` |
| 12 | 14 | 8,556 | `*3` | `NNNPNNNN` |
| 14 | 16 | 8,756 | `*3` | `NNNPNNNN` |
| 16 | 18 | 8,112 | `*3` | `NNNPNNNN` |
| 18 | 20 | 7,968 | `*3` | `NNNPNNNN` |
| 20 | 22 | 7,968 | `*3` | `NNNPNNNN` |
| 22 | 24 | 7,968 | `*3` | `NNNPNNNN` |

The `*3` column is **COMPUTED-1**. The signatures and edge-for-edge graph agreement are **CHECKED-2**. Direct whole-board calls to cylcgt with components disabled returned `*3` for `Q_8` and `Q_10`; the independent C solver matched `NNNPNNNN` for both (**CHECKED-2**). The direct outputs include runtime and peak RSS: `Q_8` 61.3 s / 72.8 MiB, `Q_10` 323.0 s / 247.0 MiB. For `n=12..22`, the proof uses the reduced-game canonical computation and reduction lemma, not a direct whole-board `pawns.value` call.

## Q proof and limits

**PROVED, conditional on the finite checks above.** [`PROOF_Q.md`](PROOF_Q.md) applies the phase-independent wall and insertion lemmas to Q's shifted E-wall. The base `R_22` has zone `{0,1,2,3,15,16,17,18,19,21}`, so files `5..14` stay exact wall files throughout that reduced game. Insertion at `c=9` maps `Q_n` to `Q_{n+2}` and preserves reduced options; the reduced game therefore stays `*3` for even `n>=22`. Values for `n=8..20` are finite base computations.

Scope is the whole-board game, race rule `count`, and e.p.-aware passed-pawn test. The proof has not yet had a second independent mathematical referee; the program checks do not replace that review. It does not extend the P-family `*2` theorem or assert a component-sum value.

## Reproduction and execution notes

From the project root, run these in order:

```sh
sh research/ring_q_family_check/run_q_family.sh
sh research/ring_q_family_check/run_q_base_values.sh
nice -n 15 .venv/bin/python research/ring_q_family_check/q_whole_cyl.py 8
nice -n 15 .venv/bin/python research/ring_q_family_check/q_whole_cyl.py 10
```

`run_q_family.sh` builds `rg` inside this task folder and writes logs here. `run_source_check.py` uses the existing Python helpers read-only and points them at that local binary; `run_rg_sweep.py` supplies the unreduced Q positions. Individual outputs and stderr/RSS records are in `logs/`. `run_q_base_values.sh` profiles each reduced-value process with `run_source_check.py`.

All heavy processes ran serially with `nice -n 15`; the host reported `nice: setpriority: Operation not permitted`, so it refused to lower the priority. Measured peak RSS: reduced-value processes 23.7–39.8 MiB; Q8 and Q10 direct whole-board solves 72.8 and 247.0 MiB; Q pump/reduced-graph Python processes 175.2, 184.2, and 136.5 MiB; the raw C sweep 270.4 MiB. The recorded maxima were below 4 GiB.

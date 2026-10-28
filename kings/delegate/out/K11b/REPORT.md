# K11b: blind proof and comparison

## Five-line summary

1. **PROVED:** Under (H1)–(H5), β wins F by pushing p on every turn; `PROOF.md` records the blind-first derivation.
2. **SOUND:** LOOPY's Steps 0–5; this review found no gap or counterexample.
3. **PROVED:** Corollary 2.11a's count-rule race credit matches `cylcgt.pawns._child`; its hypotheses certify the outcome.
4. **COMPUTED-1:** A tied race is resolved by `_child` after a move but raises `RaceError` at the root; command below.
5. **PROVED, conditional:** P11 covers W-defined roots when reached terminals and any passer root are certified; roots with no W(X) need explicit scope.

## Blind proof and route

I wrote the initial proof draft from the statement and permitted model/code excerpts before reading LOOPY's proof or comparison rows. After that comparison, I made the en-passant-to-path case explicit and tightened the projection argument. The final proof is independently structured and not copied, but those editorial corrections mean the final file is not an untouched blind artifact. It separates the argument into ordinary capture safety (including H4's capture into a neighboring file), en-passant safety, clear-path preservation, β's king-safety legality, ω's safe king move, and promotion timing.

LOOPY takes a more formal invariant route. Step 0 records three facts about F; Step 1 proves both king properties; Step 2 maintains the strip bounds Jβ/Jω together with the clear-file invariant I1; Step 3 derives that p is neither captured nor blocked; Step 4 projects ω's pawn play into Gω; and Step 5 counts the moves. My proof uses those same facts inline and proves the p-safety and path claims before treating timing. It does not need the three named invariants as a separate package, but it needs their content. I found no step in LOOPY that is unsound or a gap that my proof repairs.

| LOOPY step | Verdict | Check |
|---|---|---|
| 0: facts about F | **SOUND** | The pawn-file, king-move, and promotion facts follow directly from F's rules. My proof uses them inline. |
| 1: king safety | **SOUND** | H2 and file permanence keep β safe; H3 keeps t empty and unattacked, so ω always has a legal king move. |
| 2: invariant | **SOUND** | The strip bounds cover captures into the strip via H4, and distinguish β's turn from ω's turn. The en-passant and double-step cases are accounted for. |
| 3: consequences | **SOUND** | The invariant plus H1 makes each prescribed push available and prevents stalemate. |
| 4: projection to Gω | **SOUND** | p cannot be captured; removing it only removes a blocker. The only usable en-passant cases are the initial right for ω and none against p. |
| 5: timing | **SOUND** | β promotes after d pushes; ω has exactly e moves first, and H5 gives μω ≥ e+1. |

**PROVED:** All H1–H5 are used in my proof. I claim no hypothesis is unnecessary, so no hypothesis-ablation run was warranted. The theorem is sufficient, not a necessity criterion.

## Corollary 2.11a and `_child`

At a terminal reached by a move of M, `_child` is called with `mover=M` and N to move. In the `count` branch, its `other` is N and it chooses N exactly when `promote_distance(N) <= promote_distance(M)`; otherwise it chooses M. That is precisely Corollary 2.11a's race rule, including the tie in favor of the side now to move. If only one side has a passed pawn, `_child` falls through to `value`, which assigns ±BIG to that side. This code identity is **PROVED** from `pawns.py`.

The count rule is not itself a frozen-game certificate. `promote_distance` measures the fastest passed pawn; H5 instead bounds μω over every ω pawn, including a non-passer that can promote sooner. H1's clear-path and no-king-on-path requirements, together with H2–H4, supply the path, legality, king-move, and interference conditions that `_child` does not check. Thus Corollary 2.11a is a sufficient conditional bridge from the count credit to F, not a claim that every count-rule terminal has the same frozen outcome.

There is a root distinction. `_child` resolves a two-sided passer race after a move. At a root, `value()` returns immediately for a one-sided passer; for a connected position with both sides passed, `_value()` raises `RaceError` instead of applying the count branch. If the components split, `value()` sums their `_value`s instead. So a root race does not follow `_child`'s count branch (`pawns.py`, `value`, `_value`, `_child`).

**COMPUTED-1:** On `cyl:8x6`, `W: c5 / B: d2` has both passers and `dp(W)=dp(B)=1`. This is an isolated branch-semantics probe, not a reachability certificate: calling `_child(..., "W")` credits Black (`-W`), as Corollary 2.11a predicts with N = Black; calling `value()` at the root raises `RaceError`. Reproduce from the project root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python - <<'PY'
from cylcgt import cgt, pawns

board = pawns.Board(8, 6, True, True)
pos = pawns.Pos.parse("W: c5 / B: d2")
pawns.RACE_RULE = "count"
pawns._value.cache_clear()
print("passed:", pawns.passed(board, pos, "W"), pawns.passed(board, pos, "B"))
print("dp:", pawns.promote_distance(board, pos, "W"), pawns.promote_distance(board, pos, "B"))
print("_child after W move:", cgt.show(pawns._child(board, pos, "W")))
try:
    pawns.value(board, pos)
except pawns.RaceError as exc:
    print("root value:", type(exc).__name__)
PY
```

## P11 scope

**PROVED, conditional:** The amended P11 chain is complete for roots where W(X) is defined and every required certificate is supplied: Corollary 2.11a certifies each passer/race terminal reached by a move; Proposition 2.11 certifies X itself whenever a root already has a passer and identifies β as the side W(X) credits; the row also requires condition (E). The S(X) conclusion additionally requires hereditary sum-safety. In the stated parked-king layout, Corollary 2.11b supplies the listed H2/H3 and king-path facts; H4 and H5 still need certification for the selected beneficiary pawn.

The root clause should make its domain explicit: it covers roots for which W(X) exists and whose W(X)-credited side has a passer satisfying Proposition 2.11. A connected root with both sides passed has no W(X) in the current `value()` implementation (`RaceError`); Corollary 2.11a only resolves a race reached after a move. If P11 is intended to cover such roots too, that root case remains a **GAP** until its D-model outcome is defined and certified. With W(X)'s existence and the root certificate as premises, the amended P11 is complete on its conditional domain.

## Labels and reproduction

- Proposition 2.11: **PROVED**, conditional and sufficient under H1–H5 in frozen F; no necessity claim.
- Corollary 2.11a: **PROVED**, conditional; its count-rule selection matches `_child` for terminals reached by a move.
- Corollary 2.11b: **PROVED** for the stated layout premise that every pawn is on c–g.
- P11: **PROVED**, conditional on its terminal certificates, W-defined root scope, root certificate when a passer is present, and condition (E); hereditary sum-safety is needed for S(X). Clarify how roots with both passers are scoped.
- The tied-race/root probe above: **COMPUTED-1**. No `kpsolve` position batch was needed: Proposition 2.11 was not found false, and no hypothesis was claimed redundant. No solver value is claimed from this run.

Private solver build, from the project root:

```sh
cc -O2 -o kings/delegate/out/K11b/kp kings/kpsolve.c -lpthread
```

**Process note:** after the initial proof draft was written, one recursive locator search accidentally traversed the prohibited K10/K11/K12 output paths and printed excerpts. I disregarded those results; the draft predates that search, and the comparison above uses the named LOOPY sections and current source code.

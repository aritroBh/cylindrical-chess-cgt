# L14 second cold read — opencode

## Summary (5 lines)
1. Part A checks out: the 1/8 value, the open-root check, and the HSS counterexample are correctly stated and verified independently.
2. The monotonicity proof in `lean/CylChess/Claims/L5_EmptyTable.lean` is sound; the 1/8 claim holds for every race function in all nine settings.
3. The L6 witness lines of `lean/CylChess/Claims/L6_NotHSS.lean` are legal, have no earlier passed pawn, and really produce opposite threats.
4. The Möbius controls of `lean/CylChess/Claims/L7b_Mobius.lean` (`RNRRR`, `NNRRR`, `LLLLL`) and the `F3(0)` member (`*2`, `h=0..6`) match an independent reimplementation of the whole-board game with a heap.
5. No `sorry`/`axiom`/`unsafe`/`partial`/`implemented_by`/`@[extern]` occurs in the audited files; the remaining trust issue is that every ring result rests on `native_decide` plus memoized search, as the authors state.

## Part A — corrections after round 1

### `lean/CylChess/Claims/L5_Eighth.lean`, `L5_EmptyTable.lean` (Theorem `thm:eighth`)
- Statement matches the paper: `posG = W a2 b2 b3 / B a5 a6 b6` on the ordinary 8-file board, value `1/8`, all nine settings.
- `L5_EmptyTable.eighth_empty_table_nine_settings` checks the empty race table by `native_decide`; `eighth_empty_table_default_kernel` checks the default setting by `decide +kernel`.
- `withRace` (`L5_EmptyTable.lean:90`) and `Le` (`:28`) implement "less defined than" correctly.
- `comp_options_le` (`:92`), `sum_options_le` (`:112`), `wins_mono` (`:124`) correctly propagate a defined answer under a more defined race function: an undefined race becomes an unavailable option, and `anyOpt_mono` (`:65`) preserves `some b`.
- `isValue_mono` (`:162`) applies `wins_mono` to both colours, so `eighth_every_race_function` (`:171`) follows.
- Independent check: `delegate/out/L14_opencode/referee_A.py` reimplements the rules, passed-pawn test, components, `Game.wins`, and `IsValue` from the paper's text. It reports `isValue 1/8 = True` for all nine settings with the race table empty (reproduce: `.venv/bin/python delegate/out/L14_opencode/referee_A.py`).

### `lean/CylChess/Claims/RootsOpen.lean`
- `open_` (`:21`) is exactly "no passed pawn for either colour".
- `roots_open_AB`, `roots_open_G` (`:25`, `:29`) are by `decide` (kernel) over all nine settings; `roots_open_X` (`:33`) is by `decide` for `⟨.off,.count⟩`.
- Independent check confirms `posX`, `posG`, `posGMirror`, `posA`, `posB` have no passed pawn in the relevant settings.

### `lean/CylChess/Claims/L6_NotHSS.lean` (Proposition `prop:sumcounter`, "X is not HSS")
- `lineOK` (`:37`) checks legality and the absence of a passed pawn at every position from which a step is made, but not the last position; the last positions are tested separately. This matches the definition.
- `x1`, `x2` (`:44`, `:48`), `bd`, `fh` (`:52`, `:55`) match the paper's witness.
- `notHSS_way_in` (`:73`) confirms the route `h5-h6`, `a7xh6` across the seam, no passed pawn at `x2`, and `components cyl8 x2 = [bd, fh]`.
- `bd_white_threat` (`:80`) and `fh_black_threat` (`:86`) confirm opposite threats; `fh_race_line` (`:92`) confirms the alternative race line.
- Independent check reproduces all of these: `way_in lineOK = True`, `bd threat = True`, `fh threat = True`, `fh race line = True`, with the expected passed-pawn outcomes.

## Part B — Möbius strip

### `lean/CylChess/SearchWide.lean`, `Families.lean`, `Claims/L7b_Mobius.lean`
- `WH` (`SearchWide.lean:64`) is the whole-board game `G + *h`: pawn moves via `Rules.moves`, terminal positions decided by `Env.verdict`, heap moves lower `*h` to `*i` with the turn passing, and the e.p. right survives a heap move. This is the game defined in supplement S13.
- `passedF` (`:101`) and `scan` (`:137`) are the fast versions; their agreement with `hasPassed`/`WH` is tested, not proved, by `SearchWideAgrees.lean`.
- `Families.f1`/`f3`/`tt` (`Families.lean:85`, `:91`, `:94`) are the supplement's file lists; `Fam.ofFiles` (`SearchWide.lean:56`) parses them.
- `checkMob` (`L7b_Mobius.lean:17`) checks width, pawn count, and `starTest` for `h = 0..6`.
- `Mobius_controls` (`:32`) checks the three signatures `RNRRR`, `NNRRR`, `LLLLL`.

Independent check: `delegate/out/L14_opencode/referee_B_mobius.py` reimplements the rules (including Möbius seam captures, blocks, and passed pawns), the count race rule, and the whole-board game with a heap `WH` directly. It confirms:
- `F3(0)` (width 7, 8 pawns) is `*2` for `h = 0..6`: outcomes `TT, TT, FF, TT, TT, TT, TT`.
- Controls: `F1(0)` = `RNRRR`, `F2(0)` = `NNRRR`, `TT(0)` = `LLLLL`.

Reproduce: `.venv/bin/python delegate/out/L14_opencode/referee_B_mobius.py` (h=0..4) and `.venv/bin/python delegate/out/L14_opencode/referee_B_mobius_h0_6.py` (h=0..6).

## Trust

- Audited A files contain no `sorry`, `axiom`, `unsafe`, `partial`, `implemented_by`, or `@[extern]`.
- `eighth_empty_table_default_kernel` and `RootsOpen`/`L6_NotHSS` route checks are by `decide` (kernel); `eighth_empty_table_nine_settings`, `L5_Eighth`, `L6_SumCounter`, and all L7b results are by `native_decide`, trusting the Lean compiler/interpreter.
- The ring results depend on the memoized searches `Search.isValue` and `Wide.wide`; their agreement with the specifications is tested (`SearchAgrees`, `SearchWideAgrees`, `HeapsAgrees`), not proved.
- The authors' own notes (`lean/notes/L7_L10.md`, `lean/notes/L8_L9.md`) already record these limitations; this audit found no additional discrepancy.

## Not checked

- The insertion argument carrying the base cases to all `n` is not formalized; only finite instances.
- `SS(m)` and the cylinder families other than the Möbius controls/member above were not independently recomputed.
- The atlas, census, Dawson, and cut-lemma parts were not part of this run's independent checks.
- The completeness of `raceKeys` in `L5_Eighth.lean` is not needed for the proved monotonicity statement and was not checked.
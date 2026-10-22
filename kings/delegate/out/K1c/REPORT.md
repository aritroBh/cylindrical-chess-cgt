# K1c report — LOOPY.md §3–§6 and Appendix A

**Output:** `kings/delegate/out/K1c/EDITS.md` (27 edits + the `## STATUS ROWS` section).
Everything else in this directory is scratch: `make_edits.py` (the generator that copies each OLD block
byte-exactly out of the note by line range), `LOOPY_applied.md` (the note with the 27 edits applied, used to
proof-read the result), `p4_probe.txt` and `p4_reproduce.txt` (kpsolve runs, see below).

`kings/theory/LOOPY.md` was **not** edited: the orchestrator applies `EDITS.md` with
`kings/delegate/apply_edits.py`. I verified the file applies cleanly: `27 applied, 0 rejected`.

---

## 1. The one substantive result: P4 is refuted

The note's §6 table lists P4 as a CONJECTURE: the theory predicts that the Z = 0 convention is *right* for the
group `Z_T = Ka4 Pb3 / kc3 pb4` in all six contexts. kpsolve refutes that in 3 of the 6 contexts:

| context | theory | kpsolve (C) |
|---|---|---|
| H\* = `Pe3 / pe5` | (W, L) | **(D, L)** |
| H\*2 = `Pe2 / pe5` | (W, L) | **(D, L)** |
| H0 = `Pe3 / pe4` | (L, W) | **(L, D)** |

The other three (nothing, Hm1, Hp1) come out as predicted. `kings/results/PREDICTIONS.md` and
`kings/results/theory_P4_cap2_moves.txt` already carry the numbers; I have added them to the note's table and
written the mechanism into §6:

> the defending king walks to the locked context pawns (…Kd3, …Kd2, …Kd4) and attacks the stuck pawn there.

That is Proposition 2.10(b) in action — the zero of the group is context-dependent — and it kills the (L2)
margin the theory assumed. This is the only place where the *theory* (not just a label) had to be downgraded,
so it is worth a second pair of eyes from the orchestrator: the §6 P4 row now reads
`CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts`.

A second, smaller result: **§5.5's "Black has an escape" is now backed by kpsolve, and its move list is
complete.** The note had it as scratch evidence and had missed one of Black's four legal king moves (…Kd3).
kpsolve on `Ka4 Pb2 / kc4 pb3` (8×6) gives (D, D) after …Kc5 — White cannot force promotion, with or without
the passes — and (W, W) after …Kd3, …Kd4 and …Kd5, so the escape is exactly …Kc5. The bullet keeps the label
CONJECTURE (scratch), because a kpsolve run is data, not a proof (LOOPY.md, "Labels", line 86); it gains
"kpsolve agrees".

## 2. The edits, by review item

| edit(s) | review item | what changed |
|---|---|---|
| 1 | R4 item 7 | Proposition 3.2's chess bridge: added (V1a) as a hypothesis, label "PROVED after repair". Witness: in P2 + H\* the step e3–e4 stalemates Black, so the bridge may only be used along a strategy that avoids it. |
| 2 | R4 item 6 | "With shuttles on both sides": PROVED → CONJECTURE; needs a two-sided Proposition 3.2 (bisimulation on the four combined king states). |
| 3 | R4 item 3 | Theorem 4.2(a): R_n must have no Black options; τ of Definition 1.10 corrected to count moves into ⊕/⊖ by *either* player. Counterexample recorded (frontier `B + (−B−1) = −1 ∈ 𝓡`). |
| 4 | R4 item 4 | Theorem 4.2(b): the D-model equivalence to `R_ℓ^W` is now proved; the CGT statement needs `B > ℓ` (Lemma 1.7 is a D-result, not a CGT equality). |
| 5 | R4 item 5 | Theorem 4.2(c): negative integers included; "is on_D" needs Proposition 3.2's hypotheses; the closing sentence says **acyclic**, not "non-reversible". |
| 6–8 | R4 items 1, 2; R1 item 11 | Proposition 4.3: **FALSE as stated** (a king in check) → repaired with (H1) s is not in check on u and (H2) the reply is not a promotion and does not attack u. Counterexample `Kb2 Pc2 / kc4 pc3` added. The "0 or ∞" dichotomy is narrowed to king steps inside F_Z with the opponent frozen at *both* u and v, with three caveats. |
| 9 | R4 item 2; R1 item 11 | "n safe spare moves": the sentence now says what Proposition 4.3 (repaired) actually proves. |
| 10 | R1 item 11 | "**Over.**" → "**Definition 4.4 (over).**" (the numbering jumped 4.3 → 4.5). |
| 11 | R4 item 8 | "over" chess reading: the claim "typically a pawn move by Proposition 4.3" is withdrawn — Proposition 4.3 assumes a frozen opponent that replies outside Z; an over-group's opponent shuttles *inside* Z. |
| 12 | R1 item 10; R4 item 8 | Conjecture 4.7: "≤ 3 + 2 pawns" → "≤ 2 + 2 pawns" (what Appendix A's search actually covered). |
| 13 | R1 item 11; R4 item 9 | §5.1 "Frozen in the convention": the enumeration is written out instead of being deferred to the diagram audit. |
| 14 | R4 item 9; R1 item 11 | §5.2: the heading claimed more than the proof; split into "the certificate fails — PROVED by Lemma 2.9" and "not punished in P — CONJECTURE (scratch)", with the C-side fact (kpsolve: Z_72 bare = (D, W)) added. |
| 15 | R4 item 6 | §5.3 "Without the pawn break" → CONJECTURE. |
| 16 | R1 item 11 | §5.4 "Z_onT1 realises `on`" → labelled PROVED in P. |
| 17 | R1 items 10, 11; R4 item 9 | §5.5: Black's fourth legal king move **Kd3** added (Kc3 is illegal: White's pawn b2 attacks c3), and the "Black has an escape" bullet now carries kpsolve's numbers. Per the note's label rule (LOOPY.md line 86: "kpsolve results are data, not proofs") the bullet keeps the label CONJECTURE (scratch) with "kpsolve agrees": after …Kc5 the position is (D, D), after …Kd3/…Kd4/…Kd5 it is (W, W), so the escape is exactly Kc5. |
| 18 | R1 item 11 | §5.6: the μ/T chain now carries labels (μ_W = 5 PROVED by count; T = 5 and "(L2) fails by one tempo" CONJECTURE, scratch — R4 re-derived both). |
| 19 | R1 item 5 | §6 preamble: `--cap 2` for the three P4 rows documented; the column list and a reproduce command added; "naive convention" renamed "Z = 0 convention" (the name used in `PREDICTIONS.md`). |
| 20–23 | PREDICTIONS.md | §6 table: new **kpsolve (C)** column for every row (P1a, P1b, P2, P3, P4, P5, P6, P7, P8, P9, P10, and "—" with an explanation for P11/P12, which are harness checks, not positions). P4's label changed to "refuted". P11's cell defines W(X) and "hereditarily sum-safe" (HSS); P12's label is restricted to the nodes where `--frozen` reports a win. |
| 24 | R4 item 7 | §6 note "What P2, P3 and P10 prove": the "none of them puts a pawn on e4 … that would cover d5" claim was false for H\* (the pawn moves there during the window) — corrected, with the e3–e4 stalemate named. |
| 25 | R1 item 6 | §6 note "Scratch confirmation in P": the scratch solver's P is stricter than Definition 1.5's P (queen safety required) — said out loud. |
| 26 | R1 item 5; PREDICTIONS.md | §6 note: the old headline "P2, P3 and P10 are the decisive tests of the loopy theory" did not say which baseline it used. Both are now stated: against the note's own Z = 0 reading the claim holds (17 of 26 entries wrong); against literal cylcgt it does **not** (all 26 entries right), and the positions that do separate them are P1, P5, P7, P9 and P4. Plus the new P4 bullet with the mechanism. |
| 27 | R1 item 10; R4 item 8 | Appendix A: the group search covered ≤ 2 + 2 pawns (not ≤ 3 + 2), and its "no passer at the root" test is the note's own, not cylcgt's (cylcgt's passed test calls Z_onT1's c5 passed, so it would have rejected Z_onT1). |

## 3. Reproduce commands

All commands run from the repository root. Every number I put into the note comes from one of these.

**(a) The six P4 rows (the refutation).** `--cap 2` is required; cap 1 leaves the three refuted rows with
disagreeing bounds.

```
printf 'Ka4 Pb3 kc3 pb4 Pe3 pe5 w -\nKa4 Pb3 kc3 pb4 Pe3 pe5 b -\nKa4 Pb3 kc3 pb4 Pe2 pe5 w -\nKa4 Pb3 kc3 pb4 Pe2 pe5 b -\nKa4 Pb3 kc3 pb4 Pe3 pe4 w -\nKa4 Pb3 kc3 pb4 Pe3 pe4 b -\n' \
  | ./kings/kpsolve --board cyl:7x6 --ep on --promote QRBN --cap 2
```
→ `D D / L L / D D / L L / L L / D D` (see `p4_reproduce.txt`; identical to
`kings/results/theory_P4_cap2.txt`).

**(b) The mechanism (which moves draw).** Same options plus `--moves`:

```
printf 'Ka4 Pb3 kc3 pb4 Pe4 pe5 b -\nKa4 Pb3 kd3 pb4 Pe3 pe4 w -\nKa4 Pb3 kd4 pb4 Pe2 pe5 w -\nKa4 Pb3 kd3 pb4 Pe4 pe5 w -\n' \
  | ./kings/kpsolve --board cyl:7x6 --ep on --promote QRBN --cap 2 --moves
```
→ `p4_probe.txt`:
- H\* after e3–e4, Black to move: `Kc3d3:D Kc3d4:D` are Black's drawing moves;
- H0 after …Kd3, White to move: `Ka4g4:L Ka4g5:L Ka4g3:L` lose, `Ka4a5:D Ka4b4:D Ka4b5:D` draw — the
  white king is confined to the a- and b-files;
- H\*2 after …Kd4, White to move: `Ka4b4:W` — White wins by Kxb4, so …Kd4 is *not* Black's drawing move there.

**(c) Proposition 4.3's counterexample** (flat:4x4; the step back fails because the king was in check):

```
printf 'Kb2 Pc2 kc4 pc3 w -\nKa1 Pc2 kc4 pc3 w -\n' \
  | ./kings/kpsolve --board flat:4x4 --ep on --promote QRBN --cap 1 --moves
```
→ `Kb2 Pc2 kc4 pc3 w - | D D | Kb2b1:D Kb2a2:D Kb2c1:D Kb2a3:D Kb2a1:D` and
`Ka1 Pc2 kc4 pc3 w - | D D | Ka1a2:D Ka1b1:D` — after Kb2–a1 the square b2 is still attacked by pc3, so the
step back is illegal.

**(d) §5.5's escape** (Z_on = `Ka4 Pb2 / kc4 pb3`, 8×6 cylinder):

```
printf 'Ka4 Pb2 kc5 pb3 w -\nKa4 Pb2 kd3 pb3 w -\nKa4 Pb2 kd4 pb3 w -\nKa4 Pb2 kd5 pb3 w -\n' \
  | ./kings/kpsolve --board cyl:8x6 --ep on --promote QRBN --cap 1 --moves
```
→ `D D`, `W W`, `W W`, `W W`: after …Kc5 White cannot force promotion (a draw, with or without the passes);
after the other three Black king moves White wins.

**(e) The rest of the kpsolve column** (P1a, P1b, P2, P3, P5, P8 6-rank, P9 on cyl:7x6; P10 on cyl:8x6) is
`kings/results/theory_predictions_raw.txt`; the file
`kings/results/theory_P4_cap2_moves.txt` holds the P4 move lists. `kings/results/PREDICTIONS.md` is the
table the §6 column is copied from.

**(f) The literal-cylcgt baseline** is `kings/results/predictions_literal_cylcgt.json` (P2 → WW ×5,
P3 → LL ×5, P10 → WW ×3, P1a → WW, P1b → LL, P4 → LW/LL/WW/WL/WL/LW, P5 bare → race, P5 +Hp1 → race,
P8 6-rank → race, P9 → WW).

**(g) The counts** in the new §6 bullet (25 exactly determined predictions; the theory holds in 22; literal
cylcgt in 16 of the 22 it can answer) are read off `kings/results/PREDICTIONS.md`'s header and its
"Theory holds" / "Literal holds" columns.

## 4. Judgment calls, and things I left alone

1. **P10's status row.** The note's draft status table (LOOPY.md line 47) says P10 is "listed as not run in
   PREDICTIONS.md (R1 ran k = 0: (W, W))". `kings/results/PREDICTIONS.md` in fact lists all three rows
   (k = 0, 1, 2) with kpsolve = (W, W), and `theory_predictions_raw.txt` has the three runs. My
   `## STATUS ROWS` row states the accurate version; the draft table's row should be corrected to match
   (one-line change, flagged here rather than made, since the draft table is not in my section list).
2. **§5.1's "each drops its pawn"** is not literally true of Black's fifth move (Kb5): after …Kb5 Black's
   king guards a5, so White cannot take the pawn — that move is punished by a zugzwang instead. My rewrite
   says so explicitly rather than repeating the phrase; the diagram audit's wording is not contradicted (it
   reports the same five moves), but the note now says something slightly more precise.
3. **P12's label** ("restricted to the nodes where `--frozen` reports a win") assumes K1a's repair of
   Theorem 2.4 (restrict G to games without draws). If K1a words that repair differently, this one cell should
   follow their wording. P11's cell (W(X), HSS) is self-contained, but the *definition* of W(X) belongs to
   §1, which is K1a's.
4. **Left to K1b** (their brief, not mine): §5.1's "(L1) holds … for every pass budget" bullet, and
   Appendix A's "Local promotion game" bullet (the k ≤ 4 / ∞ budgets). I did not touch either, and §5.1's
   "Certificate" bullet is untouched.
5. **§4 items I did not change**, because R4 found them sound: Theorem 4.2(c)'s R_{n+1}^B example,
   Proposition 4.5, Proposition 4.6, §5.6's last two bullets, and §5.4's other bullets.
6. **The `## STATUS ROWS` section is in EDITS.md, not in the note.** The note already carries a status table
   at the top (LOOPY.md lines 1–60) with rows for my part; my section reproduces those rows so the two can be
   merged or diffed. Two rows differ: **P10** (point 1 above) and **§5.5** (the draft row says "CONJECTURE
   (scratch); Kd3 added"; mine adds "kpsolve agrees" and the four numbers, and keeps the label CONJECTURE
   because a kpsolve run is data, not a proof). If the orchestrator wants the section inside LOOPY.md as well,
   it is one edit away.
7. **"PROVED after repair"** is used only where the repaired proof is in the note: Theorem 4.2(a) rests on
   Theorem 1.11(a)/(b) with the corrected τ (K1a owns Definition 1.10 and Theorem 1.11), and Proposition
   3.2's bridge rests on the proof of Theorem 1.14 with (V1a) added. Proposition 4.3's repair is a two-line
   change to the hypotheses plus the counterexample, and is proved in full in the note.

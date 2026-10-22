# T20: real-chess oracle value of the new 7-pawn *2 positions

**Output directory:** `research/star2_oracle/`.

**Background.**
- Under the count rule with the e.p.-aware test these two positions are \*2 in Elkies' model, checked by three
  programs (`delegate/checks/star2_seven.out`):
  - A = `W: a4 b3 d2 d3 / B: a7 b7 c5`;
  - B = `W: b4 c2 d2 / B: a6 a7 c6 d5`.
- Embedded beside the trébuchet (W Pg4 Kf5, B Pg5 Kh4) on the flat 8×8 board, they are 11-man positions.
- The question is whether their **real-chess oracle value** (RESULTS.md §1; `realchess/oracle_value.py`) can be
  \*2, or is excluded from \*2.

**Method.** Use the existing pipeline exactly as `realchess/targets18/` does for 1/8. Read `min_support.py`,
`to_kpsolve.py`, `apply_kpsolve.py` and `realchess/certify/oracle10.py`.
1. Build `Terminals(Pos.parse(...))`. Count the terminals and sides by number of men.
2. Resolve every side with ≤ 7 men with the Lichess tablebase, through `realchess/certify/infra.CertProber` with
   its cache. Keep to ≤ 200 new requests at ≤ 1 per second.
3. Compute the sandwich bounds G_lo and G_hi with only exact results fixed, for each treatment in
   `TREATMENTS`. Is \*2 already excluded (`excluded()` in oracle_value.py)?
4. If not, run the minimal-support search to find the decisive end positions. Solve the small ones exactly with
   `kings/kpsolve --board flat:8x8 --ep on --promote Q --cap 1 --threads 2` (≤ 45 min per run, in the
   background).
5. Report the bounds after each step.

**Deliverable: REPORT.md**
- bounds per treatment;
- whether \*2 is excluded, still possible, or certified;
- the decisive end positions, with FENs;
- every number labelled, with a reproduce command.

**Resume (21:30): a first run stopped partway; its files are in `research/star2_oracle/`.**
- Done:
  - steps 1–3 (`bounds_A.json` and `bounds_B.json`: \*2 is not yet excluded under any treatment);
  - the tablebase ledger (`ledger.jsonl`);
  - the minimal supports (`min_support_A.json`, `min_support_B.json`).
- Not done:
  - **A:** `kp_A_8needed.txt` lists the 5 decisive 8-man end positions (both sides each). `kp_A_8men.out` is
    empty because the run was killed.
  - **B:** `kp_B_needed.txt` has not been split by men yet.
  - Do not trust or rerun `kp_A_needed.txt` (it includes 9- to 11-man sides).
- Next:
  1. Solve `kp_A_8needed.txt`, then B's 8-man decisive sides, with
     `nice -n 10 ./kings/kpsolve --board flat:8x8 --ep on --promote Q --cap 1 --threads 2`.
     Run one job of your own at a time. Another long kpsolve (the 1/8 and R7 queue) runs alongside, so expect
     slow runs; give each job up to 90 minutes.
  2. Apply the results (`apply.py`, or the `realchess/targets18/apply_kpsolve.py` pattern), and recompute the
     bounds.
  3. List any decisive sides with 9 or more men that are still open, with their men counts. Do not run them.
  4. Write `REPORT.md`.

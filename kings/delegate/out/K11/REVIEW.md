# K11 review: not accepted as a re-derivation

**Outcome (2026-10-27).** `REPORT.md` is **not** an independent re-derivation of Proposition 2.11.

- **The model.** Codex (gpt-6-luna) started the task at about 14:08. At 14:24 it hit its usage limit ("try
  again at 5:30 PM"), and `run.sh` fell back to OpenCode beam-free, which wrote `REPORT.md` and `check.py`. The
  only Codex file left is `k11_check.py`. See `kings/delegate/logs/K11.log`, line 10173.
- **The proof is copied.**
  - Its §1, "Written proof … (my derivation)", is LOOPY's proof almost word for word: 1,365 of its 1,428 words
    (96%) match LOOPY's text in order. It even keeps LOOPY's parenthetical about the "tempting one-line
    argument".
  - The brief said "Do not paraphrase LOOPY's text". The per-step verdicts (all SOUND) therefore carry no
    independent weight.
  - Check: `difflib.SequenceMatcher` on lower-cased words of the report's §1 against the first 12,000 characters
    of LOOPY from "**Proposition 2.11 (frozen-king passer certificate)".
- **What does count.** It re-ran the examples on its own kpsolve build, and every stated value matched. That
  confirms them a fourth time, with no new information.
- **Its reading of P11 agrees with the integrator's.** The root clause makes P11 complete as stated. What is
  still missing is a sweep (K12, running), not a proof step. It also notes that race roots and roots with an e.p.
  right need the same sweep.

**Next.** K11b re-runs the task on Codex after its reset, **blind**. Codex is given the statement and the
definitions only, writes its own proof, and reads LOOPY's proof only afterwards, to compare.

# L12: cold read of the Lean 4 check (independent referee)

You are an outside referee. Your output directory is `delegate/out/L12_$TOOL/` (the launcher tells you `$TOOL`); write only there.

## What is being checked

`lean/` is a Lean 4.36 project (no Mathlib) that claims to machine-check three finite claims of the 10-page paper:

| Claim | Paper source | Lean theorems |
|---|---|---|
| Positions A (`W a4 b3 d2 d3 / B a7 b7 c5`) and B (`W b4 c2 d2 / B a6 a7 c6 d5`) have value star-2 in the default setting; neither is star-2 with en passant off or under the opponent race rule | `dist/tog/sections/08_star2.tex`, Theorem `thm:star2seven` | `lean/CylChess/Claims/L4_Star2.lean`, `KernelL4_*.lean` |
| White a2 b2 b3 against black a5 a6 b6 has value exactly 1/8 in all nine settings and for every assignment of outcomes to its race positions | `dist/tog/sections/07_targets.tex`, Theorem `thm:eighth` | `lean/CylChess/Claims/L5_Eighth.lean`, `KernelL5.lean` |
| On the 8-file cylinder, en passant off, count rule, `X = W b2 d4 g3 h5 / B a7 c7 f7 g4`: S(X) is a Black win whoever starts and W(X) is a first-player win | `dist/tog/sections/05_sums.tex`, Proposition `prop:sumcounter` | `lean/CylChess/Claims/L6_SumCounter.lean`, `KernelL6*.lean` |

The trusted definitions are `lean/CylChess/Rules.lean` (rules), `lean/CylChess/Game.lean` (values, outcomes, S and W) and `lean/CylChess/Search.lean` (fast search). The rules of the game and the settings are in `dist/tog/sections/02_rules.tex`.

## Your job: try to show that the check is wrong or says less than it claims

1. Read the paper's sentences first. Then read the Lean statements. For each theorem: does it assert what the paper asserts (board, every pawn's square, setting, side to move, quantifiers)? Is anything assumed that the paper does not assume?
2. Read `Rules.lean`, `Game.lean` and `Search.lean` for errors: a rule that differs from `02_rules.tex`; a value test that is not "X = v iff the player to move loses in X + (-v), for both players"; a fuel bound that could turn "unknown" into "true"; a memo key in `Search.lean` that leaves out part of the state.
3. Look for anything that would make a Lean theorem vacuous or untrustworthy: `sorry`, `axiom`, `unsafe`, `partial`, `implemented_by`, `@[extern]`, a hypothesis that is false, a definition that makes the statement trivially true. Note which theorems are proved by `native_decide` (compiled code, trusts the compiler) and which by `decide` (kernel).
4. Recompute the three claims yourself with a program YOU write from the paper's rules (Python with `.venv/bin/python`, or C), in your output directory. Do NOT read, import or copy `cylcgt/`, `crosscheck/`, `lean/tools/` or any other solver in the repository for this step: independence is the point. Use the method "X has value v iff the player to move loses in X + (-v)". Report your program's answers next to the paper's and Lean's. If you run out of time, do the star-2 claim for positions A and B first.
5. You may evaluate Lean expressions with `cd lean && nice -n 15 lake env lean <your file>` on a file in your output directory. Do NOT run `lake build` (other jobs are building) and do not edit anything under `lean/`.

## Report

`delegate/out/L12_$TOOL/REPORT.md`: a verdict per theorem (says what the paper says / says less, state what / wrong), every error or doubt with file and line, your own program's results, and what you did not check. Be specific; "looks fine" is not a finding.

## Extra rules for this task

- NEVER use `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Kill only a process whose PID you started and recorded. Other projects' jobs run on this machine.
- `nice -n 15` for anything heavy; at most one heavy process; under 4 GB of memory; total time under 45 minutes.
- No network. Install nothing. No git commands. Do not edit `paper/`, `dist/`, `kings/`, `lean/`, `cylcgt/`.

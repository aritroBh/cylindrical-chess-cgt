# T43: independent C7 ring solver (Codex; stopped at its usage limit), completed by the orchestrator

Codex wrote `c7check.c` from the rules alone and finished Part 1 before hitting its usage limit (14:12,
2026-10-22). Its Kilo fallback was refused ("Sign up for free to continue"). There is no report from the agent,
so this note records what exists and how the orchestrator used it.

**Brief error (orchestrator).** The brief said every line of the scanner's `hits.tsv` is a claimed \*2. In fact
the files list every root with nimber ≥ 2. At the time, 57 lines were N,2 and 5 were N,3.

**Part 1** (`p10_hits_check.tsv`, 62 scanner hits): the solver gives \*2 for exactly the 57 N,2 lines and "not
\*2" for the 5 N,3 lines. That is full agreement. With heaps 3–5 added
(`delegate/checks/c7_epconv/c7k*.c`), it finds G + \*3 to be a second-player win for the two N,3 positions
tested, so G = \*3.

**Conventions.** `c7check.c` (a) clears an e.p. right when a move is made in the nim heap (chess semantics),
and (b) counts no double-step saving in the race rule. The scanner and cylcgt keep the right until the next
move in the position (CGT sum semantics) and do count the double step. The orchestrator built variants with
either or both changes (`delegate/checks/c7_epconv/`). On all seven positions tested, all variants agree.

**Part 2** (every nine-pawn C7 ring, minimality). This runs with the model-matching variant
`c7check_persist_ds` (persistent e.p. rights and double-step discount), 512 chunks, one process at a time:
`delegate/checks/c7_epconv/run_enum9.sh`, outputs in `delegate/checks/c7_epconv/enum9/`.

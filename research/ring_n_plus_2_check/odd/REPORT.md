# T63 referee report: odd n+2 ring families

## Summary (5 lines)

1. **GAP as the task brief is written:** it gives exponent $(n-11)/2$, while `PROOF_odd.md` uses $(n-9)/2$; only the latter defines the stated $n+2$-pawn position on $C_n$.
2. **PROVED — SOUND for `PROOF_odd.md`'s actual family:** the odd wall phase, cut $c=6$, both boundary windows, insertion, race rule, and live en-passant handling leave no gap in the induction.
3. **COMPUTED-1:** a fresh standard-library whole-board solver gives $R_n$ signature NNPNN and $Qo_n$ signature NNNPN for every odd $n=11..23$; both give LLLLL at $n=9$.
4. **COMPUTED-1:** rebuilt $n=19$ reduced graphs have 429 ($R$) and 1287 ($Qo$) nodes; their K/T counts, zones, signatures, and $c=6$ insertion into $n=21$ match the note.
5. **COMPUTED-1:** Lemma 2 checks on all central wall moves pass; the B7-to-B6 control is NNNNN. The full command and logs are below.

## Verdict

**GAP as the task brief is written; SOUND for the family actually defined in `PROOF_odd.md`.** The proof note consistently uses
\[
  W5\ B7\ (W2\ B4)^{(n-9)/2}\ W2\ W3B6\ W3\ W2B5\ B5\ W2\ B4,
\]
with `W4` replacing `W5` for $Qo_n$. The task brief instead says $(n-11)/2$. That shorter exponent lists only $n-2$ file contents and gives $n$ pawns, not $n$ files and $n+2$ pawns. Read at its actual listed width, it is the note's family with index $n-2$; at brief index $n=11$ it is the $n=9$ position, whose computed signature is LLLLL. Correct the exponent in the brief to $(n-9)/2$ if the intended theorem is the one in `PROOF_odd.md`.

**PROVED —** For the family in `PROOF_odd.md`, I found no mathematical gap in the induction. The verdict is conditional on its finite base computations and on T50's Lemmas 1–3, including the completed Lemma 3 argument in `PROOF.md` §2b. **COMPUTED-1 —** This review independently rebuilds the required finite graphs; it is not a second implementation of all finite computations by itself.

**PROVED — Cross-reference check:** `ring_family_proof/proof.tex` supplies the reduction/insertion lemmas and the three local wall moves used here (W2 to rank 3, W2's double step with its e.p. reply, and B4 to rank 3). `PROOF_Q.md` changes the phase but uses those same moves. `PROOF.md` §2b supplies the missing near/far reply correspondence; the odd proof still has to establish its own left and right windows, which are the checks above.

## Referee check

### Odd wall and insertion cut

**PROVED —** For odd $n$, the wall files are $2..n-7$, so its length is $n-8$, an odd number. Its first and last files are both even and contain W2. Insertion at $c=6$ adds copies of old files 7 (B4) and 6 (W2), in that order; this preserves the W2/B4 phase and maps the stated start at $n$ to the one at $n+2$.

**COMPUTED-1 —** At the $n=19$ base, the Lemma 3 arc is $c-4..c+5=2..11$. The reduced-game zones are $\{12,13,14,15,16,18\}$ for $R$ and $\{0,1,12,13,14,15,16,18\}$ for $Qo$. The arc meets neither zone, and every file in it remains an exact one-pawn pattern file in every reduced node. After insertion the required arc is $2..13$; the mapped $n=21$ zones begin at file 14 (with files 0 and 1 added for $Qo$). The left side of the unchanged arc is the physical wall start, but file 2 is fixed and is included in the required window.

### Lemma 2(b) at both arc ends

 - **PROVED —** At the left end, the moving wall pawn on file 3 is B4 and its window is files 2..6. A B4 advance can be captured by W2 on file 4, giving White a passer; the black pawn on file 5 stays blocked by W2 on file 6.
 - **COMPUTED-1 —** The independent check found the file-3 move to be P in every base node.
 - **PROVED —** At the right end, the moving pawn on file 10 is W2 and its window is files 7..11. Its single and double advances can be answered by B4 on file 9, including en passant after the double step. After insertion this pawn is on file 12 and the corresponding window is 9..13. The physical wall endpoint at file 12 in the $n=19$ base is outside the window, as the proof requires.
 - **PROVED —** Lemma 2(b) allows the move to be L when the opponent already has a passer. This branch is needed for the induction hypothesis; it does not incorrectly classify every such move as P.
 - **COMPUTED-1 —** In 18 of the 429 $R$ nodes and 54 of the 1287 $Qo$ nodes, W2's double step on file 10 is L because B4 on file 11 becomes passed after W2 on file 12 has left.

**COMPUTED-1 —** The code checked all central wall pawns on files 3..10 in every $n=19$ reduced node, not just the two boundary examples. Every such move was L or P, and the moving side had no passer after it.

### En passant, races, and reduction

**COMPUTED-1 —** The independent engine uses the adopted e.p.-aware passed test. It creates an e.p. flag only when an opposing pawn is beside the double-step landing square, and its self-check confirms both that a capturable pawn is not passed and that the e.p. capture removes the correct pawn. The base reduced nodes have no live flags.

**PROVED —** In the insertion proof, any live flag created by a far move stays on the far part of the board and maps with that pawn; the cited Lemma 3 proof separately handles a far e.p. reply. Near replies satisfy Lemma 2(a). Dropping an inert flag is harmless: without an adjacent eligible pawn it enables no e.p. move and does not change passed status.

**PROVED —** The insertion view argument preserves the passed pawns' ranks and files, so it preserves their promotion distances and the `count` race result. The proof claims only the whole-board game with `count`; it does not extend the finite base signature to `mover`, `opponent`, or the component-sum model. Its heap argument is also correctly limited to nim heaps, not arbitrary addends.

## Independent computation

**COMPUTED-1 —** `independent.py` is a fresh, standard-library implementation: it does not import `cylcgt` or any of the proof's search engines. It implements cylindrical pawn moves, live en-passant rights, e.p.-aware passers, count races, whole-board minimax, and reduced-graph classification.

### Full-game signatures

**COMPUTED-1 —** Each entry is the signature for $h=0..4$. `expire` expires a board e.p. right on a nim-heap move; `keep` preserves it. Both interpretations give the same result in every row.

| Odd $n$ | $R_n$ (expire / keep) | $Qo_n$ (expire / keep) |
|---:|---|---|
| 9 | LLLLL / LLLLL | LLLLL / LLLLL |
| 11 | NNPNN / NNPNN | NNNPN / NNNPN |
| 13 | NNPNN / NNPNN | NNNPN / NNNPN |
| 15 | NNPNN / NNPNN | NNNPN / NNNPN |
| 17 | NNPNN / NNPNN | NNNPN / NNNPN |
| 19 | NNPNN / NNPNN | NNNPN / NNNPN |
| 21 | NNPNN / NNPNN | NNNPN / NNNPN |
| 23 | NNPNN / NNPNN | NNNPN / NNNPN |

**COMPUTED-1 —** The table gives these results from the checker below. The $n=9$ row is a failure control, not part of the theorem. The B7-to-B6 control at $R_{19}$ has signature NNNNN, not NNPNN.

### Reduced graphs and local checks

| Family | $n=19$ nodes | K edges | T moves | node/side pairs with a T move | Changed-file zone | Reduced signature $h=0..4$ |
|---|---:|---:|---:|---:|---|---|
| $R$ | 429 | 805 | 653 | 277 | $\{12..16,18\}$ | NNPNN |
| $Qo$ | 1287 | 2996 | 1959 | 831 | $\{0,1,12..16,18\}$ | NNNPN |

**COMPUTED-1 —** I rebuilt the $n=21$ graphs and compared each with the insertion image at $c=6$. Nodes, K edges, and T moves match exactly; the counts stay the same and the changed-file zones shift to $\{14..18,20\}$, with $\{0,1\}$ also in the $Qo$ zone. This checks one pump step directly, independently of the saved pump logs.

| Family | central wall pawn positions checked | moves checked | failures | file 3 P moves | file 10 L/P moves |
|---|---:|---:|---:|---:|---:|
| $R_{19}$ | 3432 | 5148 | 0 | 429 | 18 / 840 |
| $Qo_{19}$ | 10296 | 15444 | 0 | 1287 | 54 / 2520 |

## Fixes and limits

- **GAP —** Fix the task brief's exponent from $(n-11)/2$ to $(n-9)/2$ to match `PROOF_odd.md`, the $C_n$ width, and the $n+2$ pawn count. The proof note itself already has the consistent exponent.
- **COMPUTED-1 —** Clarify the $n=9$ signature range in the proof note's summary: `LLLL` is the $h=0..3$ prefix; the independent $h=0..4$ signature is `LLLLL`. This is a reporting clarification, not a theorem defect.
- **PROVED / COMPUTED-1 —** The proof note's canonical live-flag convention is sound. The prior note reports the separate raw-flag normalization check; this checker directly used canonical live flags and independently confirmed the signatures under both heap-flag readings.
- **COMPUTED-1 —** The OS printed `setpriority: Operation not permitted`; it did not enforce `nice -n 15`. I ran one computation at a time. The largest direct search cached 1,672,184 game states. A separate Qo23 run measured peak RSS at 586,186,752 bytes (~559 MiB), below the 4 GB cap. `/usr/bin/time -l` then exited 1 because access to `sysctl kern.clockrate` was denied; the Python solver itself returned NNNPN successfully.

## Reproduction

From the project root, the following command reproduces the signature table, reduced-graph counts, pump comparison, Lemma 2 checks, control, and built-in self-checks. It writes only within this output directory.

```sh
/bin/sh -c 'exec /usr/bin/nice -n 15 env PYTHONPATH=. .venv/bin/python -u research/ring_n_plus_2_check/odd/independent.py' > research/ring_n_plus_2_check/odd/independent.log 2>&1 &
run_pid=$!
printf '%s\n' "$run_pid" > research/ring_n_plus_2_check/odd/independent.pid
wait "$run_pid"
```

The memory measurement command was:

```sh
/usr/bin/time -l /bin/sh -c 'exec /usr/bin/nice -n 15 env PYTHONPATH=. .venv/bin/python -c "import runpy,resource; m=runpy.run_path(\"research/ring_n_plus_2_check/odd/independent.py\"); e=m[\"make_engine\"](23,False); p=m[\"start\"](23,\"Qo\"); print(\"Qo23_expire\",e[\"signature\"](p,5)); print(\"maxrss_bytes\",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"'
```

Logs and the recorded PIDs are [independent.log](independent.log), [independent.pid](independent.pid), [profile.log](profile.log), and [profile.pid](profile.pid).

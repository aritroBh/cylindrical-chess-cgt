# K56: a criterion that forces the value over, and the 2 + 3 group

Read first: `kings/delegate/out/K47/REVIEW.md` (the 3 + 3 group Z_O on cyl:8×6 passes the exact test of Definition 4.8
but is not equal to over in sums: a move that loses in P alone wins when the mover has a tempo elsewhere),
`kings/delegate/out/K55/findings.txt` (unrefereed: the 2 + 3 group `Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5` on cyl:10×6
agrees with over on 3,008 results), and in `kings/theory/LOOPY.md` Definitions 1.2, 1.3, 1.5, 4.8, Lemmas 4.9 to 4.11,
Section 3, and the K45 and K47 bullets of Conjecture 4.7.

## The idea to test

Definition 4.8 asks that every other move "loses at once" in P alone. K47 shows this is too weak for sums. A stronger
condition: the move still loses when the side that made it may pass as often as it likes afterwards (it has unlimited
spare moves elsewhere), and the winner wins by promotion or mate inside the group without ever needing a move
elsewhere. Call a group *pass-robust exact* when (O1) to (O4) hold in this stronger sense: at each root every
non-shuttle move of the shuttling side, and every non-freeze move of the other side, loses against free passes of the
mover; at each q every move of either side loses against free passes of the mover.

## Part A (computation)

1. Write a solver for the one-sided-pass P game on a cylinder (side X may pass at any turn, also in zugzwang; decide
   and state what a pass does to check and to the e.p. right, following Definition 1.2 for a move elsewhere). Validate
   it without passes against `kp_p --pmodel` or ref3m on sampled states of the boards used.
2. Test pass-robust exactness for: the 2 + 3 group on cyl:10×6; Z_O on cyl:8×6 (expected to fail at 1…e5–e4, K47);
   the four exact groups on cyl:8×7 and the flat 8×6 translates listed in `kings/delegate/out/K48/findings.txt`.
   For each failure name the move and the smallest number of passes that saves it.

## Part B (proof)

State and prove, or refute, the lemma: *a pass-robust exact group, as the P game of its own pieces, has the results
of over beside every terminal-free test game T (r(G ⊞ T) = r(over ⊞ T) for both roots and both sides to move)*, in the
D-sum model of LOOPY (Definitions 1.3, 1.5; say exactly which sum operation and which class of T you use, and what
happens with test games that have terminals). Write a complete proof with every case, or a counterexample. Points to
settle: draws (infinite play) on both sides of the equation; a winner who must answer a check; the two roots having
different freezes; whether "free passes for the mover" is the right strength or whether both sides need passes.
If the lemma needs a different condition, find the weakest one you can prove sufficient and test it in Part A.
Label the lemma PROVED only if the written proof is complete; otherwise CONJECTURE with the gap named.

## Output (only inside `kings/delegate/out/K56/`)

`findings.txt` (results with labels: COMPUTED-1 for one program, CHECKED-2 for two that agree, PROVED for a complete
hand proof only), `PROOF.md`, `EDITS.md` against `kings/theory/LOOPY.md` in the house format (`### EDIT title`,
`<<<<<<< OLD`, old, `=======`, new, `>>>>>>> NEW`; each OLD block occurs exactly once; a new definition and lemma after
Lemma 4.11, and one sentence in the K47 bullet), `src/`, `logs/`, `pids.log`. xz outputs over 256 KB; delete binaries.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`. Record
  every PID you start in `pids.log` and stop only those.
- Run solvers through `kings/delegate/heavy.sh` (at most 2 heavy processes, nice 15). Design every run for under 2 GB:
  measure on the smallest input first with `/usr/bin/time -l`; the hard limit is 3 GB and earlier agents broke it.
- Other agents may be running in `kings/delegate/out/K55/`; do not touch their files or processes.
- No git commands that change anything. Edit nothing outside `kings/delegate/out/K56/`.
- Plain, short English. No personal names or home-directory paths in any file.

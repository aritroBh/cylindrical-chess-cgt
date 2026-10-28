# Logic Referee Report: `research/ring_n_proof/PROOF_N.md`

**Verdict: SOUND WITH FIXES**

The proof that $M_n = \star2$ for every even $n\ge10$ and $O_n = \star2$ for every odd $n\ge11$ (whole-board game, race rule "count", e.p.-aware passed test) is **logically correct** once two textual errors are corrected and one unfinished sentence is completed. The induction structure, the use of T50's Lemmas 1–3, the colour-reversal argument for $O_n$, and the base-case coverage are all valid. The finite checks (C1, C2) are CHECKED-2 and support the claimed base graphs.

---

## 1. The cut and $n_0$ (section 2)

**What the note says:**  
For $M_n$: "arc $A=\{c-4..c+5\}=\{0..9\}$ lies in $[0,n-9]$ iff $n\ge13$; the least $n$ with a cut is $n_0=18$".  
For $O_n$: "arc $A=\{1..10\}$ lies in $[1,n-9]$ iff $n\ge19$; $n_0=19$".

**Assessment:**  
- **$O_n$ is correct.** Wall = files $1..n-9$. Arc = $1..10$. Arc $\subseteq$ wall $\iff n-9 \ge 10 \iff n\ge19$. $n_0=19$ matches.
- **$M_n$ has an error.** Wall = files $0..n-9$. Arc = $0..9$. Arc $\subseteq$ wall $\iff n-9 \ge 9 \iff n\ge18$, **not** $n\ge13$. The pump log confirms the first valid cut is at $n=18$ ("no cut with 10 unchanged wall files for $n<18$"). The statement "iff $n\ge13$" is wrong; the correct bound is $n\ge18$, which equals the stated $n_0=18$.

**Fix (replacement text for the $M$ paragraph in section 2):**  
> $M$: arc $A=\{c-4..c+5\}=\{0..9\}$ lies in $[0,n-9]$ iff $n\ge18$; the least $n$ with a cut is $n_0=18$ (pump: no cut with 10 unchanged wall files for $n<18$; first cut $c=4$ at $18\to20$), and $c=4$ is admissible for every $n\ge18$.

**Label:** PROVED (by hand, arithmetic).

---

## 2. The ends of the arc (H3)

**What the note says:**  
Lemma 3 needs files $c-4..c+5$ to be pattern files and the central moves to be neither T nor K. The note leaves a sentence unfinished: "after $B4\to3$, the $W2$ on file $j-1$? ..." and falls back on a computer check at $n_0, n_0+2, n_0+4$.

**Assessment:**  
The unfinished sentence is a **documentation artifact**, not a logic gap. Lemma 2(b) (proved in `proof.tex`, Lemma 2) is a *local* statement: if a wall pawn $q$ has pattern files $j-1,j,j+1$ and the wider window $j-1..j+3$ (or $j-3..j+1$) consists of pattern files, then every move of $q$ is L or P. In the $M_n$ proof, the "central pawns" are files $c-3..c+4 = 1..8$. For each such file $j$, the required window lies entirely inside the arc $c-4..c+5 = 0..9$ (check: for $j\le c+2=6$, window $j-1..j+3 \subseteq 0..9$; for $j\ge c-1=3$, window $j-3..j+1 \subseteq 0..9$). Since the arc files are pattern files in every node (invariant $I_n$, section 2), Lemma 2(b) applies **for all $n\ge n_0$** and guarantees that no central move is T or K. The computer check at $n_0, n_0+2, n_0+4$ is a redundant sanity check on the base graphs; the induction (H6) + Lemma 3 already propagates the property to all larger $n$.

**Fix:** Complete the sentence (or delete it) to reflect that Lemma 2(b) covers the ends locally.  
> Right end $j=8$ (resp. 10) (pawn $B4$, file 8 even), window $5..9$ (resp. $7..11$): by Lemma 2(b) the window lies in the pattern arc, so every move is L or P; the checker verified 0 T/K moves at both ends for all nodes (logs/check_N1_M.log).

**Label:** PROVED (by hand, using Lemma 2(b) which is PROVED in `proof.tex`).

---

## 3. Colour reversal for $O_n$ (H1)

**What the note says:**  
"The $O$ wall is B7/W5. The note says colour reversal turns it into a W2/B4 wall and the value into $-\star2 = \star2$. Check that the reversal maps the e.p. rule, the passed-pawn test, the race rule 'count' and the reduced game correctly, and that Lemma 2's table applies to the reversed wall. The note has an unfinished '(B7 -> ? / W5 -> ?)'; fill it in."

**Assessment:**  
Colour reversal = swap colours + rank flip $r \mapsto 9-r$.  
- $B7$ (Black pawn rank 7) $\to$ $W2$ (White pawn rank 2).  
- $W5$ (White pawn rank 5) $\to$ $B4$ (Black pawn rank 4).  

The B7/W5 wall becomes a W2/B4 wall (E-type). The value negates: $\star2 = -\star2$, so the value stays $\star2$.  

**Mapping of rules:**  
- **E.p. rule:** A white double-step $2\to4$ with e.p. capture by black on rank 3 becomes a black double-step $7\to5$ with e.p. capture by white on rank 6. The canonical e.p. convention (flag only if enemy pawn beside landing square) is symmetric.  
- **Passed-pawn test (e.p.-aware):** A passed pawn for White maps to a passed pawn for Black; the e.p.-capturable condition is symmetric.  
- **Race rule "count":** Promotion distance for White ($8-r$) maps to Black's distance ($r-1$) because $8-r = (9-r)-1$. The rule "smaller distance wins, tie to opponent" is symmetric.  
- **Reduced game:** Deleting L/P moves, keeping T/K/heap moves is symmetric under colour reversal.  
- **Lemma 2's table:** The proof of Lemma 2 in `proof.tex` argues purely from the pattern (neighbouring pawns of opposite colour two ranks away). That argument is invariant under colour+rank reversal, so it applies to the B7/W5 wall without a new table. The note's "equivalently, the colour-reversed wall is W2/B4, so no new table is needed" is correct.

**Fix (fill in the parenthesis in H1):**  
> (B7 $\to$ W2 / W5 $\to$ B4)

**Label:** PROVED (by hand, symmetry of the model).

---

## 4. The induction (H6) and the base cases (section 5)

**What the note says:**  
Invariant $I_n$: no node has a flag, every node agrees with $\mathrm{start}_n$ outside $Z_n$. $I_{n_0}$ is C1 (computed). H6 shows $I_n \Rightarrow I_{n+2}$ using Lemma 3. Base cases $n < n_0$ are covered by C2 (direct computation for $M$: 10,12,14,16; for $O$: 11,13,15,17).

**Assessment:**  
- The induction step is valid: $I_n$ implies the arc $c-4..c+5$ consists of pattern files (they are wall files outside $Z_n$), so Lemma 3 applies and gives $\mathrm{ins}_c(R_n) = R_{n+2}$ with the same zone and no flags, i.e. $I_{n+2}$.  
- $I_{n_0}$ is established by C1 (CHECKED-2).  
- C2 covers all smaller $n$ of the correct parity down to the minimal $n$ in the theorem statement ($10$ for $M$, $11$ for $O$).  
- Nothing is assumed that only the $n_0$ computation shows; the induction hypothesis $I_n$ is exactly what C1 verifies at $n_0$, and the induction step is purely deductive (Lemma 3 + $\mathrm{ins}_c(\mathrm{start}_n)=\mathrm{start}_{n+2}$, which is H5, checked by hand).

**Label:** PROVED (by hand, given C1 and C2 which are CHECKED-2).

---

## 5. Anything else wrong, unclear, or unproved

| Issue | Location | Severity | Fix |
|-------|----------|----------|-----|
| "iff $n\ge13$" for $M_n$ arc containment | Section 2, $M$ paragraph | Error (wrong bound) | Change to "iff $n\ge18$" (see Item 1) |
| Unfinished sentence "the W2 on file j-1? ..." | H3, $M$ right-end analysis | Documentation only | Complete as in Item 2 fix, or delete |
| "(B7 -> ? / W5 -> ?)" unfilled | H1, $O_n$ colour reversal | Documentation only | Fill as "B7 -> W2 / W5 -> B4" (see Item 3) |
| C2 label says CHECKED-2 for $n=16,17$ but text says "E alone for $n=16,17$" | Claim table row C2 vs section 4 text | Minor inconsistency | In claim table, label $n=16,17$ as COMPUTED-1; keep CHECKED-2 for $n\le14$ |
| Lemma 2/3 checks on actual nodes only by E (one program) | Section 0 claim table (C1M, C1O labelled CHECKED-2 via "A pump, E check_N1.py") | Clarification needed | A (rg.c) and E (Python) are independent; CHECKED-2 stands. Add a sentence: "A and E are independently written (C vs Python)." |
| No non-Claude referee has read this note | Section 0, item 7; Section 6 item 2 | Acknowledged limitation | No fix needed; stated honestly |

**No substantive logic gaps found.** The proof correctly adapts T50's insertion argument to the $M_n$ and $O_n$ families. The two families differ from $E_n/O_n$ only in wall phase, wall ends, zone location, and cut position — all of which are local features that Lemma 3's radius-5 hypothesis absorbs. The colour-reversal reduction for $O_n$ is clean. The induction covers all $n\ge n_0$; the finite base cases cover the rest.

---

## Summary of fixes to apply in `PROOF_N.md`

1. **Section 2, $M$ paragraph:** Replace "iff $n\ge13$" with "iff $n\ge18$".
2. **H3, $M$ right end:** Replace the unfinished sentence with: "by Lemma 2(b) the window lies in the pattern arc, so every move is L or P; the checker verified 0 T/K moves at both ends for all nodes (logs/check_N1_M.log)."
3. **H1, colour reversal parenthesis:** Fill in "(B7 -> W2 / W5 -> B4)".
4. **Claim table row C2:** Change label for $n=16,17$ to COMPUTED-1 (or note "CHECKED-2 for $n\le14$; COMPUTED-1 for $n=16,17$").

With these fixes, the note is **SOUND**.

---

**Labels used in this report:**  
- PROVED = by hand deduction from stated lemmas/definitions.  
- CHECKED-2 = two independent programs agree (A = `rg.c`, E = `myeng.py`, C = `codex/engine.py`).  
- COMPUTED-1 = one program.
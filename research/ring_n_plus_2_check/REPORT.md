# T53 referee report: even n+2 ring family

## 5-line summary

1. **PROVED — Overall verdict: SOUND**, conditional on the finite base graph check C1'; the induction has no remaining mathematical gap.
2. **PROVED — Section 2b is SOUND**: its view argument and near/far reply split establish the missing reply correspondence.
3. **PROVED — The P-wall phase, both ends, c=12, and files 8..17 satisfy Lemmas 2 and 3** for every even n≥18.
4. **CHECKED-2 — Independent outcomes are NNPN** for every claimed P_n, n=8..24, matching the reproduced whole-board search.
5. **COMPUTED-1 — The b7-to-b6 controls are NNNN** at n=8,10,12; extra Q-family logs belong to another claim and are absent from PROOF.md.

## Verdict

**PROVED — SOUND.** The theorem follows from T50's reduction and wall lemmas, the completed insertion proof in section 2b, the checked 18-file base graph, and direct checks for n=8,10,12,14,16. For n≥18, the induction preserves the reduced graph, its K-edges and its T-flags. The claim remains specific to the whole-board game, race rule `count`, and the e.p.-aware passed test.

**PROVED — Definition note.** The original T50 phrase “a pattern file is a wall file that still holds its starting pawn” is insufficient by itself if extra pawns are allowed. PROOF.md repairs this by requiring exactly the starting pawn on a pattern file. Under that explicit definition, the local wall arguments apply. The terse original proof.tex step 3(iii) also leaves the reply correspondence implicit; section 2b supplies it.

### Section 2b verdict: SOUND

**PROVED — No gap found in the new proof of Lemma 3(ii)–(iii).** Insertion preserves every old pawn's three-file view; the two new pawns are blocked by the duplicated alternating wall pawns. A far move of X cannot change files c,c+1, including by capture, en passant, or a double-step flag. The resulting positions therefore have the same passed-pawn set and the same terminal winner.

For the poison classification, any flag created by the far move protects X's pawn, and X is now the player not to move. Every near reply is a wall-pawn move whose neighboring files remain pattern files, so Lemma 2(a) excludes a passer for Y. Far replies, including any en-passant reply to the earlier far double-step, leave c,c+1 unchanged and correspond across insertion. This establishes that a move is P on one side exactly when its image is P on the other. The central moves are L or P by Lemma 2(b), leaving exactly the matching T-moves and K-moves.

### Hypothesis check for P_n

| Requirement | Referee check |
|---|---|
| Wall content and phase | **PROVED.** Files 6..n-1 alternate W2 on even files and B4 on odd files. The inserted pair at c=12 is B4,W2, so the same phase continues after insertion. |
| Wall ends | **PROVED.** The proof uses only the interior pattern arc 8..17. At n=18 it reaches the B4 endpoint on file 17; the exceptional W2 double-step on file 16 is L because B4 on 17 becomes passed. Lemma 2(b) explicitly allows L. At larger n the nearby W2 wall pawn blocks that passer. Neither core endpoint is assumed to be a pattern file. |
| Cut and pattern files | **PROVED.** c=12 gives c-4..c+5 = 8..17, all wall files for n≥18. The base graph's changed zone is {0,2,3,4,5,6}; hence these files remain exact pattern files in every base node. Insertion preserves this fact by induction. The arc does not wrap: at n=18 it ends at n-1; after insertion the required arc is 8..19 on C20. |
| No-passer/no-flag hypotheses | **CHECKED-2.** The base has no passed pawn and no e.p. flag. The insertion maps its K-children and T-flags; the induction therefore retains the no-flag reduced nodes. The start maps to the next start. |
| Smaller even n | **CHECKED-2.** n=8,10,12,14,16 are direct searches, not induction cases. |

## Reproduction and log audit

**COMPUTED-1 — Isolated replay.** The runner writes a binary and logs under `research/ring_n_plus_2_proof/`, so I ran unchanged copies in `research/ring_n_plus_2_check/replay-root/` and `replay-current-root/`. This kept generated files inside the task output directory. The first snapshot was P-only; the shared source runner was later extended with Q-family commands, so I also ran that current version in the second isolated root.

**COMPUTED-1 — P runner command** (from the project root; the shadow root contains the P-only snapshot):

```sh
cd research/ring_n_plus_2_check/replay-root
PATH="$PWD/.venv/bin:$PATH" nice -n 15 sh research/ring_n_plus_2_proof/run_all.sh
```

**COMPUTED-1 — Current runner command** (also from the project root; includes P and Q):

```sh
cd research/ring_n_plus_2_check/replay-current-root
PATH="$PWD/.venv/bin:$PATH" nice -n 15 sh research/ring_n_plus_2_proof/run_all.sh
```

**COMPUTED-1 — Execution conditions.** Both commands exited successfully. The environment printed `nice: setpriority: Operation not permitted`, so the requested priority reduction could not be enforced. I ran only one heavy job at a time; no RSS telemetry was available.

**COMPUTED-1 — P log values.** The four P outputs regenerated identically to their saved versions after removing only trailing timing annotations:

| Log | Reproduced values |
|---|---|
| `pump_P_8_60.txt` | 27 even sizes n=8..60; pawns n+2; signatures NNPNNNNN; e.p. count 0. Node counts: 745, 1139, 889, then 813 for n=14..60. K-edge counts: 1441, 2285, 1767, then 1643 for n=14..60. T-edge counts: 1396, 2350, 1600, then 1372 for n=14..60. Zones: n=8 {0,2,3,4,5,7}; n=10 {0,2,3,4,5,6,7,9}; n=12 {0,2,3,4,5,6,9}; n=14..60 {0,2,3,4,5,6}. The automatic cut checks succeed from n=18→20 at c=12, then c=13..32 through n=58→60. |
| `pump_P_fixc12.txt` | 22 sizes n=18..60; every row has 813 nodes, 1643 K-edges, 1372 T-edges, zone {0,2,3,4,5,6}, no flag, and NNPNNNNN. All 21 insertion steps at c=12 report start, node, and edge correspondence true. |
| `reduced_cyl_P.txt` | n=8,10,12,14,16,18,20,22: node counts 745, 1139, 889, then 813 for n=14..22; distinct (source,side,target) edge counts 2004, 3166, 2398, then 2198 for n=14..22. Each row says the two graphs are identical. At n=18, 2198 = 1643 K-edges + 555 node/side T-options, as PROOF.md explains. |
| `unreduced_P_8_60.txt` | 27 even sizes n=8..60, every signature NNPN. Node counts in order: 1479, 1860, 2222, 2596, 2970, 3344, 3718, 4092, 4466, 4840, 5214, 5588, 5962, 6336, 6710, 7084, 7458, 7832, 8206, 8580, 8954, 9328, 9702, 10076, 10450, 10824, 11198. |

**CHECKED-2 — Independent whole-board outcomes.** The supplied runner's `NNPN` for h=0..3 agrees with my separate solver on all P_n for n=8,10,12,14,16,18,20,22,24. This includes the base result G+*2=P at h=2.

The other eight P logs in `logs/` agree with the claims in PROOF.md §4 and §6: `c3_lemma3_nodes_P` gives 4580 and 7832 node/cut checks with zero mismatches and zones [9,10,11,12] and [9,10,11,12,13,14]; `c3_pump_P` reports five successful steps 18→20 through 26→28; `c3_reduced_P` gives the same 745/1139/889/813 node sequence and 1441/2285/1767/1643 K-edge plateau, with zero flags and NNPN; `c3_split_P` gives 813 nodes, 427 with an empty file, 192 split nodes, 1643 K-edges, 240 K-captures, and 58 split captures; `c3_unreduced_P` gives NNPN for n=8..22 with nodes 1809, 2214, 2615, 3010, 3405, 3800, 4195, 4590. `reduced_value_P` records *2 for n=8..20; `whole_cyl_P` records *2 for n=8 and 10 (saved run times 30s and 300s; these are timings, not theorem claims). The randomized Lemma 2/3 log reports 8000 L2 trials (9220 and 6992 move counts, zero failures), then 8000 L3 trials with shrink 0 (1857 accepted, 6143 rejected, zero mismatches), and 3000 trials with shrink 3 (42 accepted, 2957 rejected, one mismatch). PROOF.md reports the 1-of-42 shortened-arc result as an expected negative control. No unexplained P-log mismatch was found.

**COMPUTED-1 — Saved-log provenance.** The commands cited by PROOF.md are `sh research/ring_n_plus_2_proof/run_check3.sh` for the C3 logs and `PYTHONPATH=. .venv/bin/python research/ring_n_plus_2_proof/whole_cyl.py 8 10` for the two whole-board cylcgt values. I compared those saved logs read-only; I did not rerun these source-writing commands.

### Q-family files

**COMPUTED-1 — Scope discrepancy, not a P-proof counterexample.** The current `run_all.sh` adds Q-family (*3) runs that are not discussed in PROOF.md. Their two pump logs and `unreduced_Q_8_60.txt` reproduce; their signature is NNNPNNNN, with 7968 reduced nodes from n=18 onward. The saved `reduced_cyl_Q.txt` stops at n=12, while the current runner produces n=8..24. Thus PROOF.md's statement that `run_all.sh` writes four logs describes its earlier P-only version, not the current runner. The Q results are outside T53 and do not affect the P_n proof.

## Independent checker

**COMPUTED-1 — Implementation boundary.** The checker is [independent.py](independent.py). It imports only `Board`, `Pos`, and `cylcgt.pawns.passed`; its move generation, e.p. handling, race count, and nim-heap recursion are written from the stated rules. It checks both interpretations of an e.p. right across a heap move (`expire` and `keep`); the signatures coincide.

**CHECKED-2 — P_n:**

| n | 8 | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| G+*h, h=0..3 | NNPN | NNPN | NNPN | NNPN | NNPN | NNPN | NNPN | NNPN | NNPN |

**COMPUTED-1 — Control rings:** move only the b-file black pawn from rank 7 to rank 6. The signatures are NNNN for n=8,10,12, under both e.p.-heap interpretations. At h=2 these are N, whereas *2+*2 is P, so the checker distinguishes the controls from the claimed family.

Exact command from the project root:

```sh
PYTHONPATH=. nice -n 15 .venv/bin/python -u research/ring_n_plus_2_check/independent.py
```

The same `setpriority` warning applies to this invocation. The script's built-in assertions check e.p.-aware passed-pawn status, en-passant capture generation, and the empty game plus nim heaps *0 and *1.

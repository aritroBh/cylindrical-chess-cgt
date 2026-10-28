# Findings

**PROVED:** Proposition 3.2′(a)–(c), Lemma B, Lemma 3.2″, and the principal bridge proofs under stated hypotheses.
**PROVED:** The attractor and geometry arguments apply to loopy D-games under their stated hypotheses.
**PROVED, conditional:** The chess bridge requires move matching, decisive-event transfer, punishment, and e.p. handling.
**COMPUTED-1 / FALSE:** At G=0 a deleted arrow changes only its source state's result, not all four states.
Recommend PROVED for the core results; amend that subclaim and retain COMPUTED-1 for randomized deletion evidence.

## Comparison with the blind proof

My route for Proposition 3.2′(a) compares winning attractors directly on the full and exact four-state arenas. LOOPY first deletes the suicidal options, then uses a p-morphism to identify the remaining shuttle arena with `G ⊞ dud_D`. These are different presentations of the same least-fixed-point argument. Both work for loopy games.

For (b), my proof spells out monotonicity separately for the two attractors; LOOPY cites option monotonicity. For (c), the arguments agree: Lemma B removes the winner's pass, and induction needs only the two states where the winner's king stays still. My blind proof kept the en-passant condition abstract because the packet did not include the text of (E); LOOPY explicitly models the flag and explains why the stage argument survives its reset. Lemma 3.2″ and the chess bridge follow the same geometry, rank certification, and converse-induction routes.

## LOOPY proof audit

| LOOPY step | Assessment | Reason |
|---|---|---|
| Lemma A, stage-set definition and induction | **SOUND** | The option-surjectivity and option-preservation conditions transfer the existential and universal clauses at each finite stage. Taking the union gives equality of both least attractors; loopy edges do not affect this induction. |
| Lemma B, first-entry pass contradiction | **SOUND** | If the pass is the only first-entry witness, the opponent-turn node must already be winning at a lower stage. Its pass-back option then forces the original node into an even earlier stage, contradiction. A G-option must witness entry. |
| Proposition 3.2′(a), deletion of suicide options | **SOUND** | A mover's terminal loss cannot witness that mover's win; at an opponent-turn universal clause it is a terminal win for the attractor being proved. Removing these options preserves stages. |
| Proposition 3.2′(a), shuttle p-morphism | **SOUND** | At every retained state, G options map identically and each side's shuttle maps to, and covers, the dud pass; the two option conditions of Lemma A hold. |
| Proposition 3.2′(b), one-sided extra options | **SOUND** | Adding only White options preserves White's witnesses and can only strengthen White's universal conditions at Black-turn nodes; the dual argument gives the other inequality. |
| Proposition 3.2′(c), half-slice induction | **SOUND** | White does not need to shuttle by Lemma B. At Black-turn nodes, the Black shuttle simulates pass, context options are handled inductively, and extra `⊕` options are favorable to White. Only the stipulated two states are visited. Color reversal gives the mirror. |
| En-passant extension to Lemma B | **SOUND, CONDITIONAL ON THE FLAG MODEL** | The extra EP option is available only to the side to move at the flagged state. On a winner-to-move node, adding options cannot raise its first-entry stage. The pass-back reaches the flag-free node, so the stated option-monotonicity comparison closes the same contradiction. The text's flag-reset rule must match the chess move semantics. |
| Lemma 3.2″ geometry | **SOUND** | Buffer invariance excludes context pawn attacks; (K1) excludes Z-pawn attacks; (K2) excludes king attacks. Empty destinations and these attack exclusions make each shuttle legal and preclude stalemate. |
| Theorem 3.2‴(a), certified-set construction | **SOUND, CONDITIONAL ON (V1a-ctx), (V2-ctx), (Pun), AND (E)** | The winner's G-only strategy supplies S1; the opponent's context moves and shuttle are D responses and all other moves close by punishment. Legal shuttle availability supplies S3. Decisive events and EP moves need the stated matching hypotheses. The sharp theorem then applies. |
| Theorem 3.2‴(b), D-win to P-win | **SOUND, CONDITIONAL ON THE SAME BRIDGE HYPOTHESES** | This is the win transfer in either color, available at every regular position under global punishment. |
| Theorem 3.2‴(b), P-win to D-win | **SOUND, CONDITIONAL ON THE SAME BRIDGE HYPOTHESES** | Induction on P attractor stage rules out a non-D winning witness by punishment; at the opponent node, failure of D-attractor membership supplies a nonterminal, non-winning D option, whose matching legal move contradicts the P-win clause. Promotions are handled as beneficiary terminals. |
| Theorem 3.2‴, draw conclusion | **SOUND, CONDITIONAL ON EXACTNESS** | Since both finite-win attractors coincide, their complement is the draw set. If G has no decisive event, the D sum with dud is a draw. |
| Proposition 3.2′(d), opposition and one-arrow examples | **SOUND** | Direct application of the finite normal-play attractor clauses gives the listed outcomes. |
| Proposition 3.2′(d), positive-fraction deletion claim | **COMPUTED-1** | The specified random generator found changed root outcomes for every arrow in 621–630 of 1,000 instances, depending on the arrow. This supports but does not prove the general positive-fraction claim. |
| Proposition 3.2′(d), “at G=0 it changes the result at all four states” | **FALSE (under the literal all-states reading)** | For every single-arrow deletion at G=0, only the source state on the source side's turn changes; the other seven state/turn results remain D. The exact table is reproduced by `blind_deletions.py`. |

The principal proofs have no identified gap. The all-four-states subclaim is false as worded; if the intended meaning was only that each deletion changes at least one outcome, the G=0 computation supports that narrower statement. The bridge remains conditional, and the en-passant flag model must be part of (E)/(V1a-ctx), as stated.

## Random check

**COMPUTED-1, finite randomized sample only:** an independently written finite-arena least-fixed-point solver compared `r(G ⊞ Z)` against `r(G ⊞ dud_D)` for each position of G, all four shuttle states, and both turns. The generator used seed `340027`; for each instance it chose `n` uniformly from 1 through 5, then gave each side at each G position 0–3 IID options chosen uniformly from the `n` positions plus `⊕,⊖`. `Z` had the exact four-state two-shuttle cycle and one suicide option for each side at every state. The sample contained **1,000 instances**; all comparisons matched. It includes both acyclic and loopy G by construction, but does not claim exhaustive coverage.

Reproduce from the project root:

```sh
.venv/bin/python kings/delegate/out/K34/blind_check.py
```

Expected output begins `PASS instances=1000 seed=340027` and prints the exact generator description. This is one independently implemented solver, so the test itself is **COMPUTED-1**; the equality proof is **PROVED** by the stage argument. The count is reproducible with the command above.

### Deletion check detail

The complete G=0 outcomes, in state order `(z,w), (z,w′), (z′,w), (z′,w′)` and turn order White then Black, are reproduced with `.venv/bin/python kings/delegate/out/K34/blind_deletions.py`. For each source state, deleting its White shuttle yields `L` for White-to-move at that source and `D` for the other seven entries. Deleting its Black shuttle yields `W` for Black-to-move at that source and `D` for the other seven entries. Thus each of the eight deletions changes one of the eight state/turn entries, not all four states.

The same command produces the randomized per-arrow changed-instance counts `[630, 621, 630, 621, 630, 621, 630, 621]`, with the eight arrows ordered by the four states listed above, White arrow then Black arrow.

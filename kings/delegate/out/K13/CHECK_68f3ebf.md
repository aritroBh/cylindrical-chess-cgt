**PROVED (conditional):** The three K13b issues are repaired in the one-sided bridge.
**PROVED (conditional):** Its constructed set is White-certified for the sharp Theorem 1.14, so the stated conclusion is exactly a White P-win.
**PROBLEM (minor wording):** Cite Proposition 3.2's shuttle-legality hypothesis; Lemma 2.2 supplies context invariance, not shuttle legality by itself.

# K13c: one-sided chess bridge re-check

Scope: `kings/theory/LOOPY.md`, especially Theorem 1.14 sharp form, Definition 2.1, Lemma 2.2, Proposition 3.2 and its chess bridge, the e.p. remark after Proposition 3.2′, and Theorem 3.2‴. The verdicts below are proof audits, not computations.

## 1. K13b points

- **OK — terminal moves of Σ.** In the bridge's (V1a), the prescribed White move must be legal; matching to a successor is required only when Σ prescribes a position of `G ⊞ on_D`, explicitly excluding a `⊕`. The next bullet makes every reached decisive event of G a P-win for its beneficiary. Thus a selected `⊕` is a closing move under the sharp theorem, with no fictitious successor or rank comparison. A nonterminal prescribed move must match its D-successor.
- **OK — e.p. under the shuttle.** G's e.p. flag is a coordinate, and the `on_D` pass resets it, matching the loss of a real e.p. right on a king move. The map π forgets only the shuttle-square state, not the flag. The stated condition (E) on both sides' context moves handles the remaining chess/D correspondence. This covers a White pass even when the root has a live right.
- **OK — stalemate versus checkmate.** “Black is not stalemated” is precisely (S3). It permits a Black node with no legal move when Black is in check (checkmate, a White win), while excluding only unchecked stalemate. The sharp theorem’s S3 clause has the same meaning.

## 2. X, N, π and the conclusion

- **OK — π is well defined on N.** A chess position determines its pawn/context state, side to move, and e.p. flag; the two White shuttle squares map to ω. The shuttle resets the flag in both chess and D, so the mapping commutes with that transition. Proposition 3.2's shuttle move is non-capturing, and the buffer lemma keeps context pawns off the buffer and out of F_Z.
- **OK — N is well defined and X ∈ N.** N consists of the pre-promotion positions reached from X while White follows Σ and Black takes any legal D-matching move, stopping at the first closing move. The definition explicitly includes X. It need not include a Black Z-move: each such move is closing by the punishment hypothesis. The chess position set and D-state set are finite; the allowed pass can make D loopy but does not make N ambiguous or infinite.
- **OK — conclusion.** The sharp form says exactly that a σ-certified N containing X makes X a P-win for σ. With σ = White, the bridge's conclusion “X is a P-win for White” is exactly licensed. It is a result in P; a real-chess conclusion still requires the separately stated (A_Q)(X), as the project’s two-sided bridge also cautions.

## 3. S1–S3 move audit

- **OK — S1, White to move.** If Σ chooses a `⊕`/decisive event, it is legal by (V1a) and closes by the decisive-event hypothesis. Otherwise (V1a) supplies the legal non-promoting matching chess move. Σ is rank-lowering in D, including when its selected option is the `on_D` pass, so the successor lies in N at strictly smaller ρ.
- **OK — S2, Black to move: context moves and checks.** Every legal Black context move is matched by (V1a), with (E) ensuring the e.p. correspondence. A decisive event for White closes. A Black context promotion cannot occur at a Black-to-move node in the White D-winning region: it would be a Black-winning terminal option, contrary to that node's attractor condition. A checked Black node causes no exception: S2 quantifies over actual legal replies; any legal context reply is covered, and any legal Z reply is covered below. A position with no legal replies is handled by S3/checkmate as above.
- **OK — S2, Black promotions and Z-pawn/king moves.** A Black promotion by a Z-pawn is a Black Z-move, hence is ruled out as a winning reply by the explicit hypothesis that every legal Black Z-move is decisively punished in P. The same hypothesis closes every other legal Black king or Z-pawn move. This is the essential separate coverage because Black has no option in `on_D`.
- **OK — S2, ordinary replies and rank.** A matched, nonterminal Black context move is a D-option from a Black-to-move node in White's finite-rank D-winning region. By its attractor definition that option has strictly lower rank and remains in N. A terminal decisive event for White is closing. These exhaust legal Black moves before promotion by Definition 2.1 and Lemma 2.2.
- **OK — S3.** The explicit “Black is not stalemated” premise supplies S3 at each Black-to-move node of N; it does not incorrectly require Black to have a legal move in checkmate.

## 4. Remaining issue and label

- **PROBLEM — shuttle-legality attribution only; exact fix:** At the bridge proof’s S1 sentence (“the shuttle is legal by Lemma 2.2”), cite Proposition 3.2’s explicit hypothesis that both shuttle moves are legal in every context, with Lemma 2.2 establishing that context pawns cannot invalidate that legality. Lemma 2.2 alone proves buffer invariance/no context-pawn attack on F_Z; it does not establish safety from Z-pawn attacks or king adjacency. Since the bridge assumes X “as in Proposition 3.2,” the legality premise is already present, so this is not a missing theorem hypothesis or a failed S1 step. Keep it explicit if the bridge is ever stated independently of Proposition 3.2.
- **OK — “PROVED after repair,” conditional.** The bridge correctly invokes the sharp form, and its listed hypotheses discharge S1–S3. The label is right as a conditional theorem, not as an unconditional claim that a given chess position satisfies the bridge hypotheses. Theorem 3.2‴ is a useful comparison: it separately models both shuttles with `dud_D`, has its own context correspondence and punishment hypotheses, and likewise derives only a P-win before adding (A_Q)(X). It does not supply or replace any premise of this one-sided bridge.

No computations were run. Reproduce this text audit by reading the cited sections of `kings/theory/LOOPY.md`; there are no numerical claims.

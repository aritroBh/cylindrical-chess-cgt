# W4 T90 fixes report

All 45 replacements were applied by exact-string replacement with an occurrence-count assertion (script: delegate/out/W4_t90_fixes/apply.py, which lists every before/after string verbatim). Files edited: research/ring_family_proof/proof.tex, dist/tog/supp_src/s14_ringn.md, s15_note1.md, s15_note2.md, s15_note3.md, s15_note4.md.

## Applied
proof.tex: finding 3 (subarc convention after "wall pawn", plus "consecutive pair of pattern files of one wall (in the above sense)" in the insertion definition); finding 5 (both "reach a terminal position won by Y" replacements); finding 7 (theorem for every integer h>=0 with "in particular 0<=h<256"; first sentence of the scope paragraph replaced, and the following "Moreover, replace" shortened to "Replace" for grammar); finding 8 (F remark replaced from "Its reduced games" through "not been written out in full"); finding 9 (C1 program attribution; underscores escaped); finding 10 (both C2 replacements); finding 13 (distance bracket sentence, nim-heap definition, P/N sentence before the theorem, "opponent of the player who made the terminal pawn move", "marking an e.p.-capturable pawn" for flag ownership at five places, "Write X=Z and let Y be the other side", three-file contents sentence, "Write q nu ..." before (C), "in old-board coordinates", "every move by either starter hands the opponent a win", heading "Scope and ordinary game value", zone_states file names, "At the root the zone ... contains" plus "Pawns in the zone may move on a K-path", "An advance classified L is resolved before a poisoning reply", "Why the side of capture matters", the +256/-256 sentence in Remark 1). Marker lines checked: \begin{wallproof}, \end{wallproof}, \paragraph{The five poisoned wall moves, \paragraph{Remarks.} each occur once at line start. \lab macros unchanged.
Note 1: V sentence (consecutive pattern pair, unrestricted file-copy), sentence after V1, H2 window wording, H4 race shorthand.
S14: line 37 replaced.
Note 2: appended sentence (4<=9<=n-6), "front passed pawns eligible under the count rule of Section S13" at the shortest-distances sentence, "adjacent enemy on the side extending two further pattern files".
Note 3: line 39 replaced ("section 2 of Note 1 of Section S15"), line 5, line 42 "At the base by C1 ...", H5 race shorthand, line 78 "the tested correspondence fails at this control cut".
Note 4: H3 window text replaced, hand-proof reference to step (iii) of Lemma 3 in Section S13.

## Skipped
- Heading rename "Wall advances and their replies": skipped as instructed (build-script marker kept).
- Note 1 line 25 (race shorthand): the line has no "any race rule"/"any function" phrase; nothing to replace. Note 1 line 83 done.
- Note 1 lines 56, 73, 91, 109-110 ("Section 2b gives the local proof in the coordinates of P_n", "only role of the cut subject to numeric bounds", h<256 as the theorem's range): no exact words given; would need composition. Note that line 91 and S14/Note 2/Note 4 H7/H8 still say "h<256 in the model"; they remain true statements.
- "Lemma 3 fails" appears only in Note 3 line 78 (done). The control-cut wording at S14 48, 70-71, Note 1 88/101/119, Note 3 42/64, Note 4 46/70-71 ("unrestricted file-copy map", "a test of the conclusion outside the sufficient hypotheses"): these lines say "control fails", not "Lemma 3 fails", and the report gives no exact sentence; left unchanged.
- Note 2 line 20 ("proof of (ii)-(iii) is now in both sources"): no exact words.
- Finding 13 label-key remark: \lab{P}/\lab{C2} kept.

## Builds
- Standalone proof (delegate/out/W4_t90_fixes/build/proof.pdf): compiled, no errors, no undefined references, no overfull boxes.
- dist/tog: tools/build_supplement.py ok; tectonic supplement.tex into build/: 108 pages, no undefined references (one font-shape warning), one overfull box of 2.4pt (none over 5pt).
- git diff --stat: proof.tex 218 lines changed (includes earlier uncommitted work), s14 2, note1 22, note2 6, note3 10, note4 4. Nothing added or committed.

# Cover letter

Date: 23 November 2026 (draft date; Author must confirm the date on the day of submission)

To the Editor-in-Chief, IEEE Transactions on Games

Re: Full paper, "Chess Endgames on a Cylindrical Chessboard: Exact Combinatorial Game Values, Real-Chess Checks, and Tablebases"

Dear Editor,

I submit the manuscript above for review as a full paper. It is 10 pages including references. Supplementary material (67 pages) holds the full proofs and listings and is not part of the page count.

Cylinder chess joins the a-file to the h-file, leaving no side edges or corners. The paper studies king-and-pawn endgames on this board with combinatorial game theory after Elkies. The main results are these.

1. With the passed-pawn test made to respect en passant and the count rule, no whole-board nimber above star has at most six pawns on ordinary boards of any width, but star two appears with seven, in one position and its color-reversed twin, confirmed by three programs. Its real-chess value is open.
2. In pawn-only whole-board rings, star two needs six pawns on three files and, from ten files on, one per file (proof sketched). On seven files, ten-pawn rings reach star three.
3. There are positions with a legal pawn history worth one-eighth, up-second star and Tiny 1. With frozen kings and queen promotions only, the one-eighth position's tablebase-backed oracle value is one-eighth.
4. Against real chess the model is right in 92.5% of the decisive 8x8 positions we can check. We also correct earlier work on cylinder Dawson's chess: the ring is a first-player win exactly when the strip three files shorter has Grundy value zero.

The paper fits the journal because it solves games. It gives exact values for positions of a real game variant, checks them against Stockfish, Lc0 and Lichess tablebases, and builds and uses endgame tablebases for the cylinder. Results carry labels that say whether they are proved, sketched, or checked by one or two independent programs.

The manuscript is original, has not been published, and is not under review elsewhere. [Author must confirm]

The paper extends an unpublished 2025 study of the basic values, and says so in the text (Section I). [Author must confirm that this study has not been posted anywhere public.]

AI use. The Acknowledgment of the paper states: "AI coding assistants (Claude, Anthropic; Codex, OpenAI; and open models run through the OpenCode and Kilo tools) wrote and ran, under the author's direction, the software for the simulations, endgame searches, tablebases and cross-checks of Sections II-XIII and the scripts that draw the figures, wrote and checked the proofs of Sections S12-S15, and helped draft and edit the text of all sections. The author chose the research questions, directed the work and is responsible for all content."

Code and data are available to reviewers through an anonymous link, https://anonymous.4open.science/r/<id> [Author must insert the real link once created], which is also given in Section XIII of the manuscript.

Thank you for considering the paper.

Sincerely,

Aritro Bhattacharjee
University of Illinois Urbana-Champaign
[Author must confirm: the ToG guidelines as audited do not say whether ScholarOne shows the cover letter to reviewers. If it does, upload a copy without the name and affiliation. Not verified.]

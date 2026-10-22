# House style: write it the way Aritro wrote the 2025 paper

The 2025 paper is `prior_work/main.tex` ("Analysis of Chess Endgames on a Cylindrical Chessboard"). This
paper is its sequel and should read like the same author, a year further on. Anyone editing `paper/`
(Claude or a delegated model) follows these rules.

## Voice

- **"We", and talk to the reader.** "In this paper, we will...", "let's begin by...", "Now let's move on
  to...", "It is highly recommended that the reader try this position on their own."
- **White (left) and black (right).** Use lowercase "white" and "black" in running text. Add "(left)" or
  "(right)" the first time a section uses them as CGT players.
- **Walk through positions move by move.** Say who moves, what each side can do, and what is left. Then write
  the game in braces: "Thus, this game can be represented by G = {0 | ⋆}."
- **Define each value when it first appears.** "The formal definition of up is ↑ = {0 | ⋆}." "Tiny 1 is
  defined as ..."
- **Plain words before notation.** One idea per sentence, in short paragraphs. Use a word like "brilliant"
  for a surprising move, as the 2025 paper did.
- **Build up.** Start from small positions, move to bigger sums, and end with puzzles and open questions.
- **Be honest about status.** Keep the evidence labels (\status{proved}, \status{checked-2},
  \status{computed-1}, \status{conjecture}), but explain what they mean in words the first time.

## Layout

- `article` class, `\parindent` 15pt, `\parskip` 6pt.
- Numbered, centred section headings: "1. Rules of the Game".
- A cover picture under the title: `figures/CoverPic.png`, from Wikimedia Commons, credited as in 2025.
- **Every position gets a board picture** in the 2025 style: blue and white squares, rank numbers on the
  left, file letters underneath.
  - Generate it with `figures/make_figures.py`; never hand-draw one.
  - Caption it `Position S.N, (a-file and h-file are connected)`, or `Position S.N (flat board)` when it is
    not a cylinder position.
  - Number positions by section: Position 6.1, 6.2, ...
- **Graphs** (bar charts, step plots) also come from `figures/make_figures.py` with pgfplots, use the same
  blue, and get a short caption and one sentence of interpretation in the text.
- Citations are numbered, [1], [2], .... Keep the 2025 references, Wu–Yü–Landry, *Winning Ways*, Elkies
  and the Wikimedia cover, and add the new ones after them.

## Content rules

- Never present a number that is not in RESULTS.md as verified. Pending work goes in "What we still do not
  know" (the open-problems section).
- Each new result names its position with a diagram and gives at least one line of play that shows why.
- Credit tools plainly: the computations were done with programs written with AI coding assistants under
  the author's direction (see §Verification).
- Do not add "Mentored Under Thomas Morley" to the author line until Prof. Morley has seen this paper
  (decision in RESULTS.md §8: not contacted yet). The acknowledgements may thank him for mentoring the 2025
  paper.

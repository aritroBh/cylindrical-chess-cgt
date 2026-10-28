# Submitting the paper

Status on 2026-10-27, 22:20.

## Ready

- **References.** All 19 were checked against Crossref, OpenAlex, arXiv and publisher pages, and every field was
  compared. Three were fixed: Wu–Yü–Landry, the PyTorch page range, and the XBoard page's year. Mäser 2002 was in the
  bibliography but never cited; it is now cited in Section II. Report: `delegate/out/citation_check/REPORT.md`.
- **Facts.** The ring and nimber claims in Sections I, VIII and XIV match the research reports
  (`delegate/out/T68/REPORT.md`; its one error, "24 million rings on up to 24 files", is fixed).
- **Builds.** `paper/ieee/main.pdf` (named, 15 pages) and `main_review.pdf` (anonymous, 14 pages). The arXiv
  package passes every rule check: `sh dist/arxiv/build.sh` gives `dist/arxiv/cylinder-chess-arxiv.zip`.
- **AI statement.** Two sentences in the Acknowledgment. They satisfy IEEE, arXiv and Sage (ICGA), which ask for
  disclosure.

## Before sending to anyone

1. **The code link.** The paper links `github.com/aritroBh/cylindrical-chess-cgt`, which is private, and the local
   commits are not pushed. Readers outside will get a 404. Make the repository public and push, or change
   `\codeurl` to say the code is available on request.
2. **arXiv first, if you want a public date.** A first math.CO paper needs a personal endorser since 2026-01-21; an
   institutional e-mail is no longer enough. A UIUC faculty member who works in combinatorics or game theory is the
   natural person to ask (see the e-mail below). Category math.CO, cross-list cs.GT, MSC 91A46. arXiv caps new
   submissions at about two a month (secondary source).

## Where to submit

| Venue | Fit | Cost | AI rule | Catch |
|---|---|---|---|---|
| Integers (Games section) | Best fit for the CGT | Free, open access | Declaration at the end; "the wording must be the authors' own, not AI-generated" | The prose must be rewritten in your own words first |
| IEEE Trans. on Games | Good; the paper is already in its format | 10-page limit, about $1,000 in over-length charges for 15 pages | Disclosure in the Acknowledgment (done) | Cut to 10 pages or pay |
| ICGA Journal | Best fit for the tablebases and engines | No fees | Disclose AI text or code that affects the results (done) | Weaker fit for nimbers and Dawson's chess; maybe split |
| Electronic J. Combinatorics | Wide reach, high bar | Free | Strictest: AI-written proofs must be rewritten in your own words | Same as Integers, only stricter |

**Recommendation.**
- If you want to keep the current text, submit to **IEEE Transactions on Games** with the Acknowledgment as it is,
  and trim toward 10 pages to avoid the charges.
- If you rewrite the prose yourself (it is already in your 2025 voice, so this is mostly rephrasing), **Integers** is
  the better and free home for the CGT results.

Either way, check the journal's preprint policy before posting to arXiv. IEEE allows preprints; for Integers and EJC,
ask the editors.

The venue research, with every URL, is in `paper/VENUES.md`.

## E-mail to UIUC faculty (draft; send it yourself)

> **Subject:** Feedback request: combinatorial game theory of pawn endgames on a cylindrical chessboard
>
> Dear Professor ___,
>
> My name is Aritro Bhattacharjee. I have been studying king-and-pawn endgames on a cylindrical chessboard (the a- and
> h-files joined) with combinatorial game theory, extending Elkies' work on CGT in chess endgames, and I would be
> grateful for your feedback on the attached paper.
>
> Some of the results:
> - a passed-pawn test that respects en passant, and conditions under which Elkies' frozen kings are exact;
> - the least positions of value \*2 (seven pawns on ordinary boards) and \*3;
> - on the n-file cylinder, a ring \*2 with only one pawn per file for 10 ≤ n ≤ 60, and rings \*3 with n+1 pawns;
> - cylinder Dawson's chess: the ring is a first-player win exactly when the strip three files shorter has Grundy
>   value 0;
> - king-and-rook and other tablebases on the cylinder and the torus.
>
> Every computational result was checked by at least two independently written programs, and the code and data are
> at [repository link].
>
> If you have time, I would value any comments on the mathematics or the presentation. I also hope to post the paper
> on arXiv (math.CO), which now requires a personal endorsement for a first submission. Would you be willing to
> endorse it, or suggest someone who might?
>
> Thank you for your time.
>
> Best regards,
> Aritro Bhattacharjee

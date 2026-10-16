"""Compare whole-position pawn chess with the project's CGT sum model.

Run from the repository root with ``.venv/bin/python -m crosscheck.compare``.
"""
from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from cylcgt import cgt, pawns
from cylcgt.verify_paper import CLAIMS

from .minimax import Board, Position, format_position, outcome_class, parse_position, passed_flags, winner

SEED = 20261015
RANDOM_POSITIONS = 3000


@dataclass(frozen=True)
class Case:
    label: str
    board: Board
    pos: Position
    source: str


def _engine_board(board: Board) -> pawns.Board:
    return pawns.Board(board.files, board.ranks, board.wrap, board.ep)


def _engine_position(pos: Position) -> pawns.Pos:
    return pawns.Pos(pos.white, pos.black, pos.ep)


def _random_position(rng: random.Random, board: Board, active_ep: bool) -> Position:
    count = rng.randint(2, 7)
    white: set[tuple[int, int]] = set()
    black: set[tuple[int, int]] = set()
    ep = None
    reserved: set[tuple[int, int]] = set()

    if active_ep:
        side = rng.choice(("W", "B"))  # side that made the double push
        file = rng.randrange(board.files)
        neighbors = [board.neighbor(file, delta) for delta in (-1, 1)]
        neighbors = [f for f in neighbors if f is not None]
        if not neighbors:
            return _random_position(rng, board, active_ep)
        adjacent = rng.choice(neighbors)
        if side == "W":
            white.add((file, 4))
            black.add((adjacent, 4))
            ep = ((file, 3), (file, 4), "B")
            reserved.update({(file, 2), (file, 3)})
        else:
            black.add((file, 5))
            white.add((adjacent, 5))
            ep = ((file, 6), (file, 5), "W")
            reserved.update({(file, 6), (file, 7)})

    available = [
        (file, rank)
        for rank in range(1, board.ranks + 1)
        for file in range(board.files)
        if (file, rank) not in white | black | reserved
        and (ep is None or (file, rank) != ep[0])
    ]
    rng.shuffle(available)
    while len(white) + len(black) < count:
        file, rank = available.pop()
        # Keep both colors present; live e.p. positions already have one of each.
        if not white:
            white.add((file, rank))
        elif not black:
            black.add((file, rank))
        elif rng.choice((True, False)):
            white.add((file, rank))
        else:
            black.add((file, rank))
    return Position(frozenset(white), frozenset(black), ep)


def _random_cases() -> tuple[list[Case], Counter]:
    rng = random.Random(SEED)
    # 80% cylinders, 20% flat boards; each geometry has e.p. enabled and disabled.
    modes = ([(True, True)] * 1200 + [(True, False)] * 1200
             + [(False, True)] * 300 + [(False, False)] * 300)
    rng.shuffle(modes)
    cases = []
    seen = set()
    skipped_dual_pass = Counter()
    for index, (wrap, ep_enabled) in enumerate(modes):
        board = Board(8, 8, wrap, ep_enabled)
        want_active_ep = ep_enabled and rng.randrange(5) == 0
        while True:
            pos = _random_position(rng, board, want_active_ep)
            key = (board, pos)
            if passed_flags(board, pos) == (True, True):
                skipped_dual_pass[(wrap, ep_enabled)] += 1
                continue
            if key in seen:
                continue
            seen.add(key)
            break
        cases.append(Case(f"random #{index + 1}", board, pos, "random"))
    return cases, skipped_dual_pass


def _cases() -> tuple[list[Case], Counter]:
    claims = []
    for label, text, _claim in CLAIMS:
        pos = parse_position(text)
        for ep_enabled in (True, False):
            claims.append(Case(f"paper claim: {label}", Board(8, 8, True, ep_enabled), pos, "claim"))
    random_cases, skipped = _random_cases()
    return claims + random_cases, skipped


def _evaluate(case: Case) -> dict:
    board, pos = case.board, case.pos
    white_to_move = winner(board, pos, "W")
    black_to_move = winner(board, pos, "B")
    exact = outcome_class(board, pos)

    c_board, c_pos = _engine_board(board), _engine_position(pos)
    components = pawns.components(c_board, c_pos)
    pawns.race_hits.clear()
    game = pawns.value(c_board, c_pos)
    cgt_outcome = cgt.outcome(game)
    return {
        "case": case,
        "white_to_move": white_to_move,
        "black_to_move": black_to_move,
        "exact": exact,
        "game": cgt.show(game),
        "cgt": cgt_outcome,
        "components": components,
        "active_ep": pos.ep is not None,
        "passers": passed_flags(board, pos),
    }


def _key(result: dict) -> tuple[str, bool]:
    return ("single" if len(result["components"]) == 1 else "multi",
            result["case"].board.ep)


def _summary_table(results: list[dict]) -> str:
    counts = Counter()
    for result in results:
        group, ep_enabled = _key(result)
        counts[(group, ep_enabled, result["exact"] == result["cgt"])] += 1
    lines = ["| Components | E.p. rule | Agree | Disagree | Total |",
             "|---|---:|---:|---:|---:|"]
    for group in ("single", "multi"):
        for ep_enabled in (True, False):
            agree = counts[(group, ep_enabled, True)]
            disagree = counts[(group, ep_enabled, False)]
            lines.append(f"| {group} | {'on' if ep_enabled else 'off'} | {agree} | {disagree} | {agree + disagree} |")
    agree = sum(n for (_, _, same), n in counts.items() if same)
    disagree = len(results) - agree
    lines.append(f"| **all** | — | **{agree}** | **{disagree}** | **{len(results)}** |")
    return "\n".join(lines)


def _diagnosis(results: list[dict]) -> str:
    bad = [r for r in results if r["exact"] != r["cgt"]]
    singles = [r for r in bad if len(r["components"]) == 1]
    multi_ep = [r for r in bad if len(r["components"]) > 1 and r["active_ep"]]
    multi_no_ep = [r for r in bad if len(r["components"]) > 1 and not r["active_ep"]]
    lines = [
        f"- **Single component: {len(singles)} mismatch(es).** A component sum cannot explain these; they indicate a disagreement in rule handling or an implementation bug. Inspect these first before assigning blame.",
        f"- **Multiple components with a live e.p. right: {len(multi_ep)} mismatch(es).** These are consistent with the known approximation: real e.p. expires after any opposing move, even one in another component, while a disjunctive sum models component options independently.",
        f"- **Multiple components without a live e.p. right: {len(multi_no_ep)} mismatch(es).** These cannot be blamed on live e.p. The main structural risk is the global passer/race rule: a move in one component can create a passer while another component supplies the opponent's passer, ending the whole position by the race rule. Summing local component values does not encode that cross-component terminal event.",
    ]
    if not bad:
        lines = ["No outcome-class disagreements were found in this run, so no mismatch diagnosis applies."]
    return "\n".join(lines)


def _case_detail(result: dict, index: int) -> str:
    case = result["case"]
    board = case.board
    geometry = "cylinder" if board.wrap else "flat"
    component_text = "; ".join(map(str, result["components"])) or "(empty)"
    ep_state = "none" if not case.pos.ep else (
        f"target={case.pos.ep[0]}, captured={case.pos.ep[1]}, side={case.pos.ep[2]}"
    )
    return (
        f"### {index}. {case.label}\n\n"
        f"- Source: {case.source}; board: {geometry}, {board.files}x{board.ranks}; e.p. rule: {'on' if board.ep else 'off'}\n"
        f"- Position: `{format_position(case.pos)}`\n"
        f"- Live e.p. state: `{ep_state}`; starting passers (W, B): `{result['passers']}`\n"
        f"- Exact wins: White to move → `{result['white_to_move']}`; Black to move → `{result['black_to_move']}`; class `{result['exact']}`\n"
        f"- CGT: value `{result['game']}`; outcome class `{result['cgt']}`\n"
        f"- Components ({len(result['components'])}): `{component_text}`\n"
    )


def run() -> None:
    cases, skipped = _cases()
    results = [_evaluate(case) for case in cases]
    disagreements = [result for result in results if result["exact"] != result["cgt"]]
    report = [
        "# Independent pawn-chess cross-check\n",
        "## Method\n",
        "`minimax.py` searches the whole board and includes side to move and the expiring en-passant right in each memoized state. It does not import `cylcgt`; only this comparison harness imports the CGT implementation. Outcome classes are derived from the winners with White and Black to move.\n",
        f"Compared all {len(CLAIMS)} `verify_paper.CLAIMS` positions with e.p. enabled and disabled ({2 * len(CLAIMS)} claim cases), plus {RANDOM_POSITIONS:,} distinct random positions (seed `{SEED}`; 2–7 pawns; 2,400 cylindrical and 600 flat; e.p. rule enabled and disabled in each geometry). The random set skipped starting positions where both sides already had passers. It generated {sum(1 for case in cases if case.source == 'random' and case.pos.ep is not None):,} live e.p. rights.\n",
        f"Random candidates skipped for two starting passer sides: {sum(skipped.values()):,}. White pawns on rank 1 and pawns on rank 8 are included in sampling.\n",
        "## Summary\n",
        _summary_table(results),
        "\n\nSingle-component rows are the decisive check: the exact search and `cylcgt` must agree there. Multi-component results expose the limits of the disjunctive-sum approximation.\n",
        "## Disagreement diagnosis\n",
        _diagnosis(results),
        "\n\nThe categories above identify the likely source, not proof by label. In particular, each single-component mismatch must be replayed against the move/race rules; multi-component mismatches without live e.p. need a concrete cross-component race witness before being attributed to that approximation.\n",
        "## First 15 disagreements\n",
    ]
    if disagreements:
        report.extend(_case_detail(result, i) for i, result in enumerate(disagreements[:15], 1))
        if len(disagreements) > 15:
            report.append(f"Only the first 15 of {len(disagreements)} disagreements are shown.\n")
    else:
        report.append("No disagreements.\n")

    report_text = "\n".join(report).rstrip() + "\n"
    report_path = Path(__file__).with_name("REPORT.md")
    report_path.write_text(report_text)
    print(_summary_table(results))
    print(f"\nCompared {len(results):,} positions; {len(disagreements):,} disagreements.")
    if disagreements:
        print("\nFirst 15 disagreements:\n")
        print("\n".join(_case_detail(result, i).rstrip()
                        for i, result in enumerate(disagreements[:15], 1)))
    print(f"\nWrote {report_path}")


if __name__ == "__main__":
    run()

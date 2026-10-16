"""Diagram-audit rerun: my own transcriptions (FEN, from notes/diagram_audit.md Part A)
fed to cylcgt.pawns, compared square-by-square with cylcgt.verify_paper.CLAIMS,
plus a small king-move legality check for the king groups (5.1, 7.2, 7.3).

Run from the project root:
  PYTHONPATH=. .venv/bin/python verify/diagrams/rerun.py
"""
from __future__ import annotations

import sys
from dataclasses import replace

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos, RaceError, describe, passed, components
from cylcgt.verify_paper import CLAIMS  # read-only import of the audited transcriptions

FILES = "abcdefgh"

# ---- My transcriptions (Part A of notes/diagram_audit.md), board part of FEN ----
MINE = {
    "2.1": "8/8/8/4p3/4P3/8/8/8",
    "2.2": "8/8/8/8/7p/p7/P7/7P",
    "2.3": "8/8/8/8/2p5/3p4/3P4/2P5",
    "3.1": "8/8/8/7p/p7/P7/8/7P",
    "3.2": "8/8/7p/p7/P7/8/8/7P",
    "4.1": "8/8/4p3/8/4P3/8/8/8",
    "4.2": "8/8/4p3/8/8/4P3/8/8",
    "4.3": "8/p7/p7/p7/P6P/7p/7P/8",
    "5.1": "8/8/8/p6K/Pk6/8/8/8",
    "7.1": "8/p4p2/2p4p/P1p5/P4P2/2P2P1P/2P4P/8",
    "7.2": "3k4/1p1Pp2p/p3K3/8/8/7P/PP6/8",
    "7.3": "6K1/5Pp1/3p1k2/P2p4/3p3p/2PP2p1/2p5/P1P3PP",
}


def parse_fen(fen: str):
    pieces = {}
    for i, row in enumerate(fen.split("/")):
        rank = 8 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                pieces[(f, rank)] = ch
                f += 1
        assert f == 8, (fen, row)
    return pieces


def to_pos(pieces, keep=None):
    w = frozenset(s for s, c in pieces.items() if c == "P" and (keep is None or s in keep))
    b = frozenset(s for s, c in pieces.items() if c == "p" and (keep is None or s in keep))
    return Pos(w, b)


def sqname(s):
    return f"{FILES[s[0]]}{s[1]}"


def pos_text(p: Pos):
    return f"W: {' '.join(sorted(map(sqname, p.white)))} / B: {' '.join(sorted(map(sqname, p.black)))}"


def solve(board: Board, pos: Pos, rule: str):
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    pawns.race_hits.clear()
    try:
        d = describe(board, pos)
    except RaceError as e:
        return f"RACE({e})", 0, None
    finally:
        pass
    return d, len(pawns.race_hits), None


def report(label, board: Board, pos: Pos):
    tag = f"{'cyl' if board.wrap else 'flat'} ep={'on' if board.ep else 'off'}"
    vals = {}
    hits = {}
    d0 = None
    for rule in ("count", "mover", "opponent"):
        d, nh, _ = solve(board, pos, rule)
        if isinstance(d, str):
            vals[rule] = d
        else:
            vals[rule] = d["value"]
            if rule == "count":
                d0 = d
        hits[rule] = nh
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    sens = "race-robust" if len(set(vals.values())) == 1 else "RACE-SENSITIVE"
    extra = ""
    if d0:
        extra = (f"outcome {d0['outcome']} mean {d0.get('mean')} temp {d0.get('temperature')} "
                 f"sum_safe {d0['sum_safe']} comps {len(d0['components'])}")
    print(f"  [{tag}] {label}: {vals['count']}  | {extra} | race nodes {hits['count']} {sens}")
    if sens == "RACE-SENSITIVE":
        print(f"      mover   -> {vals['mover']}")
        print(f"      opponent-> {vals['opponent']}")


CYL = Board(8, 8, True, True)
CYL_NOEP = replace(CYL, ep=False)
FLAT = Board(8, 8, False, True)
FLAT_NOEP = replace(FLAT, ep=False)


# ---------------- 1. square-by-square comparison with CLAIMS ----------------
def compare_claims():
    print("=== 1. My transcription vs cylcgt.verify_paper.CLAIMS (pawns only) ===")
    claim_by_pos = {}
    for label, text, claim in CLAIMS:
        key = label.split()[0]
        claim_by_pos.setdefault(key, []).append((label, Pos.parse(text), claim))
    for key, fen in MINE.items():
        pcs = parse_fen(fen)
        mine_pos = to_pos(pcs)
        kings = {sqname(s): c for s, c in pcs.items() if c in "Kk"}
        if key not in claim_by_pos:
            print(f"{key}: NOT IN CLAIMS. mine = {pos_text(mine_pos)} kings={kings}")
            continue
        for label, cp, claim in claim_by_pos[key]:
            if "total" in label or "kings removed" in label or label.strip() == key or "as drawn" in label \
                    or label.startswith(key + " ") and len(claim_by_pos[key]) == 1:
                full = True
            else:
                full = False
            if not full:
                # sub-game: compare on the files the sub-game uses
                fs = {f for f, _ in cp.white | cp.black}
                sub = Pos(frozenset(s for s in mine_pos.white if s[0] in fs),
                          frozenset(s for s in mine_pos.black if s[0] in fs))
                ok = (sub.white == cp.white and sub.black == cp.black)
                print(f"{key}: sub-game '{label.strip()}' files {''.join(FILES[f] for f in sorted(fs))}: "
                      f"{'MATCH' if ok else 'DIFF'}  claims={pos_text(cp)} mine={pos_text(sub)}")
            else:
                ok = (mine_pos.white == cp.white and mine_pos.black == cp.black)
                msg = "MATCH" if ok else "DIFF"
                if not ok:
                    msg += (f"  only-mine W{sorted(map(sqname, mine_pos.white - cp.white))} "
                            f"B{sorted(map(sqname, mine_pos.black - cp.black))}"
                            f"  only-claims W{sorted(map(sqname, cp.white - mine_pos.white))} "
                            f"B{sorted(map(sqname, cp.black - mine_pos.black))}")
                print(f"{key}: '{label.strip()}': {msg}; kings in diagram (not in CLAIMS): {kings or 'none'}")


# ---------------- 2. solver reruns on my transcription ----------------
def reruns():
    print("\n=== 2. Solver on my transcriptions (count rule shown; mover/opponent if they differ) ===")
    for key in ("2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "4.3", "7.1"):
        pos = to_pos(parse_fen(MINE[key]))
        print(f"{key}  {pos_text(pos)}  passedW={passed(CYL, pos, 'W')} passedB={passed(CYL, pos, 'B')}")
        for b in (CYL, CYL_NOEP):
            report(key, b, pos)

    print("\n-- 2.3 (caption omits 'connected': flat board; also cylinder for comparison) --")
    pos = to_pos(parse_fen(MINE["2.3"]))
    print(f"2.3  {pos_text(pos)}")
    for b in (FLAT, FLAT_NOEP, CYL, CYL_NOEP):
        report("2.3", b, pos)

    print("\n-- 4.2 alternatives (which pawn placement matches the text's {0,*|*}) --")
    for txt in ("W: e3 / B: e6", "W: e2 / B: e5", "W: e2 / B: e6", "W: e3 / B: e5", "W: e2 / B: e4"):
        p = Pos.parse(txt)
        pawns._value.cache_clear()
        g = pawns.value(CYL, p)
        Ls = sorted({cgt.show(pawns.value(CYL, q)) for q in pawns.moves(CYL, p, 'W')})
        Rs = sorted({cgt.show(pawns.value(CYL, q)) for q in pawns.moves(CYL, p, 'B')})
        print(f"  {txt}: value {cgt.show(g)}; literal options {{{', '.join(Ls)} | {', '.join(Rs)}}}")

    print("\n-- 7.1 sub-games --")
    pcs = parse_fen(MINE["7.1"])
    for files in ("c", "f", "ah"):
        keep = {s for s in pcs if FILES[s[0]] in files}
        p = to_pos(pcs, keep)
        print(f"  files {files}: {pos_text(p)}")
        for b in (CYL, CYL_NOEP):
            report(f"7.1[{files}]", b, p)

    print("\n-- 7.2: pawn group a,b,h (kings and d7/e7 omitted: the d7 pawn is king-blocked) --")
    pcs = parse_fen(MINE["7.2"])
    keep = {s for s in pcs if FILES[s[0]] in "abh"}
    p = to_pos(pcs, keep)
    print(f"  {pos_text(p)}")
    for b in (CYL, CYL_NOEP):
        report("7.2[abh]", b, p)
    full = to_pos(pcs)
    print(f"  all 7.2 pawns incl. d7/e7: {pos_text(full)} passedW={passed(CYL, full, 'W')} "
          f"passedB={passed(CYL, full, 'B')}  (solver sees d7 as passed: it cannot model the Kd8 blockade)")

    print("\n-- 7.3: whole pawn set, and the paper's claimed sub-games --")
    pcs = parse_fen(MINE["7.3"])
    full = to_pos(pcs)
    print(f"  all pawns: {pos_text(full)} passedW={passed(CYL, full, 'W')} passedB={passed(CYL, full, 'B')}")
    for b in (CYL, CYL_NOEP):
        report("7.3[all pawns]", b, full)
    print("  components found by the solver:", [str(c) for c in components(CYL, full)])
    cd = to_pos(pcs, {s for s in pcs if FILES[s[0]] in "cd"})
    print(f"  paper's {{c,d}} sub-game: {pos_text(cd)}")
    for b in (CYL, CYL_NOEP):
        report("7.3[cd]", b, cd)
    gha = to_pos(pcs, {s for s in pcs if FILES[s[0]] in "gha" and s not in {(6, 7)}})
    print(f"  paper's {{g,h,a}} sub-game without the trebuchet g7: {pos_text(gha)} "
          f"passedW={passed(CYL, gha, 'W')}")
    for b in (CYL, CYL_NOEP):
        report("7.3[gha]", b, gha)
    # what if a5 were not there (is the rest of the g/h/a group ever 1?)
    gha2 = Pos(gha.white - {(0, 5)}, gha.black)
    print(f"  same without the a5 runner: {pos_text(gha2)}")
    for b in (CYL, CYL_NOEP):
        report("7.3[gha - a5]", b, gha2)


# ---------------- 3. king groups: legal king moves on the 8x8 cylinder ----------------
def neighbours(s):
    f, r = s
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0:
                continue
            rr = r + dr
            if 1 <= rr <= 8:
                yield ((f + df) % 8, rr)


def attacks(pcs, colour):
    """Squares attacked by `colour` ('W'/'B') on the cylinder."""
    out = set()
    for s, c in pcs.items():
        if colour == "W" and c == "K" or colour == "B" and c == "k":
            out |= set(neighbours(s))
        elif colour == "W" and c == "P":
            if s[1] < 8:
                out |= {((s[0] - 1) % 8, s[1] + 1), ((s[0] + 1) % 8, s[1] + 1)}
        elif colour == "B" and c == "p":
            if s[1] > 1:
                out |= {((s[0] - 1) % 8, s[1] - 1), ((s[0] + 1) % 8, s[1] - 1)}
    return out


def king_moves(pcs, colour):
    k = "K" if colour == "W" else "k"
    ks = next(s for s, c in pcs.items() if c == k)
    own = {s for s, c in pcs.items() if (c.isupper() if colour == "W" else c.islower())}
    enemy = "B" if colour == "W" else "W"
    res = []
    for t in neighbours(ks):
        if t in own:
            continue
        new = dict(pcs)
        del new[ks]
        captured = new.pop(t, None)
        new[t] = k
        if t in attacks(new, enemy):
            continue
        res.append((t, captured, new))
    return res


def capturable(pcs, colour):
    """Pieces of `colour` that the enemy king can legally capture right now."""
    enemy = "B" if colour == "W" else "W"
    out = []
    for t, cap, _ in king_moves(pcs, enemy):
        if cap:
            out.append((sqname(t), cap))
    return out


def kings():
    print("\n=== 3. King groups on the 8x8 cylinder (legal king moves; what each one allows) ===")
    groups = {
        "5.1": MINE["5.1"],
        "7.2 king group (Ke6,Pd7 / Kd8,Pe7)": "3k4/3Pp3/4K3/8/8/8/8/8",
        "7.3 king group (Kg8,Pf7 / Kf6,Pg7)": "6K1/5Pp1/5k2/8/8/8/8/8",
    }
    for label, fen in groups.items():
        pcs = parse_fen(fen)
        print(f"{label}:  W in check={any(c=='K' and s in attacks(pcs,'B') for s,c in pcs.items())} "
              f"B in check={any(c=='k' and s in attacks(pcs,'W') for s,c in pcs.items())}")
        for colour in ("W", "B"):
            mv = king_moves(pcs, colour)
            print(f"  {colour} king legal moves: {[sqname(t) + ('x' + c if c else '') for t, c, _ in mv]}")
            for t, cap, new in mv:
                lost = capturable(new, colour)
                print(f"     K{sqname(t)}{'x'+cap if cap else ''}: enemy king may then capture {lost or 'nothing'}")
        # pawn pushes available inside the group (blocked by kings?)
        occ = set(pcs)
        for s, c in pcs.items():
            if c == "P" and (s[0], s[1] + 1) not in occ:
                print(f"  white pawn {sqname(s)} can advance to {sqname((s[0], s[1] + 1))}")
            if c == "p" and (s[0], s[1] - 1) not in occ:
                print(f"  black pawn {sqname(s)} can advance to {sqname((s[0], s[1] - 1))}")


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    compare_claims()
    reruns()
    kings()

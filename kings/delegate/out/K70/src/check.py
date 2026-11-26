"""Read the two printed strategy tables and play every legal reply on each square."""

from collections import Counter, namedtuple
from ctypes import CDLL, c_int
from functools import lru_cache
from pathlib import Path
import re
import subprocess
import tempfile

from board import X, attacked, dist, moves, name, pos, sq

HERE = Path(__file__).resolve().parent
PROOF = HERE.parent / "PROOF.md"
Row = namedtuple("Row", "fixed pawns ep zone move replies")


def read_zone(text):
    if text == "*":
        return set(range(64))
    result = set()
    for token in text.lstrip("!").split(","):
        ends = token.split("–")
        lo, hi = sq(ends[0]), sq(ends[-1])
        result.update(
            x
            for x in range(64)
            if lo % 8 <= x % 8 <= hi % 8 and lo // 8 <= x // 8 <= hi // 8
        )
    return set(range(64)) - result if text.startswith("!") else result


def read_tables():
    tables = {}
    for line in PROOF.read_text().splitlines():
        if line.startswith("## Table "):
            tables[line[9]] = rows = {}
        elif line.startswith("**White pawn "):
            w, b, c = re.fullmatch(
                r"\*\*White pawn (\S+) · Black pawns (\S+), (\S+)\*\*", line
            ).groups()
            pawns = tuple(map(sq, (w, b, c)))
        elif re.match(r"^\| \d+ \|", line):
            number, king, zone, move, links = (
                c.strip() for c in line.strip("|").split("|")
            )
            fixed, ep = re.fullmatch(r"(\w+)(?: \(ep (\w+)\))?", king).groups()
            replies = {}
            for link in links.split():
                label, targets = link.split("→")
                replies[label] = {
                    int(x) if x.isdigit() and x != "0" else x
                    for x in targets.split(",")
                }
            assert int(number) not in rows
            rows[int(number)] = Row(
                sq(fixed), pawns, sq(ep or "-"), read_zone(zone), move, replies
            )
    return tables


def diagram(s, mode):
    t, k, j, w, b, c, ep = s
    return (j, k, (w, b, c), ep) if mode == "B" else (k, j, (w, b, c), ep)


def matches(s, row, mode):
    fixed, other, pawns, ep = diagram(s, mode)
    return (
        s[0] == (mode == "B")
        and fixed == row.fixed
        and pawns == row.pawns
        and ep == row.ep
        and other in row.zone
    )


def blockade(s):
    """Recognize A, B, C and the last-rank position by coordinates."""
    t, k, j, w, b, c, ep = s
    if t != 1 or c != X or b == X or b % 8 != 2 or w not in (X, sq("b6"), sq("b7")):
        return False
    rank = b // 8 + 1
    if rank == 2:
        return k == sq("c1") and j in (sq("b3"), sq("d3"))
    if 3 <= rank <= 6:
        return (
            k == b - 8
            or (k == b - 16 and j in (b + 7, b + 8, b + 9))
            or (k == b - 17 and j == b - 1)
            or (k == b - 15 and j == b + 1)
        )
    return False


@lru_cache(maxsize=2048)
def legal(s):
    result = {}
    for m, nxt in moves(s):
        if m.startswith("K") and sq(m[1:]) in ((s[3],) if s[0] else s[4:6]):
            m = "Kx" + m[1:]
        result[m] = nxt
    return result


def check_rows(tables):
    counts = Counter()
    for mode, rows in tables.items():
        for n, row in rows.items():
            w, b, c = row.pawns
            witnessed = set()
            for x in row.zone:
                k, j = (x, row.fixed) if mode == "B" else (row.fixed, x)
                if k in (w, b, c) or j in (w, b, c) or dist(k, j) <= 1:
                    continue
                if (
                    any(attacked(p, k, 1) for p in (b, c))
                    if mode == "B"
                    else attacked(w, j, 0)
                ):
                    continue
                s = pos(k, j, w, b, c, int(mode == "B"), row.ep)
                assert row.move in legal(s), (mode, n, s, row.move)
                nxt = legal(s)[row.move]
                counts[mode, "positions"] += 1
                ends = row.replies.get("end", set())
                if nxt is None:
                    assert "P" in ends
                    witnessed.add(("end", "P"))
                    continue
                if mode == "D" and nxt[4:6] == (X, X) and "0" in ends:
                    witnessed.add(("end", "0"))
                    continue
                if mode == "D" and "F" in ends and blockade(nxt):
                    witnessed.add(("end", "F"))
                    continue
                replies = legal(nxt)
                assert replies, (mode, n, "unexpected terminal")
                for m, last in replies.items():
                    counts[mode, "replies"] += 1
                    tag = "K" if m.startswith("K") and not m.startswith("Kx") else m
                    assert last is not None, (mode, n, m, "opposing promotion")
                    candidates = row.replies.get(tag, set())
                    found = {
                        d
                        for d in candidates
                        if isinstance(d, int) and matches(last, rows[d], mode)
                    }
                    if "0" in candidates and mode == "D" and last[4:6] == (X, X):
                        found.add("0")
                    if (
                        "S" in candidates
                        and mode == "D"
                        and not legal(last)
                        and not any(attacked(p, last[1], 1) for p in last[4:6])
                    ):
                        found.add("S")
                    assert found, (mode, n, name(x), m, candidates)
                    if mode == "B":
                        assert all(d < n for d in found)
                    witnessed.update((tag, d) for d in found)
            printed = {(m, d) for m, ns in row.replies.items() for d in ns}
            assert printed == witnessed, (
                mode,
                n,
                printed - witnessed,
                witnessed - printed,
            )
    return counts


def check_starts(tables, value):
    roots = Counter()
    required = set(map(sq, "b2 c2 d2 e2 f2 b3 c3 d3 e3 f3 e4 f4 e5 f5 e6 f6".split()))
    longest = 0
    for w in map(sq, ("c2", "c3", "c4")):
        for k in range(64):
            if k == w or dist(k, 41) <= 1:
                continue
            s = pos(k, 41, w, 49, 42)
            exception = (name(k), name(w)) == ("b4", "c4")
            score = value(*s)
            assert score == 0 if exception else score < 0, (s, score)
            roots[name(w), "draw" if exception else "black"] += 1
            if not exception:
                longest = max(longest, 1000 + score)
                roots["required"] += k in required
            for m, nxt in legal(s).items():
                if exception and m == "c5":
                    replies = legal(nxt)
                    assert set(replies) == {"Ka6", "Ka7", "Kc7"}
                    for reply, after in replies.items():
                        number = 81 if reply == "Kc7" else 80
                        assert matches(after, tables["D"][number], "D")
                    continue
                entries = {
                    10: (481, 486),
                    18: (475, 480),
                    26: (445, 448, 451),
                    34: (414, 417),
                }
                assert any(matches(nxt, tables["B"][n], "B") for n in entries[nxt[3]])
    assert [roots[name(w), "black"] for w in (10, 18, 26)] == [54, 54, 53]
    assert longest == 38
    assert roots["required"] == 46
    print(
        "Starts by pawn: c2 54 wins, c3 54 wins, c4 53 wins and 1 draw. Required set: 46 wins."
    )
    print(
        "Longest optimal Black win:",
        longest,
        "plies =",
        (longest + 1) // 2,
        "Black moves.",
    )


def check_black_waiting_moves():
    guards = set(map(sq, ("a7", "a8", "b8", "c8", "c7")))
    for j in guards:
        for k in range(64):
            if (
                k in (34, 42, 49)
                or dist(k, j) <= 1
                or any(attacked(p, k, 1) for p in (42, 49))
            ):
                continue
            s = pos(k, j, 34, 42, 49, 1)
            options = [
                after
                for m, after in legal(s).items()
                if m.startswith("K") and after[2] in guards
            ]
            assert options
            for after in options:
                assert all(
                    again and again[3:6] == s[3:6] for again in legal(after).values()
                )


def check_fortress(value):
    count = 0
    for r in range(2, 7):
        p = sq("c" + str(r))
        for w in (X, sq("b6"), sq("b7")):
            for k in range(64):
                for j in range(64):
                    if (
                        dist(k, j) < 2
                        or k in (w, p)
                        or j in (w, p)
                        or attacked(p, k, 1)
                    ):
                        continue
                    s = pos(k, j, w, p, X, 1)
                    if blockade(s):
                        assert value(*s) <= 0, s
                        count += 1
    print("Blockade cross-check:", count, "legal diagrams.")


if __name__ == "__main__":
    check_black_waiting_moves()
    tables = read_tables()
    totals = check_rows(tables)
    for m, rows in tables.items():
        print(
            m,
            len(rows),
            "rows,",
            totals[m, "positions"],
            "positions,",
            totals[m, "replies"],
            "nonterminal replies.",
        )
    with tempfile.TemporaryDirectory(dir=HERE) as tmp:
        so = Path(tmp) / "independent.so"
        subprocess.run(
            [
                "c++",
                "-std=c++17",
                "-O2",
                "-shared",
                "-fPIC",
                str(HERE / "solve.cpp"),
                "-o",
                str(so),
            ],
            check=True,
        )
        value = CDLL(str(so)).val
        value.argtypes = [c_int] * 7
        check_starts(tables, value)
        check_fortress(value)

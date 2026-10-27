#!/usr/bin/env python3
"""
Prints markdown tables built from results/*.txt (output of twist), so that the tables are exactly the
program output.  The only outside file read is the replica's REPORT.md (numbers to compare with).

usage: mkreport.py            (run in this folder; writes to stdout only)
"""
import re, os, sys, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
REPLICA = os.path.join(HERE, "..", "..", "..", "tablebase", "replica", "REPORT.md")
GEOMS = ["plane", "cyl", "torus", "mobius", "klein", "rp2"]
NEW = ["mobius", "klein", "rp2"]
MAIN_MATS = ["KQK", "KRK", "KBNK", "KBBK", "KNNK", "KQRK", "KRRK", "KQQK"]
LABEL = {"plane": "plane", "cyl": "cylinder", "torus": "torus", "mobius": "Möbius", "klein": "Klein", "rp2": "RP²"}


def parse_results(path):
    out, pv = {}, {}
    if not os.path.exists(path):
        return out, pv
    for line in open(path):
        if line.startswith("RESULT\t"):
            d = {}
            for kv in line.rstrip("\n").split("\t")[1:]:
                k, v = kv.split("=", 1)
                d[k] = v
            out[d["mat"]] = d
        elif line.startswith("PV\t"):
            p = line.rstrip("\n").split("\t")
            pv[p[2]] = (p[3], p[4].strip())
    return out, pv


def num(x):
    return int(x)


def fmt(n):
    return "{:,}".format(int(n))


def pct(d):
    return "%.4f%%" % float(d["pct"])


def load(ray=0):
    R, P = {}, {}
    for g in GEOMS:
        name = "%s.txt" % g if ray == 0 else "%s_ray%d.txt" % (g, ray)
        R[g], P[g] = parse_results(os.path.join(HERE, "results", name))
    return R, P


def replica_numbers():
    rows = {}
    for line in open(REPLICA):
        if not line.startswith("|"):
            continue
        c = [x.strip().replace("**", "") for x in line.strip().strip("|").split("|")]
        if len(c) != 7 or c[0] not in ("plane", "cylinder", "torus"):
            continue
        if not re.match(r"^[\d,]+$", c[2]):
            continue
        dt = 0 if c[5] in ("none", "0") else int(c[5])
        rows[(c[0], c[1])] = (int(c[2].replace(",", "")), int(c[3].replace(",", "")), dt)
    return rows


def validation(R):
    rep = replica_numbers()
    name = {"plane": "plane", "cyl": "cylinder", "torus": "torus"}
    mats = [("KQK", "KQK"), ("KRK", "KRK"), ("KBNK", "KBNK"), ("KBBK", "KBBK"), ("KBBK", "KBBK, opposite colours"),
            ("KBBK", "KBBK, same colour"), ("KNNK", "KNNK"), ("KRBK", "KRBK"), ("KRRK", "KRRK"), ("KQRK", "KQRK")]
    L = ["| Board | Material | Legal | Won | Max DTM | Same as replica |", "|---|---|---|---|---|---|"]
    allok = True
    for g in ("plane", "cyl", "torus"):
        for m, rm in mats:
            d = R[g].get(m)
            if d is None:
                continue
            if rm.endswith("opposite colours"):
                mine = (num(d["opp_legal"]), num(d["opp_won"]), num(d["maxdtm"]) if num(d["opp_won"]) else 0)
            elif rm.endswith("same colour"):
                mine = (num(d["same_legal"]), num(d["same_won"]), num(d["maxdtm"]) if num(d["same_won"]) else 0)
            else:
                mine = (num(d["legal"]), num(d["won"]), num(d["maxdtm"]))
            ref = rep.get((name[g], rm))
            ok = ref == mine
            allok &= ok
            L.append("| %s | %s | %s | %s | %s | %s |" % (name[g], rm, fmt(mine[0]), fmt(mine[1]), mine[2] if mine[1] else "none",
                                                          "yes" if ok else "**NO** (replica %s)" % (ref,)))
    return "\n".join(L), allok


def verdict(d):
    p = float(d["pct"])
    if num(d["won"]) == num(d["legal"]):
        return "win"
    if p >= 99.0:
        return "win*"
    if p < 1.0:
        return "draw"
    return "partial"


def main_table(R):
    L = ["| Board | Material | Legal | Won | Won % | Longest mate (moves) | Forced win from every legal position? | A longest-mate position |",
         "|---|---|---|---|---|---|---|---|"]
    for g in NEW:
        for m in MAIN_MATS:
            d = R[g][m]
            allw = num(d["won"]) == num(d["legal"])
            L.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
                LABEL[g], m, fmt(d["legal"]), fmt(d["won"]), pct(d), d["maxdtm"] if num(d["won"]) else "none",
                "**yes**" if allw else "no (%s not won)" % fmt(num(d["legal"]) - num(d["won"])), d["ex"]))
    return "\n".join(L)


def matrix(R):
    L = ["| Material | " + " | ".join(LABEL[g] for g in GEOMS) + " |", "|---|" + "---|" * len(GEOMS)]
    for m in MAIN_MATS + ["KRBK", "KBK", "KNK"]:
        cells = []
        for g in GEOMS:
            d = R[g][m]
            v = verdict(d)
            mx = d["maxdtm"] if num(d["won"]) else "0"
            cells.append("%s, %s, %s" % (v, ("%.4f%%" % float(d["pct"])).rstrip("0").rstrip("."), mx))
        L.append("| %s | %s |" % (m, " | ".join(cells)))
    return "\n".join(L)


def exceptions(R):
    L = ["| Board | Material | Not won | White loses a man, is stalemated or has no move at once | White has a move that avoids both, still cannot win |",
         "|---|---|---|---|---|"]
    for g in GEOMS:
        for m in MAIN_MATS + ["KRBK"]:
            d = R[g][m]
            nw = num(d["nonwon"])
            if nw == 0:
                continue
            imm = num(d["nonwon_imm"])
            if nw == num(d["legal"]) or float(d["pct"]) < 1.0:
                continue
            L.append("| %s | %s | %s | %s | %s |" % (LABEL[g], m, fmt(nw), fmt(imm), fmt(nw - imm)))
    return "\n".join(L)


def colours(R):
    L = ["| Board | Chessboard 2-colouring of the squares exists | Bishop orbits (squares) | Diagonal steps that change (f+r) parity | Knight graph bipartite |",
         "|---|---|---|---|---|"]
    for g in GEOMS:
        txt = open(os.path.join(HERE, "results", "%s.txt" % g)).read()
        two = "NOT 2-colourable" not in re.search(r"orthogonal-step graph:.*", txt).group(0)
        orb = re.search(r"bishop \(diagonal-step\) orbits: (\d+), sizes: ([\d ]+)", txt)
        fl = re.search(r"change nominal \(f\+r\) parity: (\d+) of (\d+)", txt)
        kn = "NOT bipartite" not in re.search(r"knight orbits:.*", txt).group(0)
        L.append("| %s | %s | %s | %s of %s | %s |" % (LABEL[g], "yes" if two else "**no** (odd cycles)", "%s (%s)" % (orb.group(1), orb.group(2).strip().replace(" ", " + ")),
                                                      fl.group(1), fl.group(2), "yes" if kn else "**no**"))
    return "\n".join(L)


def bbparity(R):
    L = ["| Board | KBBK legal | Won | Bishops on same nominal parity: legal | won | Opposite parity: legal | won |", "|---|---|---|---|---|---|---|"]
    for g in GEOMS:
        d = R[g]["KBBK"]
        L.append("| %s | %s | %s (%s) | %s | %s | %s | %s |" % (LABEL[g], fmt(d["legal"]), fmt(d["won"]), pct(d), fmt(d["same_legal"]),
                                                              fmt(d["same_won"]), fmt(d["opp_legal"]), fmt(d["opp_won"])))
    return "\n".join(L)


def sensitivity():
    R0, _ = load(0)
    R1, _ = load(1)
    R2, _ = load(2)
    mats = ["KQK", "KBNK", "KBBK", "KQRK", "KQQK", "KRBK", "KRK", "KRRK", "KNNK"]
    L = ["| Board | Material | Geodesic rays (used in this report): won %, longest | Variant 1: won %, longest | Variant 2: won %, longest |", "|---|---|---|---|---|"]
    for g in NEW:
        for m in mats:
            cells = []
            for R in (R0, R1, R2):
                d = R[g].get(m)
                if d is None:
                    cells.append("n/a")
                else:
                    cells.append("%s, %s" % (("%.4f" % float(d["pct"])).rstrip("0").rstrip("."), d["maxdtm"] if num(d["won"]) else "-"))
            L.append("| %s | %s | %s |" % (LABEL[g], m, " | ".join(cells)))
    return "\n".join(L)


def lines(P):
    out = []
    for g in NEW:
        for m in MAIN_MATS:
            if m not in P[g]:
                out.append("%-6s %s   (no win)" % (g, m))
                continue
            ex, mv = P[g][m]
            head = "%-6s %-5s %-18s " % (g, m, ex)
            wrapped = textwrap.wrap(mv, 100)
            out.append(head + wrapped[0])
            for w in wrapped[1:]:
                out.append(" " * len(head) + w)
    return "\n".join(out)


def main():
    """Print the tables (markdown) to stdout; nothing is written to disk."""
    R, P = load(0)
    val, ok = validation(R)
    sections = [("VALIDATION (replica comparison, all equal: %s)" % ok, val), ("MAIN", main_table(R)), ("MATRIX", matrix(R)),
                ("EXCEPTIONS", exceptions(R)), ("COLOURS", colours(R)), ("BBPARITY", bbparity(R)),
                ("SENSITIVITY", sensitivity()), ("LINES", lines(P))]
    for title, body in sections:
        print("=== %s ===" % title)
        print(body)
        print()


if __name__ == "__main__":
    main()

"""Compare replica results with egt_prototype.c output, number by number.

Run ./run_all.sh first, and save the prototype's output for each board and
material as prototype_results/<board>_<men>.txt. Prints one row per table and
exits non-zero if any number differs.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
BOARDS = ["plane", "cyl", "torus"]
MEN = ["Q", "R", "BB", "BN", "NN", "RB", "RR", "QR"]


def replica_numbers(board, men):
    text = (HERE / "results" / f"{board}_{men}.txt").read_text()
    out = {}
    for label in ["all", "opp-col"]:
        w = re.search(rf"K{men}K {label}\s+wtm legal\s+(\d+) won\s+(\d+) \(\s*[\d.]+%\) maxDTM\s+(\d+)", text)
        if not w:
            continue
        m = re.search(rf"K{men}K {label}\s+btm mates (\d+) stalemates (\d+)", text)
        key = "" if label == "all" else "opp_"
        out[key + "legal"], out[key + "won"] = int(w[1]), int(w[2])
        if label == "all":
            out["maxDTM"] = int(w[3])
            out["mates"], out["stalemates"] = int(m[1]), int(m[2])
    out["checks"] = "FAILED" not in text and text.count("passed") >= 1
    return out


def prototype_numbers(board, men):
    text = (HERE / "prototype_results" / f"{board}_{men}.txt").read_text()
    m = re.search(
        rf"K{men}vK: legal wtm=(\d+) won=(\d+) \([\d.]+%\) maxDTM=(\d+) \| btm mates=(\d+) stalemates=(\d+)",
        text,
    )
    out = dict(zip(["legal", "won", "maxDTM", "mates", "stalemates"], map(int, m.groups())))
    o = re.search(r"opposite-coloured bishops: legal wtm=(\d+) won=(\d+)", text)
    if o:
        out["opp_legal"], out["opp_won"] = int(o[1]), int(o[2])
    return out


def main():
    bad = 0
    for board in BOARDS:
        for men in MEN:
            r, p = replica_numbers(board, men), prototype_numbers(board, men)
            keys = [k for k in p if k in r]
            diff = [k for k in keys if r[k] != p[k]]
            bad += bool(diff) or not r["checks"]
            status = "agree" if not diff else "DIFFER " + ", ".join(f"{k}: replica {r[k]} vs prototype {p[k]}" for k in diff)
            pct = 100.0 * r["won"] / r["legal"]
            print(f"{board:6} K{men}K  {len(keys)} numbers  won {pct:8.4f}%  maxDTM {r['maxDTM']:2}  "
                  f"checks {'ok' if r['checks'] else 'FAILED'}  {status}")
    print("ALL AGREE" if not bad else f"{bad} tables differ")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

"""Score theory/LOOPY.md section 6 predictions against kpsolve results.

Inputs: kings/positions/theory_predictions.json (id, board, position, predicted,
naive) and kings/results/theory_predictions_raw.txt (kpsolve --moves output).
Run from the project root:  python3 kings/predictions.py
Writes kings/results/PREDICTIONS.md.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    preds = json.load(open(f"{ROOT}/kings/positions/theory_predictions.json"))
    got = {}
    board = None
    for line in open(f"{ROOT}/kings/results/theory_predictions_raw.txt"):
        if line.startswith("== "):
            board = line[3:].strip().replace("_", ":")
            continue
        if "|" not in line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        got[(board, parts[0])] = parts[1].split()
    # cap-2 reruns (7x6 cylinder) resolve positions whose cap-1 bounds differed
    cap2 = f"{ROOT}/kings/results/theory_P4_cap2.txt"
    if os.path.exists(cap2):
        for line in open(cap2):
            if "|" in line:
                parts = [p.strip() for p in line.split("|")]
                a, b = parts[1].split()
                if a == b:
                    got[("cyl:7x6", parts[0])] = [a, b]
    out = ["# Theory predictions (LOOPY.md §6) against kpsolve", "",
           "Result pairs are (White to move, Black to move), from White's point of view. "
           "kpsolve: `--cap 1 --promote QRBN --ep on`, and `--cap 2` for the three P4 rows whose cap-1 bounds "
           "differed; \"bounds\" means the two cap bounds differ.", "",
           "| # | Board | Position | Predicted | Naive convention | kpsolve | Prediction holds |",
           "|---|---|---|---|---|---|---|"]
    holds = total = 0
    for pid, board, pos, pred, naive in preds:
        w, b = got.get((board, f"{pos} w -")), got.get((board, f"{pos} b -"))
        if not w or not b:
            res, ok = "not run", "—"
        else:
            exact = w[0] == w[1] and b[0] == b[1]
            res = f"{w[0]}{b[0]}" if exact else f"bounds {w[0]}{b[0]}/{w[1]}{b[1]}"
            if exact:
                total += 1
                ok = "yes" if res == pred else "**NO**"
                holds += res == pred
            else:
                ok = "undetermined"
        out.append(f"| {pid} | {board} | `{pos}` | {pred} | {naive} | {res} | {ok} |")
    out += ["", f"{holds} of {total} exactly determined predictions hold."]
    with open(f"{ROOT}/kings/results/PREDICTIONS.md", "w") as fh:
        fh.write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()

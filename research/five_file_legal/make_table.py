"""Turn results.json (from run_t32_c.py) into the 21-row table of REPORT.md (Markdown on stdout).

PYTHONPATH=. .venv/bin/python -I research/five_file_legal/make_table.py > research/five_file_legal/table.md
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def verdict(entry):
    st = entry["status"]
    if st == "not run":
        return "not run"
    if st == "found":
        return "history" if entry.get("replay") else "history (replay FAILED)"
    if st == "exhausted":
        return "IMPOSSIBLE"
    if st == "cap":
        return "UNDECIDED (node cap)"
    if st == "timeout":
        return "UNDECIDED (time limit)"
    return "UNDECIDED (" + st + ")"


def main():
    rows = json.load(open(os.environ.get("T32_RESULTS", os.path.join(HERE, "results.json"))))
    print("| # | position | captures needed (W / B) | S0: pawn-only history from the start | "
          "S1: with trebuchet pawns | legal beside T | notes |")
    print("|---|---|---|---|---|---|---|")
    for r in rows:
        caps = f"{r['captures_W_exact']} / {r['captures_B_exact']} (file-shift bound {r['LB_W_fileshift']} / {r['LB_B_fileshift']})"
        s0 = verdict(r.get("S0", {"status": "not run"}))
        if r.get("S0", {}).get("status") == "found":
            s0 += ": " + " ".join(r["S0"]["history"])
        s1 = verdict(r.get("S1", {"status": "not run"}))
        legal = "yes" if r["legal_beside_T"] else "no"
        notes = []
        for c in r["checks"]:
            notes.append(c)
        for c in r["king_capture_conflicts"]:
            notes.append(c)
        if not notes:
            notes.append("no conflict")
        print(f"| {r['idx']} | {r['position']} | {caps} | {s0} | {s1} | {legal} | {'; '.join(notes)} |")


if __name__ == "__main__":
    main()

"""K50 item 3: the known groups on eight files, bare (no context): files left for the components, the local
certificate per sortie (least T of (L1_P), whether (L3_F) holds), and the verdict with and without --ctx.
Run from the project root: python3 kings/delegate/out/K50/scripts/table_groups.py"""
import os
import sys

sys.path.insert(0, os.getcwd())
from kings.embed_check import Board, Checker  # noqa: E402

GROUPS = [
    ("Fig (a) trebuchet", "cyl:8x8", "Kh5 Pa4 kb4 pa5", None),
    ("Fig (b) trebuchet T", "flat:8x8", "Kf5 Pg4 kh4 pg5", None),
    ("Z_T", "cyl:8x6", "Ka4 Pb3 kc3 pb4", None),
    ("K29 class 1", "cyl:8x6", "Kb3 Pa2 Pc2 kb1 pa3 pc3", "a,b,c"),
    ("K29 class 2", "cyl:8x6", "Kb1 Pa2 Pb3 ka3 pb2 pc5", None),
    ("K29 class 3", "cyl:8x6", "Kb3 Pa2 Pa4 ka5 pa3 pb4", "a,b,c"),
    ("K29 class 4", "cyl:8x6", "Kb3 Pc2 Pa4 ka5 pc3 pb4", "a,b,c"),
    ("Fig (c) 7.2 group", "cyl:8x8", "Ke6 Pd7 kd8 pe7", None),
]


def main():
    for name, board, grp, fz in GROUPS:
        W, H = map(int, board.split(":")[1].split("x"))
        for stm in "wb":
            for ctx in (False, True):
                r = Checker(Board(W, H, board.startswith("cyl")), 8, 300000, ctx, 60).run(f"{grp} {stm} -", fz)
                s = r["separation"]
                print(f"{name} | {board} | {grp} {stm} | ctx={ctx} | F_Z={''.join(s.get('F_Z', []))} "
                      f"buffer={''.join(s.get('buffer', []))} files_left={s.get('files_left_for_components')} | "
                      f"{r['verdict']} | D={r.get('D_result', {}).get('winner')}")
                if not ctx and stm == "w":
                    for side in ("white", "black"):
                        for q in r["V3"][side]["sorties"] if isinstance(r["V3"].get(side), dict) else []:
                            t = q.get("T", q.get("L1_P", {}).get("T"))
                            print(f"    {q['move']}: {q['verdict']}, T={t}, "
                                  f"{'(L3_F) holds' if 'T' in q and q.get('T') else q.get('why', '')}")
                if not ctx and stm == "w" and "witness" in s:
                    print("    separation:", s["witness"])


if __name__ == "__main__":
    main()

"""K24: (L1), (L1_P) and (L3_F) of Definition 2.6 for the king-group sorties of LOOPY 5.1, 5.2 and the 6-rank analogue.
Run from the K24 directory with the project venv:  PYTHONPATH=scripts .venv/bin/python scripts/lg_run.py"""
import sys, json
sys.path.insert(0, "scripts")
import lg

def files(board, letters): return {ord(c) - 97 for c in letters}

CASES = [
 # label, board, root, s_white, FZ letters, reply square
 ("5.1 White sorties (P6)",        (8, 8, True),  "Kh5 Pa4 kb4 pa5", True,  "hab", "a4"),
 ("5.1 Black sorties (P6, dual)",  (8, 8, True),  "Kh5 Pa4 kb4 pa5", False, "hab", "a5"),
 ("7.2 Black Kc7 (P7), cyl",       (8, 8, True),  "Ke6 Pd7 kd8 pe7", False, "de",  "e7"),
 ("7.2 Black Kc7 (P7), flat",      (8, 8, False), "Ke6 Pd7 kd8 pe7", False, "de",  "e7"),
 ("7.2 White sorties (P7), cyl",   (8, 8, True),  "Ke6 Pd7 kd8 pe7", True,  "de",  "d7"),
 ("7.2 White sorties (P7), flat",  (8, 8, False), "Ke6 Pd7 kd8 pe7", True,  "de",  "d7"),
 ("Z_72 6-rank, Black sortie (P5)",(7, 6, True),  "Kc4 Pb5 kb6 pc5", False, "bc",  "c5"),
 ("Z_72 6-rank, White sorties (P5)",(7, 6, True), "Kc4 Pb5 kb6 pc5", True,  "bc",  "b5"),
]
out = []
for label, (W, H, wrap), root, sw, fz, rsq in CASES:
    board = lg.B(W, H, wrap)
    print(f"=== {label}: {root}, s = {'White' if sw else 'Black'}, F_Z = {fz}, reply = king captures on {rsq}")
    for qc in (True, False):
        res = lg.build_qz(board, root, sw, files(board, fz), qc, rsq)
        for txt, T, info in res:
            l3 = info.get("l3f") if isinstance(info, dict) else None
            print(f"   {'(L1)  ' if qc else '(L1_P)'} {txt:22s} T_min = {T}   " + (f"(L3_F) ok={l3[0]}; stalemates of s on winning lines: {l3[3]} (s-nodes {l3[1]})" if l3 else (str(info) if T is None else "")))
            out.append({"case": label, "queen_clause": qc, "move": txt, "Tmin": T, "l3f_ok": (l3[0] if l3 else None), "stalemates": (l3[3] if l3 else None)})
json.dump(out, open("lg_results.json", "w"), indent=1)

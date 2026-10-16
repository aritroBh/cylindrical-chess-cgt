"""Is the 7.3 king group a zugzwang if the kings stood as in 7.2 reflected (d->f, e->g)?
Run: PYTHONPATH=. .venv/bin/python verify/diagrams/king73_alt.py"""
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("rerun", pathlib.Path(__file__).with_name("rerun.py"))
rr = importlib.util.module_from_spec(spec); spec.loader.exec_module(rr)
for label, fen in [("7.3 as drawn  (Kg8,Pf7 / Kf6,Pg7)", "6K1/5Pp1/5k2/8/8/8/8/8"),
                   ("7.3 alt: WKg6, BKf8 (7.2 reflected)", "5k2/5Pp1/6K1/8/8/8/8/8")]:
    pcs = rr.parse_fen(fen)
    print(label)
    for colour in ("W", "B"):
        for t, cap, new in rr.king_moves(pcs, colour):
            print(f"   {colour} K{rr.sqname(t)}: enemy king may then capture {rr.capturable(new, colour) or 'nothing'}")
    occ = set(pcs)
    for s, c in pcs.items():
        if c == "P" and (s[0], s[1] + 1) not in occ: print(f"   white pawn {rr.sqname(s)} can advance")
        if c == "p" and (s[0], s[1] - 1) not in occ: print(f"   black pawn {rr.sqname(s)} can advance")

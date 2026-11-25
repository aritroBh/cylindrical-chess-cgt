"""K63 referee: recount the investigator's context tables (logs/ctx_<tag>_table.txt) from their rows:
contexts, agreeing contexts, differing positions, direction of each difference (White's view: a difference
is in Black's favour if the P result is worse for White than the prediction), contexts with an illegal (X)
position, and contexts that touch file g (gh tables).  Reads only; no solver.
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K63/verify/src/recount.py
"""
import re
O = {"L": 0, "D": 1, "W": 2}
for tag in ("h22", "gh11", "de11", "gh22a"):
    n = ag = df = npos = blk = wht = xc = hon = hdf = 0
    for line in open(f"kings/delegate/out/K63/logs/ctx_{tag}_table.txt"):
        m = re.match(r"^ctx\d+\s+(.*?)\s+P ([WLDX ]+?)\s+kp_p ([WLDX ]+?)\s+pred ([WLDX ]+?)(\s+DIFFER.*)?$", line.rstrip())
        if not m: continue
        n += 1
        ctx = m.group(1); P = m.group(2).split(); K = m.group(3).split(); pr = m.group(4).split()
        assert P == K, line
        honly = all(t[1] == "h" for t in ctx.split()) if ctx != "empty" else True
        hon += honly
        if "X" in P: xc += 1
        d = [i for i in range(8) if P[i] != "X" and P[i] != pr[i]]
        if d:
            df += 1; npos += len(d); hdf += honly
            for i in d:
                if O[P[i]] < O[pr[i]]: blk += 1
                else: wht += 1
        else:
            ag += 1
    print(f"{tag:6s} contexts {n}  agree {ag}  differ {df}  differing positions {npos} (Black's favour {blk}, White's {wht})"
          f"  contexts with an illegal position {xc}  h-only contexts {hon} (differ {hdf})")

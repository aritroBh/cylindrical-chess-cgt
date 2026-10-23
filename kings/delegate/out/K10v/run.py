#!/usr/bin/env python3
import sys, os, json, random, itertools, subprocess, collections
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K10v")
import check

OUT = "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K10v"
KP = "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K10v/kp"

def pos_key(pos):
    return (tuple(sorted(pos["W"])), tuple(sorted(pos["B"])), pos["wk"], pos["bk"], pos.get("ep"))

def make_pos(W, H, ws, bs, wk, bk, ep=None):
    return {"W": frozenset(ws), "B": frozenset(bs), "wk": wk, "bk": bk, "ep": ep}

def kings_adjacent(W, wrap, a, b):
    if wrap:
        df = min(abs(a[0]-b[0]), W-abs(a[0]-b[0]))
    else:
        df = abs(a[0]-b[0])
    dr = abs(a[1]-b[1])
    return max(df, dr) <= 1

def in_check(W, H, wrap, pos, side):
    king = pos["wk"] if side == "W" else pos["bk"]
    enemy = "B" if side == "W" else "W"
    epawns = pos["B"] if side == "W" else pos["W"]
    for (f, r) in epawns:
        for df in (-1, 1):
            g = check.nb(W, wrap, f, df)
            rr = r + (1 if enemy == "W" else -1)
            if g is not None and (g, rr) == king:
                return True
    other = pos["bk"] if side == "W" else pos["wk"]
    if kings_adjacent(W, wrap, king, other):
        return True
    return False

def legal_pos(W, H, wrap, pos, stm):
    # side not to move not in check
    ntm = "B" if stm == "W" else "W"
    if in_check(W, H, wrap, pos, ntm):
        return False
    if kings_adjacent(W, wrap, pos["wk"], pos["bk"]):
        return False
    return True

def gen_fixed(W, H, files, ranks, maxk, n_random=None, seed=0, wk=None, bk=None):
    if wk is None: wk = (0, 1)
    if bk is None: bk = (0, H)
    squares = [(f, r) for f in files for r in ranks]
    out = []
    if n_random is None:
        subsets = []
        for k in range(maxk + 1):
            for combo in itertools.combinations(squares, k):
                subsets.append(frozenset(combo))
        for ws in subsets:
            for bs in subsets:
                if ws & bs:
                    continue
                pos = make_pos(W, H, ws, bs, wk, bk, None)
                if not legal_pos(W, H, True, pos, "W"):
                    continue
                out.append((pos, "W"))
                out.append((pos, "B"))
        return out
    random.seed(seed)
    seen = set()
    while len(out) < n_random * 2:
        nw = random.randint(0, maxk)
        nbp = random.randint(0, maxk)
        if nw + nbp > len(squares):
            continue
        ws = set(random.sample(squares, nw))
        rem = [s for s in squares if s not in ws]
        if nbp > len(rem):
            continue
        bs = set(random.sample(rem, nbp))
        pos = make_pos(W, H, ws, bs, wk, bk, None)
        if not legal_pos(W, H, True, pos, "W"):
            continue
        key = pos_key(pos)
        if key in seen:
            continue
        seen.add(key)
        stm = random.choice(["W", "B"])
        out.append((pos, stm))
        if len(out) >= n_random:
            break
    return out

def try_add_ep(W, H, wrap, ws, bs, stm, wk, bk):
    ws = set(ws); bs = set(bs)
    if stm == "W":
        cands = []
        for (f, r) in bs:
            if r != H - 3:
                continue
            origin = (f, H - 1)
            skipped = (f, H - 2)
            if origin in ws or origin in bs or origin in (wk, bk):
                continue
            if skipped in ws or skipped in bs or skipped in (wk, bk):
                continue
            for df in (-1, 1):
                g = check.nb(W, wrap, f, df)
                if g is not None and (g, H - 3) in ws:
                    cands.append((f, r))
        if not cands:
            return None
        f, r = random.choice(cands)
        return ((f, H - 2), (f, H - 3), "W")
    else:
        cands = []
        for (f, r) in ws:
            if r != 4:
                continue
            origin = (f, 2)
            skipped = (f, 3)
            if origin in ws or origin in bs or origin in (wk, bk):
                continue
            if skipped in ws or skipped in bs or skipped in (wk, bk):
                continue
            for df in (-1, 1):
                g = check.nb(W, wrap, f, df)
                if g is not None and (g, 4) in bs:
                    cands.append((f, r))
        if not cands:
            return None
        f, r = random.choice(cands)
        return ((f, 3), (f, 4), "B")

def gen_random_kings(W, H, n, seed):
    random.seed(seed)
    out = []
    seen = set()
    squares_all = [(f, r) for f in range(W) for r in range(2, H)]
    while len(out) < n:
        wk = (random.randrange(W), random.randint(1, H))
        bk = (random.randrange(W), random.randint(1, H))
        if kings_adjacent(W, True, wk, bk):
            continue
        avail = [s for s in squares_all if s not in (wk, bk)]
        nw = random.randint(0, 3)
        nbp = random.randint(0, 3)
        if nw + nbp > len(avail):
            continue
        ws = set(random.sample(avail, nw))
        rem = [s for s in avail if s not in ws]
        if nbp > len(rem):
            continue
        bs = set(random.sample(rem, nbp))
        stm = random.choice(["W", "B"])
        ep = None
        if random.random() < 0.35:
            ep = try_add_ep(W, H, True, ws, bs, stm, wk, bk)
        pos = make_pos(W, H, ws, bs, wk, bk, ep)
        if not legal_pos(W, H, True, pos, stm):
            continue
        key = pos_key(pos) + (stm,)
        if key in seen:
            continue
        seen.add(key)
        out.append((pos, stm))
    return out

def certify_drop(W, H, wrap, pos, beta, stm, drop):
    # certify with one hypothesis dropped
    # replicate check.certify but skip specified H
    omega = "B" if beta == "W" else "W"
    wk = pos["wk"]; bk = pos["bk"]
    mine = pos["W"] if beta == "W" else pos["B"]
    res = []
    for p in mine:
        ok = True
        if drop != "H1":
            if not check.H1(W, H, wrap, pos, beta, p):
                ok = False
        if ok and drop != "H2":
            if not check.H2(W, H, wrap, pos, beta):
                ok = False
        if ok and drop != "H3":
            if not check.H3(W, H, wrap, pos, omega):
                ok = False
        if ok and drop != "H4":
            if not check.H4(W, H, wrap, pos, beta, p):
                ok = False
        if not ok:
            continue
        # H5 (unless drop H5)
        pos2 = {"W": set(pos["W"]), "B": set(pos["B"]), "wk": wk, "bk": bk, "ep": pos.get("ep")}
        if beta == "W":
            pos2["W"].discard(p)
        else:
            pos2["B"].discard(p)
        pos2["W"] = frozenset(pos2["W"]); pos2["B"] = frozenset(pos2["B"])
        if omega == "W":
            omega_pawns = pos2["W"]; beta_pawns = pos2["B"]
        else:
            omega_pawns = pos2["B"]; beta_pawns = pos2["W"]
        d = check.d_beta(p[1], beta, H)
        e = d if stm == omega else d - 1
        allow_ep = (stm == omega and pos.get("ep") is not None and pos["ep"][2] == omega)
        mu = check.mu_omega_val(W, H, wrap, omega, beta, omega_pawns, beta_pawns, wk, bk, allow_ep, pos.get("ep"))
        h5_ok = mu >= e + 1
        if drop != "H5":
            if not h5_ok:
                continue
        # if dropped H5, accept regardless
        res.append(p)
    return res

def run_case(case):
    if case == "a":
        positions = gen_fixed(6, 6, [2,3,4], [2,3,4,5], 3, None, 0)
        W,H = 6,6
    elif case == "b":
        positions = gen_fixed(7, 6, [2,3,4,5], [2,3,4,5], 2, None, 0)
        W,H = 7,6
    elif case == "b_rand":
        positions = gen_fixed(7, 6, [2,3,4,5], [2,3,4,5], 3, 20000, 1)
        W,H = 7,6
    elif case == "c":
        positions = gen_random_kings(8, 6, 10000, 2)
        W,H = 8,6
    else:
        raise SystemExit("unknown case")
    wrap = True

    # certify full
    instances = []  # list of dict
    cert_pos_stm = set()  # keys with any full certified instance
    for (pos, stm) in positions:
        for beta in ("W", "B"):
            ps = check.certify(W, H, wrap, pos, beta, stm)
            for p in ps:
                instances.append({"pos": pos, "stm": stm, "beta": beta, "p": p})
                cert_pos_stm.add(pos_key(pos) + (stm,))
    # map pos_stm key -> index in input list
    unique_list = list(cert_pos_stm)
    # build input lines
    key_to_line = {}
    input_lines = []
    for key in unique_list:
        # find a pos/stm from positions
        pass
    # We need reconstruct pos/stm from key; store mapping
    key_to_posstm = {}
    for (pos, stm) in positions:
        k = pos_key(pos) + (stm,)
        if k in cert_pos_stm:
            key_to_posstm[k] = (pos, stm)
    for k in unique_list:
        pos, stm = key_to_posstm[k]
        input_lines.append(check.pos_to_str(W, H, wrap, pos, stm))
    in_path = os.path.join(OUT, f"in_{case}.txt")
    out_path = os.path.join(OUT, f"out_{case}.txt")
    with open(in_path, "w") as f:
        f.write("\n".join(input_lines) + ("\n" if input_lines else ""))
    # run kpsolve
    cmd = ["nice", "-n", "10", KP, f"--board", f"cyl:{W}x{H}", "--frozen", "--cap", "1", "--threads", "2"]
    with open(in_path) as fin, open(out_path, "w") as fout:
        subprocess.run(cmd, stdin=fin, stdout=fout, stderr=subprocess.DEVNULL, check=True)
    # parse output
    results = {}  # key -> (A,B)
    with open(out_path) as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    # output lines correspond to input lines in order, but may include? no.
    for idx, ln in enumerate(lines):
        if " | " not in ln:
            continue
        left, right = ln.split(" | ", 1)
        parts = right.split()
        A = parts[0] if len(parts) > 0 else "?"
        B = parts[1] if len(parts) > 1 else "?"
        results[idx] = (A, B)
    # map key -> result by index
    key_result = {}
    for idx, k in enumerate(unique_list):
        if idx < len(results):
            key_result[k] = results[idx]

    # count violations
    violations = []
    for inst in instances:
        pos = inst["pos"]; stm = inst["stm"]; beta = inst["beta"]
        k = pos_key(pos) + (stm,)
        A, B = key_result.get(k, ("?", "?"))
        expected = "W" if beta == "W" else "L"
        ok = (A == expected and B == expected)
        if not ok:
            violations.append({
                "pos": check.pos_to_str(W, H, wrap, pos, stm),
                "stm": stm, "beta": beta, "p": list(inst["p"]),
                "result": f"{A} {B}", "expected": expected
            })
            if len(violations) >= 10:
                pass
    # targeted stats
    h4_bound = 0
    ep_instances = 0
    beta_to_move_omega_adj = 0
    for inst in instances:
        pos = inst["pos"]; beta = inst["beta"]; p = inst["p"]; stm = inst["stm"]
        # H4 equality
        pr = check.rho_beta(p[1], beta, H)
        adj = {check.nb(W, wrap, p[0], -1), check.nb(W, wrap, p[0], 1)}
        adj.discard(None)
        mine = pos["W"] if beta == "W" else pos["B"]
        eq = False
        for q in mine:
            if q == p: continue
            if q[0] in adj and check.rho_beta(q[1], beta, H) == pr + 1:
                eq = True
        if eq:
            h4_bound += 1
        if pos.get("ep") is not None:
            ep_instances += 1
        # beta to move with omega pawn at rho+1 beside p
        if stm == beta:
            omega_color = "B" if beta == "W" else "W"
            omega_pawns = pos["B"] if omega_color == "B" else pos["W"]
            for q in omega_pawns:
                if q[0] in adj and check.rho_beta(q[1], beta, H) == pr + 1:
                    beta_to_move_omega_adj += 1
                    break

    # controls: drop each hypothesis
    control_counts = {}
    for drop in ("H2", "H3", "H4", "H5"):
        drop_instances = 0
        drop_violations = 0
        drop_viol_examples = []
        for (pos, stm) in positions:
            for beta in ("W", "B"):
                ps = certify_drop(W, H, wrap, pos, beta, stm, drop)
                for p in ps:
                    drop_instances += 1
                    k = pos_key(pos) + (stm,)
                    A, B = key_result.get(k, ("?", "?"))
                    expected = "W" if beta == "W" else "L"
                    if not (A == expected and B == expected):
                        drop_violations += 1
                        if len(drop_viol_examples) < 5:
                            drop_viol_examples.append(check.pos_to_str(W, H, wrap, pos, stm))
        control_counts[drop] = {"instances": drop_instances, "violations": drop_violations}

    summary = {
        "case": case,
        "W": W, "H": H,
        "n_positions": len(positions),
        "n_certified_instances": len(instances),
        "n_certified_pos_stm": len(unique_list),
        "n_violations": len(violations),
        "violations_examples": violations[:10],
        "targeted": {
            "H4_equality_instances": h4_bound,
            "ep_instances": ep_instances,
            "beta_to_move_omega_adjacent_rho_plus1": beta_to_move_omega_adj,
        },
        "controls_drop": control_counts,
    }
    with open(os.path.join(OUT, f"summary_{case}.json"), "w") as f:
        json.dump(summary, f, indent=2)
    # delete bulk
    try:
        os.remove(in_path); os.remove(out_path)
    except OSError:
        pass
    print(json.dumps({k: summary[k] for k in ("case","n_positions","n_certified_instances","n_certified_pos_stm","n_violations")}, indent=2))
    print("controls:", {k: v["violations"] for k,v in control_counts.items()})

if __name__ == "__main__":
    case = sys.argv[1]
    run_case(case)

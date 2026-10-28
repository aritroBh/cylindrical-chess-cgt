"""K21 experiments.  usage: run_tests.py <exp> <N> <seed> [B]"""
import sys, json, random, itertools, time, os
RICH = int(os.environ.get("KRICH", "0"))
from dsum import *

def pick_comp(rng, kind):
    """kind: 'short' | 'loopy' | 'named' | 'stopper' | 'quiet_any'"""
    if kind == "named":
        return NAMED[rng.choice(list(NAMED))]()
    if kind == "short":
        return rand_short(rng, nmax=5 if RICH else 4, pplus=(0.2, 0.12), pminus=(0.12, 0.2), nopt=3 if RICH else 2)
    if kind == "loopy":
        while True:
            c = rand_loopy(rng, nmax=3, pplus=(0.15, 0.1), pminus=(0.1, 0.15), nopt=2, terms=True)
            return c
    if kind == "stopper":   # terminal-free loopy stopper, or with terminals
        while True:
            c = rand_loopy(rng, nmax=5 if RICH else 4, nopt=3 if RICH else 2, terms=False)
            if c.is_stopper() and not c.is_short():
                return c
    if kind == "quiet_any":
        return rand_loopy(rng, nmax=3, nopt=2, terms=False)
    raise ValueError(kind)

def rand_instance(rng):
    k = rng.choice([2, 2, 3])
    comps = []
    for _ in range(k):
        kind = rng.choice(["short", "short", "loopy", "named", "stopper"])
        comps.append(pick_comp(rng, kind))
    return comps

def exp_bridge(N, seed, B):
    """E1 + E2: dominance => D = CGT (Thm A); reserve criterion => dominance (Thm B); counts."""
    rng = random.Random(seed)
    tab = {}
    bad = []
    t0 = time.time()
    for it in range(N):
        comps = rand_instance(rng)
        d = d_results(comps)
        c = cgt_results(comps, B)
        eq = all(d[k] == c[k] for k in d)
        eq_root = d[(tuple(x.root for x in comps), 0)] == c[(tuple(x.root for x in comps), 0)] and d[(tuple(x.root for x in comps), 1)] == c[(tuple(x.root for x in comps), 1)]
        dom, _ = dominance(comps, B)
        crit, _ = reserve_criterion(comps, B)
        has_ev = any(x.events() for x in comps)
        has_loopy = any(not x.is_short() for x in comps)
        key = ("ev" if has_ev else "noev", "loopy" if has_loopy else "short", "dom" if dom else "nodom", "crit" if crit else "nocrit", "eq" if eq else "NEQ")
        tab[key] = tab.get(key, 0) + 1
        if (dom and not eq) or (crit and not dom):
            bad.append([comp_str(x) for x in comps])
    out = {"exp": "bridge", "N": N, "seed": seed, "B": B, "secs": round(time.time() - t0, 1),
           "table": {" ".join(k): v for k, v in sorted(tab.items())}, "violations": bad[:5], "n_violations": len(bad)}
    return out

if __name__ == "__main__":
    exp, N, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    B = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    if exp == "bridge":
        print(json.dumps(exp_bridge(N, seed, B), indent=1))


# ------------------------------------------------------------------------------------------------
def rand_K(rng, loopy=False):
    k = rng.choice([1, 2])
    return [pick_comp(rng, "loopy" if (loopy and rng.random() < 0.5) else "short") for _ in range(k)]

def exp_sandwich(N, seed):
    """E3: W(K+off) subset W(K+S) subset W(K+on); L(K+on) subset L(K+S) subset L(K+off); W(off)=W(dud), L(on)=L(dud)"""
    rng = random.Random(seed)
    cnt = {"states": 0, "inst": 0, "viol": 0, "viol_suicide_S": 0, "states_suicide_S": 0, "dud_eq_viol": 0, "nontrivial_off_W_strict": 0, "nontrivial_S_between": 0}
    ex = []
    for it in range(N):
        K = rand_K(rng, loopy=True)
        skind = rng.choice(["named", "short_quiet", "stopper", "quiet_any", "quiet_any", "suicide", "suicide"])
        if skind == "suicide":
            S = rand_loopy(rng, nmax=3, pplus=(0.0, 0.25), pminus=(0.25, 0.0), nopt=2, terms=True)
        elif skind == "short_quiet":
            S = rand_short(rng, nmax=4, terms=False)
        else:
            S = pick_comp(rng, skind)
        kts = product_nodes(K)
        r_off = solve(K + [mk_off()], [kt + (0,) for kt in kts])
        r_on = solve(K + [mk_on()], [kt + (0,) for kt in kts])
        r_dud = solve(K + [mk_dud()], [kt + (0,) for kt in kts])
        r_S = solve(K + [S], [kt + (s,) for kt in kts for s in S.reach()])
        cnt["inst"] += 1
        for kt in kts:
            for m in (0, 1):
                off, on, dud = r_off[(kt + (0,), m)], r_on[(kt + (0,), m)], r_dud[(kt + (0,), m)]
                if (off == "W") != (dud == "W") or (on == "L") != (dud == "L"):
                    cnt["dud_eq_viol"] += 1
                for s in S.reach():
                    v = r_S[(kt + (s,), m)]
                    cnt["states"] += 1
                    if skind == "suicide": cnt["states_suicide_S"] += 1
                    ok = True
                    if off == "W" and v != "W": ok = False
                    if v == "W" and on != "W": ok = False
                    if on == "L" and v != "L": ok = False
                    if v == "L" and off != "L": ok = False
                    if not ok:
                        cnt["viol"] += 1
                        if skind == "suicide": cnt["viol_suicide_S"] += 1
                        if len(ex) < 3: ex.append([comp_str(c) for c in K] + [comp_str(S), m, s, off, on, dud, v])
                    if off == "W" and on == "W" and v == "W": pass
        # nontrivial: some state where result of S differs from both off and on
        for kt in kts:
            for m in (0, 1):
                off, on = r_off[(kt + (0,), m)], r_on[(kt + (0,), m)]
                if off != on:
                    for s in S.reach():
                        if r_S[(kt + (s,), m)] not in (off, on): cnt["nontrivial_S_between"] += 1
    return {"exp": "sandwich", "N": N, "seed": seed, **cnt, "examples": ex}

def exp_stopper(N, seed):
    """E4: stopper (with or without terminals) + short comps: no draws; non-stoppers: draws occur"""
    rng = random.Random(seed)
    out = {"stopper_states": 0, "stopper_draws": 0, "nonstopper_inst": 0, "nonstopper_inst_with_draw": 0,
           "nonstopper_states": 0, "nonstopper_draws": 0, "stopper_inst": 0}
    for it in range(N):
        K = rand_K(rng, loopy=False)
        if rng.random() < 0.5:
            S = pick_comp(rng, "stopper")
            if rng.random() < 0.4:   # add terminals to the stopper (random re-draw until stopper)
                for _ in range(20):
                    c = rand_loopy(rng, nmax=4, pplus=(0.15, 0.1), pminus=(0.1, 0.15), nopt=2, terms=True)
                    if c.is_stopper() and not c.is_short():
                        S = c; break
            assert S.is_stopper()
            r = solve(K + [S], [kt + (s,) for kt in product_nodes(K) for s in S.reach()])
            out["stopper_inst"] += 1
            out["stopper_states"] += len(r)
            out["stopper_draws"] += sum(1 for v in r.values() if v == "D")
        else:
            S = rand_loopy(rng, nmax=4, nopt=2, terms=bool(rng.random() < 0.5), pplus=(0.15, 0.1), pminus=(0.1, 0.15))
            if S.is_stopper():
                continue
            r = solve(K + [S], [kt + (s,) for kt in product_nodes(K) for s in S.reach()])
            out["nonstopper_inst"] += 1
            nd = sum(1 for v in r.values() if v == "D")
            out["nonstopper_states"] += len(r)
            out["nonstopper_draws"] += nd
            out["nonstopper_inst_with_draw"] += 1 if nd else 0
    return {"exp": "stopper", "N": N, "seed": seed, **out}

def exp_regime(N, seed, B=14):
    """E5: K short (1-2 comps) + terminal-free S.  Theorem E: P_L -> W, P_R -> L for every S (must hold).
    Conjecture C1: outside P_L u P_R, D-result = CGT outcome of K^B + S."""
    rng = random.Random(seed)
    stats = {}
    ex = []
    def bump(*k):
        stats[" ".join(map(str, k))] = stats.get(" ".join(map(str, k)), 0) + 1
    for it in range(N):
        K = rand_K(rng, loopy=False)
        r = rng.random()
        if r < 0.45:
            nm = rng.choice(list(NAMED)); S = NAMED[nm](); skind = nm
        elif r < 0.8:
            S = pick_comp(rng, "stopper"); skind = "stopper"
        elif r < 0.9:
            S = rand_short(rng, nmax=3, terms=False); skind = "short"
        else:
            S = pick_comp(rng, "quiet_any"); skind = "quiet_any" if not S.is_stopper() else "stopper"
        kts = product_nodes(K)
        sn = S.reach()
        evs = [c.events() for c in K]
        safe = not any(1 in evs[i] and -1 in evs[j] for i in range(len(K)) for j in range(len(K)) if i != j)
        r_off = solve(K + [mk_off()], [kt + (0,) for kt in kts])
        r_on = solve(K + [mk_on()], [kt + (0,) for kt in kts])
        r_D = solve(K + [S], [kt + (s,) for kt in kts for s in sn])
        crit = reserve_criterion(K + [S], B)[0]
        tS = translate(S, B)[0]
        tK = [translate(c, B)[0] for c in K]
        r_C = solve(tK + [S], [kt + (s,) for kt in kts for s in sn])
        for kt in kts:
            for m in (0, 1):
                PL = r_off[(kt + (0,), m)] == "W"
                PR = r_on[(kt + (0,), m)] == "L"
                assert not (PL and PR)
                for s in sn:
                    d = r_D[(kt + (s,), m)]
                    c = r_C[(kt + (s,), m)]
                    if PL or PR:
                        want = "W" if PL else "L"
                        bump("ALL", "decided", "thmE_ok" if d == want else "THME_VIOLATION"); bump(skind, "crit" if crit else "nocrit", "decided", "transl_eq" if c == d else "transl_NEQ")
                    else:
                        bump(skind, "crit" if crit else "nocrit", "T", "C1_ok" if c == d else "C1_FAIL")
                        if c != d and len(ex) < 8:
                            ex.append([[comp_str(x) for x in K], comp_str(S), skind, m, s, d, c])
    return {"exp": "regime", "N": N, "seed": seed, "B": B, "stats": dict(sorted(stats.items())), "C1_examples": ex}

def exp_subadd(N, seed, B=5):
    """E7: lam_B(y1+y2) <= lam_B(y1) + lam_B(y2) at the roots (Left wins y1^B + y2^B + C second)"""
    rng = random.Random(seed)
    Cmax = 2 * B + 3
    n = 0; viol = 0; finite = 0
    for it in range(N):
        kinds = ["short", "short", "loopy", "named", "stopper"]
        a, b = pick_comp(rng, rng.choice(kinds)), pick_comp(rng, rng.choice(kinds))
        la, ra = reserves(a, B, Cmax); lb, rb = reserves(b, B, Cmax)
        x, y = la[a.root], lb[b.root]
        if x is None or y is None:
            continue
        finite += 1
        ta, tb = translate(a, B)[0], translate(b, B)[0]
        C = x + y
        res = solve([ta, tb, mk_int(C)], [(a.root, b.root, C)])
        n += 1
        if res[((a.root, b.root, C), 1)] != "W":
            viol += 1
        # mirror
        x2, y2 = ra[a.root], rb[b.root]
        if x2 is not None and y2 is not None:
            C2 = x2 + y2
            res2 = solve([ta, tb, mk_negint(C2)], [(a.root, b.root, C2)])
            n += 1
            if res2[((a.root, b.root, C2), 0)] != "L":
                viol += 1
    return {"exp": "subadd", "N": N, "seed": seed, "B": B, "checked": n, "violations": viol}

def lam_rho_preds(K):
    """Theorem 3.4 predicates on a single short comp K (nodes reachable)."""
    from functools import lru_cache
    @lru_cache(None)
    def LamL(x):
        return any(o == PLUS or (o >= 0 and LamR(o)) for o in K.L[x])
    @lru_cache(None)
    def LamR(x):
        return LamL(x) and all(o == PLUS or (o >= 0 and LamL(o)) for o in K.R[x])
    @lru_cache(None)
    def RhoR(x):
        return any(o == MINUS or (o >= 0 and RhoL(o)) for o in K.R[x])
    @lru_cache(None)
    def RhoL(x):
        return RhoR(x) and all(o == MINUS or (o >= 0 and RhoR(o)) for o in K.L[x])
    return LamL, LamR, RhoL, RhoR

def exp_thm34(N, seed):
    rng = random.Random(seed)
    n = 0; viol = 0
    for it in range(N):
        K = pick_comp(rng, "short")
        LamL, LamR, RhoL, RhoR = lam_rho_preds(K)
        for nm, S in (("dud", mk_dud()), ("on", mk_on()), ("off", mk_off())):
            res = solve([K, S], [(x, 0) for x in K.reach()])
            for x in K.reach():
                for m in (0, 1):
                    lam = LamL(x) if m == 0 else LamR(x)
                    rho = RhoL(x) if m == 0 else RhoR(x)
                    if nm == "dud": want = "W" if lam else ("L" if rho else "D")
                    elif nm == "on": want = "L" if rho else "W"
                    else: want = "W" if lam else "L"
                    n += 1
                    if res[((x, 0), m)] != want: viol += 1
    return {"exp": "thm34", "N": N, "seed": seed, "checked": n, "violations": viol}

def exp_over(N, seed):
    """Prop 4.6: White wins G moving second => White wins G + over_D (either mover); plus: over translation correct for pairwise safe K"""
    rng = random.Random(seed)
    n = 0; viol = 0; ncase = 0
    for it in range(N):
        K = pick_comp(rng, "short")
        S = mk_over()
        res = solve([K, S], [(x, 0) for x in K.reach()])
        resK = solve([K], [(x,) for x in K.reach()])
        for x in K.reach():
            if resK[((x,), 1)] == "W":
                ncase += 1
                for m in (0, 1):
                    n += 1
                    if res[((x, 0), m)] != "W": viol += 1
    return {"exp": "over46", "N": N, "seed": seed, "cases_W_second": ncase, "checked": n, "violations": viol}

if __name__ == "__main__" and sys.argv[1] not in ("bridge", "thm111b", "pure", "onestopper"):
    exp, N, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    f = {"sandwich": exp_sandwich, "stopper": exp_stopper, "subadd": exp_subadd, "thm34": exp_thm34, "over46": exp_over}
    if exp == "regime":
        B = int(sys.argv[4]) if len(sys.argv) > 4 else 14
        print(json.dumps(exp_regime(N, seed, B), indent=1))
    else:
        print(json.dumps(f[exp](N, seed), indent=1))


def tempo_counts(c):
    """M_L, M_R of the root of a short component (LOOPY Def 1.10): longest number of Left (Right) moves in any sequence of moves, final move into a terminal counted"""
    from functools import lru_cache
    @lru_cache(None)
    def M(x, side):
        best = 0
        for s, opts in ((0, c.L[x]), (1, c.R[x])):
            for o in opts:
                v = (1 if s == side else 0) + (0 if o < 0 else M(o, side))
                best = max(best, v)
        return best
    return M(c.root, 0), M(c.root, 1)

def exp_thm111b(N, seed):
    """Theorem 3.8(a): short, pairwise safe (either-player tau), B > max(M_L(Y), M_R(Y))  =>  criterion, dominance, D = CGT"""
    rng = random.Random(seed)
    n = 0; cr_fail = 0; dom_fail = 0; eq_fail = 0; withev = 0
    for it in range(N):
        k = rng.choice([2, 2, 3])
        comps = [pick_comp(rng, "short") for _ in range(k)]
        evs = [c.events() for c in comps]
        if any(1 in evs[i] and -1 in evs[j] for i in range(k) for j in range(k) if i != j):
            continue
        ML = sum(tempo_counts(c)[0] for c in comps); MR = sum(tempo_counts(c)[1] for c in comps)
        B = max(ML, MR) + 1
        n += 1
        if any(evs): withev += 1
        if not reserve_criterion(comps, B)[0]: cr_fail += 1
        if not dominance(comps, B)[0]: dom_fail += 1
        d = d_results(comps); c_ = cgt_results(comps, B)
        if any(d[x] != c_[x] for x in d): eq_fail += 1
    return {"exp": "thm111b", "N": N, "seed": seed, "pairwise_safe_instances": n, "with_events": withev,
            "criterion_fail": cr_fail, "dominance_fail": dom_fail, "D_neq_CGT": eq_fail}

if __name__ == "__main__" and sys.argv[1] == "thm111b":
    print(json.dumps(exp_thm111b(int(sys.argv[2]), int(sys.argv[3])), indent=1))


def exp_pure(N, seed, B=14):
    """Prop 3.12: for S in {on, off, dud} and K short: translation right iff not P_R (on), not P_L (off), not (P_L or P_R) (dud)."""
    rng = random.Random(seed)
    n = 0; viol = 0
    for it in range(N):
        K = rand_K(rng, loopy=False)
        kts = product_nodes(K)
        r_off = solve(K + [mk_off()], [kt + (0,) for kt in kts]); r_on = solve(K + [mk_on()], [kt + (0,) for kt in kts])
        tK = [translate(c, B)[0] for c in K]
        for nm, S in (("on", mk_on()), ("off", mk_off()), ("dud", mk_dud())):
            rD = solve(K + [S], [kt + (0,) for kt in kts]); rC = solve(tK + [S], [kt + (0,) for kt in kts])
            for kt in kts:
                for m in (0, 1):
                    PL = r_off[(kt + (0,), m)] == "W"; PR = r_on[(kt + (0,), m)] == "L"
                    want_right = {"on": not PR, "off": not PL, "dud": not (PL or PR)}[nm]
                    # 'right' = D-result equals translation; for on/off it must be: eq iff want_right; for dud eq iff not forced
                    eq = rD[(kt + (0,), m)] == rC[(kt + (0,), m)]
                    n += 1
                    if eq != want_right: viol += 1
    return {"exp": "pure", "N": N, "seed": seed, "B": B, "checked": n, "violations": viol}

if __name__ == "__main__" and sys.argv[1] == "pure":
    print(json.dumps(exp_pure(int(sys.argv[2]), int(sys.argv[3])), indent=1))


def exp_onestopper(N, seed):
    """Corollary of Thm 3.8: one terminal-free stopper S with finite reserves + pairwise safe short K, B = 1 + max(Lam_S, P_S) + max(M_L(K), M_R(K)):
    criterion holds and D = CGT at every reachable state."""
    rng = random.Random(seed)
    n = 0; skipped = 0; cr_fail = 0; eq_fail = 0; with_ev = 0
    for it in range(N):
        K = rand_K(rng, loopy=False)
        evs = [c.events() for c in K]
        if any(1 in evs[i] and -1 in evs[j] for i in range(len(K)) for j in range(len(K)) if i != j):
            continue
        r = rng.random()
        S = pick_comp(rng, "stopper") if r < 0.8 else rng.choice([mk_over(), mk_under()])
        lam, rho = reserves(S, 1, 14)
        if any(v is None for v in lam.values()) or any(v is None for v in rho.values()):
            skipped += 1; continue
        ML = sum(tempo_counts(c)[0] for c in K); MR = sum(tempo_counts(c)[1] for c in K)
        B = 1 + max(max(lam.values()), max(rho.values())) + max(ML, MR)
        comps = K + [S]
        n += 1
        if any(evs): with_ev += 1
        if not reserve_criterion(comps, B)[0]: cr_fail += 1
        d = d_results(comps); c_ = cgt_results(comps, B)
        if any(d[x] != c_[x] for x in d): eq_fail += 1
    return {"exp": "onestopper", "N": N, "seed": seed, "instances": n, "with_events": with_ev, "skipped_infinite_reserve": skipped, "criterion_fail": cr_fail, "D_neq_CGT": eq_fail}

if __name__ == "__main__" and sys.argv[1] == "onestopper":
    print(json.dumps(exp_onestopper(int(sys.argv[2]), int(sys.argv[3])), indent=1))

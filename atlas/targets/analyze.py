#!/usr/bin/env python3
"""Workstream A3-targets: Elkies-target hunt, statistics, cylinder comparison.

Input: a pcgt run file (work/run_SCOPE.tsv, from runs.py): exact canonical values
of every position under 15 settings (5 race rules x {e.p. on textbook, e.p. on
aware, e.p. off}) on the flat board and (scope db, w5) on the cylinder of the
same width. Value ids (gid) are comparable across settings and boards because
one pcgt process computes the whole run with one hash-consed game store.

Subcommands (run from the project root):
  .venv/bin/python atlas/targets/analyze.py classify SCOPE   -> work/classes_SCOPE.json
  .venv/bin/python atlas/targets/analyze.py targets  SCOPE   -> targets_SCOPE.json, targets_SCOPE.out
  .venv/bin/python atlas/targets/analyze.py stats    SCOPE   -> stats_SCOPE.json, stats_SCOPE.out
  .venv/bin/python atlas/targets/analyze.py cylinder SCOPE   -> cylinder_SCOPE.json, cylinder_SCOPE.out
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C  # noqa: E402

WORK = C.WORK


def load(scope):
    return C.Run(os.path.join(WORK, f"run_{scope}.tsv"))


def load_classes(scope):
    with C.opener(os.path.join(WORK, f"classes_{scope}.json")) as fh:
        return {int(k): v for k, v in json.load(fh).items()}


# ------------------------------------------------------------------ classify
def cmd_classify(scope):
    run = load(scope)
    out = {}
    n = 0
    for gid, v in run.vals.items():
        if v["big"]:
            continue
        g = C.parse_key(v["key"])
        assert C.cgt.show(g) == v["show"] or True
        c = C.classify(g)
        c["show"] = v["show"]
        c["key"] = v["key"]
        c["hash"] = v["hash"]
        out[gid] = c
        n += 1
    with open(os.path.join(WORK, f"classes_{scope}.json"), "w") as fh:
        json.dump(out, fh, ensure_ascii=False)
    cls = Counter(c["cls"] for c in out.values())
    print(f"{scope}: {len(run.vals)} distinct root values in the run, {n} BIG-free classified: {dict(cls)}")


# ------------------------------------------------------------------ helpers
def target_kind(c):
    """Return a target label for a BIG-free class dict, or None."""
    k = c["cls"]
    if k == "nimber" and c["nim"] >= 2:
        return f"*{c['nim']}"
    if k == "dyadic" and c["den"] >= 8:
        return "dyadic den>=8"
    if k == "upsecond-family":
        return "up-second family"
    if k in ("tiny", "miny") and c["sub_is_number"] and not c["sub_is_integer"]:
        return "fractional tiny (number subscript)"
    if k in ("tiny", "miny") and not c["sub_is_number"]:
        return "tiny, non-number subscript"
    return None


def robustness(run, i, ref_setting, wrap=0):
    g0 = run.g(i, wrap, ref_setting)
    same = [C.sname(s) for s in C.SETTINGS if run.g(i, wrap, s) == g0]
    core_same = all(run.g(i, wrap, s) == g0 for s in C.CORE)
    all_same = len(same) == len(C.SETTINGS)
    return {"same_in": len(same), "of": len(C.SETTINGS), "core9": core_same, "all15": all_same,
            "settings_equal": same}


def vshow(run, classes, gid):
    if gid in classes:
        return classes[gid]["show"]
    v = run.vals.get(gid)
    if v is None:
        return "?"
    return v["show"] if v["show"] != "-" else f"(±W game {v['hash']})"


def sortkey(run, i):
    return (C.npawns(run.pos[i]), run.width[i], run.pos[i])


# ------------------------------------------------------------------ targets
def cmd_targets(scope):
    run = load(scope)
    classes = load_classes(scope)
    has_cyl = run.has(1, C.TEXTBOOK)
    res = {"scope": scope, "positions": len(run.pos), "settings": [C.sname(s) for s in C.SETTINGS]}
    lines = []
    P = lines.append

    # nimbers k>=2 under every setting (flat)
    nim = defaultdict(lambda: defaultdict(list))
    for i in range(len(run.pos)):
        for s in C.SETTINGS:
            c = classes.get(run.g(i, 0, s))
            if c and c["cls"] == "nimber" and c["nim"] >= 2:
                nim[f"*{c['nim']}"][C.sname(s)].append(run.pos[i])
    res["nimbers_k_ge_2"] = {k: dict(v) for k, v in nim.items()}
    P(f"== {scope}: {len(run.pos)} positions, flat board ==")
    P("Nimbers *k (k>=2) by setting:")
    if not nim:
        P("   none under any of the 15 settings")
    for k, v in sorted(nim.items()):
        for s, ps in sorted(v.items()):
            P(f"   {k} under {s}: {len(ps)}  e.g. {ps[:4]}")

    # targets under the two reference settings
    hits = {}
    for ref_name, ref in (("textbook", C.TEXTBOOK), ("aware", C.AWARE)):
        per = defaultdict(list)
        for i in range(len(run.pos)):
            gid = run.g(i, 0, ref)
            c = classes.get(gid)
            if not c:
                continue
            t = target_kind(c)
            if t is None:
                continue
            label = c["show"]
            if c["cls"] in ("upsecond-family", "tiny", "miny"):
                label = (c["shift"] + " + " if c.get("shift") else "") + c["inf"]
            per[(t, label)].append(i)
        hits[ref_name] = per
    res["targets"] = {}
    for ref_name, per in hits.items():
        P("")
        P(f"Targets under the {ref_name} passed test (count rule, e.p. on), flat board:")
        out = []
        for (t, label), idx in sorted(per.items(), key=lambda kv: (kv[0][0], kv[0][1])):
            idx.sort(key=lambda i: sortkey(run, i))
            entries = []
            for i in idx:
                gid = run.g(i, 0, C.TEXTBOOK if ref_name == "textbook" else C.AWARE)
                rb = robustness(run, i, C.TEXTBOOK if ref_name == "textbook" else C.AWARE)
                other = C.AWARE if ref_name == "textbook" else C.TEXTBOOK
                e = {"position": run.pos[i], "width": run.width[i], "npawns": C.npawns(run.pos[i]),
                     "value": classes[gid]["show"], "robust": rb,
                     "other_test_value": vshow(run, classes, run.g(i, 0, other)),
                     "values_by_setting": {C.sname(s): vshow(run, classes, run.g(i, 0, s)) for s in C.SETTINGS}}
                if has_cyl:
                    e["cylinder_textbook"] = vshow(run, classes, run.g(i, 1, C.TEXTBOOK))
                    e["cylinder_aware"] = vshow(run, classes, run.g(i, 1, C.AWARE))
                entries.append(e)
            nrob = sum(1 for e in entries if e["robust"]["all15"])
            nrob9 = sum(1 for e in entries if e["robust"]["core9"])
            out.append({"kind": t, "label": label, "count": len(entries), "robust_all15": nrob,
                        "robust_core9": nrob9, "positions": entries})
            best = entries[0]
            P(f"   [{t}] {label}: {len(entries)} positions; same under all 15 settings: {nrob}; "
              f"under the 9 core settings: {nrob9}; smallest {best['position']} (w{best['width']}, "
              f"{best['npawns']} pawns; other test: {best['other_test_value']})")
            shown = 0
            for e in entries:
                if e["robust"]["all15"] and shown < 3:
                    shown += 1
                    P(f"        same under all 15: {e['position']} w{e['width']} ({e['npawns']} pawns)"
                      + (f"  cylinder: {e['cylinder_textbook'][:60]} / {e['cylinder_aware'][:60]}" if has_cyl else ""))
        res["targets"][ref_name] = out

    # integer tinies (counts only)
    for ref_name, ref in (("textbook", C.TEXTBOOK), ("aware", C.AWARE)):
        cnt = Counter()
        for i in range(len(run.pos)):
            c = classes.get(run.g(i, 0, ref))
            if c and c["cls"] in ("tiny", "miny") and c["sub_is_integer"]:
                cnt[(c["shift"] + " + " if c.get("shift") else "") + c["inf"]] += 1
        res.setdefault("integer_tinies", {})[ref_name] = dict(cnt)
        P("")
        P(f"Integer-subscript tinies/minies ({ref_name}): {dict(sorted(cnt.items()))}")

    with open(os.path.join(HERE, f"targets_{scope}.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, f"targets_{scope}.out"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


# ------------------------------------------------------------------ stats
CLASS_ORDER = ["±W", "integer", "dyadic", "nimber", "number+nimber", "ups", "upsecond-family",
               "tiny", "miny", "other-infinitesimal", "switch", "hot-other"]


def coarse(run, classes, gid):
    c = classes.get(gid)
    if c is None:
        return "±W", None
    k = c["cls"]
    if k in ("number+nimber", "ups", "upsecond-family", "tiny", "miny", "other-infinitesimal"):
        k2 = k if c.get("infinitesimal") else k  # same class name; shift recorded separately
        return k2, c
    return k, c


def cmd_stats(scope):
    run = load(scope)
    classes = load_classes(scope)
    res = {}
    lines = []
    P = lines.append
    for ref_name, ref in (("textbook", C.TEXTBOOK), ("aware", C.AWARE)):
        table = defaultdict(Counter)        # (width, npawns) -> class -> count
        distinct = defaultdict(set)
        maxT = {}
        tempspec = defaultdict(Counter)
        infin = Counter()
        witness = {}
        hot_w = defaultdict(list)
        for i in range(len(run.pos)):
            w, n = run.width[i], C.npawns(run.pos[i])
            gid = run.g(i, 0, ref)
            k, c = coarse(run, classes, gid)
            table[(w, n)][k] += 1
            distinct[w].add(gid)
            if c is not None:
                if c.get("infinitesimal") or c["cls"] == "nimber":
                    infin[(w, n)] += 1
                lab = c["show"]
                key = (n, w, run.pos[i])
                if lab not in witness or key < witness[lab][0]:
                    witness[lab] = (key, k)
                if c["cls"] in ("switch", "hot-other"):
                    t = Fraction(c["temp"])
                    tempspec[w][c["temp"]] += 1
                    if w not in maxT or t > maxT[w][0] or (t == maxT[w][0] and key < maxT[w][2]):
                        maxT[w] = (t, c["show"], key)
        P(f"== {scope}, {ref_name} passed test, count rule, e.p. on, flat board ==")
        P("Value classes by width and pawn count (records = positions up to mirror image):")
        hdr = "  w  n   total " + " ".join(f"{k:>9s}" for k in CLASS_ORDER) + "  infinitesimal%"
        P(hdr)
        rows = {}
        for (w, n) in sorted(table):
            cnt = table[(w, n)]
            tot = sum(cnt.values())
            inf = infin[(w, n)]
            P(f"  {w}  {n} {tot:7d} " + " ".join(f"{cnt.get(k, 0):9d}" for k in CLASS_ORDER) + f"  {100.0 * inf / tot:6.2f}")
            rows[f"{w},{n}"] = {"total": tot, **{k: cnt.get(k, 0) for k in CLASS_ORDER}, "infinitesimal_incl_nimbers": inf}
        tot_all = sum(sum(c.values()) for c in table.values())
        inf_all = sum(infin.values())
        P(f"  all positions {tot_all}; infinitesimal (mean 0, temperature 0, incl. nimbers, excl. 0): "
          f"{inf_all} = {100.0 * inf_all / tot_all:.2f}%")
        P("Distinct values per width: " + ", ".join(f"w{w}: {len(s)}" for w, s in sorted(distinct.items())))
        P("Maximum temperature of a ±W-free hot value, per width (smallest witness):")
        for w in sorted(maxT):
            t, sh, key = maxT[w]
            P(f"  w{w}: {C.fnum(t)}  {sh}  at {key[2]} ({key[0]} pawns)")
        P("Temperature spectrum of ±W-free hot values (records), per width:")
        for w in sorted(tempspec):
            P(f"  w{w}: " + ", ".join(f"{t}:{c}" for t, c in sorted(tempspec[w].items(), key=lambda kv: Fraction(kv[0]))))
        res[ref_name] = {"by_width_pawns": rows, "infinitesimal_total": inf_all, "positions": tot_all,
                         "distinct_values_per_width": {w: len(s) for w, s in distinct.items()},
                         "max_temperature": {w: {"temp": C.fnum(t), "value": sh, "witness": key[2]}
                                             for w, (t, sh, key) in maxT.items()},
                         "temperature_spectrum": {w: dict(c) for w, c in tempspec.items()},
                         "smallest_witness": {lab: {"position": key[2], "width": key[1], "npawns": key[0], "class": k}
                                              for lab, (key, k) in witness.items()}}
        P("")
    with open(os.path.join(HERE, f"stats_{scope}.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, f"stats_{scope}.out"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


# ------------------------------------------------------------------ cylinder
def cmd_cylinder(scope):
    run = load(scope)
    classes = load_classes(scope)
    res = {}
    lines = []
    P = lines.append
    for s in [C.TEXTBOOK, C.AWARE] + [x for x in C.SETTINGS if x not in (C.TEXTBOOK, C.AWARE)]:
        per_w = defaultdict(lambda: {"positions": 0, "changed": 0, "outcome_changed": 0,
                                     "flat_vals": set(), "cyl_vals": set()})
        for i in range(len(run.pos)):
            w = run.width[i]
            gf, gc = run.g(i, 0, s), run.g(i, 1, s)
            d = per_w[w]
            d["positions"] += 1
            d["changed"] += gf != gc
            d["outcome_changed"] += run.o(i, 0, s) != run.o(i, 1, s)
            d["flat_vals"].add(gf)
            d["cyl_vals"].add(gc)
        out = {}
        for w, d in sorted(per_w.items()):
            fv, cv = d["flat_vals"], d["cyl_vals"]
            fo = fv - cv
            co = cv - fv
            fo_free = sorted((vshow(run, classes, g) for g in fo if g in classes))
            co_free = sorted((vshow(run, classes, g) for g in co if g in classes))
            out[w] = {"positions": d["positions"], "value_changed": d["changed"],
                      "outcome_changed": d["outcome_changed"], "flat_distinct": len(fv), "cyl_distinct": len(cv),
                      "flat_only": len(fo), "cyl_only": len(co), "flat_only_W_free": fo_free,
                      "cyl_only_W_free": co_free}
        res[C.sname(s)] = out
        if s in (C.TEXTBOOK, C.AWARE):
            P(f"== {scope}: same position on the flat strip vs the cylinder of the same width, {C.sname(s)} ==")
            for w, d in out.items():
                P(f"  w{w}: {d['positions']} positions; value differs {d['value_changed']} "
                  f"({100.0 * d['value_changed'] / d['positions']:.1f}%), outcome differs {d['outcome_changed']}; "
                  f"distinct values flat {d['flat_distinct']} / cyl {d['cyl_distinct']}; "
                  f"only-flat {d['flat_only']} (±W-free {len(d['flat_only_W_free'])}), "
                  f"only-cyl {d['cyl_only']} (±W-free {len(d['cyl_only_W_free'])})")
                P(f"      created by the edge (flat only, ±W-free): {d['flat_only_W_free'][:40]}")
                P(f"      destroyed by the edge (cylinder only, ±W-free): {d['cyl_only_W_free'][:40]}")
            P("")
    # whole-scope (all widths pooled) flat-only / cyl-only, W-free, per setting
    P("Pooled over widths: ±W-free values found on flat strips but on no cylinder (and vice versa), per setting:")
    pooled = {}
    for s in C.SETTINGS:
        fv, cv = set(), set()
        for i in range(len(run.pos)):
            fv.add(run.g(i, 0, s)); cv.add(run.g(i, 1, s))
        fo = sorted(vshow(run, classes, g) for g in fv - cv if g in classes)
        co = sorted(vshow(run, classes, g) for g in cv - fv if g in classes)
        pooled[C.sname(s)] = {"flat_only_W_free": fo, "cyl_only_W_free": co}
        P(f"  {C.sname(s):24s}: flat-only {len(fo)}, cylinder-only {len(co)}")
    res["pooled"] = pooled
    # values cylinder-only or flat-only under every setting
    keys = list(pooled)
    always_flat = set(pooled[keys[0]]["flat_only_W_free"])
    always_cyl = set(pooled[keys[0]]["cyl_only_W_free"])
    for k in keys[1:]:
        always_flat &= set(pooled[k]["flat_only_W_free"])
        always_cyl &= set(pooled[k]["cyl_only_W_free"])
    res["flat_only_under_all_15"] = sorted(always_flat)
    res["cyl_only_under_all_15"] = sorted(always_cyl)
    P(f"  ±W-free values flat-only under all 15 settings: {sorted(always_flat)}")
    P(f"  ±W-free values cylinder-only under all 15 settings: {sorted(always_cyl)}")
    with open(os.path.join(HERE, f"cylinder_{scope}.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, f"cylinder_{scope}.out"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


def cmd_hot(scope):
    """Temperatures of ±W-free hot values (flat board): hottest per width, values above
    3/2 (= (N-5)/2 for N = 8, the temperature the survey attributes to Elkies'
    constructions on files of length N), and temperatures with denominator >= 16; each
    with its robustness over the 15 settings."""
    run = load(scope)
    classes = load_classes(scope)
    res = {}
    lines = []
    P = lines.append
    for ref_name, ref in (("textbook", C.TEXTBOOK), ("aware", C.AWARE)):
        hot = []
        for i in range(len(run.pos)):
            gid = run.g(i, 0, ref)
            c = classes.get(gid)
            if not c or c["cls"] not in ("switch", "hot-other"):
                continue
            t = Fraction(c["temp"])
            gids = [run.g(i, 0, s) for s in C.SETTINGS]
            hot.append({"i": i, "t": t, "value": c["show"], "cls": c["cls"],
                        "robust15": len(set(gids)) == 1,
                        "same_in": sum(1 for g in gids if g == gid)})
        P(f"== {scope}, {ref_name} test (count rule, e.p. on): {len(hot)} positions with a ±W-free hot value ==")
        byw = defaultdict(list)
        for h in hot:
            byw[run.width[h["i"]]].append(h)
        out = {"by_width": {}}
        for w in sorted(byw):
            hs = sorted(byw[w], key=lambda h: (-h["t"], C.npawns(run.pos[h["i"]]), run.pos[h["i"]]))
            top = hs[0]
            rob = [h for h in hs if h["robust15"]]
            toprob = rob[0] if rob else None
            above = [h for h in hs if h["t"] > Fraction(3, 2)]
            fine = [h for h in hs if h["t"].denominator >= 16]
            sw = [h for h in hs if h["cls"] == "switch"]
            topsw = sw[0] if sw else None
            P(f"  w{w}: hottest {C.fnum(top['t'])} = {top['value']} at {run.pos[top['i']]} (same in {top['same_in']}/15); "
              f"hottest identical under all 15: " + (f"{C.fnum(toprob['t'])} = {toprob['value']} at {run.pos[toprob['i']]}" if toprob else "none"))
            P(f"       hottest switch x±y: " + (f"{topsw['value']} (t={C.fnum(topsw['t'])}) at {run.pos[topsw['i']]}" if topsw else "none")
              + f"; temperature > 3/2: {len(above)} positions ({sum(h['robust15'] for h in above)} identical under all 15)"
              + f"; denominator >= 16: {len(fine)} ({sum(h['robust15'] for h in fine)} identical under all 15)")
            for h in sorted(fine, key=lambda h: (h["t"].denominator, h["t"]), reverse=True)[:6]:
                P(f"         fine: t={C.fnum(h['t'])} {h['value'][:70]} at {run.pos[h['i']]} same in {h['same_in']}/15")
            out["by_width"][w] = {
                "hottest": {"temp": C.fnum(top["t"]), "value": top["value"], "position": run.pos[top["i"]], "same_in_of15": top["same_in"]},
                "hottest_robust15": ({"temp": C.fnum(toprob["t"]), "value": toprob["value"], "position": run.pos[toprob["i"]]} if toprob else None),
                "hottest_switch": ({"temp": C.fnum(topsw["t"]), "value": topsw["value"], "position": run.pos[topsw["i"]]} if topsw else None),
                "n_above_3_2": len(above), "n_above_3_2_robust15": sum(h["robust15"] for h in above),
                "n_den_ge_16": len(fine), "n_den_ge_16_robust15": sum(h["robust15"] for h in fine),
                "den_ge_16": [{"temp": C.fnum(h["t"]), "value": h["value"], "position": run.pos[h["i"]], "same_in_of15": h["same_in"]} for h in fine],
                "robust15_above_3_2": sorted({(C.fnum(h["t"]), h["value"]) for h in above if h["robust15"]}),
            }
        res[ref_name] = out
        P("")
    with open(os.path.join(HERE, f"hot_{scope}.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, default=str)
    with open(os.path.join(HERE, f"hot_{scope}.out"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


def label_of(c):
    t = target_kind(c)
    if t is None:
        return None, None
    label = c["show"]
    if c["cls"] in ("upsecond-family", "tiny", "miny"):
        label = (c["shift"] + " + " if c.get("shift") else "") + c["inf"]
    return t, label


def cmd_matrix(scope, wrap=0):
    """Every target under every setting (flat board, or wrap=1: the cylinder of the
    same width): label -> setting -> positions; plus the positions whose value is a
    target and is the same under all 15 settings."""
    run = load(scope)
    classes = load_classes(scope)
    board = "cyl" if wrap else "flat"
    mat = defaultdict(lambda: defaultdict(list))
    robust = defaultdict(list)
    for i in range(len(run.pos)):
        gids = [run.g(i, wrap, s) for s in C.SETTINGS]
        for s, gid in zip(C.SETTINGS, gids):
            c = classes.get(gid)
            if not c:
                continue
            t, label = label_of(c)
            if t:
                mat[(t, label)][C.sname(s)].append(run.pos[i])
        if len(set(gids)) == 1 and gids[0] in classes:
            t, label = label_of(classes[gids[0]])
            if t:
                robust[(t, label)].append(run.pos[i])
    lines = [f"== {scope}: targets by setting ({board} board; number of positions) =="]
    snames = [C.sname(s) for s in C.SETTINGS]
    short = {n: n.replace("epon-textbook", "T").replace("epon-aware", "A").replace("epoff", "off")
             .replace("count", "cnt").replace("mover", "mov").replace("opponent", "opp").replace("white", "wht")
             .replace("black", "blk") for n in snames}
    lines.append(f"{'kind':36s} {'label':34s} " + " ".join(f"{short[n]:>8s}" for n in snames))
    out = {}
    for (t, label) in sorted(mat):
        row = mat[(t, label)]
        lines.append(f"{t:36s} {label[:34]:34s} " + " ".join(f"{len(row.get(n, [])):8d}" for n in snames))
        out[f"{t} | {label}"] = {n: sorted(row.get(n, []), key=lambda p: (C.npawns(p), p)) for n in snames if row.get(n)}
    lines.append("")
    lines.append("Targets whose value is identical under all 15 settings:")
    if not robust:
        lines.append("   none")
    for (t, label), ps in sorted(robust.items()):
        ps.sort(key=lambda p: (C.npawns(p), p))
        lines.append(f"   [{t}] {label}: {len(ps)}  e.g. {ps[:3]}")
    suffix = "" if not wrap else "_cyl"
    with open(os.path.join(HERE, f"matrix_{scope}{suffix}.json"), "w") as fh:
        json.dump({"by_label": out, "robust_all15": {f"{t} | {l}": ps for (t, l), ps in robust.items()}}, fh,
                  indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, f"matrix_{scope}{suffix}.out"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    cmd, scope = sys.argv[1], sys.argv[2]
    if cmd == "matrix-cyl":
        cmd_matrix(scope, wrap=1)
    else:
        {"classify": cmd_classify, "targets": cmd_targets, "stats": cmd_stats, "cylinder": cmd_cylinder,
         "matrix": cmd_matrix, "hot": cmd_hot}[cmd](scope)

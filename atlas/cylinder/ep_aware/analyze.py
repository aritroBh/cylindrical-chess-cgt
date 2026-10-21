"""Merge atlas parts into values.jsonl / value_index.jsonl and summarise.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python atlas/cylinder/analyze.py

Inputs: atlas/cylinder/parts/*.jsonl (+ .vals) written by atlas_run.py.
Outputs (atlas/cylinder/):
  values.jsonl        one line per canonical position (race rule "count", e.p. on)
  value_index.jsonl   one line per distinct value: vid, exact key, display, class, ...
  summary.json        machine-readable aggregates used in REPORT.md
  summary.txt         human-readable tables

Two comparison levels:
  ALL  : every canonical position with w+b <= 5 (both boards, widths 3..8).
  CONN : connected positions (a single component) with w+b <= 6.  For 6 pawns
         only "atoms" were computed: full-width flat components of width k and
         rings of width n.  A full-width flat atom of width k occurs (translated)
         on every flat strip of width >= k and on every cylinder of width >= k+1;
         a ring of width n occurs only on the cylinder of width n.
"""
from __future__ import annotations

import glob
import json
import os
import re
from collections import Counter, defaultdict
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(HERE, "parts")


def span(pos, n, wrap):
    files = set()
    for tok in re.findall(r"[a-h]\d", pos):
        files.add("abcdefgh".index(tok[0]))
    if not wrap:
        return max(files) - min(files) + 1
    # smallest cyclic arc covering all files
    best = n
    for start in files:
        far = max((f - start) % n for f in files)
        best = min(best, far + 1)
    return best


def simplicity(rec, n, wrap):
    return (rec["w"] + rec["b"], span(rec["pos"], n, wrap), rec["ncomp"], rec["pos"])


def main(rule="count", ep=1):
    index = {}
    for vf in glob.glob(os.path.join(PARTS, "*.vals")):
        with open(vf) as fh:
            for line in fh:
                d = json.loads(line)
                index.setdefault(d["vid"], d)
    # aggregates
    allset = defaultdict(dict)    # (board, n) -> vid -> best witness rec
    allcount = defaultdict(Counter)
    wbset = defaultdict(dict)     # (board, n, w, b) -> vid -> witness
    conn_atoms = defaultdict(dict)  # ("flatk", k) or ("ring", n) -> vid -> witness
    ringrecs = defaultdict(Counter)
    nposs = Counter()
    out = open(os.path.join(HERE, "values.jsonl"), "w")
    files = sorted(glob.glob(os.path.join(PARTS, f"*_{rule}_ep{ep}_*.jsonl")))
    seen_tags = set()
    for pf in files:
        tag = os.path.basename(pf)
        mode = "atoms" if "_atoms_" in tag else ("all" if "_all_" in tag else "connected")
        with open(pf) as fh:
            for line in fh:
                r = json.loads(line)
                board = "cyl" if r["wrap"] else "flat"
                n = r["n"]
                key = (board, n, r["pos"])
                if key in seen_tags:
                    continue  # the same position can appear in an 'all' and an 'atoms' run
                seen_tags.add(key)
                rec = {"board": board, "n": n, "w": r["w"], "b": r["b"], "pos": r["pos"], "vid": r["vid"],
                       "val": r["val"], "ring": r["ring"], "ncomp": r["ncomp"]}
                if "safe" in r:
                    rec["safe"] = r["safe"]
                out.write(json.dumps(rec, separators=(",", ":"), ensure_ascii=False) + "\n")
                nposs[(board, n, r["w"] + r["b"], mode)] += 1
                wrap = board == "cyl"
                vid = r["vid"]
                s = simplicity(r, n, wrap)
                if mode == "all":
                    d = allset[(board, n)]
                    if vid not in d or s < d[vid]["_s"]:
                        d[vid] = {**rec, "_s": s}
                    allcount[(board, n)][vid] += 1
                    d2 = wbset[(board, n, r["w"], r["b"])]
                    if vid not in d2 or s < d2[vid]["_s"]:
                        d2[vid] = {**rec, "_s": s}
                # connected atoms (from both modes)
                if r["ncomp"] == 1:
                    if wrap and r["ring"]:
                        akey = ("ring", n)
                    else:
                        akey = ("flatk", span(r["pos"], n, wrap))
                    d3 = conn_atoms[akey]
                    if vid not in d3 or s < d3[vid]["_s"]:
                        d3[vid] = {**rec, "_s": s}
                    if wrap and r["ring"]:
                        ringrecs[n][vid] += 1
    out.close()
    with open(os.path.join(HERE, "value_index.jsonl"), "w") as fh:
        for vid, d in sorted(index.items()):
            fh.write(json.dumps(d, separators=(",", ":"), ensure_ascii=False) + "\n")

    widths = sorted({n for (_, n) in allset})
    summ = {"nposs": {f"{b}{n}_p{t}_{m}": c for (b, n, t, m), c in sorted(nposs.items())}}

    def cls(v):
        return index[v]["cls"]

    def label(v):
        d = index[v]
        return d.get("detail") or d["show"]

    def wit(rec):
        return {"pos": rec["pos"], "w": rec["w"], "b": rec["b"], "ncomp": rec["ncomp"], "ring": rec["ring"],
                "safe": rec.get("safe", 1)}

    # ---- level ALL: cylinder-only and flat-only values per width
    lvl_all = {}
    for n in widths:
        C, F = allset[("cyl", n)], allset[("flat", n)]
        conly = sorted(set(C) - set(F), key=lambda v: C[v]["_s"])
        fonly = sorted(set(F) - set(C), key=lambda v: F[v]["_s"])
        lvl_all[n] = {
            "n_values_cyl": len(C), "n_values_flat": len(F),
            "cyl_only": [{"vid": v, "value": label(v), "cls": cls(v), **wit(C[v])} for v in conly],
            "flat_only": [{"vid": v, "value": label(v), "cls": cls(v), **wit(F[v])} for v in fonly],
        }
    summ["level_all"] = lvl_all

    # ---- level CONN (<= 6 pawns): derived from atoms
    lvl_conn = {}
    maxk = max(k for (t, k) in conn_atoms if t == "flatk")
    for n in widths:
        F, C = {}, {}
        for k in range(1, maxk + 1):
            for v, rec in conn_atoms.get(("flatk", k), {}).items():
                if k <= n and (v not in F or rec["_s"] < F[v]["_s"]):
                    F[v] = rec
                if k <= n - 1 and (v not in C or rec["_s"] < C[v]["_s"]):
                    C[v] = rec
        for v, rec in conn_atoms.get(("ring", n), {}).items():
            if v not in C or rec["_s"] < C[v]["_s"]:
                C[v] = rec
        conly = sorted(set(C) - set(F), key=lambda v: C[v]["_s"])
        fonly = sorted(set(F) - set(C), key=lambda v: F[v]["_s"])
        lvl_conn[n] = {
            "n_values_cyl": len(C), "n_values_flat": len(F),
            "cyl_only": [{"vid": v, "value": label(v), "cls": cls(v), **wit(C[v])} for v in conly],
            "flat_only": [{"vid": v, "value": label(v), "cls": cls(v), **wit(F[v])} for v in fonly],
        }
    summ["level_conn"] = lvl_conn

    # ---- lemma check: non-ring cylinder values (ALL level, same w,b) lie in flat(n-1)
    lemma = {}
    for n in widths:
        if n - 1 not in widths:
            continue
        bad = 0
        tot = 0
        for (bd, nn, w, b), d in wbset.items():
            if bd != "cyl" or nn != n:
                continue
            flat_prev = wbset.get(("flat", n - 1, w, b), {})
            for v, rec in d.items():
                if rec["ring"]:
                    continue
                tot += 1
                if v not in flat_prev:
                    bad += 1
        lemma[n] = {"nonring_values_checked": tot, "missing_from_flat_n_minus_1": bad}
    summ["lemma_check"] = lemma

    # ---- value classes per board/width (ALL level + CONN atoms)
    classes = {}
    for (bd, n), d in sorted(allset.items()):
        byc = defaultdict(list)
        for v, rec in d.items():
            byc[cls(v)].append(v)
        temps = [(Fraction(index[v]["temp"]), v) for v in d if index[v].get("temp") not in (None,)
                 and not index[v]["big"]]
        temps_big = [(Fraction(index[v]["temp"]), v) for v in d if index[v].get("temp") not in (None,)
                     and index[v]["big"]]
        entry = {"counts": {c: len(vs) for c, vs in sorted(byc.items())}}
        for c in ("nimber", "number+nimber", "ups", "tiny", "switch", "dyadic", "other_inf", "hot"):
            vs = sorted(byc.get(c, []), key=lambda v: d[v]["_s"])
            entry[c] = [{"value": label(v) if c not in ("other_inf", "hot") else index[v]["show"],
                         "temp": index[v].get("temp"), "mean": index[v].get("mean"), **wit(d[v])} for v in vs]
        if temps:
            t, v = max(temps)
            entry["max_temp_nonW"] = {"temp": str(t), "value": index[v]["show"], **wit(d[v])}
        if temps_big:
            t, v = max(temps_big)
            entry["max_temp_W"] = {"temp": str(t), "value": index[v]["show"][:120], **wit(d[v])}
        classes[f"{bd}{n}"] = entry
    # atoms classes (6 pawns included)
    for akey, d in sorted(conn_atoms.items()):
        byc = defaultdict(list)
        for v in d:
            byc[cls(v)].append(v)
        temps = [(Fraction(index[v]["temp"]), v) for v in d if index[v].get("temp") is not None and not index[v]["big"]]
        entry = {"counts": {c: len(vs) for c, vs in sorted(byc.items())}}
        for c in ("nimber", "number+nimber", "ups", "tiny", "switch", "dyadic", "other_inf", "hot"):
            vs = sorted(byc.get(c, []), key=lambda v: d[v]["_s"])
            entry[c] = [{"value": label(v) if c not in ("other_inf", "hot") else index[v]["show"],
                         "temp": index[v].get("temp"), "mean": index[v].get("mean"), **wit(d[v])} for v in vs]
        if temps:
            t, v = max(temps)
            entry["max_temp_nonW"] = {"temp": str(t), "value": index[v]["show"], **wit(d[v])}
        classes[f"atoms_{akey[0]}{akey[1]}"] = entry
    summ["classes"] = classes

    # ---- rings
    rings = {}
    for n, cnt in sorted(ringrecs.items()):
        d = conn_atoms[("ring", n)]
        flat_all = set()
        for (t, k), dd in conn_atoms.items():
            if t == "flatk":
                flat_all |= set(dd)
        lst = []
        for v, c in cnt.most_common():
            lst.append({"vid": v, "value": label(v) if index[v]["cls"] not in ("hot", "other_inf", "involves_W") else index[v]["show"][:160],
                        "cls": cls(v), "count": c, "in_any_flat_atom": v in flat_all, **wit(d[v])})
        rings[n] = {"n_positions": sum(cnt.values()), "n_values": len(cnt),
                    "n_values_not_in_any_flat_atom": sum(1 for x in lst if not x["in_any_flat_atom"]),
                    "values": lst}
    summ["rings"] = rings

    with open(os.path.join(HERE, "summary.json"), "w") as fh:
        json.dump(summ, fh, indent=1, ensure_ascii=False, default=str)
    print("wrote values.jsonl, value_index.jsonl, summary.json")
    for k, v in summ["nposs"].items():
        print(k, v)


if __name__ == "__main__":
    main()

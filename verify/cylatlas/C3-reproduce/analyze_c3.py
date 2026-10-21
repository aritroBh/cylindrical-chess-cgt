"""Verifier analysis for claim C3 (reads out_main/, out_ep/ and, read-only, the
worker's atlas/cylinder/values.jsonl + value_index.jsonl).

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python verify/cylatlas/C3-reproduce/analyze_c3.py
"""
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from enum_atoms import images, canon, TASKS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ATLAS = os.path.join(ROOT, "atlas", "cylinder")


def load(impl):
    recs, sums, meta = [], [], set()
    files = glob.glob(os.path.join(HERE, f"out_{impl}", "*.jsonl"))
    for f in files:
        lines = [json.loads(l) for l in open(f)]
        assert "meta" in lines[0] and lines[-1].get("done"), f
        meta.add((lines[0]["meta"]["module"], lines[0]["meta"]["PASSED_RESPECTS_EP"], lines[0]["meta"]["race_rule"]))
        body = lines[1:-1]
        (sums if lines[0]["meta"]["task"] == "sums" else recs).extend(body)
    return recs, sums, meta, len(files)


def sets_of(recs, sums):
    big = {}
    flat, ring = set(), defaultdict(set)
    wit = {}
    for r in recs:
        big[r["vid"]] = r["big"]
        wit.setdefault((r["kind"], r["n"], r["vid"]), r)
        if r["kind"] == "flat":
            flat.add(r["vid"])
        else:
            ring[r["n"]].add(r["vid"])
    for s in sums:
        big[s["vid"]] = s["big"]
        flat.add(s["vid"])
    return flat, ring, big, wit


def report(impl, expected_files=14 + 7 * 4):
    recs, sums, meta, nf = load(impl)
    print(f"== {impl}: files {nf} (expected {expected_files}); module/flag/rule {meta}")
    cnt = Counter((r["kind"], r["n"], r["p"]) for r in recs)
    print("   positions per task:", dict(sorted(cnt.items())), "sums:", len(sums))
    flat, ring, big, wit = sets_of(recs, sums)
    R = ring[3] | ring[4] | ring[5]
    co = R - flat
    nw = {v for v in co if not big[v]}
    first = Counter(min(n for n in (3, 4, 5) if v in ring[n]) for v in nw)
    print(f"   flat values {len(flat)}  ring values C3 {len(ring[3])} C4 {len(ring[4])} C5 {len(ring[5])}")
    print(f"   cylinder-only values: {len(co)} total, {len(nw)} without W; by smallest ring width {dict(sorted(first.items()))}")
    return flat, ring, big, wit, nw, recs


def worker_sets():
    idx = {}
    for l in open(os.path.join(ATLAS, "value_index.jsonl")):
        d = json.loads(l)
        idx[d["vid"]] = d
    C, F = set(), set()
    per_pos = {}
    for l in open(os.path.join(ATLAS, "values.jsonl")):
        r = json.loads(l)
        if r["w"] + r["b"] > 5 or not (3 <= r["n"] <= 8):
            continue
        (C if r["board"] == "cyl" else F).add(r["vid"])
        # map single-component positions to my atom canonical form
        if r["ncomp"] == 1:
            W = [("abcdefgh".index(t[0]), int(t[1])) for t in r["pos"].split("/")[0].split(":")[1].split()]
            B = [("abcdefgh".index(t[0]), int(t[1])) for t in r["pos"].split("/")[1].split(":")[1].split()]
            if r["board"] == "cyl" and r["ring"]:
                n = r["n"]
                per_pos[("ring", n, canon(n, True, W, B, images(n, True)))] = r["vid"]
            elif r["board"] == "flat":
                lo = min(f for f, _ in W + B)
                k = max(f for f, _ in W + B) - lo + 1
                W2 = [(f - lo, s) for f, s in W]
                B2 = [(f - lo, s) for f, s in B]
                per_pos[("flat", k, canon(k, False, W2, B2, images(k, False)))] = r["vid"]
    return idx, C, F, per_pos


def parse(t):
    w, b = t.split("/")
    W = [("abcdefgh".index(x[0]), int(x[1])) for x in w.split(":")[1].split()]
    B = [("abcdefgh".index(x[0]), int(x[1])) for x in b.split(":")[1].split()]
    return W, B


if __name__ == "__main__":
    fm, rm, bm, wm, nwm, recm = report("main")
    idx, C, F, per_pos = worker_sets()
    print("\n== textbook test vs worker's stored atlas")
    myC = fm | rm[3] | rm[4] | rm[5]
    print(f"   my flat set == worker flat set (widths 3-8): {fm == F}  (mine {len(fm)}, worker {len(F)})")
    print(f"   my cylinder set == worker cylinder set: {myC == C}  (mine {len(myC)}, worker {len(C)})")
    wnw = set(json.load(open(os.path.join(HERE, "worker_nonW_cylonly_vids.json"))))
    print(f"   my 53-set == worker's non-W cylinder-only set: {nwm == wnw}")
    # per position
    agree = dis = miss = 0
    for r in recm:
        W, B = parse(r["pos"])
        k = (r["kind"], r["n"], canon(r["n"], r["kind"] == "ring", W, B, images(r["n"], r["kind"] == "ring")))
        v = per_pos.get(k)
        if v is None:
            miss += 1
        elif v == r["vid"]:
            agree += 1
        else:
            dis += 1
    print(f"   per-position (atoms/rings): agree {agree}, disagree {dis}, not in worker file {miss}")

    fe, re_, be, we, nwe, rece = report("ep")
    print("\n== e.p.-aware vs textbook")
    surv = nwm & nwe
    print(f"   non-W cylinder-only: textbook {len(nwm)}, e.p.-aware {len(nwe)}, in both {len(surv)}, "
          f"lost {len(nwm - nwe)}, new {len(nwe - nwm)}")
    # per-position value changes
    vm = {(r["kind"], r["n"], r["pos"]): r for r in recm}
    ch = Counter()
    for r in rece:
        k = (r["kind"], r["n"], r["pos"])
        if vm[k]["vid"] != r["vid"]:
            ch[(r["kind"], r["n"])] += 1
    print("   positions whose value changes:", dict(sorted(ch.items())), "of", dict(sorted(Counter((r['kind'], r['n']) for r in rece).items())))
    lab = {}
    for r in recm + rece:
        lab.setdefault(r["vid"], r["show"])

    def show(v):
        return idx[v].get("detail") or idx[v]["show"] if v in idx else lab.get(v)
    print("   lost under e.p.-aware:")
    for v in sorted(nwm - nwe, key=lambda v: str(show(v))):
        w = min((wm[(k, n, vv)] for (k, n, vv) in wm if vv == v and k == "ring"), key=lambda r: (r["p"], r["n"]))
        print(f"     {show(v)}  e.g. C{w['n']} {w['pos']}")
    print("   new under e.p.-aware:")
    for v in sorted(nwe - nwm, key=lambda v: str(lab.get(v))):
        w = min((we[(k, n, vv)] for (k, n, vv) in we if vv == v and k == "ring"), key=lambda r: (r["p"], r["n"]))
        print(f"     {lab.get(v)}  e.g. C{w['n']} {w['pos']}")
    first = Counter(min(n for n in (3, 4, 5) if v in re_[n]) for v in nwe)
    print("   e.p.-aware split by smallest ring width:", dict(sorted(first.items())))
    print(f"   e.p.-aware: flat-only none by construction; cylinder set contains flat set: True")

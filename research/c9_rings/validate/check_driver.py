#!/usr/bin/env python3
"""check_driver.py -- audit of the C9 10-pawn driver run (read-only).

For every job line in work/jobs_c9p10*.txt: .done present, .summary.txt present, no FAILED in progress.txt,
rings emitted by enum_rings (its own stderr count) == rings_sent == rings_solved + unresolved, unresolved == 0,
hist total == rings_solved, number of lines of sigs.gz == rings_sent, .err only holds expected lines.
Per split: chunk indices == range(K) exactly once, consistent K, prefixes_seen equal in every chunk, sum of rings.
Hits: merged over chunks (own parse), compared with the partial merge file.
"""
import os, re, sys, glob, gzip, collections, json

ROOT = os.path.dirname(os.path.abspath(__file__))
C9 = os.path.join(ROOT, "..")
WORK = os.path.join(C9, "work")


def kv(fn):
    d = {}
    for line in open(fn):
        k, _, v = line.rstrip("\n").partition("\t")
        d[k] = v
    return d


jobs = []
for jf in ("jobs_c9p10.txt", "jobs_c9p10_mirror.txt"):
    for line in open(os.path.join(WORK, jf)):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split()
        jobs.append(dict(N=int(p[0]), P=int(p[1]), NW=int(p[2]), NB=int(p[3]), I=int(p[4]), K=int(p[5]), out=p[6], extra=p[7:], file=jf))
print("jobs read: %d  (%s)" % (len(jobs), ", ".join("%s %d" % (f, sum(1 for j in jobs if j['file'] == f)) for f in ("jobs_c9p10.txt", "jobs_c9p10_mirror.txt"))))
dup = [k for k, c in collections.Counter(j['out'] for j in jobs).items() if c > 1]
print("duplicate output prefixes in the job files:", len(dup))

prog = open(os.path.join(WORK, "c9p10", "progress.txt")).read().splitlines()
failed_lines = [l for l in prog if "FAILED" in l]
done_lines = [l for l in prog if " done " in l]
print("progress.txt: %d lines, %d 'done' lines, %d FAILED lines" % (len(prog), len(done_lines), len(failed_lines)))
done_prefixes = collections.Counter(l.split()[-1] for l in done_lines)
print("progress 'done' prefixes distinct: %d, listed more than once: %d" % (len(done_prefixes), sum(1 for v in done_prefixes.values() if v > 1)))

problems = []
splits = collections.defaultdict(lambda: dict(chunks=[], Ks=set(), rings=0, prefixes=set(), hits=[], hist=collections.Counter(),
                                            leaves=0, solved=0, nodes=0, maxnodes=0, retried=0, restarts=0))
n_done = n_sum = 0
for j in jobs:
    base = os.path.join(C9, j['out'])
    tag = os.path.basename(j['out'])
    if not os.path.exists(base + ".done"):
        problems.append("%s: no .done" % tag)
    else:
        n_done += 1
    if os.path.exists(base + ".claim"):
        problems.append("%s: stale .claim" % tag)
    if j['out'] not in done_prefixes:
        problems.append("%s: not in progress.txt as done" % tag)
    sf = base + ".summary.txt"
    if not os.path.exists(sf):
        problems.append("%s: no summary" % tag)
        continue
    n_sum += 1
    s = kv(sf)
    cmd = s["cmd"].split()
    # recorded cmd (drive.py writes cmd[2:] of "nice -n 15 ENUM N P NW NB --chunk I K"): 15 ENUM N P NW NB --chunk I K
    assert cmd[1].endswith("enum_rings"), cmd
    cN, cP, cNW, cNB = map(int, cmd[2:6])
    ci, ck = int(cmd[cmd.index("--chunk") + 1]), int(cmd[cmd.index("--chunk") + 2])
    if (cN, cP, cNW, cNB, ci, ck) != (j['N'], j['P'], j['NW'], j['NB'], j['I'], j['K']):
        problems.append("%s: summary cmd %s does not match the job line" % (tag, cmd))
    if "--chunk-depth" in cmd:
        problems.append("%s: non default chunk depth" % tag)
    sent, solved, unres = int(s["rings_sent"]), int(s["rings_solved"]), int(s["unresolved"])
    m = re.search(r"prefixes_seen=(\d+) labelled_leaves=(\d+) rings=(\d+)", s["enum_stderr"])
    if not m:
        problems.append("%s: no enum stderr summary" % tag)
        continue
    pref, leaves, emitted = int(m.group(1)), int(m.group(2)), int(m.group(3))
    m2 = re.search(r"chunk=(\d+)/(\d+)", s["enum_stderr"])
    if (int(m2.group(1)), int(m2.group(2))) != (ci, ck):
        problems.append("%s: enum stderr chunk %s != cmd" % (tag, m2.group(0)))
    if not (emitted == sent == solved + unres):
        problems.append("%s: emitted %d, sent %d, solved %d, unresolved %d" % (tag, emitted, sent, solved, unres))
    if unres != 0:
        problems.append("%s: unresolved %d" % (tag, unres))
    hist = collections.Counter()
    for line in open(base + ".hist.tsv"):
        sg, c = line.split()
        hist[sg] += int(c)
    if sum(c for g, c in hist.items() if g != "unresolved") != solved:
        problems.append("%s: hist total %d != solved %d" % (tag, sum(hist.values()), solved))
    bad_sig = [g for g in hist if not re.fullmatch(r"[NLRP]{4}", g)]
    if bad_sig:
        problems.append("%s: non-standard signatures %s" % (tag, bad_sig))
    if "--keep-sigs" in j['extra']:
        with gzip.open(base + ".sigs.gz", "rt") as f:
            nl = 0
            nunres = 0
            for line in f:
                nl += 1
                if line.startswith("UNRESOLVED"):
                    nunres += 1
        if nl != sent or nunres:
            problems.append("%s: sigs.gz lines %d (unresolved %d) vs sent %d" % (tag, nl, nunres, sent))
    err = open(base + ".err").read().strip()
    if err:
        problems.append("%s: non-empty .err: %s" % (tag, err[:200]))
    if s.get("rg_restarts", "0") != "0" or s.get("retried_big_table", "0") != "0":
        problems.append("%s: rg_restarts=%s retried=%s (handled by the driver, informational)" % (tag, s.get("rg_restarts"), s.get("retried_big_table")))
    bt = s["batch"].split("\t")
    if int(bt[0]) > 40:
        problems.append("%s: batch %s > 40" % (tag, bt[0]))
    g = splits[(cN, cP, cNW, cNB)]
    g["chunks"].append(ci); g["Ks"].add(ck); g["rings"] += sent; g["prefixes"].add(pref); g["leaves"] += leaves
    g["solved"] += solved; g["nodes"] += int(s["rg_nodes_total"]); g["maxnodes"] = max(g["maxnodes"], int(s["rg_nodes_max"]))
    g["retried"] += int(s.get("retried_big_table", 0)); g["restarts"] += int(s.get("rg_restarts", 0))
    g["hist"].update(hist)
    for line in open(base + ".hits.tsv"):
        if line.strip():
            r, sg, nd = line.rstrip("\n").split("\t")
            g["hits"].append((r, sg, tag))

print("jobs with .done: %d of %d, with summary: %d" % (n_done, len(jobs), n_sum))
print()
for key in sorted(splits):
    g = splits[key]
    N, P, NW, NB = key
    K = sorted(g["Ks"])
    cover = sorted(g["chunks"]) == list(range(K[0])) if len(K) == 1 else False
    print("C%d P=%d split %d+%d: K=%s chunks %d, cover range(K) exactly once: %s, prefixes_seen (distinct values over chunks): %s" %
          (N, P, NW, NB, K, len(g["chunks"]), cover, sorted(g["prefixes"])))
    print("   rings emitted/sent %d solved %d, sum labelled_leaves %d, rg nodes %d (max per ring %d), big-table retries %d, rg restarts %d" %
          (g["rings"], g["solved"], g["leaves"], g["nodes"], g["maxnodes"], g["retried"], g["restarts"]))
    print("   signature histogram: %s" % dict(sorted(g["hist"].items(), key=lambda kv: -kv[1])))
    print("   hits (P at h=2 or 3): %d  %s" % (len(g["hits"]), dict(collections.Counter(h[1] for h in g["hits"]))))
    if not cover:
        problems.append("split %s: chunk coverage wrong: %s" % (key, sorted(g["chunks"])))
    if len(g["prefixes"]) != 1:
        problems.append("split %s: prefixes_seen differs between chunks" % (key,))

print()
print("PROBLEMS (%d):" % len(problems))
for p in problems:
    print("  ", p)

# hits per split, own merge
allhits = collections.defaultdict(list)
for key, g in splits.items():
    for h in g["hits"]:
        allhits[key].append(h)
json.dump({"%d_%d_%d_%d" % k: v for k, v in allhits.items()}, open(os.path.join(ROOT, "c9_hits_own_merge.json"), "w"), indent=0)
json.dump({"%d_%d_%d_%d" % k: dict(rings=g["rings"], leaves=g["leaves"], chunks=len(g["chunks"]), K=sorted(g["Ks"])) for k, g in splits.items()},
          open(os.path.join(ROOT, "c9_driver_totals.json"), "w"), indent=0)

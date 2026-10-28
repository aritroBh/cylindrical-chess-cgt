#!/usr/bin/env python3
"""solve_rings.py RINGFILE OUTPREFIX [--rg original|copy] [--tbits 22] [--restart-batches 10] [--limit M]

Solve every ring of RINGFILE (rg tokens, one ring per line) with `rg solve 3` in batches of at most 40 positions, and write
    OUTPREFIX.sigs.gz     one signature per input line (same order; UNRESOLVED for a ring that failed)
    OUTPREFIX.hist.tsv    signature <TAB> count
    OUTPREFIX.hits.tsv    ring <TAB> signature <TAB> nodes   for every ring with a P at h=2 or h=3 (G+*2 or G+*3 a P-position)
    OUTPREFIX.summary.txt totals, failures, wall time
--rg original  : research/ring_family_proof/rg  (the original engine; exits 3 "solver table full"; the process is restarted
                 every --restart-batches batches, always BETWEEN batches, and a batch whose reply is short is redone ring by
                 ring in fresh processes with a bigger table, TBITS up to 24 = 1.4 GB)
--rg copy      : research/c9_rings/rg_copy (clears its memo when a quarter full, prints FULL instead of exiting)
Only processes started here are ever stopped, by handle.  Everything runs under nice -n 15.  Two processes at a time: this
driver and one rg.
"""
import sys, os, subprocess, time, re, gzip, collections

HERE = os.path.dirname(os.path.abspath(__file__))
RGS = {"original": os.path.join(HERE, "..", "..", "ring_family_proof", "rg"),
       "copy": os.path.join(HERE, "..", "rg_copy")}
SIGRE = re.compile(r"^([NLRP]{4}|FULL) nodes=(\d+)$")


def start(rgpath, tbits):
    return subprocess.Popen(["nice", "-n", "15", rgpath, "solve", "3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, text=True, bufsize=1, env=dict(os.environ, TBITS=str(tbits)))


def stop(p):
    try:
        p.stdin.close()
    except Exception:
        pass
    try:
        p.wait(timeout=60)
    except Exception:
        p.terminate()
        try:
            p.wait(timeout=10)
        except Exception:
            p.kill()


def batch_solve(p, rings):
    out = []
    try:
        p.stdin.write("".join(r + "\n" for r in rings))
        p.stdin.flush()
        for _ in rings:
            line = p.stdout.readline()
            m = SIGRE.match(line.strip()) if line else None
            if not m:
                break
            out.append((m.group(1), int(m.group(2))))
    except (BrokenPipeError, ValueError):
        pass
    return out


def main():
    a = sys.argv[1:]
    ringfile, prefix = a[0], a[1]
    which, tbits, restart, limit = "original", 22, 10, None
    i = 2
    while i < len(a):
        if a[i] == "--rg": which = a[i + 1]; i += 2
        elif a[i] == "--tbits": tbits = int(a[i + 1]); i += 2
        elif a[i] == "--restart-batches": restart = int(a[i + 1]); i += 2
        elif a[i] == "--limit": limit = int(a[i + 1]); i += 2
        else: raise SystemExit("unknown arg " + a[i])
    rgpath = os.path.abspath(RGS[which])
    os.makedirs(os.path.dirname(os.path.abspath(prefix)), exist_ok=True)
    rings = [l.strip() for l in open(ringfile) if l.strip()]
    if limit:
        rings = rings[:limit]
    hist = collections.Counter()
    sigs = gzip.open(prefix + ".sigs.gz", "wt", compresslevel=6)
    hits = open(prefix + ".hits.tsv", "w")
    nodes_total = nodes_max = redone = failed = restarts = 0
    t0 = time.time()
    rg = start(rgpath, tbits)
    nb = 0
    for s in range(0, len(rings), 40):
        batch = rings[s:s + 40]
        if which == "original" and nb and nb % restart == 0:          # planned restart between batches
            stop(rg); rg = start(rgpath, tbits); restarts += 1
        res = batch_solve(rg, batch)
        nb += 1
        if len(res) != len(batch) or any(r[0] == "FULL" for r in res):
            stop(rg); rg = start(rgpath, tbits); restarts += 1
            res2 = []
            for ring in batch:                                          # redo singly in fresh processes, big table
                r = None
                for tb in (24, 24):
                    q = start(rgpath, tb)
                    x = batch_solve(q, [ring]); stop(q)
                    if len(x) == 1 and x[0][0] != "FULL":
                        r = x[0]; break
                redone += 1
                res2.append(r)
            res = res2
        for ring, r in zip(batch, res):
            if r is None:
                failed += 1; hist["UNRESOLVED"] += 1; sigs.write("UNRESOLVED\n")
                sys.stderr.write("UNRESOLVED ring: %s\n" % ring)
                continue
            sig, nd = r
            hist[sig] += 1; sigs.write(sig + "\n")
            nodes_total += nd; nodes_max = max(nodes_max, nd)
            if sig[2] == "P" or sig[3] == "P":
                hits.write("%s\t%s\t%d\n" % (ring, sig, nd)); hits.flush()
        if nb % 500 == 0:
            sys.stderr.write("%s: %d / %d rings, %.0fs\n" % (os.path.basename(prefix), min(s + 40, len(rings)), len(rings), time.time() - t0))
    stop(rg)
    sigs.close(); hits.close()
    with open(prefix + ".hist.tsv", "w") as f:
        for k, v in sorted(hist.items()):
            f.write("%s\t%d\n" % (k, v))
    with open(prefix + ".summary.txt", "w") as f:
        f.write("ringfile\t%s\nrg\t%s\nrings\t%d\nsolved\t%d\nunresolved\t%d\nredone_singly\t%d\nrg_restarts\t%d\n"
                "nodes_total\t%d\nnodes_max\t%d\nwall_seconds\t%.1f\ntbits\t%d\n"
                % (ringfile, rgpath, len(rings), len(rings) - failed, failed, redone, restarts, nodes_total, nodes_max,
                   time.time() - t0, tbits))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

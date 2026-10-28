#!/usr/bin/env python3
"""solve.py CAND.tsv OUT.tsv [--tbits 22] [--big 24] -- solve every ring of CAND.tsv (first column) with the ORIGINAL rg
("./rg solve 3", built from research/ring_family_proof/rg.c), batches of at most 40 rings, nice 15, one rg at a time.
Checks that every batch returns exactly one result line per ring and exit code 0.  A failed batch (exit 3 'solver table
full', short output, timeout) is split in halves and retried; a single ring that fails is retried with a table of 2^big
entries; if that fails too it is written as UNRESOLVED (never counted as solved).
OUT.tsv rows: ring <TAB> signature <TAB> nodes <TAB> provenance.   Resumable: rings already in OUT.tsv are skipped."""
import sys, os, subprocess, time, re
HERE = os.path.dirname(os.path.abspath(__file__))
RG = os.environ.get("RGBIN", os.path.join(HERE, "rg"))
SIGRE = re.compile(r"^([NLRP]{4}) nodes=(\d+)$")

def run(rings, tbits, timeout=7200):
    try:
        p = subprocess.run(["nice", "-n", "15", RG, "solve", "3"], input="\n".join(rings) + "\n", capture_output=True, text=True,
                           env=dict(os.environ, TBITS=str(tbits)), timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    res = []
    for l in p.stdout.splitlines():
        m = SIGRE.match(l.strip())
        if not m:
            return None, "garbled:%r" % l[:60]
        res.append((m.group(1), int(m.group(2))))
    if p.returncode != 0 or len(res) != len(rings):
        return None, "rc=%d outputs=%d/%d stderr=%s" % (p.returncode, len(res), len(rings), p.stderr.strip()[:80])
    return res, ""

def solve_list(rings, tbits, big, log):
    res, why = run(rings, tbits)
    if res is not None:
        return res
    log("  batch of %d failed (%s)" % (len(rings), why))
    if len(rings) > 1:
        h = len(rings) // 2
        return solve_list(rings[:h], tbits, big, log) + solve_list(rings[h:], tbits, big, log)
    res, why = run(rings, big, timeout=14400)
    if res is not None:
        log("  single ring solved with TBITS=%d" % big)
        return res
    log("  UNRESOLVED %s (%s)" % (rings[0], why))
    return [("UNRESOLVED", 0)]

def main():
    a = sys.argv[1:]
    cand, out = a[0], a[1]
    tbits = int(a[a.index("--tbits") + 1]) if "--tbits" in a else 22
    big = int(a[a.index("--big") + 1]) if "--big" in a else 24
    rows = [l.rstrip("\n").split("\t") for l in open(cand) if l.strip()]
    done = set()
    if os.path.exists(out):
        done = set(l.split("\t")[0] for l in open(out) if l.strip())
    todo = [r for r in rows if r[0] not in done]
    t0 = time.time()
    logf = open(out + ".log", "a")
    def log(s):
        logf.write("%s %s\n" % (time.strftime("%H:%M:%S"), s)); logf.flush()
    log("start: %d rings, %d already done" % (len(todo), len(done)))
    f = open(out, "a")
    n = 0
    for i in range(0, len(todo), 40):
        b = todo[i:i + 40]
        res = solve_list([r[0] for r in b], tbits, big, log)
        assert len(res) == len(b)
        for r, (sig, nd) in zip(b, res):
            f.write("%s\t%s\t%d\t%s\n" % (r[0], sig, nd, r[1] if len(r) > 1 else ""))
        f.flush()
        n += len(b)
        log("done %d/%d  elapsed %.0fs" % (n, len(todo), time.time() - t0))
    log("finished")
    return 0

if __name__ == "__main__":
    sys.exit(main())

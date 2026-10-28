#!/usr/bin/env python3
"""drive.py -- pipe the rings of enum_rings through a copy of rg ("rg_copy solve 3") in safe batches.

usage: drive.py N P NW NB OUTPREFIX [--chunk I K] [--batch 40] [--tbits 22] [--max-rings M] [--keep-sigs]

  enum_rings N P NW NB [--chunk I K]  |  rg_copy solve 3   (both under nice -n 15)

* rg_copy is rg.c with two changes (see rg_copy.c): the memo table is cleared between positions when it is a
  quarter full, and a position that would fill 70% of the table prints "FULL" instead of exiting with code 3.
* Rings are sent in batches of --batch (default 40) lines and exactly that many reply lines are read back.  A
  short reply (rg died) or a "FULL" reply is retried ring by ring in a fresh rg with a larger table (TBITS 24);
  a ring that still fails is recorded as FULL/ERR in the summary and is NOT counted as solved.
* Output files (OUTPREFIX is a path prefix):
    OUTPREFIX.hist.tsv      signature<TAB>count   (signature = outcome of G+*h for h=0..3, e.g. NNPN = *2)
    OUTPREFIX.hits.tsv      every ring whose signature has a P at h=2 or h=3 (i.e. *2 or *3, or G+*2 / G+*3 a P-position):
                            ring<TAB>signature<TAB>nodes
    OUTPREFIX.examples.tsv  the first 5 rings of every signature class
    OUTPREFIX.sigs.gz       (only with --keep-sigs) one signature per line, in enumeration order of enum_rings
    OUTPREFIX.summary.txt   totals, node counts, timing, failures
"""
import sys, os, subprocess, time, re, gzip, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ENUM = os.path.join(HERE, "enum_rings")
RG = os.path.join(HERE, "rg_copy")
SIGRE = re.compile(r"^([NLRP]{4}|FULL) nodes=(\d+)$")


def start_rg(tbits):
    env = dict(os.environ, TBITS=str(tbits))
    return subprocess.Popen(["nice", "-n", "15", RG, "solve", "3"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, text=True, bufsize=1, env=env)


def stop_rg(p):
    try:
        p.stdin.close()
    except Exception:
        pass
    try:
        p.wait(timeout=30)
    except Exception:
        p.terminate()          # only the child we started, by handle
        try:
            p.wait(timeout=10)
        except Exception:
            p.kill()


def solve_batch(rg, rings):
    """returns (list of (sig,nodes) or None for missing, rg_alive)"""
    out = []
    try:
        rg.stdin.write("".join(r + "\n" for r in rings))
        rg.stdin.flush()
        for _ in rings:
            line = rg.stdout.readline()
            if not line:
                break
            m = SIGRE.match(line.strip())
            if not m:
                break
            out.append((m.group(1), int(m.group(2))))
    except (BrokenPipeError, ValueError):
        pass
    alive = len(out) == len(rings)
    return out, alive


def solve_single_big(ring, tbits=24):
    rg = start_rg(tbits)
    try:
        res, ok = solve_batch(rg, [ring])
    finally:
        stop_rg(rg)
    return res[0] if ok and res else None


def main():
    a = sys.argv[1:]
    if len(a) < 5:
        print(__doc__)
        return 2
    n, p, nw, nb, prefix = a[0], a[1], a[2], a[3], a[4]
    chunk = (0, 1)
    batch = 40
    tbits = 22
    max_rings = None
    keep = False
    i = 5
    while i < len(a):
        if a[i] == "--chunk":
            chunk = (int(a[i + 1]), int(a[i + 2])); i += 3
        elif a[i] == "--batch":
            batch = int(a[i + 1]); i += 2
        elif a[i] == "--tbits":
            tbits = int(a[i + 1]); i += 2
        elif a[i] == "--max-rings":
            max_rings = int(a[i + 1]); i += 2
        elif a[i] == "--keep-sigs":
            keep = True; i += 1
        else:
            print("unknown argument", a[i]); return 2
    batch = min(batch, 40)
    os.makedirs(os.path.dirname(os.path.abspath(prefix)), exist_ok=True)
    cmd = ["nice", "-n", "15", ENUM, n, p, nw, nb, "--chunk", str(chunk[0]), str(chunk[1])]
    enum = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1 << 16)
    rg = start_rg(tbits)
    hist = collections.Counter()
    ex_count = collections.Counter()
    hits = open(prefix + ".hits.tsv", "w")
    exs = open(prefix + ".examples.tsv", "w")
    sigs = gzip.open(prefix + ".sigs.gz", "wt", compresslevel=6) if keep else None
    total = nodes = maxnodes = retried = failed = restarts = 0
    t0 = time.time()
    buf = []
    done = False

    def record(ring, sig, nd):
        nonlocal nodes, maxnodes
        hist[sig] += 1
        nodes += nd
        if nd > maxnodes:
            maxnodes = nd
        if sig[:1] != "F" and (sig[2] == "P" or sig[3] == "P"):
            hits.write("%s\t%s\t%d\n" % (ring, sig, nd))
        if ex_count[sig] < 5:
            ex_count[sig] += 1
            exs.write("%s\t%s\t%d\n" % (ring, sig, nd))
        if sigs is not None:
            sigs.write(sig + "\n")

    def flush(rings):
        nonlocal rg, retried, failed, restarts
        if not rings:
            return
        res, alive = solve_batch(rg, rings)
        if not alive:                                  # rg died or garbled: restart, redo the rest singly
            stop_rg(rg)
            rg = start_rg(tbits)
            restarts += 1
        for k, ring in enumerate(rings):
            r = res[k] if k < len(res) else None
            if r is None or r[0] == "FULL":
                retried += 1
                r = solve_single_big(ring)
                if r is None or r[0] == "FULL":
                    failed += 1
                    sys.stderr.write("UNRESOLVED ring: %s\n" % ring)
                    r = ("ERR!", 0) if r is None else ("FULL", r[1])
                    hist["unresolved"] += 1
                    if sigs is not None:
                        sigs.write("UNRESOLVED\n")      # keeps the line numbers aligned with the enumeration order
                    continue
            record(ring, r[0], r[1])

    for line in enum.stdout:
        ring = line.strip()
        if not ring:
            continue
        buf.append(ring)
        total += 1
        if len(buf) >= batch:
            flush(buf); buf = []
        if max_rings is not None and total >= max_rings:
            break
    flush(buf)
    if max_rings is not None:
        enum.terminate()                              # our own child
    enum.wait()
    estderr = enum.stderr.read()
    stop_rg(rg)
    secs = time.time() - t0
    hits.close(); exs.close()
    if sigs is not None:
        sigs.close()
    with open(prefix + ".hist.tsv", "w") as f:
        for s, c in sorted(hist.items()):
            f.write("%s\t%d\n" % (s, c))
    with open(prefix + ".summary.txt", "w") as f:
        f.write("cmd\t%s\n" % " ".join(cmd[2:]))
        f.write("rings_sent\t%d\n" % total)
        f.write("rings_solved\t%d\n" % sum(c for s, c in hist.items() if s != "unresolved"))
        f.write("unresolved\t%d\n" % failed)
        f.write("retried_big_table\t%d\n" % retried)
        f.write("rg_restarts\t%d\n" % restarts)
        f.write("rg_nodes_total\t%d\nrg_nodes_max\t%d\n" % (nodes, maxnodes))
        ct = os.times()
        f.write("cpu_seconds_children\t%.1f\n" % (ct.children_user + ct.children_system))   # rg + enum_rings
        f.write("cpu_seconds_driver\t%.1f\n" % (ct.user + ct.system))
        f.write("wall_seconds\t%.1f\n" % secs)
        f.write("rings_per_second\t%.2f\n" % (total / secs if secs > 0 else 0))
        f.write("enum_stderr\t%s\n" % estderr.strip().replace("\n", " | "))
        f.write("batch\t%d\ttbits\t%d\n" % (batch, tbits))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

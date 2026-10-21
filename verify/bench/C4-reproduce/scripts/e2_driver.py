"""C4 verifier: exact replica of bench.conventions main() step 5 (instances under the
e.p.-aware test), run from a byte-identical copy of bench/ (cwd = C4-reproduce/run).
Uses bench.conventions._b_task unchanged. Adds only a counting wrapper around
pawns.ep_capturable (same return value) to count positions where the e.p.-aware
test actually withholds 'passed' status from a pawn.
usage: e2_driver.py EP_ROOT OUT_JSON [jobs]"""
import os, sys
EP = os.path.abspath(sys.argv[1])
sys.path.insert(0, EP)
import json, random, time
from collections import Counter
from multiprocessing import get_context
from cylcgt import pawns, cgt
import bench.conventions as CV
import bench.verify as V
assert pawns.__file__.startswith(EP), pawns.__file__
assert CV.pawns is pawns and V.pawns is pawns and V.cgt is cgt
assert hasattr(pawns, "PASSED_RESPECTS_EP")
import crosscheck
print("cylcgt:", pawns.__file__, "| bench:", CV.__file__, "| crosscheck:", crosscheck.__file__, flush=True)

HITS = [0]
_orig = pawns.ep_capturable
def counting(board, pos, side, square):
    r = _orig(board, pos, side, square)
    if r:
        HITS[0] += 1
    return r
pawns.ep_capturable = counting

def task(arg):
    h0 = HITS[0]
    sp, rid, res = CV._b_task(arg)
    return sp, rid, res, HITS[0] - h0, pawns.PASSED_RESPECTS_EP, pawns.RACE_RULE, os.getpid()

if __name__ == "__main__":
    out, jobs = sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 6
    t0 = time.time()
    rng = random.Random(5)                      # conventions --seed default 5
    tasks = []
    for sp in ("train", "val", "test", "test_heldout"):
        rows = [json.loads(x) for x in (CV.DATA / f"{sp}.jsonl").read_text().splitlines()]
        if sp == "train":
            rows = rng.sample(rows, min(3000, len(rows)))   # --train default 3000
        tasks += [(sp, r) for r in rows]
    inst, bad, hits, flags, rules, pids = Counter(), [], Counter(), Counter(), Counter(), set()
    ids = {}
    n = 0
    with get_context("fork").Pool(jobs) as pool:
        for sp, rid, res, h, flag, rule, pid in pool.imap_unordered(task, tasks, chunksize=20):
            n += 1
            inst[f"{sp} (agree)"] += res["count"]
            inst[f"{sp} (total)"] += 1
            hits[sp] += h
            flags[flag] += 1
            rules[rule] += 1
            pids.add(pid)
            ids.setdefault(sp, []).append(rid)
            if not res["count"]:
                bad.append(rid)
            if n % 500 == 0:
                print(f"  {n}/{len(tasks)} rows, {len(bad)} disagreements [{time.time()-t0:.0f}s]", flush=True)
    res = {"instances": dict(sorted(inst.items())), "disagreements": bad,
           "ep_capturable_true_calls_by_split": dict(hits),
           "PASSED_RESPECTS_EP_after_task": {str(k): v for k, v in flags.items()},
           "RACE_RULE_after_task": dict(rules), "worker_pids": len(pids),
           "train_ids_sorted": sorted(ids.get("train", [])), "seconds": round(time.time() - t0)}
    open(out, "w").write(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "train_ids_sorted"}, indent=1))

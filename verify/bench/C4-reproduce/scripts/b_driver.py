"""C4 verifier: exact replica of bench.verify main() checks A (only to consume the
rng identically) and B, from a byte-identical copy of bench/ (cwd = C4-reproduce/run),
with the main (textbook) cylcgt. Uses bench.verify functions unchanged.
usage: b_driver.py OUT_JSON"""
import sys, json, random, time
from collections import Counter
from multiprocessing import get_context
from cylcgt import pawns
import bench.verify as V
from bench.prompts import load

if __name__ == "__main__":
    out = sys.argv[1]
    assert not hasattr(pawns, "PASSED_RESPECTS_EP"), pawns.__file__
    print("cylcgt:", pawns.__file__, "| bench:", V.__file__, flush=True)
    t0 = time.time()
    rng = random.Random(99)
    comps = load(V.DATA / "components.jsonl")
    s, b = V.check_components(comps, rng, 300)
    print("A:", dict(s), "bad:", b, f"[{time.time()-t0:.0f}s]", flush=True)
    splits = ["train", "val", "test", "test_heldout"]
    rows = {sp: load(V.DATA / f"{sp}.jsonl") for sp in splits}
    tasks = []
    for sp in splits:
        rs = rows[sp]
        if sp == "train":
            rs = rng.sample(rs, min(3000, len(rs)))
        triple = set(rng.sample(range(len(rs)), min(len(rs), 250)))
        tasks += [(sp, r, ("count", "mover", "opponent") if i in triple else ("count",)) for i, r in enumerate(rs)]
    summary, bad, ids, n = Counter(), [], {}, 0
    with get_context("spawn").Pool(4, initializer=V._init_worker) as pool:
        for sp, rid, res in pool.imap_unordered(V.b_task, tasks, chunksize=25):
            n += 1
            ids.setdefault(sp, []).append(rid)
            for rule, ok in res.items():
                summary[f"B {sp} rule={rule} (agree)"] += ok
                summary[f"B {sp} rule={rule} (total)"] += 1
                if not ok:
                    bad.append(("B", rid, rule))
            if n % 500 == 0:
                print(f"  {n}/{len(tasks)} rows, {len(bad)} disagreements [{time.time()-t0:.0f}s]", flush=True)
    res = {"A": dict(s), "A_bad": b, "B": dict(sorted(summary.items())), "B_bad": bad,
           "train_ids_sorted": sorted(ids.get("train", [])), "seconds": round(time.time() - t0)}
    open(out, "w").write(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "train_ids_sorted"}, indent=1))

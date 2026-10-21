"""Reproduction only (NOT the decisive check): run the worker's own E2 comparison
(bench.verify.check_cylcgt under the e.p.-aware cylcgt from the ep-wt worktree) on one split.
Writes nothing outside verify/bench/C4-refute/results."""
import json, os, sys, time
EW = "/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt"
sys.path.insert(0, EW)
sys.path.insert(1, "/Users/aritro/Downloads/Research/Chessendgames")
sys.dont_write_bytecode = True
from cylcgt import pawns
assert pawns.PASSED_RESPECTS_EP is True and EW in pawns.__file__
from bench.verify import check_cylcgt
split = sys.argv[1]
rows = [json.loads(x) for x in open(f"/Users/aritro/Downloads/Research/Chessendgames/bench/data/{split}.jsonl")]
t0 = time.time()
ok = sum(check_cylcgt(r, ("count",))["count"] for r in rows)
out = {"split": split, "agree": ok, "total": len(rows), "cylcgt": pawns.__file__, "seconds": round(time.time() - t0)}
json.dump(out, open(f"/Users/aritro/Downloads/Research/Chessendgames/verify/bench/C4-refute/results/worker_e2_{split}.json", "w"))
print(out)

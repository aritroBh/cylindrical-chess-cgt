"""Count (position, rule, e.p.) cases whose cylcgt outcome vector is constant, and ERR entries."""
import gzip, json, os
D = "/Users/aritro/Downloads/Research/Chessendgames/sumtest/data"
tot = const = err = 0; distinct = set()
for n in sorted(os.listdir(D)):
    if n.startswith("cylcgt__"):
        o = json.load(gzip.open(os.path.join(D, n), "rt"))["outcomes"]
        tot += len(o); const += sum(1 for v in o.values() if len(set(v)) == 1)
        err += sum(1 for v in o.values() if v.startswith("ERR")); distinct |= set(o.values())
print("cases", tot, "constant-vector cases", const, f"({const/tot:.1%})", "non-constant", tot - const,
      "-> non-constant predictions", (tot - const) * 15, "ERR entries", err, "distinct vectors overall", len(distinct))

"""G_lo / G_hi of the oracle value with ONLY a certificate's support fixed
(every other terminal free in [-2BIG, +2BIG]); canonical form and outcome.
    PYTHONPATH=. .venv/bin/python -m realchess.certify.support_bound <cert.json> [lower|upper]"""
import json
import sys

from cylcgt import cgt
from cylcgt.pawns import Pos

from realchess.oracle_value import Terminals

from .certify_check import cgt_test, direct_test

d = json.load(open(sys.argv[1]))
test = sys.argv[2] if len(sys.argv) > 2 else "lower"
T = Terminals(Pos.parse(d["component"]))
byname = {str(t): t for t in T.terms}
fixed = {byname[s["terminal"]]: s["class"] for s in d["tests"][test]["support"]}
ok, g = cgt_test(T, fixed, test, cgt.nimber(2))
print(json.dumps({"cert": sys.argv[1], "test": test, "support": len(fixed), "excludes_star2": ok,
                  "bound": cgt.show(g), "bound_outcome": cgt.outcome(g),
                  "direct": {"star2_test": direct_test(T, fixed, test),
                             "White first wins bound": direct_test(T, fixed, test, heap=0, first="W"),
                             "Black first wins bound": direct_test(T, fixed, test, heap=0, first="B")}}))

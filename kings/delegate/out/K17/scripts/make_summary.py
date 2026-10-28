import json
S = dict(
 task="K17: isolated counterexample for (V1a) of Theorem 1.14",
 result="counterexample found for the 'no checks' clause; none found for clause (E)",
 reproduce=dict(
  build="cc -O2 -o bin/kp kings/kpsolve.c -lpthread; cc -O2 -o bin/kp_p kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread",
  headline_real="printf 'Ka2 kb4 Pa3 pa4 Pd2 pe3 b -\\nKa2 kb5 Pa3 pa4 Pd2 pe3 b -\\nKa2 kb5 Pa3 pa4 Pd2 pe3 w -\\n' | bin/kp_p --board cyl:6x6 --pmodel --moves",
  headline_frozen="printf 'Ka1 kb4 Pa3 pa4 Pd2 pe3 b -\\nKa1 kb5 Pa3 pa4 Pd2 pe3 b -\\nKa1 kb5 Pa3 pa4 Pd2 pe3 w -\\n' | bin/kp --board cyl:6x6 --frozen --moves",
  check2="PYTHONPATH=<repo> python scripts/check2.py logs/examples_A.json logs/check2_A.json",
  searchA="HEAVY=0 python scripts/search_A.py cyl:6x6 3,4 3  (also flat:6x6 3,4,5 2; cyl:7x6 3,4,5 2; cyl:5x6 3 3)",
  searchA_real="python scripts/search_A_real.py cyl:6x6 3,4 2; python scripts/search_A_real2.py cyl:6x6",
  searchB="python scripts/search_B3.py flat:8x6 2,3,5,6 5 f86_5; python scripts/search_B3.py flat:8x6 2,3,5,6 4 f86_4b; python scripts/search_B2.py flat:6x6 2,3,4,5 3 f66_3"),
)
json.dump(S, open("summary.json", "w"), indent=1)

import sys
sys.path.insert(0, ".")
from stopsA import *
# graphs given as {name: (L, R)} lists, root 0
G = {
 "0": ([[]], [[]]),
 "on": ([[0]], [[]]),
 "off": ([[]], [[0]]),
 "over={0|over}": ([[1], []], [[0], []]),
 "under={under|0}": ([[0], []], [[1], []]),
 "*={0|0}": ([[1], []], [[1], []]),
 "1": ([[1], []], [[], []]),
 "2": ([[1], [2], []], [[], [], []]),
 "-1": ([[], []], [[1], []]),
 "1/2={0|1}": ([[1], [], [1]], [[2], [], []]),
 "up={0|*}": ([[1], [2], []][:0] or [[1], [], [1]], [[2], [], []]),
}
# fix up properly
G["up={0|*}"] = ([[1], [], [1]], [[2], [], [1]])  # node0: L->0(node1), R->*(node2); node2 = {0|0}; node1 = 0
G["up={0|*}"] = ([[1], [], [1]], [[2], [], [1]])
G["{on|off}"] = ([[1], [1], []], [[2], [], [2]])
G["{0|on}"] = ([[1], [], [2]][:0] or [[1], [], [2]], [[2], [], []])
G["{off|0}"] = ([[1], [], []], [[2], [], []])
G["on+1? {on,1|}"] = ([[0, 1], [2], []], [[], [], []])
G["{1|-1}"] = ([[1], [], []], [[2], [], []])
st = Stops(3, 5)
for name, (L, R) in G.items():
    key = quotient(L, R, 0)
    if not is_stopper(*key_to_graph(key)):
        print(name, "NOT A STOPPER"); continue
    print("%-18s LS=%s RS=%s lam,rho=%s" % (name, fmt(st.LS(key)), fmt(st.RS(key)), tuple(fmt(v) for v in reserves(key, 12))))

"""Named games as graphs; prints graph lines (name \t line) for stopsA/stopsB."""
G = {}
def add(name, L, R): G[name] = (L, R)
def line(L, R):
    n = len(L); s = [str(n)]
    for i in range(n):
        s.append(str(sum(1 << j for j in L[i]))); s.append(str(sum(1 << j for j in R[i])))
    return " ".join(s)
add("0", [[]], [[]])
add("on", [[0]], [[]])
add("off", [[]], [[0]])
add("over {0|over}", [[1], []], [[0], []])
add("under {under|0}", [[0], []], [[1], []])
add("* {0|0}", [[1], []], [[1], []])
add("1 {0|}", [[1], []], [[], []])
add("-1 {|0}", [[], []], [[1], []])
add("2 {1|}", [[1], [2], []], [[], [], []])
add("-2 {|-1}", [[], [], []], [[1], [2], []])
add("1/2 {0|1}", [[1], [], [1]], [[2], [], []])
add("up {0|*}", [[1], [], [1]], [[2], [], []]) if False else None
# up = {0|*}: nodes 0:{1|2}, 1: zero, 2: * = {1|1}
add("up {0|*}", [[1], [], [1]], [[2], [], [1]])
add("down {*|0}", [[2], [], [1]], [[1], [], [1]])
add("+-1 {1|-1}", [[1], [3], [], []], [[2], [], [3], []]) if False else None
# +-1: nodes 0:{1|2}, 1: one {3|}, 2: minus one {|3}, 3: zero
add("+-1 {1|-1}", [[1], [3], [], []], [[2], [], [3], []])
add("{on|off}", [[1], [1], []], [[2], [], [2]]) if False else None
# {on|off}: nodes 0:{1|2}, 1: on {1|}, 2: off {|2}
add("{on|off}", [[1], [1], []], [[2], [], [2]])
add("{0|off}", [[1], []], [[2], [], [2]]) if False else None
add("{0|off}", [[1], [], []], [[2], [], [2]])
add("{on|0}", [[1], [1], []], [[2], [], []]) if False else None
add("{on|0}", [[1], [1], []], [[2], [], []])
# K21 'what fails' stopper S: a:L->c, R->b,c ; b: R->a,b ; c: L->b,c   (a=0,b=1,c=2)
add("K21 S_abc", [[2], [], [1, 2]], [[1, 2], [0, 1], []])
# K21 first example S3: 0:{2/1,2}|1:{/0,1}|2:{1,2/}  (same graph)
# {0,over|} ... a few more loopy: {over|}, {|under}
add("{over|}", [[1, 2], [], []], [[], [], []]) if False else None
add("{over|} (over=1,0=2)", [[1], [2], []], [[], [2], [1]]) if False else None
if __name__ == "__main__":
    for k, v in G.items():
        if v is not None: print("%s\t%s" % (k, line(*v)))

"""K55 part 2: the D-game candidates with a decisive Black threat: tD = {0 || 0 | ⊖} (root A) and uD = {0 | tD} (root B),
and for comparison tA = {0 || 0 | off}, tB = {0 | tA}.  r(H + T) by games55.rsolve2 (terminals end the play).
usage: python3 candsD.py <za outputs...> -- <test files...>"""
import sys
from games55 import readT, rsolve2, G, node
from compare55 import read_za
i = sys.argv.index('--'); Z = {}
for f in sys.argv[1:i]: Z.update(read_za(f))
tests = [t for f in sys.argv[i + 1:] for t in readT(f)]
tD = ([[1], [], [1]], [[2], [], [-2]])                 # 0: {0 | 2}, 1: zero, 2: {0 | ⊖}
uD = ([[1], [], [1], [2]], [[3], [], [-2], [2]])       # 0: {0 | 3}, 3 = tD with its nodes 3 -> {0 | 2}
uD = ([[1], [], [1], [1]], [[3], [], [-2], [2]])
tA = node([G['0']], [node([G['0']], [G['off']])]); tB = node([G['0']], [tA])
print('battery: %d tests, %d results per root' % (len(tests), 2 * len(tests)))
for name, H in (('tD = {0||0|⊖}', tD), ('uD = {0|tD}', uD), ('tA = {0||0|off}', tA), ('tB = {0|tA}', tB)):
    for r in (0, 1):
        bad = []
        for tn, T in tests:
            rr = rsolve2(H, T)
            for s, si in (('w', 0), ('b', 1)):
                if rr[si] != Z[(tn, r, s)][0]: bad.append('%s/%s(Z %s, H %s)' % (tn, s, Z[(tn, r, s)][0], rr[si]))
        print('%-16s root %s: mismatches %3d  %s' % (name, 'AB'[r], len(bad), ' '.join(bad[:10])))

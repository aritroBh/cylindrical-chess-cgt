import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, greedy
tops=[pm.parse(l.split('#')[0].strip()) for l in open(sys.argv[1])]
tops.sort(key=lambda p:-greedy.D(p))
for p in tops: greedy.add(p)
print('\n'.join(greedy.render(tops)))

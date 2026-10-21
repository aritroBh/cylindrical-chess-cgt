import sys, collections
sys.path.insert(0, '.')
from png2 import read_png
for name in sys.argv[1:]:
    w, h, px = read_png(name)
    c = collections.Counter(px(x, y) for y in range(0, h, 2) for x in range(0, w, 2))
    print(name.split('/')[-1], w, h, c.most_common(8))

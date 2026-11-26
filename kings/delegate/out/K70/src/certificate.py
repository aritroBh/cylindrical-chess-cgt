"""Produce a finite, local chessboard certificate using a restricted repertoire."""

from repertoire import *
from collections import namedtuple, deque

path = next(
    (Path(s) for s in sys.argv[1:] if s.endswith(".txt")),
    here / ("draw-policy.txt" if hold else "policy.txt"),
)
policy = read_policy(path)
for a in action:
    lib.toggle(a, a in policy)
assert works()
Row = namedtuple("Row", "i m z area")
rows = []
zones = defaultdict(int)


def safe(i, known):
    if i < 0:
        return ALL
    d = ds[i]
    valid, check, _ = geom(d)
    if hold and d[3] == d[4] == X:
        return valid
    bad = legal = 0
    for m, h, a, king in es[i]:
        fail = a & ~(known[h] if h >= 0 else 0)
        bad |= dilation(fail) if king else fail
        legal |= dilation(a) if king else a
    return (valid & ~bad & (ALL if hold else legal | check)) | (
        fortress(d) if hold else 0
    )


def allowable(i):
    v, ch, _ = geom(ds[i])
    return v & ~ch


if not hold:
    # Irreversible moves strictly lower total remaining pawn travel.
    groups = defaultdict(list)
    for a in sorted(policy):
        i, m, z, area = action[a]
        groups[ds[i][2:5]].append(a)
    for key, aa in sorted(groups.items(), key=lambda kv: weight((0, 0, *kv[0], 64))):
        while True:
            opts = []
            for a in aa:
                i, m, z, area = action[a]
                wanted = area & allowable(i) & ~zones[i]
                if not wanted:
                    continue
                src = wanted & safe(z, zones)
                if src:
                    ceiling = wanted & (ALL if z < 0 else lib.zone(z))
                    opts.append(
                        (
                            (src == ceiling, src.bit_count(), m[0] != "K"),
                            Row(i, m, z, src),
                        )
                    )
            if not opts:
                break
            _, r = max(opts, key=lambda item: item[0])
            zones[r.i] |= r.area
            rows.append(r)
    assert all(safe(i, zones) & a == a for i, a in enumerate(targets))
else:
    full = defaultdict(int, ((i, lib.zone(i)) for i in range(len(ds))))
    for a in sorted(policy):
        i, m, z, area = action[a]
        area &= allowable(i) & ~zones[i] & safe(z, full)
        if area:
            rows.append(Row(i, m, z, area))
            zones[i] |= area
    # Bare opponent and genuine stalemate are additional terminal predicates.
    for i, d in enumerate(ds):
        if d[0] and d[3] == d[4] == X:
            zones[i] = allowable(i)
    assert all(safe(i, zones) & a == a for i, a in enumerate(targets))

# Follow the printed strategy from the given initial zones and record its edges.
at = defaultdict(list)
for n, r in enumerate(rows):
    at[r.i].append(n)
out = defaultdict(lambda: defaultdict(set))
used = defaultdict(int)
pending = deque((-(i + 1), i, a) for i, a in enumerate(targets))
while pending:
    parent, i, area = pending.popleft()
    if i < 0:
        out[parent]["end"].add("P")
        continue
    if hold and ds[i][3] == ds[i][4] == X:
        out[parent]["end"].add("0")
        continue
    if hold and area & fortress(ds[i]):
        out[parent]["end"].add("F")
        area &= ~fortress(ds[i])
        if not area:
            continue
    legal = 0
    for m, h, a, king in es[i]:
        legal |= dilation(a) if king else a
        reachable = (dilation(area) if king else area) & a
        if not reachable:
            continue
        assert h >= 0, (ds[i], m)
        left = reachable
        for n in at[h]:
            r = rows[n]
            part = left & r.area
            if not part:
                continue
            out[parent][m].add(n)
            left &= ~part
            if part & ~used[n]:
                pending.append((n, r.z, part & ~used[n]))
                used[n] |= part
        if left:
            assert hold
            valid, _, chk = geom(ds[h])
            assert ds[h][3] == ds[h][4] == X or (
                not chk and not any(ma & left for _, _, ma, _ in es[h])
            )
            out[parent][m].add("0" if ds[h][3] == ds[h][4] == X else "S")
    if area & ~legal:
        out[parent]["end"].add("S" if hold else "M")


# A paper-friendly area description. Each rectangle is files x ranks. Cells
# impossible in the diagram are don't-cares, as are unneeded safe cells.
def rects(required, allowed):
    items = []
    while required:
        top = None
        for a in range(8):
            for b in range(a, 8):
                files = (2 ** (b - a + 1) - 1) << a
                z = 0
                start = 0
                for r in range(9):
                    bits = files << (r * 8)
                    if r < 8 and bits & allowed == bits:
                        z |= bits
                        continue
                    useful = z & required
                    if useful:
                        cells = list(squares(useful))
                        lo = min(v % 8 for v in cells) + 8 * min(v // 8 for v in cells)
                        hi = max(v % 8 for v in cells) + 8 * max(v // 8 for v in cells)
                        label = name(lo) if lo == hi else name(lo) + "–" + name(hi)
                        score = (
                            useful.bit_count() / max(2, len(label)),
                            useful.bit_count(),
                            -z.bit_count(),
                        )
                        if top is None or score > top[0]:
                            top = (score, label, z)
                    z = 0
                    start = r + 1
        assert top
        items.append(top[1])
        required &= ~top[2]
    return ",".join(items)


def format_area(area, domain):
    if area == domain:
        return "*"

    def fmt(mask_):
        return rects(mask_, mask_ | (ALL & ~domain))

    a = fmt(area)
    b = "!" + fmt(domain & ~area)
    return a if len(a) <= len(b) else b


def table():
    # Material blocks. Every arrow to a numerical row is explicit.
    order = sorted(used, key=lambda n: (weight(ds[rows[n].i]), ds[rows[n].i][2:5], n))
    idx = {n: i + 1 for i, n in enumerate(order)}

    def targets_(vs):
        return ",".join(
            [str(i) for i in sorted(idx[v] for v in vs if isinstance(v, int))]
            + sorted(v for v in vs if isinstance(v, str))
        )

    def routes(n):
        return " ".join(m + "→" + targets_(vs) for m, vs in out[n].items())

    print("ENTRY")
    for i in range(len(targets)):
        print(name(ds[i][2]), routes(-i - 1))
    for k, ns in groupby(order, key=lambda n: ds[rows[n].i][2:5]):
        print(
            "\n**"
            + ("White pawn %s · Black pawns %s, %s" % tuple(map(name, k)))
            + "**\n"
        )
        print("| # | King | Zone | Play | Replies |\n|---:|:---:|:---|:---|:---|")
        for n in ns:
            i, m, z, area = rows[n]
            t, j, w, b, c, e = ds[i]
            ep = " (ep " + name(e) + ")" if e != X else ""
            if m.startswith("K") and sq(m[1:]) in ((b, c) if hold else (w,)):
                m = "Kx" + m[1:]
            print(
                "|",
                idx[n],
                "|",
                name(j) + ep,
                "|",
                format_area(used[n], allowable(i)),
                "|",
                m,
                "|",
                routes(n),
                "|",
            )
    print("SIZE", len(used), sum(m.bit_count() for m in used.values()))


if __name__ == "__main__":
    table()

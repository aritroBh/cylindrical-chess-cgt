"""grow.py -- driver for the local-growth search (no worker processes of its own).

  python3 grow.py init                 seeds_all.txt + cache.tsv (seeds count as round 0)
  python3 grow.py gen R [LIMIT]        candidates of round R (neighbours of the *3 found up to round R-1),
                                       written as cand_rR_{a,b}.txt  (two interleaved halves for two rg workers)
  python3 grow.py merge R              read out_rR_{a,b}.txt back into cache.tsv
  python3 grow.py status               counts

cache.tsv columns: ring(canonical) sig nodes status round move_class parent
"""
import sys, os, re, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from growlib import *

CACHE = 'cache.tsv'
CHUNK = 100


def load_cache():
    d = {}
    if os.path.exists(CACHE):
        for l in open(CACHE):
            f = l.rstrip('\n').split('\t')
            if len(f) >= 7:
                d[f[0]] = f
    return d


def kind(sig):
    """nimber index, 'N8' (all N), or 'non' / 'ABORT'"""
    if sig == 'ABORT' or sig == 'ERR':
        return sig
    if re.fullmatch(r'N*PN*', sig):
        return '*%d' % sig.index('P')
    if re.fullmatch(r'N+', sig):
        return 'allN'
    return 'non'


def seeds_for_round(R, cache):
    """rings that are *3 and were found in round R-1 (round 0 = the known seeds)"""
    return sorted(k for k, f in cache.items() if f[1] == 'NNNPNNNN' and int(f[4]) == R - 1)


def cmd_init():
    seeds = [l.split('\t')[0] for l in open('seeds_all.txt') if l.strip()]
    with open(CACHE, 'w') as o:
        for s in seeds:
            c = fmt(canon(parse(s)))
            o.write('\t'.join([c, 'NNNPNNNN', '0', 'OK', '0', 'seed', '-']) + '\n')
    print('init', len(seeds), 'seeds')


def cmd_gen(R, limit=None, quota=None):
    """limit: cap on the total (priority order, random sample inside the class that does not fit);
    quota: {class: max count} random sample (seed 12345) per class, applied before the limit"""
    cache = load_cache()
    seeds = seeds_for_round(R, cache)
    ringonly = os.environ.get('RINGONLY') == '1'      # round 3: only genuine rings (every file occupied)
    if ringonly:
        seeds = [s for s in seeds if is_ring(parse(s))]
    cands = {}      # canonical string -> (class_rank, class, parent)
    rank = {n: i for i, (n, _) in enumerate(MOVE_CLASSES)}
    for s in seeds:
        sr = parse(s)
        for name, q in neighbours(sr):
            if ringonly and not is_ring(q):
                continue
            c = fmt(canon(q))
            if c in cache:
                continue
            if c not in cands or rank[name] < cands[c][0]:
                cands[c] = (rank[name], name, s)
    items = sorted(cands.items(), key=lambda kv: (kv[1][0], len(kv[0].split()), kv[0]))
    tot = len(items)
    avail = collections.Counter(v[1] for _, v in items)
    if quota:
        random.seed(12345)
        byc = collections.defaultdict(list)
        for kv in items:
            byc[kv[1][1]].append(kv)
        items = []
        for name, _ in MOVE_CLASSES:
            lst = byc.get(name, [])
            q = quota.get(name, len(lst))
            items += lst if len(lst) <= q else random.sample(lst, q)
        items.sort(key=lambda kv: (kv[1][0], len(kv[0].split()), kv[0]))
    if limit is not None and len(items) > limit:
        random.seed(12345)
        keep, byc = [], collections.defaultdict(list)
        for kv in items:
            byc[kv[1][0]].append(kv)
        for rk in sorted(byc):
            room = limit - len(keep)
            if room <= 0:
                break
            lst = byc[rk]
            if len(lst) <= room:
                keep += lst
            else:
                keep += random.sample(lst, room)
        items = keep
    # order for memo locality: by (n, parent, class), then chunk-interleave over two workers
    items.sort(key=lambda kv: (len(kv[0].split()), kv[1][2], kv[1][0], kv[0]))
    parts = ([], [])
    for i in range(0, len(items), CHUNK):
        parts[(i // CHUNK) % 2].extend(items[i:i + CHUNK])
    with open('meta_r%d.tsv' % R, 'w') as m:
        for c, (rk, name, par) in items:
            m.write('%s\t%s\t%s\n' % (c, name, par))
    for tag, part in zip('ab', parts):
        with open('cand_r%d_%s.txt' % (R, tag), 'w') as o:
            for c, _ in part:
                o.write(c + '\n')
    byclass = collections.Counter(v[1] for _, v in items)
    print('round', R, 'seeds', len(seeds), 'candidates available', tot, dict(avail), 'written', len(items), dict(byclass))


def cmd_merge(R):
    cache = load_cache()
    meta = {}
    for l in open('meta_r%d.tsv' % R):
        c, name, par = l.rstrip('\n').split('\t')
        meta[c] = (name, par)
    new = 0; bad = 0
    with open(CACHE, 'a') as o:
        for tag in 'ab':
            fn = 'out_r%d_%s.txt' % (R, tag)
            if not os.path.exists(fn):
                continue
            for l in open(fn):
                f = l.rstrip('\n').split('\t')
                if len(f) != 4 or f[0] not in meta or not f[2].startswith('nodes='):
                    if l.strip():
                        bad += 1
                    continue
                if f[0] in cache:
                    continue
                name, par = meta[f[0]]
                nodes = f[2][6:]
                status = f[3] if f[3] in ('OK', 'ERR') else 'ABORT'
                row = [f[0], f[1], nodes, status, str(R), name, par]
                cache[f[0]] = row
                o.write('\t'.join(row) + '\n')
                new += 1
    pending = sum(1 for c in meta if c not in cache)
    print('merged', new, 'new results; unparsable lines', bad, '; candidates of this round still without result', pending)


def cmd_resume(R):
    """after a deadline stop: rewrite cand_rR_{a,b}.txt with the meta_rR entries that have no result yet"""
    cache = load_cache()
    todo = [l.split('\t')[0] for l in open('meta_r%d.tsv' % R) if l.split('\t')[0] not in cache]
    parts = ([], [])
    for i in range(0, len(todo), CHUNK):
        parts[(i // CHUNK) % 2].extend(todo[i:i + CHUNK])
    for tag, part in zip('ab', parts):
        with open('cand_r%d_%s.txt' % (R, tag), 'w') as o:
            for c in part:
                o.write(c + '\n')
    print('resume round', R, 'todo', len(todo))


def cmd_status():
    cache = load_cache()
    byr = collections.defaultdict(collections.Counter)
    for c, f in cache.items():
        byr[int(f[4])][kind(f[1])] += 1
    for r in sorted(byr):
        print('round', r, 'evaluated', sum(byr[r].values()), dict(sorted(byr[r].items())))
    print('total', len(cache))


if __name__ == '__main__':
    a = sys.argv
    if a[1] == 'init':
        cmd_init()
    elif a[1] == 'gen':
        lim = int(a[3]) if len(a) > 3 and a[3] != '-' else None
        qt = dict((k, int(v)) for k, v in (x.split(':') for x in a[4].split(','))) if len(a) > 4 else None
        cmd_gen(int(a[2]), lim, qt)
    elif a[1] == 'resume':
        cmd_resume(int(a[2]))
    elif a[1] == 'merge':
        cmd_merge(int(a[2]))
    elif a[1] == 'status':
        cmd_status()

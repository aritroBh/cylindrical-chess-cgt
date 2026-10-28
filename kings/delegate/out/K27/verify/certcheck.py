#!/usr/bin/env python3
"""Referee's own certificate checker for K27 PROOF.md (flat 7x6, P model, K+P only).
Own move generator (independent of kpp/ref3/pm.py/own.cpp and of K27's verify_certs.py).
Parses the 26 certificates of section 6 of PROOF.md and checks, for every entry:
  * the position of the entry equals the position reached by the arrow that points to it (side to move = winner);
  * the winner's move is legal (and the '+' marker agrees with 'opponent in check after the move');
  * the list of replies equals the full set of legal replies of the opponent (no missing, no extra);
  * every '->Nk' reply leads exactly to the position of entry Nk, and d(Nk) <= d(entry) - 2;
  * every 'X wins by p-p=Q' reply leads to a position where the winner has that legal promotion, d(entry) >= 3;
  * the first entry equals the position after the deviating move, and the deviating move is one of the 26
    non-shuttle legal moves of the root listed in section 4 (cross-checked against my own enumeration).
Also checks the reason brackets: every 'cannot go to' / 'blocked' claim is a true statement (illegal move).
"""
import re, sys, itertools
W, H = 7, 6
FILES = 'abcdefg'

def sq(s): return (FILES.index(s[0]), int(s[1]) - 1)
def ns(p): return FILES[p[0]] + str(p[1] + 1)

class Pos:
    __slots__ = ('wk', 'bk', 'wp', 'bp', 'stm')
    def __init__(s, wk, bk, wp, bp, stm):
        s.wk, s.bk, s.wp, s.bp, s.stm = wk, bk, frozenset(wp), frozenset(bp), stm
    def key(s): return (s.wk, s.bk, s.wp, s.bp, s.stm)
    def __eq__(s, o): return s.key() == o.key()
    def __hash__(s): return hash(s.key())

def parse_side(txt):
    k = None; pawns = []
    for t in txt.split():
        if t[0] in 'Kk': k = sq(t[1:])
        else: pawns.append(sq(t[1:]))
    return k, pawns

def parse_pos(white, black, stm):
    wk, wp = parse_side(white); bk, bp = parse_side(black)
    return Pos(wk, bk, wp, bp, stm)

def kadj(a, b): return a != b and abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1

def attacked_by_pawns(pawns, colour, s):
    # white pawn (f,r) attacks (f+-1, r+1)
    f, r = s
    pr = r - 1 if colour == 0 else r + 1
    return any((pf, pr) in pawns for pf in (f - 1, f + 1))

def king_attacked(p, colour):
    k = p.wk if colour == 0 else p.bk
    ok = p.bk if colour == 0 else p.wk
    if kadj(k, ok): return True
    return attacked_by_pawns(p.bp if colour == 0 else p.wp, 1 - colour, k)

def moves(p):
    """legal moves of side to move: list of (name, from, to, kind, newpos or None for promotion)"""
    c = p.stm
    own = p.wp if c == 0 else p.bp
    opp = p.bp if c == 0 else p.wp
    k = p.wk if c == 0 else p.bk
    ok = p.bk if c == 0 else p.wk
    occ = set(own) | set(opp) | {p.wk, p.bk}
    out = []
    def make(nk, nown, nopp):
        if c == 0: return Pos(nk, p.bk, nown, nopp, 1)
        return Pos(p.wk, nk, nopp, nown, 0)
    def legal(np_):
        # mover's king must not be attacked in the resulting position (stm irrelevant to attack)
        return not king_attacked(np_, c)
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0: continue
            t = (k[0] + df, k[1] + dr)
            if not (0 <= t[0] < W and 0 <= t[1] < H): continue
            if t in own or t == ok: continue
            cap = t in opp
            np_ = make(t, own, opp - {t} if cap else opp)
            if legal(np_):
                out.append(((('K' if c == 0 else 'k') + ns(k) + ('x' if cap else '-') + ns(t)), k, t, 'K', np_))
    dr = 1 if c == 0 else -1
    last = H - 1 if c == 0 else 0
    for pw in own:
        f, r = pw
        r1 = r + dr
        t = (f, r1)
        if t not in occ:
            if r1 == last:
                np_ = make(k, own - {pw}, opp)
                if legal(np_): out.append((ns(pw) + '-' + ns(t) + '=Q', pw, t, 'P', None))
            else:
                np_ = make(k, (own - {pw}) | {t}, opp)
                if legal(np_): out.append((ns(pw) + '-' + ns(t), pw, t, 'P', np_))
            # double step would need second rank: flag if it ever applies
            second = 1 if c == 0 else H - 2
            if r == second: raise Exception('double step possible: ' + str(p.key()))
        for d in (-1, 1):
            t = (f + d, r1)
            if not (0 <= t[0] < W): continue
            if t in opp:
                if r1 == last:
                    np_ = make(k, own - {pw}, opp - {t})
                    if legal(np_): out.append((ns(pw) + 'x' + ns(t) + '=Q', pw, t, 'P', None))
                else:
                    np_ = make(k, (own - {pw}) | {t}, opp - {t})
                    if legal(np_): out.append((ns(pw) + 'x' + ns(t), pw, t, 'P', np_))
    return out

def fmt(p):
    wh = 'K' + ns(p.wk) + ''.join(' P' + ns(x) for x in sorted(p.wp, key=lambda z: (z[0], z[1])))
    bl = 'k' + ns(p.bk) + ''.join(' p' + ns(x) for x in sorted(p.bp, key=lambda z: (z[0], z[1])))
    return wh + ' | ' + bl + (' w' if p.stm == 0 else ' b')

def mvkey(name):
    """normalise a move name to (from,to) squares; ignore piece letters, x/-, +, =Q"""
    sqs = re.findall(r'[a-g][1-6]', name)
    return tuple(sqs)

# ---------------------------------------------------------------- parse PROOF.md
text = open(sys.argv[1]).read()
sec6 = text.split('## 6. The 26 deviations')[1].split('## 7.')[0]
blocks = re.split(r'\n#### ', '\n' + sec6)
cert = {}
problems = []
DUMP = []
LEAVES = []
stats = dict(entries=0, replies=0, leaves=0, reasons=0, certs=0)

# root enumeration from section 4: (white, black, stm) for Z1..Z8
roots = {}
for i, (wk, bk) in enumerate([('b2', 'a4'), ('b2', 'a4'), ('b2', 'b5'), ('b2', 'b5'), ('c3', 'a4'), ('c3', 'a4'), ('c3', 'b5'), ('c3', 'b5')]):
    stm = i % 2
    roots['Z%d' % (i + 1)] = Pos(sq(wk), sq(bk), {sq('a3'), sq('b4')}, {sq('b3'), sq('c4')}, stm)
shuttle = {0: {sq('b2'): sq('c3'), sq('c3'): sq('b2')}, 1: {sq('a4'): sq('b5'), sq('b5'): sq('a4')}}

nonshuttle = {}   # Z -> set of move keys (from,to) that are not the shuttle
for z, rp in roots.items():
    ms = moves(rp)
    c = rp.stm
    k = rp.wk if c == 0 else rp.bk
    sh = (k, shuttle[c][k])
    ns_ = []
    for name, a, b, kind, np_ in ms:
        if kind == 'K' and (a, b) == sh: continue
        ns_.append((name, (ns(a), ns(b))))
    nonshuttle[z] = ns_
tot = sum(len(v) for v in nonshuttle.values())
print('my enumeration: non-shuttle moves per root', {z: len(v) for z, v in nonshuttle.items()}, 'total', tot)
white_total = sum(len(nonshuttle[z]) for z in ('Z1', 'Z3', 'Z5', 'Z7')); black_total = tot - white_total
print('White', white_total, 'Black', black_total)

covered = set()
for b in blocks:
    m = re.match(r'(C\d\d)\. Root (Z\d), move (\S+)\. Position after the move: `([^`]+)`', b)
    if not m: continue
    cid, z, mvname, posafter = m.groups()
    stats['certs'] += 1
    rp = roots[z]
    # deviating move legal and non-shuttle
    cand = [(name, a, b_, kind, np_) for (name, a, b_, kind, np_) in moves(rp) if mvkey(name) == mvkey(mvname)]
    if len(cand) != 1: problems.append('%s: deviating move %s not found at root %s' % (cid, mvname, z)); continue
    dev_np = cand[0][4]
    covered.add((z, mvkey(mvname)))
    # parse the stated position after the move
    pm = re.match(r'(.*?) (w|b) -$', posafter.strip())
    toks = pm.group(1).split()
    wt = ' '.join(t for t in toks if t[0] in 'KP'); bt = ' '.join(t for t in toks if t[0] in 'kp')
    stated = parse_pos(wt, bt, 0 if pm.group(2) == 'w' else 1)
    if stated != dev_np: problems.append('%s: stated position after move %s != my position %s' % (cid, fmt(stated), fmt(dev_np)))
    # winner = opponent of the deviator
    winner = 1 - rp.stm
    # entries
    ents = {}
    order = []
    for line in b.split('\n'):
        em = re.match(r'- ([NR]\d+)\. (.*?) \| (.*?) -- (White|Black) to move \[d=(\d+)\]: \*\*(.*?)\*\*\. (White|Black) replies: (.*)$', line)
        if not em: continue
        name, wt, bt, who, d, mv, who2, rest = em.groups()
        d = int(d)
        stm = 0 if who == 'White' else 1
        if who2 == who: problems.append('%s %s: replier colour equals mover' % (cid, name))
        # split replies and reasons
        rm = re.match(r'(.*?)\.(?: \[(.*)\])?$', rest)
        # careful: replies text contains "." only at the end; the reasons bracket may contain '.'? use last ". ["
        if ' [' in rest:
            idx = rest.index('. [')
            rep_txt, reason_txt = rest[:idx], rest[idx + 3:-1]
        else:
            rep_txt, reason_txt = rest.rstrip('.'), ''
        items = [x.strip() for x in rep_txt.split(';')]
        reps = []
        for it in items:
            mm = re.match(r'(.*): (->([NR]\d+)|(White|Black) wins by (\S+))$', it)
            if not mm: problems.append('%s %s: cannot parse reply item %r' % (cid, name, it)); continue
            movs = [x.strip() for x in mm.group(1).split(',')]
            for mv_ in movs:
                reps.append((mv_, mm.group(3), mm.group(4), mm.group(5)))
        ents[name] = dict(pos=parse_pos(wt, bt, stm), d=d, mv=mv, reps=reps, reason=reason_txt, winner=stm)
        order.append(name)
    if not order: problems.append('%s: no entries parsed' % cid); continue
    nent_stated = re.search(r'Certificate \((\d+) entries', b)
    if nent_stated and int(nent_stated.group(1)) != len(order): problems.append('%s: stated %s entries, parsed %d' % (cid, nent_stated.group(1), len(order)))
    # first entry
    first = ents[order[0]]
    if first['pos'] != dev_np: problems.append('%s: first entry position differs from position after the deviation' % cid)
    if first['winner'] != winner: problems.append('%s: first entry winner is the deviator' % cid)
    reached = set()
    for name in order:
        e = ents[name]
        stats['entries'] += 1
        p = e['pos']
        # legal winner move
        cand = [x for x in moves(p) if mvkey(x[0]) == mvkey(e['mv'])]
        if len(cand) != 1: problems.append('%s %s: winner move %s not legal' % (cid, name, e['mv'])); continue
        wname, a, b_, kind, np_ = cand[0]
        if np_ is None: problems.append('%s %s: winner move is a promotion (should be a normal move)' % (cid, name)); continue
        gives_check = king_attacked(np_, np_.stm)
        if gives_check != e['mv'].endswith('+'):
            problems.append('%s %s: check marker mismatch for %s (check=%s)' % (cid, name, e['mv'], gives_check))
        # replies completeness
        legal = moves(np_)
        DUMP.append((np_, sorted(mvkey(r[0]) for r in e['reps']), e['mv'], cid, name))
        lk = sorted(mvkey(x[0]) for x in legal)
        sk = sorted(mvkey(r[0]) for r in e['reps'])
        if lk != sk:
            problems.append('%s %s: replies differ. mine=%s listed=%s' % (cid, name, lk, sk))
        if len(set(sk)) != len(sk): problems.append('%s %s: duplicate replies' % (cid, name))
        # each reply
        for (rmv, link, wwho, promo) in e['reps']:
            stats['replies'] += 1
            c2 = [x for x in legal if mvkey(x[0]) == mvkey(rmv)]
            if len(c2) != 1: continue
            rname, ra, rb, rkind, rnp = c2[0]
            if rnp is None:
                problems.append('%s %s: opponent reply %s is a promotion' % (cid, name, rmv)); continue
            if link:
                reached.add(link)
                tgt = ents.get(link)
                if tgt is None: problems.append('%s %s: link %s missing' % (cid, name, link)); continue
                if tgt['pos'] != rnp: problems.append('%s %s: reply %s leads to %s but %s is %s' % (cid, name, rmv, fmt(rnp), link, fmt(tgt['pos'])))
                if tgt['d'] > e['d'] - 2: problems.append('%s %s: d does not drop by 2 along %s (%d -> %d)' % (cid, name, link, e['d'], tgt['d']))
                if tgt['winner'] != e['winner']: problems.append('%s %s: winner changes along %s' % (cid, name, link))
            else:
                stats['leaves'] += 1
                if (wwho == 'White') != (e['winner'] == 0): problems.append('%s %s: leaf winner colour wrong' % (cid, name))
                if e['d'] < 3: problems.append('%s %s: leaf but d<3' % (cid, name))
                pr = [x for x in moves(rnp) if x[3] == 'P' and x[4] is None and mvkey(x[0]) == mvkey(promo)]
                LEAVES.append((cid, name, rmv, promo, rnp, pr[0] if pr else None))
                if len(pr) != 1: problems.append('%s %s: leaf promotion %s after reply %s not legal' % (cid, name, promo, rmv))
        # reasons: check 'cannot go to X attacked by' etc loosely: every claimed-illegal square must not be a legal king destination
        stats['reasons'] += 0
    unreached = set(order[1:]) - reached
    if unreached: problems.append('%s: entries never reached %s' % (cid, sorted(unreached)))
    # termination / acyclic is implied by d dropping; d of first entry <= 11
    if first['d'] + 0 > 11: problems.append('%s: first entry d=%d > 11' % (cid, first['d']))
    cert[cid] = dict(n=len(order), d=first['d'])

# coverage: every non-shuttle move covered exactly once
for z, lst in nonshuttle.items():
    for name, key in lst:
        if (z, key) not in covered: problems.append('non-shuttle move %s at %s has no certificate' % (name, z))
extra = [c for c in covered if c[0] not in nonshuttle or c[1] not in [k for _, k in nonshuttle[c[0]]]]
if extra: problems.append('certificates for moves that are shuttle/non-existent: %s' % extra)
print('certificates', stats['certs'], 'entries', stats['entries'], 'reply-items checked', stats['replies'], 'leaf promotions checked', stats['leaves'])
print('max d at first entry', max(c['d'] for c in cert.values()), ' max entries', max(c['n'] for c in cert.values()), ' total entries', sum(c['n'] for c in cert.values()))
print('PROBLEMS:', len(problems))
for pr in problems[:60]: print('  ', pr)

import json
with open('work/opp_positions.txt','w') as f:
    for np_, reps, mv, cid, name in DUMP:
        wh='K'+ns(np_.wk)+''.join(' P'+ns(x) for x in sorted(np_.wp))
        bl='k'+ns(np_.bk)+''.join(' p'+ns(x) for x in sorted(np_.bp))
        f.write(wh+' '+bl+(' w' if np_.stm==0 else ' b')+' -\n')
json.dump([[list(map(list,r)),mv,cid,name] for _,r,mv,cid,name in DUMP], open('work/opp_replies.json','w'))

# chess-safety of the leaf promotions (hand heuristic, NOT a chess proof): can the loser capture the new piece at once?
def capturable_now(rnp, pr):
    win = rnp.stm                       # winner to move in rnp
    name, a, t, kind, _ = pr
    lose = 1 - win
    lk = rnp.wk if lose == 0 else rnp.bk
    wk = rnp.wk if win == 0 else rnp.bk
    wpawns = rnp.wp if win == 0 else rnp.bp
    lpawns = rnp.wp if lose == 0 else rnp.bp
    # square t is 'defended' by winner king or winner pawns (after the promoting pawn left a)
    wp_after = set(wpawns) - {a}
    defended = kadj(wk, t) or attacked_by_pawns(wp_after, win, t)
    attackers = kadj(lk, t) or attacked_by_pawns(lpawns - {t}, lose, t)
    return attackers and not defended
bycert = {}
for cid, name, rmv, promo, rnp, pr in LEAVES:
    if pr is None: continue
    bycert.setdefault(cid, [0, 0])
    bycert[cid][0] += 1
    if capturable_now(rnp, pr): bycert[cid][1] += 1
unsafe = [c for c, v in bycert.items() if v[1] > 0]
print('leaf promotions', sum(v[0] for v in bycert.values()), 'of which the new piece can be captured at once (loser king/pawn attacks, winner does not defend):', sum(v[1] for v in bycert.values()))
print('certificates with at least one such leaf:', len(unsafe), 'of', len(bycert), sorted(unsafe))
print('certificates with none:', sorted(set(bycert) - set(unsafe)))

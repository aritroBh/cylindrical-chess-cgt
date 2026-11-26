// K66 checker's own solver (written from kings/theory/LOOPY.md Def. 4.8, Lemma 4.15, Thm 4.18, and the
// K61 packet section 1). Flat 8x8, kings and pawns, promotion game P (a promotion is a win for the promoter),
// e.p., no move into check. Group as a component of a D-sum: promotion ends the sum, a side in check may not
// move elsewhere, a move elsewhere clears the mover's e.p. right, a side with no move anywhere loses, infinite
// play is a draw (Aux: White win iff White passed infinitely often).
//
// Layout: a "configuration" is (white pawns, black pawns, e.p. target). Configurations are closed under an
// over-approximation of the pawn moves and of king captures and are solved in an order in which every pawn move,
// capture or loss of the right leads to an earlier one. A block is (configuration, T-position); inside a block
// only king moves (and White's pass in under) stay; solved by retrograde analysis (draw mode) or by the Buchi
// fixpoint nu Y. mu X (Aux). One byte of value and two bytes of rank per state and T-position.
//
// Usage: k66 <group spec> [maxN]    e.g.  k66 "Kg5 ke5/ke6 Pb2 Pf2 Pf6 pc4 pf5 pf7" 6
//        k66 -pv <group spec> <N> <fen-ish position: side wk bk wp.. / bp..>   (see main)
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <functional>
#include <unistd.h>
using namespace std;
typedef uint64_t U64;

static inline U64 B(int s) { return 1ULL << s; }
static const U64 FA = 0x0101010101010101ULL, FH = 0x8080808080808080ULL;
static inline U64 wpAtt(U64 b) { return ((b & ~FA) << 7) | ((b & ~FH) << 9); }
static inline U64 bpAtt(U64 b) { return ((b & ~FA) >> 9) | ((b & ~FH) >> 7); }
static inline int rk(int s) { return s >> 3; }
static inline int fl(int s) { return s & 7; }
static inline int cheb(int a, int b) { return max(abs(rk(a) - rk(b)), abs(fl(a) - fl(b))); }
static string sqn(int s) { string r; r += char('a' + fl(s)); r += char('1' + rk(s)); return r; }
static int parsesq(const char* p) { return (p[1] - '1') * 8 + (p[0] - 'a'); }

struct Cfg { U64 wp, bp; int ep; };  // ep: target square or -1
struct KH { size_t operator()(const pair<pair<U64, U64>, int>& k) const {
    return std::hash<U64>()(k.first.first * 0x9E3779B97F4A7C15ULL ^ (k.first.second + 0x12345) * 0xC2B2AE3D27D4EB4FULL) ^ (size_t)(k.second + 7) * 0x165667B19E3779F9ULL; } };

vector<Cfg> cfgs;
unordered_map<pair<pair<U64, U64>, int>, int, KH> cmap;
vector<int> baseOf;   // configuration without the right
vector<int> order;    // solve order (successors first)

static int epSide(int ep) { return ep < 0 ? -1 : (rk(ep) == 2 ? 1 : 0); }  // side holding the right: 0 White, 1 Black

int findCfg(U64 wp, U64 bp, int ep) {
    auto it = cmap.find({{wp, bp}, ep});
    if (it == cmap.end()) { fprintf(stderr, "missing cfg\n"); exit(3); }
    return it->second;
}

// ep target after a double step of side s from sq, or -1 if no enemy pawn could take
static int epAfter(int s, int from, int to, U64 enemyPawns) {
    U64 adj = 0;
    if (fl(to) > 0) adj |= B(to - 1);
    if (fl(to) < 7) adj |= B(to + 1);
    if (adj & enemyPawns) return (from + to) / 2;
    return -1;
}

void enumerateCfgs(U64 wp0, U64 bp0) {
    vector<int> st;
    auto add = [&](U64 wp, U64 bp, int ep) {
        auto k = make_pair(make_pair(wp, bp), ep);
        if (cmap.count(k)) return;
        int id = cfgs.size(); cfgs.push_back({wp, bp, ep}); cmap[k] = id; st.push_back(id);
    };
    add(wp0, bp0, -1);
    while (!st.empty()) {
        int id = st.back(); st.pop_back();
        Cfg c = cfgs[id];
        U64 occ = c.wp | c.bp;
        if (c.ep >= 0) add(c.wp, c.bp, -1);
        // king captures (over-approximation: any one pawn)
        for (U64 b = c.wp; b; b &= b - 1) add(c.wp & ~B(__builtin_ctzll(b)), c.bp, -1);
        for (U64 b = c.bp; b; b &= b - 1) add(c.wp, c.bp & ~B(__builtin_ctzll(b)), -1);
        // white pawn moves
        for (U64 b = c.wp; b; b &= b - 1) {
            int s = __builtin_ctzll(b);
            int t = s + 8;
            if (!(occ & B(t)) && rk(t) < 7) {
                add((c.wp & ~B(s)) | B(t), c.bp, -1);
                if (rk(s) == 1 && !(occ & B(s + 16))) {
                    U64 nw = (c.wp & ~B(s)) | B(s + 16);
                    add(nw, c.bp, -1);
                    int e = epAfter(0, s, s + 16, c.bp);
                    if (e >= 0) add(nw, c.bp, e);
                }
            }
            for (int d : {7, 9}) {
                if (d == 7 && fl(s) == 0) continue;
                if (d == 9 && fl(s) == 7) continue;
                int u = s + d;
                if ((c.bp & B(u)) && rk(u) < 7) add((c.wp & ~B(s)) | B(u), c.bp & ~B(u), -1);
                if (c.ep == u && epSide(c.ep) == 0) add((c.wp & ~B(s)) | B(u), c.bp & ~B(u - 8), -1);
            }
        }
        for (U64 b = c.bp; b; b &= b - 1) {
            int s = __builtin_ctzll(b);
            int t = s - 8;
            if (!(occ & B(t)) && rk(t) > 0) {
                add(c.wp, (c.bp & ~B(s)) | B(t), -1);
                if (rk(s) == 6 && !(occ & B(s - 16))) {
                    U64 nb = (c.bp & ~B(s)) | B(s - 16);
                    add(c.wp, nb, -1);
                    int e = epAfter(1, s, s - 16, c.wp);
                    if (e >= 0) add(c.wp, nb, e);
                }
            }
            for (int d : {9, 7}) {
                if (d == 9 && fl(s) == 0) continue;
                if (d == 7 && fl(s) == 7) continue;
                int u = s - d;
                if ((c.wp & B(u)) && rk(u) > 0) add(c.wp & ~B(u), (c.bp & ~B(s)) | B(u), -1);
                if (c.ep == u && epSide(c.ep) == 1) add(c.wp & ~B(u + 8), (c.bp & ~B(s)) | B(u), -1);
            }
        }
    }
    int n = cfgs.size();
    baseOf.resize(n);
    for (int i = 0; i < n; i++) baseOf[i] = cmap.at({{cfgs[i].wp, cfgs[i].bp}, -1});
    // order: fewer pawns first, then more advanced first, then no right before right
    auto adv = [&](const Cfg& c) { int a = 0; for (U64 b = c.wp; b; b &= b - 1) a += rk(__builtin_ctzll(b));
        for (U64 b = c.bp; b; b &= b - 1) a += 7 - rk(__builtin_ctzll(b)); return a; };
    order.resize(n);
    for (int i = 0; i < n; i++) order[i] = i;
    vector<long> key(n);
    for (int i = 0; i < n; i++) key[i] = (long)__builtin_popcountll(cfgs[i].wp | cfgs[i].bp) * 100000 - adv(cfgs[i]) * 10 + (cfgs[i].ep >= 0);
    sort(order.begin(), order.end(), [&](int a, int b) { return key[a] < key[b]; });
}

// ---- moves ----
enum { M_TERM_WIN = 1, M_STATE = 2 };
struct Mv { int kind; int cfg; int side; int wk, bk; int from, to; bool ep; bool prom; };

static inline bool inCheck(const Cfg& c, int side, int wk, int bk) {
    return side == 0 ? (bpAtt(c.bp) & B(wk)) != 0 : (wpAtt(c.wp) & B(bk)) != 0;
}
static inline bool validState(const Cfg& c, int side, int wk, int bk) {
    if (wk == bk || cheb(wk, bk) < 2) return false;
    U64 occ = c.wp | c.bp;
    if (occ & (B(wk) | B(bk))) return false;
    if (c.ep >= 0) { if (epSide(c.ep) != side) return false; if (B(c.ep) & (B(wk) | B(bk))) return false; }
    if (inCheck(c, 1 - side, wk, bk)) return false;
    return true;
}

// group moves of `side` at (cfg id, wk, bk)
void genMoves(int ci, int side, int wk, int bk, vector<Mv>& out) {
    out.clear();
    const Cfg c = cfgs[ci];
    U64 occ = c.wp | c.bp | B(wk) | B(bk);
    static const int KD[8][2] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
    if (side == 0) {
        int r = rk(wk), f = fl(wk);
        for (auto& d : KD) {
            int rr = r + d[0], ff = f + d[1];
            if (rr < 0 || rr > 7 || ff < 0 || ff > 7) continue;
            int t = rr * 8 + ff;
            if (c.wp & B(t)) continue;
            if (cheb(t, bk) < 2) continue;
            U64 nb = c.bp & ~B(t);
            if (bpAtt(nb) & B(t)) continue;
            int nc = (nb != c.bp) ? findCfg(c.wp, nb, -1) : baseOf[ci];
            out.push_back({M_STATE, nc, 1, t, bk, wk, t, false, false});
        }
        for (U64 b = c.wp; b; b &= b - 1) {
            int s = __builtin_ctzll(b);
            int t = s + 8;
            if (!(occ & B(t))) {
                if (!(bpAtt(c.bp) & B(wk))) {
                    if (rk(t) == 7) out.push_back({M_TERM_WIN, -1, 1, wk, bk, s, t, false, true});
                    else {
                        U64 nw = (c.wp & ~B(s)) | B(t);
                        out.push_back({M_STATE, findCfg(nw, c.bp, -1), 1, wk, bk, s, t, false, false});
                        if (rk(s) == 1 && !(occ & B(s + 16))) {
                            U64 nw2 = (c.wp & ~B(s)) | B(s + 16);
                            int e = epAfter(0, s, s + 16, c.bp);
                            out.push_back({M_STATE, findCfg(nw2, c.bp, e), 1, wk, bk, s, s + 16, false, false});
                        }
                    }
                }
            }
            for (int d : {7, 9}) {
                if (d == 7 && fl(s) == 0) continue;
                if (d == 9 && fl(s) == 7) continue;
                int u = s + d;
                if (c.bp & B(u)) {
                    U64 nb = c.bp & ~B(u);
                    if (bpAtt(nb) & B(wk)) continue;
                    if (rk(u) == 7) out.push_back({M_TERM_WIN, -1, 1, wk, bk, s, u, false, true});
                    else out.push_back({M_STATE, findCfg((c.wp & ~B(s)) | B(u), nb, -1), 1, wk, bk, s, u, false, false});
                } else if (c.ep == u && epSide(c.ep) == 0 && !(occ & B(u)) && (c.bp & B(u - 8))) {
                    U64 nb = c.bp & ~B(u - 8);
                    if (bpAtt(nb) & B(wk)) continue;
                    out.push_back({M_STATE, findCfg((c.wp & ~B(s)) | B(u), nb, -1), 1, wk, bk, s, u, true, false});
                }
            }
        }
    } else {
        int r = rk(bk), f = fl(bk);
        for (auto& d : KD) {
            int rr = r + d[0], ff = f + d[1];
            if (rr < 0 || rr > 7 || ff < 0 || ff > 7) continue;
            int t = rr * 8 + ff;
            if (c.bp & B(t)) continue;
            if (cheb(t, wk) < 2) continue;
            U64 nw = c.wp & ~B(t);
            if (wpAtt(nw) & B(t)) continue;
            int nc = (nw != c.wp) ? findCfg(nw, c.bp, -1) : baseOf[ci];
            out.push_back({M_STATE, nc, 0, wk, t, bk, t, false, false});
        }
        for (U64 b = c.bp; b; b &= b - 1) {
            int s = __builtin_ctzll(b);
            int t = s - 8;
            if (!(occ & B(t))) {
                if (!(wpAtt(c.wp) & B(bk))) {
                    if (rk(t) == 0) out.push_back({M_TERM_WIN, -1, 0, wk, bk, s, t, false, true});
                    else {
                        U64 nb = (c.bp & ~B(s)) | B(t);
                        out.push_back({M_STATE, findCfg(c.wp, nb, -1), 0, wk, bk, s, t, false, false});
                        if (rk(s) == 6 && !(occ & B(s - 16))) {
                            U64 nb2 = (c.bp & ~B(s)) | B(s - 16);
                            int e = epAfter(1, s, s - 16, c.wp);
                            out.push_back({M_STATE, findCfg(c.wp, nb2, e), 0, wk, bk, s, s - 16, false, false});
                        }
                    }
                }
            }
            for (int d : {9, 7}) {
                if (d == 9 && fl(s) == 0) continue;
                if (d == 7 && fl(s) == 7) continue;
                int u = s - d;
                if (c.wp & B(u)) {
                    U64 nw = c.wp & ~B(u);
                    if (wpAtt(nw) & B(bk)) continue;
                    if (rk(u) == 0) out.push_back({M_TERM_WIN, -1, 0, wk, bk, s, u, false, true});
                    else out.push_back({M_STATE, findCfg(nw, (c.bp & ~B(s)) | B(u), -1), 0, wk, bk, s, u, false, false});
                } else if (c.ep == u && epSide(c.ep) == 1 && !(occ & B(u)) && (c.wp & B(u + 8))) {
                    U64 nw = c.wp & ~B(u + 8);
                    if (wpAtt(nw) & B(bk)) continue;
                    out.push_back({M_STATE, findCfg(nw, (c.bp & ~B(s)) | B(u), -1), 0, wk, bk, s, u, true, false});
                }
            }
        }
    }
}

// ---- T games ----
// option target: >=0 position, -1 = White terminal win (+), -2 = Black terminal win (-)
struct TPos { vector<int> L, R; };
struct TGame { string name; vector<TPos> pos; vector<int> topo; bool aux = false; bool palone = false; };

TGame mkT(int N) {  // T_N: u_0..u_N = 0..N, z = N+1
    TGame g; g.name = "T" + to_string(N); g.pos.resize(N + 2);
    for (int i = 0; i <= N; i++) { g.pos[i].L = {i < N ? i + 1 : -1}; g.pos[i].R = {N + 1}; }
    g.topo.push_back(N + 1);
    for (int i = N; i >= 0; i--) g.topo.push_back(i);
    return g;
}
TGame mkMinus1() { TGame g; g.name = "-1"; g.pos.resize(2); g.pos[0].R = {1}; g.topo = {1, 0}; return g; }
TGame mkZero() { TGame g; g.name = "0"; g.pos.resize(1); g.topo = {0}; return g; }
TGame mkP() { TGame g = mkZero(); g.name = "P"; g.palone = true; return g; }
TGame mkUnder() { TGame g; g.name = "Aux"; g.aux = true; g.pos.resize(2); g.pos[0].L = {0}; g.pos[0].R = {1}; g.topo = {1, 0}; return g; }

// values: 0 = undetermined/draw, 1 = White win, 2 = Black win
enum { VD = 0, VW = 1, VL = 2 };
const size_t BS = 8192;
struct Solved {
    TGame T;
    vector<vector<uint8_t>> val;   // [tpos][cfg*BS + idx]
    vector<vector<uint16_t>> rnk;  // in-block rank (for lines of play)
};
static inline int sidx(int side, int wk, int bk) { return side * 4096 + wk * 64 + bk; }

size_t peakAlloc = 0;
Solved solve(const TGame& T) {
    Solved S; S.T = T;
    size_t n = cfgs.size(), np = T.pos.size();
    size_t bytes = np * n * BS * 3;
    if (bytes > (size_t)1600 << 20) { fprintf(stderr, "would allocate %zu bytes, over limit\n", bytes); exit(4); }
    peakAlloc = max(peakAlloc, bytes);
    S.val.assign(np, vector<uint8_t>(n * BS, VD));
    S.rnk.assign(np, vector<uint16_t>(n * BS, 0));
    vector<uint8_t> valid(BS), known(BS), isW(BS);
    vector<int> cnt(BS), head(BS + 1), radj;
    vector<uint8_t> exitBest(BS);
    vector<vector<int>> succ(BS);   // in-block successors
    vector<vector<char>> succPass(BS);
    vector<uint8_t> hasL(BS), hasWexit(BS), nomove(BS);
    vector<Mv> mv;
    for (int tp : T.topo) {
        const TPos& P = T.pos[tp];
        bool selfPassW = false;
        for (int o : P.L) if (o == tp) selfPassW = true;
        for (int o : P.R) if (o == tp) { fprintf(stderr, "black self loop unsupported\n"); exit(5); }
        if (selfPassW && !T.aux) { fprintf(stderr, "self loop only in Aux\n"); exit(5); }
        bool buchi = T.aux && selfPassW;
        bool infL = T.aux && !selfPassW;  // in Aux, at 0-bar infinite play is a Black win
        auto& V = S.val[tp];
        auto& R = S.rnk[tp];
        for (int ci : order) {
            const Cfg& c = cfgs[ci];
            size_t off = (size_t)ci * BS;
            // build block
            for (size_t i = 0; i < BS; i++) { succ[i].clear(); succPass[i].clear(); }
            for (int side = 0; side < 2; side++)
                for (int wk = 0; wk < 64; wk++)
                    for (int bk = 0; bk < 64; bk++) {
                        int i = sidx(side, wk, bk);
                        valid[i] = validState(c, side, wk, bk);
                        known[i] = 0; hasL[i] = 0; hasWexit[i] = 0; nomove[i] = 0; exitBest[i] = 0;
                        if (!valid[i]) continue;
                        // exitBest from mover's view: 3 = win, 2 = draw, 1 = loss, 0 = none
                        int best = 0;
                        bool chk = inCheck(c, side, wk, bk);
                        int nmoves = 0;
                        genMoves(ci, side, wk, bk, mv);
                        for (auto& m : mv) {
                            nmoves++;
                            if (m.kind == M_TERM_WIN) { best = 3; continue; }
                            if (m.cfg == ci) { succ[i].push_back(sidx(m.side, m.wk, m.bk)); succPass[i].push_back(0); continue; }
                            uint8_t v = V[(size_t)m.cfg * BS + sidx(m.side, m.wk, m.bk)];
                            int mvw = (v == VD) ? 2 : ((v == VW) == (side == 0) ? 3 : 1);
                            best = max(best, mvw);
                        }
                        if (!T.palone && !chk) {
                            const vector<int>& opts = side == 0 ? P.L : P.R;
                            for (int o : opts) {
                                nmoves++;
                                if (o == -1 || o == -2) { int mvw = ((o == -1) == (side == 0)) ? 3 : 1; best = max(best, mvw); continue; }
                                int bc = baseOf[ci];
                                int j = sidx(1 - side, wk, bk);
                                if (o == tp) {  // White pass in under
                                    if (bc == ci) { succ[i].push_back(j); succPass[i].push_back(1); }
                                    else { uint8_t v = V[(size_t)bc * BS + j]; best = max(best, v == VW ? 3 : 1); }
                                    continue;
                                }
                                uint8_t v = S.val[o][(size_t)bc * BS + j];
                                int mvw = (v == VD) ? 2 : ((v == VW) == (side == 0) ? 3 : 1);
                                best = max(best, mvw);
                            }
                        }
                        exitBest[i] = best;
                        if (nmoves == 0) nomove[i] = 1;
                        (void)chk;
                    }
            // reverse adjacency
            fill(head.begin(), head.end(), 0);
            for (size_t i = 0; i < BS; i++) if (valid[i]) for (int j : succ[i]) head[j + 1]++;
            for (size_t i = 0; i < BS; i++) head[i + 1] += head[i];
            radj.assign(head[BS], 0);
            {
                vector<int> pos(head.begin(), head.end() - 1);
                for (size_t i = 0; i < BS; i++) if (valid[i]) for (int j : succ[i]) radj[pos[j]++] = i;
            }
            if (!buchi) {
                // retrograde; values from White's view
                vector<int> q; q.reserve(BS);
                vector<uint16_t> rr(BS, 0);
                for (size_t i = 0; i < BS; i++) {
                    if (!valid[i]) continue;
                    int side = i >= 4096;
                    cnt[i] = succ[i].size();
                    uint8_t v = 255;
                    if (exitBest[i] == 3) v = side == 0 ? VW : VL;
                    else if (nomove[i]) {
                        if (T.palone) {
                            int wk = (i & 4095) >> 6, bk = i & 63;
                            v = inCheck(c, side, wk, bk) ? (side == 0 ? VL : VW) : VD;
                        } else v = side == 0 ? VL : VW;
                    } else if (cnt[i] == 0) v = exitBest[i] == 2 ? VD : (side == 0 ? VL : VW);
                    if (v != 255) { V[off + i] = v; known[i] = 1; if (v != VD) q.push_back(i); }
                }
                for (size_t h = 0; h < q.size(); h++) {
                    int t = q[h]; uint8_t vt = V[off + t];
                    for (int k = head[t]; k < head[t + 1]; k++) {
                        int p = radj[k];
                        if (known[p]) continue;
                        int ps = p >= 4096;
                        bool winForMover = (vt == VW) == (ps == 0);
                        if (winForMover) { V[off + p] = vt; known[p] = 1; rr[p] = rr[t] + 1; q.push_back(p); }
                        else if (--cnt[p] == 0) {
                            if (exitBest[p] == 2) { V[off + p] = VD; known[p] = 1; }
                            else { V[off + p] = vt; known[p] = 1; rr[p] = rr[t] + 1; q.push_back(p); }
                        }
                    }
                }
                for (size_t i = 0; i < BS; i++) {
                    if (!valid[i]) { V[off + i] = VD; continue; }
                    if (!known[i]) V[off + i] = VD;
                    if (infL && V[off + i] == VD) V[off + i] = VL;
                    R[off + i] = rr[i];
                }
            } else {
                // Buchi: White wins iff infinitely many passes. nu Y. mu X.
                vector<uint8_t> inY(BS, 0), inX(BS, 0);
                for (size_t i = 0; i < BS; i++) inY[i] = valid[i];
                vector<int> q; q.reserve(BS);
                while (true) {
                    fill(inX.begin(), inX.end(), 0); q.clear();
                    vector<uint16_t> rr(BS, 0);
                    for (size_t i = 0; i < BS; i++) {
                        if (!valid[i]) continue;
                        int side = i >= 4096;
                        bool in = false;
                        if (side == 0) {
                            if (exitBest[i] == 3) in = true;
                            for (size_t k = 0; k < succ[i].size(); k++) if (succPass[i][k] && inY[succ[i][k]]) in = true;
                            if (nomove[i]) in = false;
                        } else {
                            cnt[i] = succ[i].size();
                            if (nomove[i]) in = true;
                            else if (exitBest[i] == 3) in = false;          // Black has a winning exit
                            else if (exitBest[i] == 0 || exitBest[i] == 1) in = (cnt[i] == 0);  // all exits lose for Black
                            else in = false;
                        }
                        if (in) { inX[i] = 1; q.push_back(i); }
                    }
                    for (size_t h = 0; h < q.size(); h++) {
                        int t = q[h];
                        for (int k = head[t]; k < head[t + 1]; k++) {
                            int p = radj[k];
                            if (inX[p]) continue;
                            int ps = p >= 4096;
                            if (ps == 0) { inX[p] = 1; rr[p] = rr[t] + 1; q.push_back(p); }
                            else {
                                if (exitBest[p] == 3) continue;
                                if (--cnt[p] == 0) { inX[p] = 1; rr[p] = rr[t] + 1; q.push_back(p); }
                            }
                        }
                    }
                    bool same = true;
                    for (size_t i = 0; i < BS; i++) if (inY[i] != inX[i]) same = false;
                    if (same) { for (size_t i = 0; i < BS; i++) { V[off + i] = inX[i] ? VW : VL; R[off + i] = rr[i]; } break; }
                    inY = inX;
                }
            }
        }
    }
    return S;
}

// ---- group parsing ----
struct Group { string name; int wk, bk0, bk1; U64 wp, bp; };
Group parseGroup(const string& name, const string& s) {
    Group g; g.name = name; g.wp = g.bp = 0; g.wk = g.bk0 = g.bk1 = -1;
    const char* p = s.c_str();
    while (*p) {
        while (*p == ' ') p++;
        if (!*p) break;
        char t = *p++;
        if (t == 'K') g.wk = parsesq(p), p += 2;
        else if (t == 'k') { g.bk0 = parsesq(p); p += 2; if (*p == '/') { p++; p++; g.bk1 = parsesq(p); p += 2; } }
        else if (t == 'P') g.wp |= B(parsesq(p)), p += 2;
        else if (t == 'p') g.bp |= B(parsesq(p)), p += 2;
        else { fprintf(stderr, "bad spec\n"); exit(2); }
    }
    return g;
}

const char* vs(uint8_t v) { return v == VW ? "W" : v == VL ? "L" : "D"; }
string mvName(const Mv& m, int side) {
    string s = side == 0 ? "" : "...";
    if (m.from == (side == 0 ? -999 : -999)) {}
    return s + sqn(m.from) + "-" + sqn(m.to) + (m.ep ? "ep" : "") + (m.prom ? "=" : "");
}
string mvDesc(int ci, const Mv& m, int side, int wk, int bk) {
    bool king = (side == 0 ? m.from == wk : m.from == bk);
    string s = side == 0 ? "" : "...";
    s += king ? (side == 0 ? "K" : "K") : "";
    s += sqn(m.from);
    U64 enemy = side == 0 ? cfgs[ci].bp : cfgs[ci].wp;
    s += ((enemy & B(m.to)) || m.ep) ? "x" : "-";
    s += sqn(m.to);
    if (m.ep) s += "ep";
    if (m.prom) s += "=";
    return s;
}

int main(int argc, char** argv) {
    if (argc < 3) { fprintf(stderr, "usage: k66 name spec [maxN]\n"); return 1; }
    if (const char* pf = getenv("K66_PIDFILE")) { FILE* f = fopen(pf, "w"); if (f) { fprintf(f, "%d\n", (int)getpid()); fclose(f); } }
    Group g = parseGroup(argv[1], argv[2]);
    int maxN = argc > 3 ? atoi(argv[3]) : 6;
    enumerateCfgs(g.wp, g.bp);
    size_t n = cfgs.size();
    printf("group %s  %s\nconfigurations %zu (states %zu per T-position)\n", g.name.c_str(), argv[2], n, n * BS);
    fflush(stdout);
    int c0 = findCfg(g.wp, g.bp, -1);
    int roots[2] = {g.bk0, g.bk1};

    Solved SP = solve(mkP());
    auto PV = [&](int ci, int side, int wk, int bk) { return SP.val[0][(size_t)ci * BS + sidx(side, wk, bk)]; };
    // ---- Definition 4.8 (over form) ----
    bool exact = true;
    vector<Mv> mv;
    struct Bad { int root; Mv m; };
    vector<Bad> bads;
    printf("\n== Definition 4.8 in P ==\n");
    for (int r = 0; r < 2; r++) {
        int bk = roots[r], obk = roots[1 - r];
        const Cfg& c = cfgs[c0];
        bool v0 = validState(c, 1, g.wk, bk) && validState(c, 0, g.wk, bk);
        bool chk = inCheck(c, 0, g.wk, bk) || inCheck(c, 1, g.wk, bk);
        printf("root k%s: legal both sides %d, a king in check %d; P value Black to move %s, White to move %s\n", sqn(bk).c_str(), v0, chk,
               vs(PV(c0, 1, g.wk, bk)), vs(PV(c0, 0, g.wk, bk)));
        if (!v0 || chk) exact = false;
        // (O1)
        genMoves(c0, 1, g.wk, bk, mv);
        bool shuttle = false;
        for (auto& m : mv) {
            if (m.kind == M_STATE && m.cfg == c0 && m.bk == obk && m.from == bk) { shuttle = true; continue; }
            uint8_t v = m.kind == M_TERM_WIN ? VL : PV(m.cfg, m.side, m.wk, m.bk);
            printf("  bad %s: P %s\n", mvDesc(c0, m, 1, g.wk, bk).c_str(), vs(v));
            if (v != VW) exact = false;
            if (m.kind == M_STATE) bads.push_back({r, m});
        }
        if (!shuttle) { printf("  shuttle illegal\n"); exact = false; }
        // (O2)-(O4)
        genMoves(c0, 0, g.wk, bk, mv);
        int nfreeze = 0;
        for (auto& m : mv) {
            uint8_t v = m.kind == M_TERM_WIN ? VW : PV(m.cfg, m.side, m.wk, m.bk);
            if (m.kind == M_TERM_WIN) { printf("  White promotes at root: not exact\n"); exact = false; continue; }
            if (v == VL) continue;
            nfreeze++;
            printf("  freeze %s (q Black to move, right %s: %s)\n", mvDesc(c0, m, 0, g.wk, bk).c_str(), cfgs[m.cfg].ep >= 0 ? "yes" : "no", vs(v));
            int q = m.cfg, qb = baseOf[m.cfg];
            const Cfg& qc = cfgs[q];
            bool qchk = inCheck(qc, 0, m.wk, m.bk) || inCheck(qc, 1, m.wk, m.bk);
            if (qchk) { printf("    a king in check at q\n"); exact = false; }
            // (O3): q Black to move (with the right): legal move, every move loses
            vector<Mv> mv2;
            genMoves(q, 1, m.wk, m.bk, mv2);
            bool o3 = !mv2.empty();
            for (auto& m2 : mv2) { uint8_t v2 = m2.kind == M_TERM_WIN ? VL : PV(m2.cfg, m2.side, m2.wk, m2.bk); if (v2 != VW) o3 = false; }
            if (q != qb) {  // also without the right
                genMoves(qb, 1, m.wk, m.bk, mv2);
                for (auto& m2 : mv2) { uint8_t v2 = m2.kind == M_TERM_WIN ? VL : PV(m2.cfg, m2.side, m2.wk, m2.bk); if (v2 != VW) o3 = false; }
            }
            genMoves(qb, 0, m.wk, m.bk, mv2);
            bool o4 = validState(cfgs[qb], 0, m.wk, m.bk) && !mv2.empty();
            for (auto& m2 : mv2) { uint8_t v2 = m2.kind == M_TERM_WIN ? VW : PV(m2.cfg, m2.side, m2.wk, m2.bk); if (v2 != VL) o4 = false; }
            printf("    (O3) %d  (O4) %d   q White to move P %s\n", o3, o4, vs(PV(qb, 0, m.wk, m.bk)));
            if (!o3 || !o4) exact = false;
        }
        if (nfreeze == 0) exact = false;
    }
    printf("EXACT %s\n", exact ? "yes" : "NO");
    printf("bad Black root moves: %zu\n", bads.size());
    fflush(stdout);
    if (!exact) return 0;

    if (argc > 5 && string(argv[4]) == "explain") {
        // White's moves at x_m (bad move k) with the value after each in P, beside 0, beside -1, in Aux;
        // and the same board with Black to move (no right) in P and beside 0.
        int k = atoi(argv[5]);
        Solved S0 = solve(mkZero()), S1 = solve(mkMinus1()), SA = solve(mkUnder());
        const Mv& b = bads[k].m;
        int ci = b.cfg, wk = b.wk, bk = b.bk;
        auto val = [&](const Solved& S, int tp, int c, int sd, int w, int bb) { return S.val[tp][(size_t)c * BS + sidx(sd, w, bb)]; };
        printf("\n== x_m after %s: White to move: P %s, beside 0 %s, beside -1 %s, Aux %s ==\n", mvDesc(c0, b, 1, g.wk, roots[bads[k].root]).c_str(),
               vs(val(SP, 0, ci, 0, wk, bk)), vs(val(S0, 0, ci, 0, wk, bk)), vs(val(S1, 0, ci, 0, wk, bk)), val(SA, 0, ci, 0, wk, bk) == VW ? "W" : "lost");
        genMoves(ci, 0, wk, bk, mv);
        for (auto& m : mv) {
            if (m.kind == M_TERM_WIN) { printf("  %s promotes\n", mvDesc(ci, m, 0, wk, bk).c_str()); continue; }
            printf("  %-10s P %s  0 %s  -1(token unspent) %s  Aux(under unspent) %s\n", mvDesc(ci, m, 0, wk, bk).c_str(), vs(val(SP, 0, m.cfg, 1, m.wk, m.bk)),
                   vs(val(S0, 0, m.cfg, 1, m.wk, m.bk)), vs(val(S1, 0, m.cfg, 1, m.wk, m.bk)), val(SA, 0, m.cfg, 1, m.wk, m.bk) == VW ? "W" : "lost");
        }
        int bc = baseOf[ci];
        if (!inCheck(cfgs[ci], 0, wk, bk)) {
            printf("  pass (Aux): Black to move at the same board: Aux %s; P %s, beside 0 %s\n", val(SA, 0, bc, 1, wk, bk) == VW ? "W" : "lost",
                   vs(val(SP, 0, bc, 1, wk, bk)), vs(val(S0, 0, bc, 1, wk, bk)));
            genMoves(bc, 1, wk, bk, mv);
            for (auto& m : mv) {
                if (m.kind == M_TERM_WIN) { printf("    %s promotes\n", mvDesc(bc, m, 1, wk, bk).c_str()); continue; }
                printf("    %-12s P %s  0 %s  Aux(under unspent) %s  Aux(after Black's freeze) %s\n", mvDesc(bc, m, 1, wk, bk).c_str(), vs(val(SP, 0, m.cfg, 0, m.wk, m.bk)),
                       vs(val(S0, 0, m.cfg, 0, m.wk, m.bk)), val(SA, 0, m.cfg, 0, m.wk, m.bk) == VW ? "W" : "lost", val(SA, 1, m.cfg, 0, m.wk, m.bk) == VW ? "W" : "lost");
            }
            printf("    ...freeze in under: White to move, board unchanged: Aux %s\n", val(SA, 1, bc, 0, wk, bk) == VW ? "W" : "lost");
        }
        return 0;
    }
    if (argc > 6 && string(argv[4]) == "pv") {
        // line of play beside u_0 of T_N from x_m of bad move number k (0-based, in the order printed)
        int N = atoi(argv[5]), k = atoi(argv[6]), plies = argc > 7 ? atoi(argv[7]) : 40;
        SP.val.clear(); SP.rnk.clear();
        Solved ST = solve(mkT(N));
        struct St { int ci, side, wk, bk, tp; };
        St s{bads[k].m.cfg, 0, bads[k].m.wk, bads[k].m.bk, 0};
        auto V = [&](const St& x) { return ST.val[x.tp][(size_t)x.ci * BS + sidx(x.side, x.wk, x.bk)]; };
        auto Rk = [&](const St& x) { return ST.rnk[x.tp][(size_t)x.ci * BS + sidx(x.side, x.wk, x.bk)]; };
        auto tname = [&](int tp) { return tp == N + 1 ? string("z") : "u" + to_string(tp); };
        printf("\n== line of play beside T_%d after %s: start value %s ==\n", N, mvDesc(c0, bads[k].m, 1, g.wk, roots[bads[k].root]).c_str(), vs(V(s)));
        for (int ply = 0; ply < plies; ply++) {
            const Cfg& c = cfgs[s.ci];
            struct Opt { string d; int term; St t; uint8_t v; };
            vector<Opt> opts;
            genMoves(s.ci, s.side, s.wk, s.bk, mv);
            for (auto& m : mv) {
                if (m.kind == M_TERM_WIN) opts.push_back({mvDesc(s.ci, m, s.side, s.wk, s.bk), 1, s, (uint8_t)(s.side == 0 ? VW : VL)});
                else { St t{m.cfg, m.side, m.wk, m.bk, s.tp}; opts.push_back({mvDesc(s.ci, m, s.side, s.wk, s.bk), 0, t, V(t)}); }
            }
            if (!inCheck(c, s.side, s.wk, s.bk) && s.tp <= N) {
                if (s.side == 0) {
                    if (s.tp == N) opts.push_back({"T:u" + to_string(N) + "->(+)", 1, s, VW});
                    else { St t{baseOf[s.ci], 1, s.wk, s.bk, s.tp + 1}; opts.push_back({"T:" + tname(s.tp) + "->" + tname(s.tp + 1), 0, t, V(t)}); }
                } else { St t{baseOf[s.ci], 0, s.wk, s.bk, N + 1}; opts.push_back({"...T:" + tname(s.tp) + "->z", 0, t, V(t)}); }
            }
            uint8_t cur = V(s);
            printf("%2d %s to move, K%s k%s, T at %s, value %s, rank %d | ", ply, s.side ? "Black" : "White", sqn(s.wk).c_str(), sqn(s.bk).c_str(), tname(s.tp).c_str(), vs(cur), Rk(s));
            for (auto& o : opts) printf("%s:%s ", o.d.c_str(), vs(o.v));
            printf("\n");
            if (opts.empty()) { printf("   no move: %s loses\n", s.side ? "Black" : "White"); break; }
            // choose: winner -> terminal, else successor of the same value with the smallest rank (exits rank as -1);
            // loser -> successor with the largest rank; draw -> a drawing successor, preferring the group
            int best = -1; long bkey = 0;
            int me = s.side == 0 ? VW : VL;
            for (size_t i = 0; i < opts.size(); i++) {
                auto& o = opts[i];
                long key;
                if (cur == me) {
                    if (o.v != me) continue;
                    if (o.term) key = -1000000; else key = (o.t.ci == s.ci && o.t.tp == s.tp) ? Rk(o.t) : -1 - (long)(o.t.tp != s.tp ? 0 : 1);
                    key = -key;
                } else if (cur == VD) {
                    if (o.v != VD) continue;
                    key = (o.d.find("T:") == string::npos) ? 1 : 0;
                } else {
                    key = o.term ? -1000000 : ((o.t.ci == s.ci && o.t.tp == s.tp) ? Rk(o.t) : 0);
                }
                if (best < 0 || key > bkey) { best = i; bkey = key; }
            }
            printf("   -> %s\n", opts[best].d.c_str());
            if (opts[best].term) { printf("   ends: %s\n", vs(opts[best].v)); break; }
            s = opts[best].t;
        }
        return 0;
    }
    // ---- sums ----
    Solved S0 = solve(mkZero());
    auto at = [&](const Solved& S, int tp, const Mv& m) { return S.val[tp][(size_t)m.cfg * BS + sidx(m.side, m.wk, m.bk)]; };
    vector<uint8_t> b0(bads.size()), b1(bads.size()), ax(bads.size());
    for (size_t k = 0; k < bads.size(); k++) b0[k] = at(S0, 0, bads[k].m);
    S0.val.clear(); S0.rnk.clear();
    { Solved S1 = solve(mkMinus1()); for (size_t k = 0; k < bads.size(); k++) b1[k] = at(S1, 0, bads[k].m); }
    { Solved SA = solve(mkUnder()); for (size_t k = 0; k < bads.size(); k++) ax[k] = at(SA, 0, bads[k].m); }
    Solved ST = solve(mkT(maxN));
    printf("\n== bad moves: beside 0, beside -1 (B1), Aux, ladders T_0..T_%d (x_m + u_0, White to move) ==\n", maxN);
    for (size_t k = 0; k < bads.size(); k++) {
        const Mv& m = bads[k].m;
        printf("root k%s %-12s 0:%s  -1:%s  Aux:%s  T:", sqn(roots[bads[k].root]).c_str(), mvDesc(c0, m, 1, g.wk, roots[bads[k].root]).c_str(),
               vs(b0[k]), vs(b1[k]), ax[k] == VW ? "W" : "lost");
        for (int N = 0; N <= maxN; N++) printf(" %s", vs(ST.val[maxN - N][(size_t)m.cfg * BS + sidx(m.side, m.wk, m.bk)]));
        printf("%s\n", (b1[k] != VW) ? "   <- (B1) fails" : "");
    }
    printf("\n== roots, Black to move, beside u_0 of T_N (N = 0..%d) ==\n", maxN);
    for (int r = 0; r < 2; r++) {
        printf("root k%s:", sqn(roots[r]).c_str());
        for (int N = 0; N <= maxN; N++) printf(" %s", vs(ST.val[maxN - N][(size_t)c0 * BS + sidx(1, g.wk, roots[r])]));
        printf("\n");
    }
    fprintf(stderr, "peak planned allocation %.1f MB\n", peakAlloc / 1048576.0);
    return 0;
}

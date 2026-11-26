// K67 copy, unchanged, of kings/delegate/out/K65/src/r48.cpp.
// K65 copy: enum accepts 2 or 3 files (marked K65); nothing else changed.
// K48: r45.cpp (K45 referee) with a flat-board option added (board names pln:WxH or flat:WxH); otherwise unchanged.
// K45 referee: independent solver of model P (LOOPY Definition 1.5) on cyl:WxH, written from SPEC.md
// and LOOPY Definition 4.8 without reading the investigator's code. Kings and pawns only; the first
// promotion wins for the promoter; checkmate loses; stalemate and endless play are draws; e.p. on.
// Layers = pawn sets (masks); pawn moves and captures go to child layers (solved first, memoised);
// king moves inside a layer are solved by retrograde analysis with move counters.
// Modes:
//   r45 val  cyl:WxH          < positions      -> value W/D/L/X from White's view
//   r45 moves cyl:WxH         < positions      -> every legal move with the value of the position after it
//   r45 group cyl:WxH over|under <pawns> <shuttle sq1> <sq2> <other king sq>  -> clauses (O1)..(O4)
//   r45 enum cyl:WxH f1,f2,f3 maxW maxB         -> exhaustive Definition 4.8 test (over orientation), counts + hits
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
#include <memory>
#include <algorithm>
using namespace std;
typedef unsigned __int128 M;
static int W, H, N, FLAT = 0;
static inline M bit(int s) { return ((M)1) << s; }
static inline int FI(int s) { return s % W; }
static inline int RK(int s) { return s / W; }
static inline int SQ(int f, int r) { if (FLAT) return (f < 0 || f >= W) ? -1 : f + r * W; return ((f % W) + W) % W + r * W; }
static inline M bitS(int s) { return s < 0 ? (M)0 : bit(s); }
static inline bool adj(int a, int b) {
    int df = abs(FI(a) - FI(b)); if (!FLAT) df = min(df, W - df);
    int dr = abs(RK(a) - RK(b));
    return df <= 1 && dr <= 1 && a != b;
}
static inline int kdist(int a, int b) {
    int df = abs(FI(a) - FI(b)); if (!FLAT) df = min(df, W - df);
    return max(df, abs(RK(a) - RK(b)));
}
// is square s attacked by pawns of colour c (0 white, 1 black) in mask P
static inline bool pattacked(int s, int c, M P) {
    int f = FI(s), r = RK(s);
    int pr = (c == 0) ? r - 1 : r + 1;  // a white pawn attacks upward, so it stands one rank below
    if (pr < 0 || pr >= H) return false;
    return (P & bitS(SQ(f - 1, pr))) || (P & bitS(SQ(f + 1, pr)));
}
struct Key { M w, b; bool operator==(const Key &o) const { return w == o.w && b == o.b; } };
struct KH { size_t operator()(const Key &k) const {
    unsigned long long a = (unsigned long long)k.w ^ (unsigned long long)(k.w >> 64) * 0x9E3779B97F4A7C15ULL;
    unsigned long long b = (unsigned long long)k.b ^ (unsigned long long)(k.b >> 64) * 0xC2B2AE3D27D4EB4FULL;
    return a * 31 + b * 0x165667B19E3779F9ULL; } };
// values for side to move: 0 draw, 1 win, 2 loss, 3 illegal
struct Layer { vector<unsigned char> v; };
static unordered_map<Key, unique_ptr<Layer>, KH> memo;
struct Mv { int kind; Key ch; int wk, bk, ep; int from, to; bool promo; };
// kind 0 = in-layer king move; 1 = to child layer (no ep); 2 = to child layer with ep square

static inline int idx(int wk, int bk, int stm) { return (wk * N + bk) * 2 + stm; }

static bool legalState(const Key &k, int wk, int bk, int stm) {
    if (wk == bk) return false;
    M occ = k.w | k.b;
    if (occ & bit(wk)) return false;
    if (occ & bit(bk)) return false;
    if (adj(wk, bk)) return false;
    // side not to move must not be in check
    if (stm == 0) { if (pattacked(bk, 0, k.w)) return false; }
    else { if (pattacked(wk, 1, k.b)) return false; }
    return true;
}
static bool inCheck(const Key &k, int wk, int bk, int stm) {
    return stm == 0 ? pattacked(wk, 1, k.b) : pattacked(bk, 0, k.w);
}
static void gen(const Key &k, int wk, int bk, int stm, int ep, vector<Mv> &out) {
    out.clear();
    int c = stm, my = c == 0 ? wk : bk, en = c == 0 ? bk : wk;
    M P = c == 0 ? k.w : k.b, Q = c == 0 ? k.b : k.w;
    int d = c == 0 ? 1 : -1;
    // king moves
    int f = FI(my), r = RK(my);
    for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
        if (!df && !dr) continue;
        int rr = r + dr; if (rr < 0 || rr >= H) continue;
        int t = SQ(f + df, rr); if (t < 0) continue;
        if (P & bit(t)) continue;
        if (t == en || adj(t, en)) continue;
        Mv m; m.promo = false; m.ep = -1; m.from = my; m.to = t;
        if (Q & bit(t)) {
            M Q2 = Q & ~bit(t);
            if (pattacked(t, 1 - c, Q2)) continue;
            m.kind = 1; m.ch = c == 0 ? Key{P, Q2} : Key{Q2, P};
        } else {
            if (pattacked(t, 1 - c, Q)) continue;
            m.kind = 0; m.ch = k;
        }
        m.wk = c == 0 ? t : wk; m.bk = c == 0 ? bk : t;
        out.push_back(m);
    }
    // pawn moves
    int last = c == 0 ? H - 1 : 0, start = c == 0 ? 1 : H - 2;
    for (int p = 0; p < N; p++) {
        if (!(P & bit(p))) continue;
        int pf = FI(p), pr = RK(p), tr = pr + d;
        if (tr < 0 || tr >= H) continue;
        auto add = [&](int t, M P2, M Q2, int epn) {
            // legality: own king not attacked by enemy pawns after the move
            if (pattacked(my, 1 - c, Q2)) return;
            Mv m; m.from = p; m.to = t; m.wk = wk; m.bk = bk; m.ep = epn;
            if (RK(t) == last) { m.promo = true; m.kind = 1; m.ch = k; out.push_back(m); return; }
            m.promo = false; m.kind = epn >= 0 ? 2 : 1;
            m.ch = c == 0 ? Key{P2, Q2} : Key{Q2, P2};
            out.push_back(m);
        };
        int t = SQ(pf, tr);
        M occ = P | Q | bit(wk) | bit(bk);
        if (!(occ & bit(t))) {
            add(t, (P & ~bit(p)) | bit(t), Q, -1);
            if (pr == start) {
                int t2 = SQ(pf, tr + d);
                if (tr + d >= 0 && tr + d < H && !(occ & bit(t2))) add(t2, (P & ~bit(p)) | bit(t2), Q, t);
            }
        }
        for (int df = -1; df <= 1; df += 2) {
            int tc = SQ(pf + df, tr); if (tc < 0) continue;
            if (Q & bit(tc)) add(tc, (P & ~bit(p)) | bit(tc), Q & ~bit(tc), -1);
            else if (ep >= 0 && tc == ep) {
                int cap = SQ(FI(ep), RK(ep) - d);
                if (Q & bit(cap)) add(tc, (P & ~bit(p)) | bit(tc), Q & ~bit(cap), -1);
            }
        }
    }
}
static Layer *solve(const Key &k);
static int evalEp(const Key &k, int wk, int bk, int stm, int ep);
// value of the position after move m, for the side that made it: 1 mover wins, 2 mover loses, 0 draw
static int afterVal(int stm, const Mv &m) {
    if (m.promo) return 1;
    int o = 1 - stm, v;
    if (m.kind == 2) v = evalEp(m.ch, m.wk, m.bk, o, m.ep);
    else v = solve(m.ch)->v[idx(m.wk, m.bk, o)];
    return v == 1 ? 2 : v == 2 ? 1 : 0;
}
static int evalEp(const Key &k, int wk, int bk, int stm, int ep) {
    if (!legalState(k, wk, bk, stm)) return 3;
    vector<Mv> ms; gen(k, wk, bk, stm, ep, ms);
    if (ms.empty()) return inCheck(k, wk, bk, stm) ? 2 : 0;
    bool anyDraw = false;
    for (auto &m : ms) { int a = afterVal(stm, m); if (a == 1) return 1; if (a == 0) anyDraw = true; }
    return anyDraw ? 0 : 2;
}
static Key lastK; static Layer *lastL = nullptr;   // K48: one-entry front cache for memo (speed only)
static Layer *solve(const Key &k) {
    if (lastL && k == lastK) return lastL;
    auto it = memo.find(k);
    if (it != memo.end()) { lastK = k; lastL = it->second.get(); return lastL; }
    int S = N * N * 2;
    vector<unsigned char> val(S, 3);
    vector<int> cnt(S, 0);
    vector<vector<int>> succ(S);
    vector<Mv> ms;
    vector<int> q;
    // first pass: children (recursion before inserting this layer)
    vector<unsigned char> ext(S, 0); // 1 = has external move to opp loss (win); 2 = has external draw
    for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) for (int stm = 0; stm < 2; stm++) {
        if (!legalState(k, wk, bk, stm)) continue;
        int s = idx(wk, bk, stm);
        gen(k, wk, bk, stm, -1, ms);
        int c = 0; bool win = false, dr = false;
        for (auto &m : ms) {
            if (m.kind == 0) { succ[s].push_back(idx(m.wk, m.bk, 1 - stm)); c++; continue; }
            int a = afterVal(stm, m);
            if (a == 1) win = true; else if (a == 0) { dr = true; c++; }
        }
        cnt[s] = c;
        if (win) val[s] = 1;
        else if (ms.empty()) val[s] = inCheck(k, wk, bk, stm) ? 2 : 0;  // mate / stalemate
        else if (c == 0) val[s] = 2;
        else val[s] = 4;  // undetermined
    }
    // reverse edges
    vector<int> rs(S + 1, 0);
    for (int s = 0; s < S; s++) for (int t : succ[s]) rs[t + 1]++;
    for (int s = 0; s < S; s++) rs[s + 1] += rs[s];
    vector<int> pos(rs.begin(), rs.end() - 1), pred(rs[S]);
    for (int s = 0; s < S; s++) for (int t : succ[s]) pred[pos[t]++] = s;
    for (int s = 0; s < S; s++) if (val[s] == 1 || val[s] == 2) q.push_back(s);
    for (size_t i = 0; i < q.size(); i++) {
        int t = q[i];
        for (int j = rs[t]; j < rs[t + 1]; j++) {
            int s = pred[j];
            if (val[s] != 4) continue;
            if (val[t] == 2) { val[s] = 1; q.push_back(s); }
            else if (--cnt[s] == 0) { val[s] = 2; q.push_back(s); }
        }
    }
    for (int s = 0; s < S; s++) if (val[s] == 4) val[s] = 0;
    auto L = make_unique<Layer>(); L->v.swap(val);
    Layer *res = L.get();
    memo.emplace(k, std::move(L));
    lastK = k; lastL = res;
    return res;
}
// ---------- parsing ----------
static int parseSq(const char *s) { int f = s[0] - 'a'; int r = atoi(s + 1) - 1; return f + r * W; }
static string sqName(int s) { char b[8]; snprintf(b, 8, "%c%d", 'a' + FI(s), RK(s) + 1); return b; }
static bool parseBoard(const char *b) {
    if (!strncmp(b, "pln:", 4) || !strncmp(b, "flat:", 5)) FLAT = 1; else if (strncmp(b, "cyl:", 4)) return false;
    if (sscanf(strchr(b, ':') + 1, "%dx%d", &W, &H) != 2) return false;
    N = W * H; return N <= 128;
}
struct Pos { Key k; int wk, bk, stm, ep; };
static bool parsePos(const string &line, Pos &p) {
    p.k = {0, 0}; p.wk = p.bk = -1; p.stm = 0; p.ep = -1;
    char buf[4096]; strncpy(buf, line.c_str(), 4095); buf[4095] = 0;
    vector<string> tok; for (char *t = strtok(buf, " \t\n"); t; t = strtok(0, " \t\n")) tok.push_back(t);
    if (tok.size() < 2) return false;
    for (size_t i = 0; i + 2 < tok.size(); i++) {
        const string &t = tok[i]; int s = parseSq(t.c_str() + 1);
        if (t[0] == 'K') p.wk = s; else if (t[0] == 'k') p.bk = s;
        else if (t[0] == 'P') p.k.w |= bit(s); else if (t[0] == 'p') p.k.b |= bit(s); else return false;
    }
    p.stm = tok[tok.size() - 2] == "w" ? 0 : 1;
    p.ep = tok.back() == "-" ? -1 : parseSq(tok.back().c_str());
    return true;
}
static char whiteView(int v, int stm) {
    if (v == 3) return 'X'; if (v == 0) return 'D';
    bool stmWins = v == 1; bool whiteWins = (stm == 0) == stmWins; return whiteWins ? 'W' : 'L';
}
static int value(const Pos &p) {
    // pawn on first/last rank -> illegal
    for (int s = 0; s < N; s++) {
        if ((p.k.w & bit(s)) && (RK(s) == 0 || RK(s) == H - 1)) return 3;
        if ((p.k.b & bit(s)) && (RK(s) == 0 || RK(s) == H - 1)) return 3;
    }
    if ((p.k.w & p.k.b)) return 3;
    if (p.ep >= 0) return evalEp(p.k, p.wk, p.bk, p.stm, p.ep);
    if (!legalState(p.k, p.wk, p.bk, p.stm)) return 3;
    return solve(p.k)->v[idx(p.wk, p.bk, p.stm)];
}
static string mvName(const Mv &m) { return sqName(m.from) + "-" + sqName(m.to) + (m.promo ? "=" : "") + (m.ep >= 0 ? "(dbl)" : ""); }

// ---------- Definition 4.8 test (under orientation: White shuttles on z0,z1, Black king on b0) ----------
// For the over orientation we colour-mirror the configuration (rank r -> H-1-r, colours swapped).
struct GroupRes { bool k12, o1, o2, promoFreeze, o3, o4; int nfreeze[2]; string detail; };
static GroupRes testUnder(const Key &k, int z0, int z1, int b0, bool verbose) {
    GroupRes R; R.k12 = R.o1 = R.o2 = R.o3 = R.o4 = false; R.promoFreeze = false; R.nfreeze[0] = R.nfreeze[1] = 0;
    char line[512];
    M occ = k.w | k.b;
    int z[2] = {z0, z1};
    // K1: z squares empty, not attacked by a Black pawn; b0 empty, not attacked by a White pawn. K2: dist >= 2.
    if (!adj(z0, z1)) return R;
    for (int a = 0; a < 2; a++) if ((occ & bit(z[a])) || pattacked(z[a], 1, k.b)) return R;
    if ((occ & bit(b0)) || pattacked(b0, 0, k.w)) return R;
    if (kdist(b0, z0) < 2 || kdist(b0, z1) < 2) return R;
    R.k12 = true;
    vector<Mv> ms, ms2;
    // (U1) White-to-move roots: every non-shuttle White move loses at once; shuttle legal
    bool u1 = true;
    for (int a = 0; a < 2; a++) {
        gen(k, z[a], b0, 0, -1, ms);
        bool sh = false;
        for (auto &m : ms) {
            bool isSh = !m.promo && m.kind == 0 && m.from == z[a] && m.to == z[1 - a];
            int av = afterVal(0, m);
            if (verbose) { snprintf(line, 512, "  U1 root z=%s W to move: %s -> %s%s\n", sqName(z[a]).c_str(), mvName(m).c_str(), av == 1 ? "wins" : av == 2 ? "loses" : "draws", isSh ? " (shuttle)" : ""); R.detail += line; }
            if (isSh) { sh = true; continue; }
            if (av != 2) { u1 = false; if (!verbose) break; }
        }
        if (!sh) u1 = false;
        if (!u1 && !verbose) break;
    }
    R.o1 = u1; if (!u1 && !verbose) return R;
    // (U2) Black-to-move roots: Black has a freeze (move that does not lose at once); no freeze a promotion
    bool u2 = true, u3 = true, u4 = true;
    for (int a = 0; a < 2; a++) {
        gen(k, z[a], b0, 1, -1, ms);
        int nf = 0;
        for (auto &m : ms) {
            int av = afterVal(1, m);
            if (verbose) { snprintf(line, 512, "  U2 root z=%s B to move: %s -> %s\n", sqName(z[a]).c_str(), mvName(m).c_str(), av == 1 ? "wins" : av == 2 ? "loses" : "draws"); R.detail += line; }
            if (av == 2) continue;
            nf++;
            if (m.promo) { R.promoFreeze = true; continue; }
            // (U3): q with White to move (with ep flag) has a legal move, and all White moves lose at once
            gen(m.ch, m.wk, m.bk, 0, m.ep, ms2);
            bool ok3 = !ms2.empty();
            int nw = 0, nl = 0;
            for (auto &m2 : ms2) { int a2 = afterVal(0, m2); nw++; if (a2 == 2) nl++; else ok3 = false;
                if (verbose) { snprintf(line, 512, "    U3 after %s, W to move: %s -> %s\n", mvName(m).c_str(), mvName(m2).c_str(), a2 == 1 ? "wins" : a2 == 2 ? "loses" : "draws"); R.detail += line; } }
            if (!ok3) u3 = false;
            // (U4): q with Black to move (no flag): legal, Black has a move, all Black moves lose at once
            bool ok4 = legalState(m.ch, m.wk, m.bk, 1);
            if (ok4) {
                gen(m.ch, m.wk, m.bk, 1, -1, ms2);
                if (ms2.empty()) ok4 = false;
                for (auto &m2 : ms2) { int a2 = afterVal(1, m2); if (a2 != 2) ok4 = false;
                    if (verbose) { snprintf(line, 512, "    U4 after %s, B to move: %s -> %s\n", mvName(m).c_str(), mvName(m2).c_str(), a2 == 1 ? "wins" : a2 == 2 ? "loses" : "draws"); R.detail += line; } }
            } else if (verbose) R.detail += "    U4: q with Black to move is illegal\n";
            if (!ok4) u4 = false;
            if (verbose) { snprintf(line, 512, "  freeze %s at z=%s: U3 %s, U4 %s\n", mvName(m).c_str(), sqName(z[a]).c_str(), ok3 ? "holds" : "FAILS", ok4 ? "holds" : "FAILS"); R.detail += line; }
        }
        R.nfreeze[a] = nf;
        if (nf == 0) u2 = false;
    }
    R.o2 = u1 && u2 && !R.promoFreeze; R.o3 = R.o2 && u3; R.o4 = R.o3 && u4;
    return R;
}
static Key mirrorKey(const Key &k) {
    Key r{0, 0};
    for (int s = 0; s < N; s++) {
        int t = FI(s) + (H - 1 - RK(s)) * W;
        if (k.w & bit(s)) r.b |= bit(t);
        if (k.b & bit(s)) r.w |= bit(t);
    }
    return r;
}
static int mirrorSq(int s) { return FI(s) + (H - 1 - RK(s)) * W; }

int main(int argc, char **argv) {
    if (argc < 3 || !parseBoard(argv[2])) { fprintf(stderr, "usage: see header\n"); return 1; }
    string mode = argv[1];
    if (mode == "val" || mode == "moves") {
        char buf[4096];
        while (fgets(buf, sizeof buf, stdin)) {
            string line(buf); while (!line.empty() && (line.back() == '\n' || line.back() == '\r')) line.pop_back();
            if (line.empty() || line[0] == '#') { printf("%s\n", line.c_str()); continue; }
            Pos p; if (!parsePos(line, p)) { printf("%s | ?\n", line.c_str()); continue; }
            int v = value(p);
            printf("%s | %c\n", line.c_str(), whiteView(v, p.stm));
            if (mode == "moves" && v != 3) {
                vector<Mv> ms; gen(p.k, p.wk, p.bk, p.stm, p.ep, ms);
                for (auto &m : ms) { int a = afterVal(p.stm, m); printf("   %s -> mover %s\n", mvName(m).c_str(), a == 1 ? "wins" : a == 2 ? "loses" : "draws"); }
            }
            fflush(stdout);
        }
        return 0;
    }
    if (mode == "group") {
        // r45 group cyl:WxH over|under "Pb2 Pb4 pa4 ..." z0 z1 other
        string orient = argv[3];
        Pos p; string s = string(argv[4]) + " w -";
        parsePos(s, p);
        int z0 = parseSq(argv[5]), z1 = parseSq(argv[6]), o = parseSq(argv[7]);
        Key k = p.k;
        if (orient == "over") { k = mirrorKey(k); z0 = mirrorSq(z0); z1 = mirrorSq(z1); o = mirrorSq(o); }
        GroupRes R = testUnder(k, z0, z1, o, true);
        if (orient == "over") printf("(over orientation, reported in the colour-mirrored under frame: White = original Black, ranks flipped)\n");
        printf("%s", R.detail.c_str());
        printf("K1K2 %d  U1/O1 %d  U2/O2 %d (freezes %d,%d; promo freeze %d)  U3/O3 %d  U4/O4 %d\n", R.k12, R.o1, R.o2, R.nfreeze[0], R.nfreeze[1], R.promoFreeze, R.o3, R.o4);
        return 0;
    }
    if (mode == "enum") {
        // r45 enum cyl:WxH f1,f2,f3 maxW maxB : every pawn configuration with <= maxW White, <= maxB Black pawns on the
        // three files, ranks 2..H-1, at most one pawn per square; every placement; under orientation (over = colour mirror,
        // and the mirror of the domain is the domain itself when maxW == maxB; otherwise run with swapped counts).
        int fs[3] = {-1, -1, -1}; int nf = sscanf(argv[3], "%d,%d,%d", &fs[0], &fs[1], &fs[2]);   // K65: 2 or 3 files
        if (nf < 2) { fprintf(stderr, "need 2 or 3 files\n"); return 1; }
        int maxW = atoi(argv[4]), maxB = atoi(argv[5]);
        vector<int> sqs; for (int i = 0; i < nf; i++) for (int r = 1; r <= H - 2; r++) sqs.push_back(SQ(fs[i], r));   // K65: nf files
        int ns = sqs.size();
        long long nlayers = 0, nplace = 0, n1 = 0, n2 = 0, n3 = 0, n4 = 0, nPromo = 0;
        // enumerate assignments: each square empty / white / black
        vector<int> a(ns, 0);
        long long total = 1; for (int i = 0; i < ns; i++) total *= 3;
        for (long long code = 0; code < total; code++) {
            long long c = code; int nw = 0, nb = 0; Key k{0, 0};
            for (int i = 0; i < ns; i++) { a[i] = c % 3; c /= 3; if (a[i] == 1) { nw++; k.w |= bit(sqs[i]); } else if (a[i] == 2) { nb++; k.b |= bit(sqs[i]); } }
            if (nw > maxW || nb > maxB) continue;
            nlayers++;
            M occ = k.w | k.b;
            for (int z0 = 0; z0 < N; z0++) {
                if ((occ & bit(z0)) || pattacked(z0, 1, k.b)) continue;
                for (int dz = 0; dz < 8; dz++) {
                    // each unordered adjacent pair once: z1 > z0
                    int df[8] = {-1, -1, -1, 0, 0, 1, 1, 1}, dr[8] = {-1, 0, 1, -1, 1, -1, 0, 1};
                    int rr = RK(z0) + dr[dz]; if (rr < 0 || rr >= H) continue;
                    int z1 = SQ(FI(z0) + df[dz], rr); if (z1 < 0 || z1 <= z0) continue;
                    if ((occ & bit(z1)) || pattacked(z1, 1, k.b)) continue;
                    for (int b0 = 0; b0 < N; b0++) {
                        if ((occ & bit(b0)) || pattacked(b0, 0, k.w)) continue;
                        if (kdist(b0, z0) < 2 || kdist(b0, z1) < 2) continue;
                        nplace++;
                        GroupRes R = testUnder(k, z0, z1, b0, false);
                        if (R.o1) n1++;
                        if (R.promoFreeze) nPromo++;
                        if (R.o2) n2++;
                        if (R.o3) n3++;
                        if (R.o4) {
                            n4++;
                            string ps;
                            for (int s = 0; s < N; s++) { if (k.w & bit(s)) ps += " P" + sqName(s); }
                            for (int s = 0; s < N; s++) { if (k.b & bit(s)) ps += " p" + sqName(s); }
                            printf("HIT under: shuttle %s-%s, Black king %s,%s\n", sqName(z0).c_str(), sqName(z1).c_str(), sqName(b0).c_str(), ps.c_str());
                        }
                    }
                }
            }
            if ((double)memo.size() * N * N * 2 > 1.0e9) { memo.clear(); lastL = nullptr; }  // memory guard (about 1 GB of tables)
        }
        printf("SUMMARY %s:%dx%d files %d,%d,%d max %d+%d: layers %lld placements %lld U1 %lld promoFreeze %lld U1+U2 %lld loose %lld exact %lld\n",
               FLAT ? "flat" : "cyl", W, H, fs[0], fs[1], fs[2], maxW, maxB, nlayers, nplace, n1, nPromo, n2, n3, n4);
        return 0;
    }
    if (mode == "layers") {
        // r45 layers cyl:WxH < lines "Pa2 pa3 ..." : every placement, both orientations (over = colour mirror)
        char buf[4096]; long long tot4 = 0, nl = 0;
        while (fgets(buf, sizeof buf, stdin)) {
            string line(buf); while (!line.empty() && (line.back() == '\n' || line.back() == '\r')) line.pop_back();
            if (line.empty() || line[0] == '#') continue;
            Pos p; parsePos(line + " w -", p);
            for (int o = 0; o < 2; o++) {
                Key k = o == 0 ? p.k : mirrorKey(p.k);
                M occ = k.w | k.b; long long np = 0, c1 = 0, c3 = 0, c4 = 0;
                for (int z0 = 0; z0 < N; z0++) {
                    if ((occ & bit(z0)) || pattacked(z0, 1, k.b)) continue;
                    for (int z1 = z0 + 1; z1 < N; z1++) {
                        if (!adj(z0, z1) || (occ & bit(z1)) || pattacked(z1, 1, k.b)) continue;
                        for (int b0 = 0; b0 < N; b0++) {
                            if ((occ & bit(b0)) || pattacked(b0, 0, k.w)) continue;
                            if (kdist(b0, z0) < 2 || kdist(b0, z1) < 2) continue;
                            np++; GroupRes R = testUnder(k, z0, z1, b0, false);
                            c1 += R.o1; c3 += R.o3; c4 += R.o4;
                        }
                    }
                }
                nl++; tot4 += c4;
                printf("LAYER %s %s placements %lld O1 %lld loose %lld exact %lld\n", line.c_str(), o ? "over" : "under", np, c1, c3, c4);
            }
            if ((double)memo.size() * N * N * 2 > 1.0e9) { memo.clear(); lastL = nullptr; }
        }
        printf("SUMMARY layer lines %lld exact %lld\n", nl, tot4);
        return 0;
    }
    return 1;
}

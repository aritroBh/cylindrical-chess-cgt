// K42 referee solver, written from kings/SPEC.md and LOOPY Definition 2.6 (no other solver read).
// Model P: the first legal promotion wins for the promoter; mate loses; stalemate and infinite play draw.
// Engine options give the local game of Definition 2.6 for s = White:
//   bconf: Black's king may only step onto files of the mask (moves off it are not permitted);
//   wpass: White may pass when not in check (the pass clears the e.p. right);
//   qclause: a Black promotion wins only if no legal White move captures the new queen.
// Retrograde by pawn-configuration layers (pawn moves and captures leave the layer), bucket queue inside a layer.
// Modes:
//   pos   : read positions (SPEC format), print value from White's view (W/D/L/X) and depth in plies.
//   sorties: enumerate roots (both kings on a..c, <= maxw + maxb Z-pawns on a..c, ranks 2..H-1, White to move, no e.p.)
//            and White sorties (legal non-promoting moves after which Black has no legal immediate promotion);
//            print "root | move | position after | flags P0 Pinf P0q Pinfq" (1 = Black wins that local game).
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
#include <unordered_map>
#include <memory>
#include <iostream>
#include <sstream>
#include <fstream>
#include <functional>
#include <algorithm>
using namespace std;
typedef unsigned long long u64;
static int W = 8, H = 6, N = 48; static bool CYL = true; static bool NODEPTH = false;
static int sq(int f, int r) { return r * W + f; }
static int fileOf(int s) { return s % W; }
static int rankOf(int s) { return s / W; }
static int step(int s, int df, int dr) {
    int f = fileOf(s) + df, r = rankOf(s) + dr;
    if (r < 0 || r >= H) return -1;
    if (f < 0 || f >= W) { if (!CYL) return -1; f = (f + W) % W; }
    return sq(f, r);
}
struct Cfg { u64 wp, bp; int ep; bool operator==(const Cfg& o) const { return wp == o.wp && bp == o.bp && ep == o.ep; } };
struct CH { size_t operator()(const Cfg& c) const { return std::hash<u64>()(c.wp * 1000003ULL ^ (c.bp + 0x9e3779b97f4a7c15ULL) * 31 ^ (u64)(c.ep + 7)); } };
static inline bool bit(u64 b, int s) { return (b >> s) & 1ULL; }

struct Engine {
    unsigned bconf = 0;  // 0 = no confinement; else mask of files allowed for Black's king
    bool wpass = false, qclause = false, wstaleLoss = false; unsigned wconf = 0;
    // layer: val[(wk*N+bk)*2+stm] : 0 draw/unknown, 1 = side to move wins, 2 = side to move loses, 3 illegal
    struct Layer { vector<uint8_t> val, dep; };
    unordered_map<Cfg, unique_ptr<Layer>, CH> layers;

    // attacks
    bool wkAttacked(const Cfg& c, int wk, int bk) const {  // white king attacked by black pawns or adjacent to bk
        int a = step(wk, -1, 1), b = step(wk, 1, 1);
        if (a >= 0 && bit(c.bp, a)) return true;
        if (b >= 0 && bit(c.bp, b)) return true;
        return adj(wk, bk);
    }
    bool bkAttacked(const Cfg& c, int wk, int bk) const {
        int a = step(bk, -1, -1), b = step(bk, 1, -1);
        if (a >= 0 && bit(c.wp, a)) return true;
        if (b >= 0 && bit(c.wp, b)) return true;
        return adj(wk, bk);
    }
    static bool adj(int x, int y) {
        for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
            if (!df && !dr) continue; if (step(x, df, dr) == y) return true; }
        return false;
    }
    Cfg norm(Cfg c) const {  // drop an e.p. right no pawn can use (pseudo)
        if (c.ep < 0) return c;
        int t = c.ep, r = rankOf(t);
        bool ok = false;
        if (r == 2) {  // White double step; the pawn is on step(t,0,1); Black captures from there's neighbours
            int v = step(t, 0, 1), a = step(t, -1, 1), b = step(t, 1, 1);
            if (v >= 0 && bit(c.wp, v) && ((a >= 0 && bit(c.bp, a)) || (b >= 0 && bit(c.bp, b)))) ok = true;
        }
        if (r == H - 3) {  // Black double step
            int v = step(t, 0, -1), a = step(t, -1, -1), b = step(t, 1, -1);
            if (v >= 0 && bit(c.bp, v) && ((a >= 0 && bit(c.wp, a)) || (b >= 0 && bit(c.wp, b)))) ok = true;
        }
        if (!ok) c.ep = -1;
        return c;
    }
    // A move result: kind 0 = normal (successor), 1 = promotion (terminal)
    struct Mv { int kind; Cfg c; int wk, bk; bool inLayer; int qsq; string name; };
    // generate legal moves of side stm in (c, wk, bk); passes not included
    void gen(const Cfg& c, int wk, int bk, int stm, vector<Mv>& out, bool names = false) const {
        out.clear();
        u64 occ = c.wp | c.bp;
        auto nm = [&](char p, int a, int b) { if (!names) return string(); string s; s += p; s += char('a' + fileOf(a)); s += char('1' + rankOf(a)); s += char('a' + fileOf(b)); s += char('1' + rankOf(b)); return s; };
        if (stm == 0) {
            // king
            for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
                if (!df && !dr) continue; int t = step(wk, df, dr); if (t < 0 || bit(c.wp, t)) continue;
                if (wconf && !((wconf >> fileOf(t)) & 1)) continue;
                Cfg n{c.wp, c.bp & ~(1ULL << t), -1};
                if (wkAttacked(n, t, bk)) continue;
                bool cap = bit(c.bp, t);
                out.push_back({0, norm(n), t, bk, !cap && c.ep < 0, -1, nm('K', wk, t)});
            }
            for (int s = 0; s < N; s++) if (bit(c.wp, s)) {
                auto addp = [&](int t, u64 bpNew, int ep) {
                    Cfg n{(c.wp & ~(1ULL << s)) | (1ULL << t), bpNew, ep};
                    if (wkAttacked(n, wk, bk)) return;
                    if (rankOf(t) == H - 1) { n.wp &= ~(1ULL << t); out.push_back({1, n, wk, bk, false, t, nm('P', s, t)}); return; }
                    out.push_back({0, norm(n), wk, bk, false, -1, nm('P', s, t)});
                };
                int t = step(s, 0, 1);
                if (t >= 0 && !bit(occ, t) && t != wk && t != bk) {
                    addp(t, c.bp, -1);
                    if (rankOf(s) == 1) { int t2 = step(t, 0, 1);
                        if (t2 >= 0 && !bit(occ, t2) && t2 != wk && t2 != bk) addp(t2, c.bp, rankOf(t2) == H - 1 ? -1 : t); }
                }
                for (int df = -1; df <= 1; df += 2) {
                    int u = step(s, df, 1); if (u < 0) continue;
                    if (bit(c.bp, u)) addp(u, c.bp & ~(1ULL << u), -1);
                    else if (u == c.ep) { int v = step(u, 0, -1); if (v >= 0 && bit(c.bp, v)) addp(u, c.bp & ~(1ULL << v), -1); }
                }
            }
        } else {
            for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
                if (!df && !dr) continue; int t = step(bk, df, dr); if (t < 0 || bit(c.bp, t)) continue;
                if (bconf && !((bconf >> fileOf(t)) & 1)) continue;
                Cfg n{c.wp & ~(1ULL << t), c.bp, -1};
                if (bkAttacked(n, wk, t)) continue;
                bool cap = bit(c.wp, t);
                out.push_back({0, norm(n), wk, t, !cap && c.ep < 0, -1, nm('k', bk, t)});
            }
            for (int s = 0; s < N; s++) if (bit(c.bp, s)) {
                auto addp = [&](int t, u64 wpNew, int ep) {
                    Cfg n{wpNew, (c.bp & ~(1ULL << s)) | (1ULL << t), ep};
                    if (bkAttacked(n, wk, bk)) return;
                    if (rankOf(t) == 0) { n.bp &= ~(1ULL << t); out.push_back({1, n, wk, bk, false, t, nm('p', s, t)}); return; }
                    out.push_back({0, norm(n), wk, bk, false, -1, nm('p', s, t)});
                };
                int t = step(s, 0, -1);
                if (t >= 0 && !bit(occ, t) && t != wk && t != bk) {
                    addp(t, c.wp, -1);
                    if (rankOf(s) == H - 2) { int t2 = step(t, 0, -1);
                        if (t2 >= 0 && !bit(occ, t2) && t2 != wk && t2 != bk) addp(t2, c.wp, rankOf(t2) == 0 ? -1 : t); }
                }
                for (int df = -1; df <= 1; df += 2) {
                    int u = step(s, df, -1); if (u < 0) continue;
                    if (bit(c.wp, u)) addp(u, c.wp & ~(1ULL << u), -1);
                    else if (u == c.ep) { int v = step(u, 0, 1); if (v >= 0 && bit(c.wp, v)) addp(u, c.wp & ~(1ULL << v), -1); }
                }
            }
        }
    }
    // is a Black promotion on q (pawn removed in n) a win under the queen clause? (n: config after, queen on q)
    bool queenSafe(const Cfg& n, int wk, int bk, int q) const {
        if (!adj(wk, q)) return true;
        // White king captures on q: legal iff q not attacked by black pawns and not adjacent to bk
        int a = step(q, -1, 1), b = step(q, 1, 1);
        bool att = (a >= 0 && bit(n.bp, a)) || (b >= 0 && bit(n.bp, b)) || adj(q, bk);
        return att;
    }
    bool legalState(const Cfg& c, int wk, int bk, int stm) const {
        if (wk == bk || bit(c.wp | c.bp, wk) || bit(c.wp | c.bp, bk)) return false;
        if (adj(wk, bk)) return false;
        if (bconf && !((bconf >> fileOf(bk)) & 1)) return false;
        if (wconf && !((wconf >> fileOf(wk)) & 1)) return false;
        if (stm == 0) { if (bkAttacked(c, wk, bk)) return false; } else { if (wkAttacked(c, wk, bk)) return false; }
        return true;
    }
    Layer* get(const Cfg& c0) {
        Cfg c = norm(c0);
        auto it = layers.find(c); if (it != layers.end()) return it->second.get();
        unique_ptr<Layer> L(new Layer); Layer* p = L.get();
        solve(c, *p);
        if (NODEPTH) { vector<uint8_t>().swap(p->dep); }
        layers.emplace(c, std::move(L));
        return p;
    }
    // value of a state from the side-to-move's view: 1 win, 2 loss, 0 draw, 3 illegal; d = plies
    int value(const Cfg& c, int wk, int bk, int stm, int* d = nullptr) {
        Layer* L = get(c); int i = (wk * N + bk) * 2 + stm;
        if (d) *d = NODEPTH ? 0 : L->dep[i];
        return L->val[i];
    }
    void solve(const Cfg& c, Layer& L) {
        int S = N * N * 2;
        L.val.assign(S, 0); L.dep.assign(S, 0);
        vector<int> cnt(S, 0), maxd(S, 0); vector<uint8_t> escape(S, 0), fin(S, 0);
        vector<vector<int>> pred(S);
        // bucket queue: (depth, idx, kind)
        vector<vector<pair<int, int>>> bucket(512);
        auto push = [&](int d, int i, int k) { if (d >= (int)bucket.size()) bucket.resize(d + 64); bucket[d].push_back({i, k}); };
        vector<Mv> mv;
        for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) for (int stm = 0; stm < 2; stm++) {
            int i = (wk * N + bk) * 2 + stm;
            if (!legalState(c, wk, bk, stm)) { L.val[i] = 3; fin[i] = 1; continue; }
            gen(c, wk, bk, stm, mv);
            bool inCheck = stm == 0 ? wkAttacked(c, wk, bk) : bkAttacked(c, wk, bk);
            int bestWin = 1000; int nmoves = 0;
            for (auto& m : mv) {
                nmoves++;
                if (m.kind == 1) {
                    bool win = true;
                    if (stm == 1 && qclause) win = queenSafe(m.c, m.wk, m.bk, m.qsq);
                    if (win) bestWin = min(bestWin, 1); else escape[i] = 1;  // unsafe promotion: a failure for Black = not a loss for White
                    continue;
                }
                if (m.inLayer) {
                    int j = (m.wk * N + m.bk) * 2 + (1 - stm);
                    pred[j].push_back(i); cnt[i]++;
                } else {
                    int d; int v = value(m.c, m.wk, m.bk, 1 - stm, &d);
                    if (v == 2) bestWin = min(bestWin, d + 1);
                    else if (v == 1) maxd[i] = max(maxd[i], d);
                    else escape[i] = 1;
                }
            }
            if (stm == 0 && wpass && !inCheck) {
                nmoves++;
                Cfg n = c; n.ep = -1; n = norm(n);
                if (n == c) { int j = (wk * N + bk) * 2 + 1; pred[j].push_back(i); cnt[i]++; }
                else { int d; int v = value(n, wk, bk, 1, &d);
                    if (v == 2) bestWin = min(bestWin, d + 1); else if (v == 1) maxd[i] = max(maxd[i], d); else escape[i] = 1; }
            }
            if (nmoves == 0) {  // mate or stalemate
                if (inCheck) { L.val[i] = 2; L.dep[i] = 0; fin[i] = 1; }
                else if (stm == 0 && wstaleLoss) { L.val[i] = 2; L.dep[i] = 0; fin[i] = 1; }
                else { L.val[i] = 0; fin[i] = 1; }
                continue;
            }
            if (bestWin < 1000) { push(bestWin, i, 1); escape[i] = 1; }
            else if (cnt[i] == 0 && !escape[i]) push(maxd[i] + 1, i, 2);
        }
        // finalised mates propagate
        for (int i = 0; i < S; i++) if (fin[i] && L.val[i] == 2) {
            for (int p : pred[i]) if (!fin[p]) push(1, p, 1);
        }
        for (int dd = 0; dd < (int)bucket.size(); dd++) {
            for (size_t k = 0; k < bucket[dd].size(); k++) {
                auto [i, kind] = bucket[dd][k];
                if (fin[i]) continue;
                fin[i] = 1; L.val[i] = kind; L.dep[i] = dd > 255 ? 255 : dd;
                for (int p : pred[i]) {
                    if (fin[p]) continue;
                    if (kind == 2) push(dd + 1, p, 1);
                    else { cnt[p]--; maxd[p] = max(maxd[p], dd); if (cnt[p] == 0 && !escape[p]) {
                        // p's out-of-layer win candidates were already queued; queue loss
                        push(maxd[p] + 1, p, 2); } }
                }
            }
        }
    }
};

static int parseSq(const string& s) { return sq(s[0] - 'a', atoi(s.c_str() + 1) - 1); }
static string sqName(int s) { string r; r += char('a' + fileOf(s)); r += to_string(rankOf(s) + 1); return r; }
struct Pos { Cfg c; int wk, bk, stm; bool ok; };
static Pos parsePos(const string& line) {
    Pos p{{0, 0, -1}, -1, -1, 0, true};
    istringstream is(line); vector<string> tok; string t; while (is >> t) tok.push_back(t);
    if (tok.size() < 3) { p.ok = false; return p; }
    for (size_t i = 0; i + 2 < tok.size(); i++) {
        char k = tok[i][0]; int s = parseSq(tok[i].substr(1));
        if (k == 'K') p.wk = s; else if (k == 'k') p.bk = s; else if (k == 'P') p.c.wp |= 1ULL << s; else if (k == 'p') p.c.bp |= 1ULL << s; else p.ok = false;
    }
    p.stm = tok[tok.size() - 2] == "w" ? 0 : 1;
    p.c.ep = tok.back() == "-" ? -1 : parseSq(tok.back());
    return p;
}
static string posStr(const Cfg& c, int wk, int bk, int stm) {
    string s = "K" + sqName(wk);
    for (int i = 0; i < N; i++) if (bit(c.wp, i)) s += " P" + sqName(i);
    s += " k" + sqName(bk);
    for (int i = 0; i < N; i++) if (bit(c.bp, i)) s += " p" + sqName(i);
    s += stm ? " b " : " w "; s += c.ep < 0 ? "-" : sqName(c.ep);
    return s;
}
static void setBoard(const string& b) {
    CYL = b.substr(0, 3) == "cyl"; size_t x = b.find('x');
    W = atoi(b.c_str() + 4); H = atoi(b.c_str() + x + 1); N = W * H;
}
int main(int argc, char** argv) {
    string mode = argv[1]; string board = "cyl:8x6"; unsigned bconf = 0; bool wpass = false, qc = false, moves = false, wsl = false; unsigned wconf = 0;
    int maxw = 2, maxb = 2;
    for (int i = 2; i < argc; i++) {
        string a = argv[i];
        if (a == "--board") board = argv[++i];
        else if (a == "--bconf") { string f = argv[++i]; for (char ch : f) bconf |= 1u << (ch - 'a'); }
        else if (a == "--wpass") wpass = true; else if (a == "--qclause") qc = true; else if (a == "--moves") moves = true;
        else if (a == "--wconf") { string f = argv[++i]; for (char ch : f) wconf |= 1u << (ch - 'a'); } else if (a == "--wstalemate-loss") wsl = true; else if (a == "--nodepth") NODEPTH = true; else if (a == "--maxw") maxw = atoi(argv[++i]); else if (a == "--maxb") maxb = atoi(argv[++i]);
    }
    setBoard(board);
    if (mode == "pos") {
        Engine E; E.bconf = bconf; E.wpass = wpass; E.qclause = qc; E.wconf = wconf; E.wstaleLoss = wsl;
        string line;
        while (getline(cin, line)) {
            if (line.empty() || line[0] == '#') { cout << line << "\n"; continue; }
            Pos p = parsePos(line);
            if (!p.ok || !E.legalState(p.c, p.wk, p.bk, p.stm)) { cout << line << " | X\n"; continue; }
            int d; int v = E.value(p.c, p.wk, p.bk, p.stm, &d);
            char res = v == 0 ? 'D' : ((v == 1) == (p.stm == 0) ? 'W' : 'L');
            cout << line << " | " << res << " " << (v == 0 ? -1 : d);
            if (moves) {
                vector<Engine::Mv> mv; E.gen(E.norm(p.c), p.wk, p.bk, p.stm, mv, true);
                cout << " |";
                for (auto& m : mv) {
                    char r;
                    if (m.kind == 1) r = p.stm == 0 ? 'W' : ((E.qclause && !E.queenSafe(m.c, m.wk, m.bk, m.qsq)) ? 'D' : 'L');
                    else { int v2 = E.value(m.c, m.wk, m.bk, 1 - p.stm); r = v2 == 0 ? 'D' : ((v2 == 1) == (p.stm == 1) ? 'W' : 'L'); }
                    cout << " " << m.name << ":" << r;
                }
            }
            cout << "\n";
        }
        fprintf(stderr, "layers %zu\n", E.layers.size());
        return 0;
    }
    if (mode == "test") {
        // --sorties FILE (lines "root | m | after | flags"), --ctx "Pe2 pe3": value of after+G (Black to move) in P
        string sf, ctx;
        for (int i = 2; i < argc; i++) { string a = argv[i]; if (a == "--sorties") sf = argv[++i]; else if (a == "--ctx") ctx = argv[++i]; }
        Cfg g{0, 0, -1}; { istringstream is(ctx); string t; while (is >> t) { int s = parseSq(t.substr(1)); if (t[0] == 'P') g.wp |= 1ULL << s; else g.bp |= 1ULL << s; } }
        Engine E; ifstream in(sf); string line; long legal = 0, nL = 0, nD = 0, nW = 0;
        while (getline(in, line)) {
            vector<string> f; size_t a = 0, b; while ((b = line.find(" | ", a)) != string::npos) { f.push_back(line.substr(a, b - a)); a = b + 3; } f.push_back(line.substr(a));
            Pos p = parsePos(f[2]);
            Pos r = parsePos(f[0]);
            Cfg c = p.c; if ((c.wp | c.bp) & (g.wp | g.bp)) continue;
            if (bit(g.wp | g.bp, p.wk) || bit(g.wp | g.bp, r.wk)) continue;
            c.wp |= g.wp; c.bp |= g.bp;
            if (!E.legalState(c, p.wk, p.bk, 1)) continue;
            legal++;
            int v = E.value(c, p.wk, p.bk, 1);
            if (v == 1) nL++; else if (v == 0) { nD++; cout << "FAIL | " << f[0] << " | " << f[1] << " | D\n"; }
            else { nW++; cout << "FAIL | " << f[0] << " | " << f[1] << " | W\n"; }
        }
        cout << "SUM | " << ctx << " | legal " << legal << " L " << nL << " D " << nD << " W " << nW << " layers " << E.layers.size() << "\n";
        return 0;
    }
    if (mode == "sorties") {
        Engine E[4];
        for (int k = 0; k < 4; k++) { E[k].bconf = 7; E[k].wpass = (k & 1); E[k].qclause = (k >= 2); }
        Engine P;  // plain P on the bare board, only for move generation / legality
        vector<int> zsq; for (int f = 0; f < 3; f++) for (int r = 1; r <= H - 2; r++) zsq.push_back(sq(f, r));
        int Z = zsq.size(); long roots = 0, nsort = 0, nflag = 0;
        // enumerate pawn sets
        vector<u64> wsets, bsets;
        function<void(int, int, u64, int, vector<u64>&)> rec = [&](int idx, int left, u64 cur, int maxn, vector<u64>& out) {
            out.push_back(cur);
            if (left == 0) return;
            for (int j = idx; j < Z; j++) rec(j + 1, left - 1, cur | (1ULL << zsq[j]), maxn, out);
        };
        rec(0, maxw, 0, maxw, wsets); rec(0, maxb, 0, maxb, bsets);
        vector<int> fz; for (int f = 0; f < 3; f++) for (int r = 0; r < H; r++) fz.push_back(sq(f, r));
        vector<Engine::Mv> mv, mv2;
        for (u64 ws : wsets) for (u64 bs : bsets) {
            if (ws & bs) continue;
            Cfg c{ws, bs, -1};
            for (int wk : fz) for (int bk : fz) {
                if (!P.legalState(c, wk, bk, 0)) continue;
                roots++;
                P.gen(c, wk, bk, 0, mv, true);
                for (auto& m : mv) {
                    if (m.kind == 1) continue;
                    // Black immediate promotion?
                    P.gen(m.c, m.wk, m.bk, 1, mv2);
                    bool prom = false; for (auto& x : mv2) if (x.kind == 1) prom = true;
                    if (prom) continue;
                    nsort++;
                    int f[4];
                    for (int k = 0; k < 4; k++) { int v = E[k].value(m.c, m.wk, m.bk, 1); f[k] = (v == 1); }
                    bool po = (f[0] && !f[1]) || (f[2] && !f[3]);
                    if (po) { nflag++;
                        cout << posStr(c, wk, bk, 0) << " | " << m.name << " | " << posStr(m.c, m.wk, m.bk, 1) << " | " << f[0] << f[1] << f[2] << f[3] << "\n"; }
                }
            }
        }
        fprintf(stderr, "roots %ld sorties %ld plain-only (either form) %ld layers %zu\n", roots, nsort, nflag, E[0].layers.size());
        return 0;
    }
}

// own.cpp -- referee's own P-model solver for K+P positions on a flat WxH board.
// Written from SPEC.md rules and the P-model definition only (first promotion wins for the promoter,
// checkmate = loss for the mover, stalemate = draw, never-ending = draw). No code shared with kpsolve/ref3/pm.py.
// Method: forward enumeration of the reachable graph from the given roots (promotion = terminal),
// then synchronous distance-to-win passes (exact plies). Includes en passant (flagged if ever used).
// Usage: own W H < positions   (positions in SPEC syntax, no officers)
// Output per input position: value (W/D/L from White's view), mover's DTW/DTL in plies, and with -m the
// list of legal moves of the root with the value of the position after the move.
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <deque>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
using std::string;
using namespace std;
typedef unsigned long long u64;
static int W = 7, H = 6;
struct St {
  int8_t wk, bk, stm, ep;  // ep = target square or -1
  u64 wp, bp;
  bool operator==(const St& o) const { return wk == o.wk && bk == o.bk && stm == o.stm && ep == o.ep && wp == o.wp && bp == o.bp; }
};
struct Hh {
  size_t operator()(const St& s) const {
    u64 h = s.wp * 0x9E3779B97F4A7C15ULL ^ (s.bp + 0x7F4A7C15ULL) * 0xC2B2AE3D27D4EB4FULL;
    h ^= ((u64)(uint8_t)s.wk << 1 | (u64)(uint8_t)s.bk << 9 | (u64)s.stm << 17 | (u64)(uint8_t)(s.ep + 1) << 20) * 0x165667B19E3779F9ULL;
    return h ^ (h >> 29);
  }
};
static inline int sq(int f, int r) { return r * W + f; }
static inline int fl(int s) { return s % W; }
static inline int rk(int s) { return s / W; }
static inline bool kadj(int a, int b) { return a != b && abs(fl(a) - fl(b)) <= 1 && abs(rk(a) - rk(b)) <= 1; }
// is square s attacked by a pawn of colour c (c=0 white pawns, bitboard pp)?
static bool pawnAttacks(u64 pp, int c, int s) {
  // white pawn on (f,r) attacks (f+-1, r+1); so s is attacked if a white pawn stands on (fs+-1, rs-1)
  int f = fl(s), r = rk(s);
  int pr = c == 0 ? r - 1 : r + 1;
  if (pr < 0 || pr >= H) return false;
  for (int df = -1; df <= 1; df += 2) {
    int pf = f + df;
    if (pf < 0 || pf >= W) continue;
    if (pp >> sq(pf, pr) & 1) return true;
  }
  return false;
}
// is the king of colour c (on square k) attacked in state s?
static bool kingAttacked(const St& s, int c) {
  int k = c == 0 ? s.wk : s.bk;
  int ok = c == 0 ? s.bk : s.wk;
  if (kadj(k, ok)) return true;
  if (c == 0) return pawnAttacks(s.bp, 1, k);
  return pawnAttacks(s.wp, 0, k);
}
struct Mv { St to; bool promo; string name; };
// generate legal moves of side to move. promo moves are terminal (to is unused).
static bool usedEP = false, sawDouble = false;
static void gen(const St& s, vector<Mv>& out) {
  out.clear();
  int c = s.stm;
  u64 own = c == 0 ? s.wp : s.bp, opp = c == 0 ? s.bp : s.wp;
  int k = c == 0 ? s.wk : s.bk, ok = c == 0 ? s.bk : s.wk;
  u64 occ = own | opp | (1ULL << s.wk) | (1ULL << s.bk);
  auto legal = [&](const St& t) { return !kingAttacked(t, c); };
  auto mk = [&](St t) { t.stm = 1 - c; return t; };
  static const char* FN = "abcdefg";
  auto nm = [&](int a, int b, bool cap) {
    string x; x += FN[fl(a)]; x += char('1' + rk(a)); x += cap ? 'x' : '-'; x += FN[fl(b)]; x += char('1' + rk(b)); return x; };
  // king moves
  for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
    if (!df && !dr) continue;
    int f = fl(k) + df, r = rk(k) + dr;
    if (f < 0 || f >= W || r < 0 || r >= H) continue;
    int t = sq(f, r);
    if (own >> t & 1) continue;
    if (t == ok) continue;
    St n = s; n.ep = -1;
    bool cap = opp >> t & 1;
    if (cap) { if (c == 0) n.bp &= ~(1ULL << t); else n.wp &= ~(1ULL << t); }
    if (c == 0) n.wk = t; else n.bk = t;
    if (!legal(n)) continue;
    out.push_back({mk(n), false, string(c ? "k" : "K") + nm(k, t, cap)});
  }
  // pawn moves
  for (int p = 0; p < W * H; p++) {
    if (!(own >> p & 1)) continue;
    int f = fl(p), r = rk(p), dir = c == 0 ? 1 : -1;
    int r1 = r + dir;
    int last = c == 0 ? H - 1 : 0;
    int second = c == 0 ? 1 : H - 2;
    auto push = [&](St n, bool promoted, string name) {
      if (!legal(n)) return;
      out.push_back({mk(n), promoted, name});
    };
    // single / double step
    if (r1 >= 0 && r1 < H) {
      int t = sq(f, r1);
      if (!(occ >> t & 1)) {
        St n = s; n.ep = -1;
        u64& pp = c == 0 ? n.wp : n.bp;
        pp &= ~(1ULL << p);
        if (r1 == last) push(n, true, nm(p, t, false) + "=Q");
        else {
          pp |= 1ULL << t;
          push(n, false, nm(p, t, false));
          if (r == second) {
            sawDouble = true;
            int r2 = r + 2 * dir;
            int t2 = sq(f, r2);
            if (!(occ >> t2 & 1)) {
              St m = s;
              u64& qq = c == 0 ? m.wp : m.bp;
              qq &= ~(1ULL << p);
              qq |= 1ULL << t2;
              m.ep = t;
              push(m, false, nm(p, t2, false));
            }
          }
        }
      }
      // captures
      for (int df = -1; df <= 1; df += 2) {
        int cf = f + df;
        if (cf < 0 || cf >= W) continue;
        int t = sq(cf, r1);
        if (opp >> t & 1) {
          St n = s; n.ep = -1;
          u64& pp = c == 0 ? n.wp : n.bp;
          u64& qq = c == 0 ? n.bp : n.wp;
          pp &= ~(1ULL << p);
          qq &= ~(1ULL << t);
          if (r1 == last) push(n, true, nm(p, t, true) + "=Q");
          else { pp |= 1ULL << t; push(n, false, nm(p, t, true)); }
        } else if (t == s.ep) {
          // en passant: captured pawn stands on (cf, r)
          int cp = sq(cf, r);
          if (opp >> cp & 1) {
            usedEP = true;
            St n = s; n.ep = -1;
            u64& pp = c == 0 ? n.wp : n.bp;
            u64& qq = c == 0 ? n.bp : n.wp;
            pp &= ~(1ULL << p);
            pp |= 1ULL << t;
            qq &= ~(1ULL << cp);
            push(n, false, nm(p, t, true) + "ep");
          }
        }
      }
    }
  }
}
static string sqs(int s) { string x; x += "abcdefg"[fl(s)]; x += char('1' + rk(s)); return x; }
static bool parse(const string& line, St& s, string& err) {
  istringstream is(line);
  string tok; s.wk = s.bk = -1; s.wp = s.bp = 0; s.ep = -1; s.stm = 0;
  vector<string> t;
  while (is >> tok) t.push_back(tok);
  if (t.size() < 3) { err = "short"; return false; }
  for (size_t i = 0; i + 2 < t.size(); i++) {
    char p = t[i][0]; int f = t[i][1] - 'a', r = t[i][2] - '1'; int q = sq(f, r);
    if (p == 'K') s.wk = q; else if (p == 'k') s.bk = q; else if (p == 'P') s.wp |= 1ULL << q; else if (p == 'p') s.bp |= 1ULL << q;
    else { err = "piece"; return false; }
  }
  s.stm = t[t.size() - 2] == "b";
  if (t.back() != "-") { s.ep = (t.back()[1] - 'a') + W * (t.back()[2] - '1'); }
  return true;
}
static string show(const St& s) {
  string x = "K" + sqs(s.wk);
  for (int p = 0; p < W * H; p++) if (s.wp >> p & 1) x += " P" + sqs(p);
  x += " k" + sqs(s.bk);
  for (int p = 0; p < W * H; p++) if (s.bp >> p & 1) x += " p" + sqs(p);
  x += s.stm ? " b " : " w ";
  x += s.ep < 0 ? "-" : sqs(s.ep);
  return x;
}
int main(int argc, char** argv) {
  W = atoi(argv[1]); H = atoi(argv[2]);
  bool wantMoves = argc > 3 && string(argv[3]) == "-m";
  vector<St> roots; vector<string> rawl;
  string line;
  while (getline(cin, line)) {
    if (line.empty() || line[0] == '#') continue;
    St s; string e;
    if (!parse(line, s, e)) { fprintf(stderr, "bad line %s\n", line.c_str()); return 1; }
    roots.push_back(s); rawl.push_back(line);
  }
  unordered_map<St, int, Hh> id;
  vector<St> sts;
  vector<vector<int>> succ;       // successor ids; -1 marks "a promoting move" (immediate win for mover)
  vector<int> npromo;
  auto getid = [&](const St& s) {
    auto it = id.find(s);
    if (it != id.end()) return it->second;
    int n = sts.size(); id[s] = n; sts.push_back(s); return n; };
  deque<int> q;
  for (auto& r : roots) { int before = sts.size(); int i = getid(r); (void)before; (void)i; }
  size_t head = 0;
  vector<Mv> mv;
  vector<char> inCheck;
  while (head < sts.size()) {
    St s = sts[head];
    gen(s, mv);
    vector<int> sc; int np = 0;
    for (auto& m : mv) {
      if (m.promo) { np++; continue; }
      sc.push_back(getid(m.to));
    }
    succ.push_back(sc); npromo.push_back(np);
    inCheck.push_back(kingAttacked(s, s.stm));
    head++;
  }
  int N = sts.size();
  fprintf(stderr, "reachable states %d, double step seen %d, ep capture used %d\n", N, (int)sawDouble, (int)usedEP);
  // value: 0 unknown, 1 mover wins (k plies), 2 mover loses (k plies)
  vector<int> val(N, 0), dist(N, 0);
  vector<int> nmv(N);
  for (int i = 0; i < N; i++) nmv[i] = succ[i].size() + npromo[i];
  // pass 0: mates
  for (int i = 0; i < N; i++) if (nmv[i] == 0 && inCheck[i]) { val[i] = 2; dist[i] = 0; }
  for (int k = 1;; k++) {
    vector<int> newW, newL;
    for (int i = 0; i < N; i++) {
      if (val[i]) continue;
      if (npromo[i] > 0) { newW.push_back(i); continue; }
      bool win = false, allw = true; int mx = 0;
      for (int j : succ[i]) {
        if (val[j] == 2 && dist[j] == k - 1) { win = true; break; }
        if (val[j] == 1) mx = max(mx, dist[j]); else allw = false;
      }
      if (win) { newW.push_back(i); continue; }
      if (allw && !succ[i].empty() && mx == k - 1) newL.push_back(i);
    }
    if (newW.empty() && newL.empty()) {
      // check whether anything could still change (a loss needs all succ won: dist could be <k-1 only if finished earlier)
      bool pending = false;
      for (int i = 0; i < N && !pending; i++) if (!val[i]) { bool allw = !succ[i].empty() && npromo[i] == 0; for (int j : succ[i]) if (val[j] != 1) { allw = false; break; } if (allw) pending = true; }
      if (!pending) break;
    }
    for (int i : newW) { val[i] = 1; dist[i] = k; }
    for (int i : newL) { val[i] = 2; dist[i] = k; }
    if (k > 100000) break;
  }
  auto whiteView = [&](int i) { // returns W/D/L from White's view
    if (val[i] == 0) return 'D';
    bool moverWins = val[i] == 1;
    bool whiteMoves = sts[i].stm == 0;
    return (moverWins == whiteMoves) ? 'W' : 'L';
  };
  if (argc > 3 && string(argv[3]) == "-d") {
    for (int i = 0; i < N; i++) printf("%s | %c %d\n", show(sts[i]).c_str(), whiteView(i), val[i] ? dist[i] : -1);
    return 0;
  }
  for (size_t r = 0; r < roots.size(); r++) {
    int i = id[roots[r]];
    printf("%s | %c  (mover %s%s)\n", rawl[r].c_str(), whiteView(i), val[i] == 1 ? "wins in " : val[i] == 2 ? "loses in " : "draws", val[i] ? to_string(dist[i]).c_str() : "");
    if (wantMoves) {
      gen(sts[i], mv);
      for (auto& m : mv) {
        if (m.promo) { printf("   %s  promotion (immediate win for mover)\n", m.name.c_str()); continue; }
        int j = id[m.to];
        printf("   %-10s -> %c", m.name.c_str(), whiteView(j));
        if (val[j]) printf("   (child: mover-of-child %s in %d)", val[j] == 1 ? "wins" : "loses", dist[j]);
        printf("\n");
      }
    }
  }
  return 0;
}

// o68.cpp -- K68 oracle: the promotion game P (and P beside -1) for king-and-pawn positions on the flat 8x8 board.
// Written for K68 from the rules in kings/theory/LOOPY.md (Definition 4.8, Lemma 4.15) and the K61 packet section 1.
// Used only as an oracle: to find lines and to test the hand proof in ../PROOF.md.
//
// Rules.  Kings and pawns, chess moves (double step from the 2nd/7th rank, e.p., no move into check, kings never
// adjacent).  A pawn reaching the last rank ends the play: the promoter wins.  A side with no move: in check -> loses;
// otherwise stalemate -> draw (mode P) or loss (mode S, the sum's rule).  Infinite play: draw.
// Token (mode S only): Black may once move elsewhere (-1 -> 0) when not in check; it clears Black's e.p. right.
//
// Usage: o68 MODE < queries
//   MODE = P or S.  Each query line: FEN-like "WK BK WP-list BP-list side ep tok", e.g.
//     d4 b4 b6,c2,c5 b7,c6 w - 0
//   ep = square that the side to move may capture onto e.p., or '-'.  tok = Black tokens (0 or 1; only in mode S).
//   Output: value for the side to move (W/D/L) with plies to the end, then every legal move with the value of the
//   position after it (from the mover's point of view) and a principal line.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
#include <deque>
#include <sstream>
#include <iostream>
using namespace std;
typedef uint64_t BB;

struct St { BB wp, bp; int8_t wk, bk, stm, ep, tok; };
static bool operator==(const St &a, const St &b) {
  return a.wp == b.wp && a.bp == b.bp && a.wk == b.wk && a.bk == b.bk && a.stm == b.stm && a.ep == b.ep && a.tok == b.tok;
}
struct H { size_t operator()(const St &s) const {
  uint64_t h = s.wp * 0x9E3779B97F4A7C15ULL ^ (s.bp + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
  h ^= (uint64_t)(uint8_t)s.wk | ((uint64_t)(uint8_t)s.bk << 8) | ((uint64_t)(uint8_t)s.stm << 16) |
       ((uint64_t)(uint8_t)s.ep << 24) | ((uint64_t)(uint8_t)s.tok << 32);
  h *= 0xFF51AFD7ED558CCDULL; h ^= h >> 29; return h; } };

static bool MODE_S = false;
static inline bool on(BB b, int s) { return (b >> s) & 1ULL; }
static inline int R(int s) { return s >> 3; }
static inline int F(int s) { return s & 7; }
static bool kadj(int a, int b) { return a != b && abs(R(a) - R(b)) <= 1 && abs(F(a) - F(b)) <= 1; }
static string SN(int s) { string r; r += char('a' + F(s)); r += char('1' + R(s)); return r; }
static int PS(const string &x) { return (x[1] - '1') * 8 + (x[0] - 'a'); }
// is square s attacked by a pawn of colour c (0 white, 1 black) in pawn set p?
static bool pawnatt(BB p, int c, int s) {
  int r = R(s), f = F(s);
  int pr = c == 0 ? r - 1 : r + 1;
  if (pr < 0 || pr > 7) return false;
  if (f > 0 && on(p, pr * 8 + f - 1)) return true;
  if (f < 7 && on(p, pr * 8 + f + 1)) return true;
  return false;
}
static bool incheck(const St &s, int side) {
  return side == 0 ? pawnatt(s.bp, 1, s.wk) : pawnatt(s.wp, 0, s.bk);
}
struct Mv { St to; bool promo; bool pass; string name; };
static void gen(const St &s, vector<Mv> &out) {
  out.clear();
  int me = s.stm;
  BB my = me == 0 ? s.wp : s.bp, op = me == 0 ? s.bp : s.wp;
  int mk = me == 0 ? s.wk : s.bk, ok = me == 0 ? s.bk : s.wk;
  BB occ = s.wp | s.bp | (1ULL << s.wk) | (1ULL << s.bk);
  auto push = [&](BB nmy, BB nop, int nmk, int nep, bool promo, const string &nm) {
    St t; t.wp = me == 0 ? nmy : nop; t.bp = me == 0 ? nop : nmy;
    t.wk = me == 0 ? nmk : ok; t.bk = me == 0 ? ok : nmk; t.stm = 1 - me; t.ep = nep; t.tok = s.tok;
    if (incheck(t, me)) return;  // own king attacked by an enemy pawn
    if (kadj(t.wk, t.bk)) return;
    out.push_back({t, promo, false, nm});
  };
  // king moves
  for (int dr = -1; dr <= 1; dr++) for (int df = -1; df <= 1; df++) {
    if (!dr && !df) continue;
    int r = R(mk) + dr, f = F(mk) + df; if (r < 0 || r > 7 || f < 0 || f > 7) continue;
    int d = r * 8 + f;
    if (on(my, d) || d == ok) continue;
    push(my, op & ~(1ULL << d), d, -1, false, "K" + SN(mk) + (on(op, d) ? "x" : "-") + SN(d));
  }
  // pawn moves
  int dir = me == 0 ? 8 : -8, last = me == 0 ? 7 : 0, start = me == 0 ? 1 : 6;
  for (int p = 0; p < 64; p++) if (on(my, p)) {
    int d = p + dir;
    if (d >= 0 && d < 64 && !on(occ, d)) {
      bool pr = R(d) == last;
      push((my & ~(1ULL << p)) | (pr ? 0 : (1ULL << d)), op, mk, -1, pr, SN(p) + "-" + SN(d) + (pr ? "=" : ""));
      int d2 = d + dir;
      if (R(p) == start && !on(occ, d2)) {
        // e.p. right for the opponent only if an opponent pawn stands beside d2
        int nep = -1;
        if ((F(d2) > 0 && on(op, d2 - 1)) || (F(d2) < 7 && on(op, d2 + 1))) nep = d;
        push((my & ~(1ULL << p)) | (1ULL << d2), op, mk, nep, false, SN(p) + "-" + SN(d2));
      }
    }
    for (int df = -1; df <= 1; df += 2) {
      int f = F(p) + df; if (f < 0 || f > 7 || d < 0 || d >= 64) continue;
      int c = R(d) * 8 + f;
      if (on(op, c)) {
        bool pr = R(c) == last;
        push((my & ~(1ULL << p)) | (pr ? 0 : (1ULL << c)), op & ~(1ULL << c), mk, -1, pr, SN(p) + "x" + SN(c) + (pr ? "=" : ""));
      } else if (c == s.ep) {
        int cap = c - dir;
        push((my & ~(1ULL << p)) | (1ULL << c), op & ~(1ULL << cap), mk, -1, false, SN(p) + "x" + SN(c) + "ep");
      }
    }
  }
  // Black's token
  if (MODE_S && me == 1 && s.tok > 0 && !incheck(s, 1)) {
    St t = s; t.stm = 0; t.ep = -1; t.tok = s.tok - 1;
    out.push_back({t, false, true, "(-1)"});
  }
}

static unordered_map<St, int, H> idx;
static vector<St> sts;
static vector<int8_t> val;   // for side to move: 1 win, -1 loss, 0 draw/unknown
static vector<int> dep;      // plies to the end
static vector<int> soff, sflat;  // successors in CSR form (memory: K68 runs must stay under 0.5 GB)
static vector<int8_t> pinf;      // immediate promotion available

static int getid(const St &s) {
  auto it = idx.find(s); if (it != idx.end()) return it->second;
  int id = sts.size(); idx[s] = id; sts.push_back(s); return id;
}
static void solve(const vector<St> &roots) {
  // states are numbered in BFS order, so the successor lists can be appended in id order
  for (auto &r : roots) getid(r);
  vector<Mv> mv;
  soff.assign(1, 0);
  for (size_t id = 0; id < sts.size(); id++) {
    St s = sts[id];
    gen(s, mv);
    int pr = 0;
    for (auto &m : mv) { if (m.promo) { pr = 1; continue; } sflat.push_back(getid(m.to)); }
    soff.push_back(sflat.size()); pinf.push_back(pr);
  }
  int n = sts.size();
  fprintf(stderr, "states: %d\n", n);
  vector<int> poff(n + 1, 0), pflat(sflat.size()), cnt(n);
  for (int t : sflat) poff[t + 1]++;
  for (int i = 0; i < n; i++) poff[i + 1] += poff[i];
  { vector<int> fill(poff.begin(), poff.end() - 1);
    for (int i = 0; i < n; i++) for (int k = soff[i]; k < soff[i + 1]; k++) pflat[fill[sflat[k]]++] = i; }
  for (int i = 0; i < n; i++) cnt[i] = soff[i + 1] - soff[i];
  val.assign(n, 0); dep.assign(n, -1);
  vector<int> cur;
  for (int i = 0; i < n; i++) {
    if (pinf[i]) { val[i] = 1; dep[i] = 1; continue; }
    if (soff[i + 1] == soff[i]) {
      bool chk = incheck(sts[i], sts[i].stm);
      if (chk || MODE_S) { val[i] = -1; dep[i] = 0; }
      else { val[i] = 0; dep[i] = 0; }  // stalemate draw, marked final
    }
  }
  // layered retrograde: process by depth
  vector<vector<int>> layer(2);
  for (int i = 0; i < n; i++) if (dep[i] >= 0 && val[i] != 0) {
    if ((int)layer.size() <= dep[i]) layer.resize(dep[i] + 1);
    layer[dep[i]].push_back(i);
  }
  for (size_t d = 0; d < layer.size(); d++) {
    for (size_t k = 0; k < layer[d].size(); k++) {
      int i = layer[d][k];
      for (int k = poff[i]; k < poff[i + 1]; k++) { int p = pflat[k];
        if (dep[p] >= 0) continue;
        if (val[i] == -1) { val[p] = 1; dep[p] = d + 1; }
        else if (--cnt[p] == 0) { val[p] = -1; dep[p] = d + 1; }
        else continue;
        if (layer.size() <= d + 1) layer.resize(d + 2);
        layer[d + 1].push_back(p);
      }
    }
  }
}
static St parse(const string &line) {
  istringstream is(line); string wk, bk, wps, bps, side, ep; int tok = 0;
  is >> wk >> bk >> wps >> bps >> side >> ep >> tok;
  St s; s.wp = s.bp = 0; s.wk = PS(wk); s.bk = PS(bk);
  auto rd = [&](const string &l, BB &b) { if (l == "-") return; stringstream ss(l); string x; while (getline(ss, x, ',')) b |= 1ULL << PS(x); };
  rd(wps, s.wp); rd(bps, s.bp); s.stm = side == "w" ? 0 : 1; s.ep = ep == "-" ? -1 : PS(ep); s.tok = tok;
  return s;
}
static string vs(int id) {
  if (dep[id] < 0) return "D";
  if (val[id] == 0) return "D(stalemate)";
  return string(val[id] > 0 ? "W" : "L") + to_string(dep[id]);
}
static string pv(St s, int maxp) {
  string out; vector<Mv> mv;
  for (int k = 0; k < maxp; k++) {
    int id = idx.at(s);
    if (dep[id] < 0 || val[id] == 0) break;
    gen(s, mv);
    if (val[id] > 0) {
      bool done = false;
      for (auto &m : mv) if (m.promo) { out += " " + m.name; done = true; break; }
      if (done) break;
      for (auto &m : mv) { int t = idx.at(m.to); if (val[t] < 0 && dep[t] == dep[id] - 1) { out += " " + m.name; s = m.to; break; } }
    } else {
      if (mv.empty()) { out += " #"; break; }
      for (auto &m : mv) { int t = idx.at(m.to); if (val[t] > 0 && dep[t] == dep[id] - 1) { out += " " + m.name; s = m.to; break; } }
    }
  }
  return out;
}
int main(int argc, char **argv) {
  if (argc < 2) { fprintf(stderr, "usage: o68 P|S < queries\n"); return 1; }
  MODE_S = string(argv[1]) == "S";
  vector<string> lines; vector<St> roots; string l;
  vector<string> tabs;  // "T WK|* BK|* WP BP side": table over the starred king's squares
  while (getline(cin, l)) {
    if (l.empty() || l[0] == '#') continue;
    if (l[0] == 'T') { tabs.push_back(l.substr(2)); continue; }
    lines.push_back(l); roots.push_back(parse(l));
  }
  // table queries: add every legal placement of the starred king as a root
  vector<vector<St>> tabst;
  for (auto &t : tabs) {
    vector<St> v;
    for (int sq = 0; sq < 64; sq++) {
      string q = t; size_t p = q.find('*'); q.replace(p, 1, SN(sq)); q += " - 0";
      St s = parse(q);
      BB occ = s.wp | s.bp;
      bool ok = !on(occ, s.wk) && !on(occ, s.bk) && s.wk != s.bk && !kadj(s.wk, s.bk) && !incheck(s, 1 - s.stm);
      if (ok) { v.push_back(s); roots.push_back(s); } else { s.wk = -1; v.push_back(s); }
    }
    tabst.push_back(v);
  }
  vector<St> rr; for (auto &s : roots) if (s.wk >= 0) rr.push_back(s);
  solve(rr);
  for (size_t k = 0; k < tabs.size(); k++) {
    printf("table %s  (value for the side to move, plies)\n", tabs[k].c_str());
    for (int r = 7; r >= 0; r--) {
      printf("%d ", r + 1);
      for (int f = 0; f < 8; f++) {
        St &s = tabst[k][r * 8 + f];
        if (s.wk < 0) { printf("   . "); continue; }
        int id = idx.at(s); string v = vs(id); printf("%4s ", v.c_str());
      }
      printf("\n");
    }
    printf("   a    b    c    d    e    f    g    h\n");
  }
  vector<Mv> mv;
  for (size_t k = 0; k < lines.size(); k++) {
    St s = roots[k]; int id = idx.at(s);
    printf("%s  =>  %s   line:%s\n", lines[k].c_str(), vs(id).c_str(), pv(s, 60).c_str());
    gen(s, mv);
    for (auto &m : mv) {
      if (m.promo) { printf("    %-10s promotes\n", m.name.c_str()); continue; }
      int t = idx.at(m.to);
      string v = dep[t] < 0 ? "D" : val[t] == 0 ? "D(st)" : string(val[t] > 0 ? "L" : "W") + to_string(dep[t] + 1);
      printf("    %-10s %s", m.name.c_str(), v.c_str());
      if (getenv("O68_TWO")) {  // the opponent's replies after this move, with values for the opponent
        vector<Mv> mv2; gen(m.to, mv2); printf("   |");
        for (auto &m2 : mv2) {
          if (m2.promo) { printf(" %s:promo", m2.name.c_str()); continue; }
          int t2 = idx.at(m2.to);
          string v2 = dep[t2] < 0 ? "D" : val[t2] == 0 ? "D" : string(val[t2] > 0 ? "L" : "W") + to_string(dep[t2] + 1);
          printf(" %s:%s", m2.name.c_str(), v2.c_str());
        }
      }
      printf("\n");
    }
  }
  return 0;
}

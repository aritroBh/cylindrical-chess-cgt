// mysolve.cpp -- K15 referee's own exact solver + classifier, written from LOOPY/FINDINGS definitions only
// (does not read grp.c, kpsolve.c, cylcgt, ref3).  Model P with real kings on a W x H cylinder or flat board;
// pawns only on files 0..F-1, ranks 1..H-2 (0-based), at most wmax white / bmax black pawns; empty context.
// Reading A: passing is a move (illegal in check).  Reading B: no passing; stalemate = draw.
// Usage: mysolve --W 7 --H 6 --F 3 --wmax 2 --bmax 2 [--flat] [--nopass] [--dump file] [--sample k seed]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <ctime>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <array>
#include <tuple>
#include <unordered_map>
#include <algorithm>
using namespace std;
typedef uint64_t u64;
static int W, H, F, N, NN, FLAT = 0, PASS = 1, WM = 2, BM = 2;
static int nb[64][8], nnb[64];
static u64 kadj[64], fromW[64], fromB[64]; // fromW[sq]: squares from which a WHITE pawn attacks sq
#define BIT(s) (1ULL << (s))
static inline int SQ(int f, int r) { return r * W + f; }
static int wrapf(int f) { if (FLAT) return (f < 0 || f >= W) ? -1 : f; return ((f % W) + W) % W; }

struct Mv { int kind; u64 nwp, nbp; int nwk, nbk; int ep, epc; }; // kind 0 pass 1 king 2 pawn 3 promo
struct St { u64 wp, bp; int wk, bk, ep, epc, owner;
  bool operator<(const St& o) const { return tie(wp,bp,wk,bk,ep,epc,owner) < tie(o.wp,o.bp,o.wk,o.bk,o.ep,o.epc,o.owner); } };

static int genMoves(u64 wp, u64 bp, int wk, int bk, int stm, int ep, int epc, bool allowPass, Mv* out) {
  int n = 0;
  int ks = stm ? bk : wk, ko = stm ? wk : bk;
  u64 my = stm ? bp : wp, op = stm ? wp : bp;
  const u64* attFrom = stm ? fromW : fromB; // enemy pawns attacking a square
  bool inCheck = (op & attFrom[ks]) != 0;
  if (allowPass && PASS && !inCheck) out[n++] = Mv{0, wp, bp, wk, bk, -1, -1};
  for (int i = 0; i < nnb[ks]; i++) {
    int t = nb[ks][i];
    if (my >> t & 1) continue;
    if (t == ko || (kadj[ko] >> t & 1)) continue;
    bool cap = op >> t & 1; u64 opA = cap ? (op & ~BIT(t)) : op;
    if (opA & attFrom[t]) continue;
    u64 nwp = stm ? opA : wp, nbp = stm ? bp : opA; // careful: stm=0 -> op = bp
    if (stm == 0) { nwp = wp; nbp = opA; } else { nwp = opA; nbp = bp; }
    out[n++] = Mv{1, nwp, nbp, stm ? wk : t, stm ? t : bk, -1, -1};
  }
  int dir = stm ? -1 : 1, start = stm ? H - 2 : 1, last = stm ? 0 : H - 1;
  u64 occ = wp | bp | BIT(wk) | BIT(bk);
  for (int s = 0; s < N; s++) if (my >> s & 1) {
    int f = s % W, r = s / W, r1 = r + dir;
    if (r1 < 0 || r1 >= H) continue;
    int t = SQ(f, r1);
    if (!(occ >> t & 1)) {
      if (!(op & attFrom[ks])) {
        if (r1 == last) out[n++] = Mv{3, 0, 0, wk, bk, -1, -1};
        else {
          u64 nm = (my & ~BIT(s)) | BIT(t);
          u64 nwp = stm ? op : nm, nbp = stm ? nm : op;
          out[n++] = Mv{2, nwp, nbp, wk, bk, -1, -1};
          if (r == start) {
            int t2 = SQ(f, r + 2 * dir);
            if (!(occ >> t2 & 1)) {
              u64 nm2 = (my & ~BIT(s)) | BIT(t2);
              u64 nwp2 = stm ? op : nm2, nbp2 = stm ? nm2 : op;
              int eps = -1, epcc = -1; bool can = false;
              for (int d = -1; d <= 1; d += 2) { int g = wrapf(f + d); if (g < 0) continue; if (op >> SQ(g, r + 2 * dir) & 1) can = true; }
              if (can) { eps = t; epcc = t2; }
              out[n++] = Mv{2, nwp2, nbp2, wk, bk, eps, epcc};
            }
          }
        }
      }
    }
    for (int d = -1; d <= 1; d += 2) {
      int g = wrapf(f + d); if (g < 0) continue;
      int tt = SQ(g, r1);
      bool capt = op >> tt & 1; bool epcap = (!capt && ep >= 0 && tt == ep && !(occ >> tt & 1));
      if (!capt && !epcap) continue;
      u64 opA = capt ? (op & ~BIT(tt)) : (op & ~BIT(SQ(g, r)));
      if (opA & attFrom[ks]) continue;
      if (r1 == last) { out[n++] = Mv{3, 0, 0, wk, bk, -1, -1}; continue; }
      u64 nm = (my & ~BIT(s)) | BIT(tt);
      u64 nwp = stm ? opA : nm, nbp = stm ? nm : opA;
      out[n++] = Mv{2, nwp, nbp, wk, bk, -1, -1};
    }
  }
  return n;
}

// ---- layers
struct LKey { u64 w, b; bool operator==(const LKey& o) const { return w == o.w && b == o.b; } };
struct LH { size_t operator()(const LKey& k) const { return k.w * 0x9E3779B97F4A7C15ULL ^ (k.b + 0x1234567ULL) * 0xC2B2AE3D27D4EB4FULL; } };
static vector<LKey> layers; static unordered_map<LKey, int, LH> lidx; static vector<uint8_t> tab; // 0 draw 1 mover wins 2 mover loses 3 illegal

static inline size_t TI(int li, int stm, int wk, int bk) { return ((size_t)li * 2 + stm) * NN + wk * N + bk; }

static int valueOf(u64 wp, u64 bp, int wk, int bk, int stm, int ep, int epc); // for mover

static int succValue(const Mv& m, int stm /*mover*/) { // value for the opponent (to move) after m; kind!=3
  int opp = 1 - stm;
  if (m.ep < 0) { auto it = lidx.find(LKey{m.nwp, m.nbp}); return tab[TI(it->second, opp, m.nwk, m.nbk)]; }
  return valueOf(m.nwp, m.nbp, m.nwk, m.nbk, opp, m.ep, m.epc);
}
static int valueOf(u64 wp, u64 bp, int wk, int bk, int stm, int ep, int epc) {
  if (ep < 0) { auto it = lidx.find(LKey{wp, bp}); return tab[TI(it->second, stm, wk, bk)]; }
  Mv mv[128]; int n = genMoves(wp, bp, wk, bk, stm, ep, epc, true, mv);
  if (n == 0) { int ks = stm ? bk : wk; u64 op = stm ? wp : bp; const u64* af = stm ? fromW : fromB; return (op & af[ks]) ? 2 : 0; }
  bool anyDraw = false;
  for (int i = 0; i < n; i++) {
    if (mv[i].kind == 3) return 1;
    int v = succValue(mv[i], stm);
    if (v == 2) return 1; if (v == 0) anyDraw = true;
  }
  return anyDraw ? 0 : 2;
}

static void solveLayer(int li) {
  u64 wp = layers[li].w, bp = layers[li].b;
  u64 occP = wp | bp;
  vector<uint8_t> val(2 * NN, 3);
  vector<int> remaining(2 * NN, 0); vector<uint8_t> noloss(2 * NN, 0);
  vector<pair<int,int>> edges; // pred, succ
  vector<int> queue;
  for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) {
    if (wk == bk || (occP >> wk & 1) || (occP >> bk & 1) || (kadj[wk] >> bk & 1)) continue;
    // non-mover's king must not be attacked
    if (stm == 0 && (wp & fromW[bk])) continue;
    if (stm == 1 && (bp & fromB[wk])) continue;
    int id = stm * NN + wk * N + bk; val[id] = 0;
    Mv mv[128]; int n = genMoves(wp, bp, wk, bk, stm, -1, -1, true, mv);
    if (n == 0) { int ks = stm ? bk : wk; u64 op = stm ? wp : bp; const u64* af = stm ? fromW : fromB; if (op & af[ks]) { val[id] = 2; queue.push_back(id); } continue; }
    bool extWin = false; int nInt = 0, extDraw = 0, extLose = 0;
    for (int i = 0; i < n; i++) {
      const Mv& m = mv[i];
      if (m.kind == 3) { extWin = true; continue; }
      bool internal = (m.nwp == wp && m.nbp == bp && m.ep < 0);
      if (internal) { int sid = (1 - stm) * NN + m.nwk * N + m.nbk; edges.push_back({id, sid}); nInt++; }
      else { int v = succValue(m, stm); if (v == 2) extWin = true; else if (v == 1) extLose++; else extDraw++; }
    }
    if (extWin) { val[id] = 1; queue.push_back(id); continue; }
    remaining[id] = nInt; noloss[id] = extDraw > 0;
    if (nInt == 0 && extDraw == 0) { val[id] = 2; queue.push_back(id); } // all moves lose (extLose>0)
  }
  // predecessor lists
  vector<int> start(2 * NN + 1, 0);
  for (auto& e : edges) start[e.second + 1]++;
  for (int i = 0; i < 2 * NN; i++) start[i + 1] += start[i];
  vector<int> preds(edges.size()), fill(start.begin(), start.end() - 1);
  for (auto& e : edges) preds[fill[e.second]++] = e.first;
  for (size_t qi = 0; qi < queue.size(); qi++) {
    int t = queue[qi];
    for (int k = start[t]; k < start[t + 1]; k++) {
      int p = preds[k]; if (val[p] != 0) continue;
      if (val[t] == 2) { val[p] = 1; queue.push_back(p); }
      else if (val[t] == 1) { if (--remaining[p] == 0 && !noloss[p]) { val[p] = 2; queue.push_back(p); } }
    }
  }
  memcpy(&tab[(size_t)li * 2 * NN], val.data(), 2 * NN);
}

// ---- analysis
struct Info { int check = 0, leak = 0; int nwin[2] = {0, 0}; vector<St> safe[2]; };
static Info analyze(const St& y) {
  Info I;
  if ((y.wp & fromW[y.bk]) || (y.bp & fromB[y.wk])) I.check = 1;
  for (int s = 0; s < 2; s++) {
    int ep = (y.ep >= 0 && y.owner == s) ? y.ep : -1, epc = (y.ep >= 0 && y.owner == s) ? y.epc : -1;
    Mv mv[128]; int n = genMoves(y.wp, y.bp, y.wk, y.bk, s, ep, epc, false, mv);
    for (int i = 0; i < n; i++) {
      const Mv& m = mv[i];
      if (m.kind == 3) { I.nwin[s]++; continue; }
      int v = succValue(m, s);
      if (v == 1) continue; // suicide
      if (v == 2) { I.nwin[s]++; continue; }
      if (m.kind == 1) { int nk = s ? m.nbk : m.nwk; if (nk % W >= F) I.leak = 1; }
      I.safe[s].push_back(St{m.nwp, m.nbp, m.nwk, m.nbk, m.ep, m.epc, m.ep >= 0 ? 1 - s : -1});
    }
  }
  return I;
}
static bool bad(const Info& I) { return I.check || I.nwin[0] || I.nwin[1] || I.leak; }

static int RELAX = 0; // 1: over/under test ignores check/threat/leak at A- and Z-states
struct Res { string cls; int csize = 0; bool nearOverRelaxed = false; vector<St> closure; };

static Res classify(const St& x) {
  Res R; Info I = analyze(x);
  if (I.check) { R.cls = "check"; return R; }
  if (I.nwin[0] || I.nwin[1]) { R.cls = "threat"; return R; }
  if (I.safe[0].empty() && I.safe[1].empty()) { R.cls = "frozen"; return R; }
  for (int mode = 0; mode < 5; mode++) {
    // 0 on, 1 off, 2 dud, 3 over (black passes), 4 under (white passes)
    if (mode == 0 && !(!I.safe[0].empty() && I.safe[1].empty())) continue;
    if (mode == 1 && !(!I.safe[1].empty() && I.safe[0].empty())) continue;
    if (mode >= 2 && (I.safe[0].empty() || I.safe[1].empty())) continue;
    if (mode >= 2 && I.leak) continue;
    set<St> seen; vector<St> stack; seen.insert(x); stack.push_back(x); bool ok = true; int cs = 0;
    int p = (mode == 3) ? 1 : 0, q = 1 - p;
    while (!stack.empty() && ok) {
      St y = stack.back(); stack.pop_back(); cs++;
      if (seen.size() > 20000) { ok = false; break; }
      Info II = analyze(y);
      if (bad(II)) { ok = false; break; }
      if (mode == 0) { if (!(II.safe[0].size() >= 1 && II.safe[1].empty())) { ok = false; break; } for (auto& t : II.safe[0]) if (seen.insert(t).second) stack.push_back(t); }
      else if (mode == 1) { if (!(II.safe[1].size() >= 1 && II.safe[0].empty())) { ok = false; break; } for (auto& t : II.safe[1]) if (seen.insert(t).second) stack.push_back(t); }
      else if (mode == 2) { if (II.safe[0].empty() || II.safe[1].empty()) { ok = false; break; }
        for (int s = 0; s < 2; s++) for (auto& t : II.safe[s]) if (seen.insert(t).second) stack.push_back(t); }
      else {
        if (II.safe[p].empty() || II.safe[q].empty()) { ok = false; break; }
        for (auto& t : II.safe[p]) if (seen.insert(t).second) stack.push_back(t);
        for (auto& t : II.safe[q]) { Info Z = analyze(t); if (bad(Z) || !Z.safe[0].empty() || !Z.safe[1].empty()) { ok = false; break; } }
      }
    }
    if (ok && mode == 2) R.closure.assign(seen.begin(), seen.end());
    if (ok) { R.cls = mode == 0 ? "on" : mode == 1 ? "off" : mode == 2 ? "dud" : mode == 3 ? "over" : "under"; R.csize = cs; return R; }
  }
  // relaxed over/under: ignore check/threat/leak everywhere (superset test); only reports, label stays leak/mixed
  if (!I.safe[0].empty() && !I.safe[1].empty()) {
    for (int p = 1; p >= 0; p--) { int q = 1 - p;
      set<St> seen; vector<St> stack; seen.insert(x); stack.push_back(x); bool ok = true;
      while (!stack.empty() && ok) {
        St y = stack.back(); stack.pop_back(); if (seen.size() > 20000) { ok = false; break; }
        Info II = analyze(y);
        if (II.safe[p].empty() || II.safe[q].empty()) { ok = false; break; }
        for (auto& t : II.safe[p]) if (seen.insert(t).second) stack.push_back(t);
        for (auto& t : II.safe[q]) { Info Z = analyze(t); if (!Z.safe[0].empty() || !Z.safe[1].empty()) { ok = false; break; } }
      }
      if (ok) R.nearOverRelaxed = true;
    }
  }
  R.cls = I.leak ? "leak" : "mixed";
  return R;
}

static string sqname(int s) { string t; t += char('a' + s % W); t += to_string(s / W + 1); return t; }
static string posstr(const St& x) {
  string s = "K" + sqname(x.wk) + " k" + sqname(x.bk);
  for (int i = 0; i < N; i++) if (x.wp >> i & 1) s += " P" + sqname(i);
  for (int i = 0; i < N; i++) if (x.bp >> i & 1) s += " p" + sqname(i);
  return s;
}


// ---- depth to forced promotion (attacker = side to move at the node), exact values used only to prune attacker moves
static map<tuple<u64,u64,int,int,int,int,int,int>, int> memoD;
static bool canWin(u64 wp, u64 bp, int wk, int bk, int stm, int ep, int epc, int d);
static bool allLose(u64 wp, u64 bp, int wk, int bk, int dstm, int ep, int epc, int d) { // defender to move; attacker wins within d plies?
  Mv mv[128]; int n = genMoves(wp, bp, wk, bk, dstm, ep, epc, true, mv);
  if (n == 0) { int ks = dstm ? bk : wk; u64 op = dstm ? wp : bp; const u64* af = dstm ? fromW : fromB; return (op & af[ks]) != 0; }
  if (d < 2) return false;
  for (int i = 0; i < n; i++) {
    if (mv[i].kind == 3) return false;
    if (!canWin(mv[i].nwp, mv[i].nbp, mv[i].nwk, mv[i].nbk, 1 - dstm, mv[i].ep, mv[i].epc, d - 1)) return false;
  }
  return true;
}
static bool canWin(u64 wp, u64 bp, int wk, int bk, int stm, int ep, int epc, int d) {
  if (d < 1) return false;
  auto key = make_tuple(wp, bp, wk * 64 + bk, stm, ep, epc, 0, d);
  auto it = memoD.find(key); if (it != memoD.end()) return it->second;
  Mv mv[128]; int n = genMoves(wp, bp, wk, bk, stm, ep, epc, true, mv); bool res = false;
  for (int i = 0; i < n && !res; i++) {
    if (mv[i].kind == 3) { res = true; break; }
    if (d < 3) continue;
    if (succValue(mv[i], stm) != 2) continue; // must be a winning move for the mover
    if (allLose(mv[i].nwp, mv[i].nbp, mv[i].nwk, mv[i].nbk, 1 - stm, mv[i].ep, mv[i].epc, d - 1)) res = true;
  }
  memoD[key] = res; return res;
}
static int parsePos(const string& s, u64& wp, u64& bp, int& wk, int& bk) {
  wp = bp = 0; wk = bk = -1; size_t i = 0; vector<string> t; string cur;
  for (char c : s + " ") { if (c == ' ') { if (!cur.empty()) t.push_back(cur); cur.clear(); } else cur += c; }
  for (auto& x : t) { if (x.size() < 3 || !strchr("KkPp", x[0])) continue; int f = x[1] - 'a', r = atoi(x.c_str() + 2) - 1; int sq = SQ(f, r);
    if (x[0] == 'K') wk = sq; else if (x[0] == 'k') bk = sq; else if (x[0] == 'P') wp |= BIT(sq); else bp |= BIT(sq); }
  (void)i; return wk >= 0 && bk >= 0;
}
static string movename(int stm, const Mv& m, u64 wp, u64 bp, int wk, int bk) { // describe by diff
  string s;
  if (m.kind == 0) return "pass"; if (m.kind == 3) return "promo";
  if (m.kind == 1) { int from = stm ? bk : wk, to = stm ? m.nbk : m.nwk; return string("K") + sqname(from) + sqname(to); }
  u64 mine = stm ? bp : wp, nmine = stm ? m.nbp : m.nwp; u64 gone = mine & ~nmine, came = nmine & ~mine;
  int a = __builtin_ctzll(gone), b = __builtin_ctzll(came); return string("P") + sqname(a) + sqname(b);
}
static void depthMode(const char* fn) {
  FILE* f = fopen(fn, "r"); char buf[512];
  while (fgets(buf, sizeof buf, f)) {
    string line(buf); while (!line.empty() && (line.back() == '\n' || line.back() == '\r')) line.pop_back();
    char stmc = 'w'; { size_t p = line.find(" w "); size_t q = line.find(" b "); if (q != string::npos && (p == string::npos || q < p)) stmc = 'b'; }
    u64 wp, bp; int wk, bk; if (!parsePos(line, wp, bp, wk, bk)) continue; int stm = stmc == 'b';
    Mv mv[128]; int n = genMoves(wp, bp, wk, bk, stm, -1, -1, true, mv);
    printf("%s |", line.c_str());
    for (int i = 0; i < n; i++) {
      string nm = movename(stm, mv[i], wp, bp, wk, bk);
      if (mv[i].kind == 3) { printf(" %s:promo", nm.c_str()); continue; }
      int v = succValue(mv[i], stm); // for opponent
      if (v == 2) { printf(" %s:W", nm.c_str()); continue; }
      if (v == 0) { printf(" %s:D", nm.c_str()); continue; }
      // opponent wins: find minimal odd d such that opponent (attacker) forces promotion within d plies
      int dd = -1; for (int d = 1; d <= 41; d += 2) { memoD.clear(); if (canWin(mv[i].nwp, mv[i].nbp, mv[i].nwk, mv[i].nbk, 1 - stm, mv[i].ep, mv[i].epc, d)) { dd = d; break; } }
      printf(" %s:L%d", nm.c_str(), dd);
    }
    printf("\n");
  }
}

int main(int argc, char** argv) {
  W = 7; H = 6; F = 3; const char* dumpfn = nullptr; const char* depthfn = nullptr; const char* dudfn = nullptr; const char* reachfn = nullptr; int sampleK = 0; unsigned seed = 1; int tri = 0;
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    if (a == "--W") W = atoi(argv[++i]); else if (a == "--H") H = atoi(argv[++i]); else if (a == "--F") F = atoi(argv[++i]);
    else if (a == "--wmax") WM = atoi(argv[++i]); else if (a == "--bmax") BM = atoi(argv[++i]);
    else if (a == "--flat") FLAT = 1; else if (a == "--nopass") PASS = 0; else if (a == "--dump") dumpfn = argv[++i]; else if (a == "--depth") depthfn = argv[++i]; else if (a == "--dudout") dudfn = argv[++i]; else if (a == "--reach") reachfn = argv[++i];
    else { fprintf(stderr, "bad arg %s\n", a.c_str()); return 1; }
  }
  (void)sampleK; (void)seed; (void)tri;
  N = W * H; NN = N * N;
  for (int s = 0; s < N; s++) {
    int f = s % W, r = s / W; nnb[s] = 0; kadj[s] = 0; fromW[s] = fromB[s] = 0;
    for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) { if (!df && !dr) continue; int g = wrapf(f + df), rr = r + dr; if (g < 0 || rr < 0 || rr >= H) continue; int t = SQ(g, rr); nb[s][nnb[s]++] = t; kadj[s] |= BIT(t); }
    for (int d = -1; d <= 1; d += 2) {
      int g = wrapf(f + d); if (g < 0) continue;
      if (r - 1 >= 0) fromW[s] |= BIT(SQ(g, r - 1)); // white pawn at (g, r-1) attacks (f, r) (g = f+d, symmetric)
      if (r + 1 < H) fromB[s] |= BIT(SQ(g, r + 1));
    }
  }
  // pawn squares
  vector<int> psq; for (int f = 0; f < F; f++) for (int r = 1; r <= H - 2; r++) psq.push_back(SQ(f, r));
  int PW = psq.size();
  struct LL { u64 w, b; long long key; }; vector<LL> L;
  auto keyOf = [&](u64 a, u64 b) { int adv = 0; for (int s = 0; s < N; s++) { if (a >> s & 1) adv += s / W; if (b >> s & 1) adv += (H - 1) - s / W; }
    return (long long)(__builtin_popcountll(a) + __builtin_popcountll(b)) * 1000 + (500 - adv); };
  vector<St> reachRoots;
  if (reachfn) { // layers = pawn closure (king captures, pushes, double pushes, pawn captures) of the given roots
    FILE* rf = fopen(reachfn, "r"); char buf[512]; set<pair<u64,u64>> seen; vector<pair<u64,u64>> q;
    while (fgets(buf, sizeof buf, rf)) { string line(buf); u64 wp, bp; int wk, bk; if (!parsePos(line, wp, bp, wk, bk)) continue; reachRoots.push_back(St{wp, bp, wk, bk, -1, -1, -1}); if (seen.insert({wp, bp}).second) q.push_back({wp, bp}); }
    for (size_t qi = 0; qi < q.size(); qi++) {
      u64 wp = q[qi].first, bp = q[qi].second; auto add = [&](u64 a, u64 b) { if (seen.insert({a, b}).second) q.push_back({a, b}); };
      for (int s = 0; s < N; s++) { if (wp >> s & 1) add(wp & ~BIT(s), bp); if (bp >> s & 1) add(wp, bp & ~BIT(s)); }
      for (int side = 0; side < 2; side++) { u64 my = side ? bp : wp, op = side ? wp : bp; int dir = side ? -1 : 1, st = side ? H - 2 : 1, last = side ? 0 : H - 1;
        for (int s = 0; s < N; s++) if (my >> s & 1) { int f = s % W, r = s / W, r1 = r + dir; if (r1 < 0 || r1 >= H || r1 == last) continue;
          int t = SQ(f, r1); if (!((wp | bp) >> t & 1)) { u64 nm = (my & ~BIT(s)) | BIT(t); if (side) add(op, nm); else add(nm, op);
            if (r == st) { int t2 = SQ(f, r + 2 * dir); if (!((wp | bp) >> t2 & 1)) { u64 nm2 = (my & ~BIT(s)) | BIT(t2); if (side) add(op, nm2); else add(nm2, op); } } }
          for (int d = -1; d <= 1; d += 2) { int g = wrapf(f + d); if (g < 0) continue; int tt = SQ(g, r1); if (op >> tt & 1) { u64 nm = (my & ~BIT(s)) | BIT(tt); u64 no = op & ~BIT(tt); if (side) add(no, nm); else add(nm, no); } } } }
    }
    for (auto& pr : q) L.push_back({pr.first, pr.second, keyOf(pr.first, pr.second)});
  } else {
  vector<u64> masks; for (u64 m = 0; m < (1ULL << PW); m++) if (__builtin_popcountll(m) <= max(WM, BM)) { u64 mm = 0; for (int i = 0; i < PW; i++) if (m >> i & 1) mm |= BIT(psq[i]); masks.push_back(mm); }
  for (u64 a : masks) for (u64 b : masks) {
    if (a & b) continue; if (__builtin_popcountll(a) > WM || __builtin_popcountll(b) > BM) continue;
    L.push_back({a, b, keyOf(a, b)});
  }
  }
  stable_sort(L.begin(), L.end(), [](const LL& x, const LL& y) { return x.key < y.key; });
  for (size_t i = 0; i < L.size(); i++) { layers.push_back({L[i].w, L[i].b}); lidx[layers.back()] = i; }
  tab.assign((size_t)layers.size() * 2 * NN, 3);
  fprintf(stderr, "layers %zu table %.1f MB pass=%d flat=%d\n", layers.size(), tab.size() / 1e6, PASS, FLAT);
  clock_t t0 = clock();
  for (size_t li = 0; li < layers.size(); li++) solveLayer(li);
  fprintf(stderr, "solved %.1fs\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
  if (depthfn) { depthMode(depthfn); return 0; }
  if (reachfn) { for (auto& x : reachRoots) { Res R = classify(x); printf("%s\t%s\t", posstr(x).c_str(), R.cls.c_str()); for (size_t q = 0; q < R.closure.size(); q++) printf("%s%s", q ? "|" : "", posstr(R.closure[q]).c_str()); printf("\n"); } return 0; }
  FILE* df = dumpfn ? fopen(dumpfn, "w") : nullptr; FILE* dudf = dudfn ? fopen(dudfn, "w") : nullptr;
  map<string, long long> cnt; long long roots = 0, nearRel = 0, selfviol = 0;
  for (size_t li = 0; li < layers.size(); li++) {
    u64 wp = layers[li].w, bp = layers[li].b; if (!wp && !bp) continue;
    u64 occP = wp | bp;
    for (int wf = 0; wf < F; wf++) for (int wr = 0; wr < H; wr++) { int wk = SQ(wf, wr); if (occP >> wk & 1) continue;
      for (int bf = 0; bf < F; bf++) for (int br = 0; br < H; br++) { int bk = SQ(bf, br);
        if (bk == wk || (occP >> bk & 1) || (kadj[wk] >> bk & 1)) continue;
        if ((wp & fromW[bk]) || (bp & fromB[wk])) continue;
        roots++;
        St x{wp, bp, wk, bk, -1, -1, -1};
        Res R = classify(x); cnt[R.cls]++; if (R.nearOverRelaxed) nearRel++;
        if (PASS && (R.cls == "frozen" || R.cls == "on" || R.cls == "off" || R.cls == "dud" || R.cls == "over" || R.cls == "under")) {
          if (tab[TI(li, 0, wk, bk)] != 0 || tab[TI(li, 1, wk, bk)] != 0) selfviol++;
        }
        if (df) fprintf(df, "%s\t%s\n", posstr(x).c_str(), R.cls.c_str());
        if (dudf && R.cls == "dud") { fprintf(dudf, "%s\t", posstr(x).c_str()); for (size_t q = 0; q < R.closure.size(); q++) fprintf(dudf, "%s%s", q ? "|" : "", posstr(R.closure[q]).c_str()); fprintf(dudf, "\n"); }
      } }
  }
  printf("{\"board\":\"%s:%dx%d\",\"F\":%d,\"wmax\":%d,\"bmax\":%d,\"reading\":\"%s\",\"layers\":%zu,\"roots\":%lld,\"selfcheck_violations\":%lld,\"relaxed_over_or_under_roots\":%lld,\"counts\":{", FLAT ? "flat" : "cyl", W, H, F, WM, BM, PASS ? "A" : "B", layers.size(), roots, selfviol, nearRel);
  bool first = true; for (auto& kv : cnt) { printf("%s\"%s\":%lld", first ? "" : ",", kv.first.c_str(), kv.second); first = false; }
  printf("}}\n");
  return 0;
}

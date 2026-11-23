// b45.cpp -- K45, implementation B of the exact under/over test of LOOPY Definition 4.8 in the promotion model P.
// Written for K45 from SPEC.md and Definition 4.8 (not from K43's code): explicit pawn lists, a layer = a set of pawn
// squares reached from one configuration of blocked pairs by captures and pushes (layers are created on demand,
// children first), in-layer retrograde analysis with explicit forward successor lists.
// Value codes (mover's view): 0 draw, 1 win, 2 loss, 3 illegal.
// usage: b45 --W 10 [--H 6] --reach reach.txt < configs.txt      (config line: "file:rank file:rank ..." = white pawn of each blocked pair)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <string>
#include <map>
#include <unordered_map>
#include <iostream>
#include <sstream>
using namespace std;

static int W, H, N;
static inline int sqf(int s) { return s % W; }
static inline int sqr(int s) { return s / W; }
static inline int mk(int f, int r) { return r * W + ((f % W) + W) % W; }
static int distSq(int a, int b) {
  int df = abs(sqf(a) - sqf(b)); df = min(df, W - df);
  return max(df, abs(sqr(a) - sqr(b)));
}
static string sqname(int s) { char b[8]; snprintf(b, 8, "%c%d", 'a' + sqf(s), sqr(s) + 1); return b; }
static vector<vector<int>> nbrs;

struct Layer;
struct PM { int kind; int from, to; Layer* child; int ep; };   // kind 0 push, 1 double, 2 capture, 3 promotion
struct Mv { Layer* child; int wk, bk, ep; bool promo; bool inl; };
struct Layer {
  vector<int> pawns[2];           // squares, sorted
  string key;
  vector<char> occ;               // 0 empty, 1 white pawn, 2 black pawn
  vector<char> att[2];            // att[c][s] = square s attacked by a pawn of colour c
  vector<uint8_t> val;            // (stm*N + wk)*N + bk
  vector<PM> pm[2];
  vector<Layer*> kcap[2];         // kcap[c][s]: layer after the pawn of colour c on s is removed
  bool testedDone = false;
};
static unordered_map<string, Layer*> cache;
static Layer* getLayer(vector<int> w, vector<int> b);

static string keyOf(const vector<int>& w, const vector<int>& b) {
  string k; for (int s : w) k += "P" + sqname(s); for (int s : b) k += "p" + sqname(s); return k;
}
static inline int sidx(int stm, int wk, int bk) { return (stm * N + wk) * N + bk; }

static bool legalState(const Layer& L, int stm, int wk, int bk) {
  if (L.occ[wk] || L.occ[bk] || distSq(wk, bk) < 2) return false;
  if (stm == 0) return !L.att[0][bk];     // Black king must not be attacked by a white pawn
  return !L.att[1][wk];
}

// all legal moves of side stm at (L, wk, bk, ep)
static void genMoves(const Layer& L, int stm, int wk, int bk, int ep, vector<Mv>& out) {
  out.clear();
  int myk = stm ? bk : wk, otk = stm ? wk : bk;
  int en = 1 - stm;
  bool inchk = L.att[en][myk];
  // king moves
  for (int d : nbrs[myk]) {
    if (distSq(d, otk) < 2) continue;
    char o = L.occ[d];
    if (o == (stm ? 2 : 1) ) continue;   // own pawn  (occ 1 = white pawn)
    if (o == 0) {
      if (L.att[en][d]) continue;
      out.push_back({(Layer*)&L, stm ? wk : d, stm ? d : bk, -1, false, true});
    } else {
      Layer* c = L.kcap[en][d];
      if (c->att[en][d]) continue;
      out.push_back({c, stm ? wk : d, stm ? d : bk, -1, false, false});
    }
  }
  // pawn moves
  for (const PM& p : L.pm[stm]) {
    if (p.kind == 0 || p.kind == 3) {
      if (inchk) continue;
      if (p.to == wk || p.to == bk) continue;
      if (p.kind == 3) { out.push_back({nullptr, wk, bk, -1, true, false}); continue; }
      out.push_back({p.child, wk, bk, -1, false, false});
    } else if (p.kind == 1) {
      if (inchk) continue;
      int mid = (p.from + p.to) / 2;      // squares differ by 2 ranks: mid = from + dir*W
      mid = p.from + (p.to - p.from) / 2;
      if (mid == wk || mid == bk || p.to == wk || p.to == bk) continue;
      out.push_back({p.child, wk, bk, p.ep, false, false});
    } else {
      // capture: own king must not be attacked by the remaining enemy pawns
      if (p.child->att[en][myk]) continue;
      out.push_back({p.child, wk, bk, -1, false, false});
    }
  }
  // en passant
  if (ep >= 0) {
    int dir = stm ? -1 : 1;
    for (int s : L.pawns[stm]) {
      if (sqr(ep) != sqr(s) + dir) continue;
      int df = abs(sqf(ep) - sqf(s)); df = min(df, W - df);
      if (df != 1) continue;
      int q = mk(sqf(ep), sqr(s));
      if (L.occ[q] != (stm ? 1 : 2)) continue;
      if (L.occ[ep] || ep == wk || ep == bk) continue;
      vector<int> mw = L.pawns[0], mb = L.pawns[1];
      vector<int>& mine = stm ? mb : mw; vector<int>& theirs = stm ? mw : mb;
      mine.erase(find(mine.begin(), mine.end(), s)); mine.push_back(ep);
      theirs.erase(find(theirs.begin(), theirs.end(), q));
      Layer* c = getLayer(mw, mb);
      if (c->att[en][myk]) continue;
      out.push_back({c, wk, bk, -1, false, false});
    }
  }
}

static int evalState(const Layer& L, int stm, int wk, int bk, int ep);
// value of the move for the mover: 1 win, 0 draw, 2 loss
static int moveValue(const Layer& L, const Mv& m, int stm) {
  if (m.promo) return 1;
  int cv;
  if (m.ep >= 0) cv = evalState(*m.child, 1 - stm, m.wk, m.bk, m.ep);
  else cv = m.child->val[sidx(1 - stm, m.wk, m.bk)];
  if (cv == 3) { fprintf(stderr, "internal: illegal child\n"); exit(3); }
  return cv == 2 ? 1 : (cv == 1 ? 2 : 0);
}
static int evalState(const Layer& L, int stm, int wk, int bk, int ep) {
  vector<Mv> mv; genMoves(L, stm, wk, bk, ep, mv);
  if (mv.empty()) return L.att[1 - stm][stm ? bk : wk] ? 2 : 0;
  bool dr = false;
  for (auto& m : mv) { int v = moveValue(L, m, stm); if (v == 1) return 1; if (v == 0) dr = true; }
  return dr ? 0 : 2;
}

static void solve(Layer& L) {
  int S = 2 * N * N;
  L.val.assign(S, 3);
  vector<int> pend(S, 0);
  vector<pair<int,int>> pairs;   // (child, parent)
  vector<int> queue;
  vector<Mv> mv;
  for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++)
    if (legalState(L, stm, wk, bk)) L.val[sidx(stm, wk, bk)] = 0;
  for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) {
    int id = sidx(stm, wk, bk);
    if (L.val[id] != 0) continue;
    genMoves(L, stm, wk, bk, -1, mv);
    if (mv.empty()) { if (L.att[1 - stm][stm ? bk : wk]) { L.val[id] = 2; queue.push_back(id); } continue; }
    bool win = false;
    for (auto& m : mv) {
      if (m.inl) { pairs.push_back({sidx(1 - stm, m.wk, m.bk), id}); pend[id]++; continue; }
      int v = moveValue(L, m, stm);
      if (v == 1) { win = true; break; }
      if (v == 0) pend[id]++;
    }
    if (win) { L.val[id] = 1; queue.push_back(id); }
    else if (pend[id] == 0) { L.val[id] = 2; queue.push_back(id); }
  }
  // reverse adjacency (CSR)
  vector<int> start(S + 1, 0);
  for (auto& p : pairs) start[p.first + 1]++;
  for (int i = 0; i < S; i++) start[i + 1] += start[i];
  vector<int> rev(pairs.size()), fill(start.begin(), start.end() - 1);
  for (auto& p : pairs) rev[fill[p.first]++] = p.second;
  for (size_t qh = 0; qh < queue.size(); qh++) {
    int x = queue[qh];
    for (int k = start[x]; k < start[x + 1]; k++) {
      int p = rev[k];
      if (L.val[p] != 0) continue;
      if (L.val[x] == 2) { L.val[p] = 1; queue.push_back(p); }
      else if (--pend[p] == 0) { L.val[p] = 2; queue.push_back(p); }
    }
  }
}

static vector<Layer*> created;
static Layer* getLayer(vector<int> w, vector<int> b) {
  sort(w.begin(), w.end()); sort(b.begin(), b.end());
  string k = keyOf(w, b);
  auto it = cache.find(k);
  if (it != cache.end()) return it->second;
  Layer* L = new Layer();
  L->pawns[0] = w; L->pawns[1] = b; L->key = k;
  L->occ.assign(N, 0); L->att[0].assign(N, 0); L->att[1].assign(N, 0);
  for (int s : w) { L->occ[s] = 1; if (sqr(s) + 1 < H) { L->att[0][mk(sqf(s) - 1, sqr(s) + 1)] = 1; L->att[0][mk(sqf(s) + 1, sqr(s) + 1)] = 1; } }
  for (int s : b) { L->occ[s] = 2; if (sqr(s) - 1 >= 0) { L->att[1][mk(sqf(s) - 1, sqr(s) - 1)] = 1; L->att[1][mk(sqf(s) + 1, sqr(s) - 1)] = 1; } }
  L->kcap[0].assign(N, nullptr); L->kcap[1].assign(N, nullptr);
  for (int c = 0; c < 2; c++) for (int s : L->pawns[c]) {   // king capture of a pawn of colour c
    vector<int> w2 = w, b2 = b; vector<int>& v = c ? b2 : w2; v.erase(find(v.begin(), v.end(), s));
    L->kcap[c][s] = getLayer(w2, b2);
  }
  for (int c = 0; c < 2; c++) {
    int dir = c ? -1 : 1, last = c ? 0 : H - 1, startR = c ? H - 2 : 1;
    for (int s : L->pawns[c]) {
      int f = sqf(s), r = sqr(s), t = s + dir * W;
      auto moved = [&](int to, int removed) {
        vector<int> w2 = w, b2 = b; vector<int>& mine = c ? b2 : w2; vector<int>& th = c ? w2 : b2;
        mine.erase(find(mine.begin(), mine.end(), s)); mine.push_back(to);
        if (removed >= 0) th.erase(find(th.begin(), th.end(), removed));
        return getLayer(w2, b2);
      };
      if (r + dir == last) {
        if (!L->occ[t]) L->pm[c].push_back({3, s, t, nullptr, -1});
      } else {
        if (!L->occ[t]) {
          L->pm[c].push_back({0, s, t, moved(t, -1), -1});
          int t2 = t + dir * W;
          if (r == startR && !L->occ[t2]) {
            int ep = -1;
            for (int d = -1; d <= 1; d += 2) { int q = mk(f + d, r + 2 * dir); if (L->occ[q] == (c ? 1 : 2)) ep = t; }
            L->pm[c].push_back({1, s, t2, moved(t2, -1), ep});
          }
        }
        for (int d = -1; d <= 1; d += 2) {
          int tt = mk(f + d, r + dir);
          if (L->occ[tt] == (c ? 1 : 2)) L->pm[c].push_back({2, s, tt, moved(tt, tt), -1});
        }
      }
    }
  }
  solve(*L);
  cache[k] = L; created.push_back(L);
  return L;
}

// ---------------------------------------------------------------- Definition 4.8 test
struct Cnt { long long pl = 0, f1 = 0, nofz = 0, promo = 0, f2 = 0, f3 = 0, f4 = 0; };
static vector<string> hitLines;
static bool allLose(const Layer& L, int stm, int wk, int bk, int ep, int& n) {
  vector<Mv> mv; genMoves(L, stm, wk, bk, ep, mv); n = mv.size();
  for (auto& m : mv) if (moveValue(L, m, stm) != 2) return false;
  return true;
}
// sh = shuttling colour (0 White = under test, 1 Black = over test), fr = freezing colour
static Cnt testLayer(const Layer& L, int sh) {
  Cnt C; int fr = 1 - sh;
  vector<Mv> mv;
  vector<char> safeSh(N), safeFr(N);
  for (int s = 0; s < N; s++) {
    safeSh[s] = !L.occ[s] && !L.att[fr][s];   // shuttler's king: not attacked by the freezer's pawns
    safeFr[s] = !L.occ[s] && !L.att[sh][s];   // freezer's king: not attacked by the shuttler's pawns
  }
  for (int u = 0; u < N; u++) {
    if (!safeSh[u]) continue;
    for (int v : nbrs[u]) {
      if (v < u || !safeSh[v]) continue;
      for (int t = 0; t < N; t++) {
        if (!safeFr[t] || distSq(t, u) < 2 || distSq(t, v) < 2) continue;
        C.pl++;
        int z[2] = {u, v};
        auto st = [&](int aa, int& wk, int& bk) { if (sh == 0) { wk = z[aa]; bk = t; } else { wk = t; bk = z[aa]; } };
        bool ok = true;
        for (int aa = 0; aa < 2 && ok; aa++) {
          int wk, bk; st(aa, wk, bk);
          genMoves(L, sh, wk, bk, -1, mv);
          int nsh = 0;
          for (auto& m : mv) {
            int dest = sh ? m.bk : m.wk;
            if (m.inl && dest == z[1 - aa]) { nsh++; continue; }
            if (moveValue(L, m, sh) != 2) { ok = false; break; }
          }
          if (nsh != 1) ok = false;
        }
        if (!ok) continue;
        C.f1++;
        struct Fz { Layer* L; int wk, bk, ep; };
        vector<Fz> fz[2]; bool promo = false, nofz = false;
        for (int aa = 0; aa < 2; aa++) {
          int wk, bk; st(aa, wk, bk);
          genMoves(L, fr, wk, bk, -1, mv);
          for (auto& m : mv) {
            if (m.promo) { promo = true; continue; }
            if (moveValue(L, m, fr) == 2) continue;
            fz[aa].push_back({m.child, m.wk, m.bk, m.ep});
          }
          if (fz[aa].empty()) nofz = true;
        }
        if (promo) C.promo++;
        if (nofz) { C.nofz++; continue; }
        if (promo) continue;
        C.f2++;
        bool u3 = true;
        for (int aa = 0; aa < 2 && u3; aa++) for (auto& f : fz[aa]) {
          int n; bool all = allLose(*f.L, sh, f.wk, f.bk, f.ep, n);
          if (n < 1 || !all) { u3 = false; break; }
        }
        if (!u3) continue;
        C.f3++;
        bool u4 = true;
        for (int aa = 0; aa < 2 && u4; aa++) for (auto& f : fz[aa]) {
          // q with the freezer to move: the shuttler's king (not to move) must not be attacked by the freezer's pawns
          bool chk = sh == 0 ? f.L->att[1][f.wk] : f.L->att[0][f.bk];
          // careful: attacks on the shuttler's king come from the freezer's pawns, colour fr
          chk = f.L->att[fr][sh == 0 ? f.wk : f.bk];
          if (chk) { u4 = false; break; }
          int n; bool all = allLose(*f.L, fr, f.wk, f.bk, -1, n);
          if (n < 1 || !all) { u4 = false; break; }
        }
        if (u4) {
          C.f4++;
          string h = "HIT sh=" + to_string(sh) + " K" + sqname(sh ? t : u) + " k" + sqname(sh ? u : t);
          for (int p : L.pawns[0]) h += " P" + sqname(p);
          for (int p : L.pawns[1]) h += " p" + sqname(p);
          h += sh ? " b - " : " w - "; h += " shuttle " + sqname(u) + sqname(v);
          hitLines.push_back(h);
        }
      }
    }
  }
  return C;
}


static int parseSq(const string& t) { int f = t[0] - 'a', r = atoi(t.c_str() + 1) - 1; return mk(f, r); }
static string mvDesc(const Layer& L, const Mv& m, int stm, int wk, int bk) {
  if (m.promo) return "promotion";
  if (m.wk != wk || m.bk != bk) return string("K") + sqname(stm ? bk : wk) + (m.child != &L ? "x" : "-") + sqname(stm ? m.bk : m.wk);
  return string("pawn move to ") + m.child->key + (m.ep >= 0 ? " (e.p. flag)" : "");
}
static const char* vname(int v) { return v == 1 ? "WIN" : (v == 2 ? "loses" : "draw"); }
// D line: "D <file:rank ...> | <sq of shuttling king, one of the pair> <sq of the other pair square> <sq of freezing king> <sh>"
static void diagLine(const string& line) {
  istringstream ss(line); string tok; ss >> tok; vector<int> w, b; string a, bb, c; int sh;
  while (ss >> tok && tok != "|") { if (tok[0] == 'P' || tok[0] == 'p') { (tok[0] == 'P' ? w : b).push_back(parseSq(tok.substr(1))); continue; } int f, r; sscanf(tok.c_str(), "%d:%d", &f, &r); w.push_back(mk(f, r - 1)); b.push_back(mk(f, r)); }
  string s1, s2, s3; ss >> s1 >> s2 >> s3 >> sh;
  Layer* L = getLayer(w, b);
  int z[2] = {parseSq(s1), parseSq(s2)}, t = parseSq(s3), fr = 1 - sh;
  printf("DIAG layer %s  shuttler=%s (%s)  pair %s %s  freezer king %s\n", L->key.c_str(), sh ? "Black" : "White", sh ? "over" : "under", s1.c_str(), s2.c_str(), s3.c_str());
  vector<Mv> mv;
  for (int aa = 0; aa < 2; aa++) for (int stm : {sh, fr}) {
    int wk = sh ? t : z[aa], bk = sh ? z[aa] : t;
    int id = sidx(stm, wk, bk);
    printf("ROOT shuttler on %s, %s to move: legal=%d value(mover)=%s\n", sqname(z[aa]).c_str(), stm ? "Black" : "White", L->val[id] != 3, L->val[id] == 3 ? "-" : vname(L->val[id]));
    genMoves(*L, stm, wk, bk, -1, mv);
    int nlose = 0, nok = 0;
    for (auto& m : mv) {
      int v = moveValue(*L, m, stm);
      bool isShuttle = stm == sh && m.inl && (sh ? m.bk : m.wk) == z[1 - aa];
      if (v == 2) { nlose++; continue; }
      nok++;
      printf("    %s%s -> %s\n", mvDesc(*L, m, stm, wk, bk).c_str(), isShuttle ? " [shuttle]" : "", vname(v));
      if (stm == fr && !m.promo) {
        int n; bool all = allLose(*m.child, sh, m.wk, m.bk, m.ep, n);
        bool chk = m.child->att[fr][sh == 0 ? m.wk : m.bk];
        int n4 = 0; bool all4 = chk ? false : allLose(*m.child, fr, m.wk, m.bk, -1, n4);
        printf("        U3: shuttler to move in q has %d moves, all lose=%d;  U4: shuttler king attacked in q=%d, freezer to move has %d moves, all lose=%d\n", n, (int)all, (int)chk, n4, (int)all4);
        if (!all4 && !chk) {
          vector<Mv> m3; genMoves(*m.child, fr, m.wk, m.bk, -1, m3);
          int v0 = L->val[0]; (void)v0;
          printf("            q value (shuttler to move)=%s, (freezer to move)=%s\n", vname(m.child->val[sidx(sh, m.wk, m.bk)]), vname(m.child->val[sidx(fr, m.wk, m.bk)]));
          for (auto& x : m3) { int vv = moveValue(*m.child, x, fr); if (vv != 2) printf("            freezer move in q %s -> %s\n", mvDesc(*m.child, x, fr, m.wk, m.bk).c_str(), vname(vv)); }
        }
        if (!all) {
          vector<Mv> m2; genMoves(*m.child, sh, m.wk, m.bk, m.ep, m2);
          for (auto& x : m2) { int vv = moveValue(*m.child, x, sh); if (vv != 2) printf("            q move %s -> %s\n", mvDesc(*m.child, x, sh, m.wk, m.bk).c_str(), vname(vv)); }
        }
      }
    }
    printf("    moves that lose at once: %d, others: %d\n", nlose, nok);
  }
}

int main(int argc, char** argv) {
  H = 6; const char* reachf = nullptr; const char* allfiles = nullptr;
  for (int i = 1; i < argc; i++) {
    string a = argv[i];
    if (a == "--W") W = atoi(argv[++i]);
    else if (a == "--H") H = atoi(argv[++i]);
    else if (a == "--reach") reachf = argv[++i];
    else if (a == "--all") allfiles = argv[++i];
    else { fprintf(stderr, "bad arg\n"); return 1; }
  }
  N = W * H;
  nbrs.assign(N, {});
  for (int s = 0; s < N; s++) for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
    if (!df && !dr) continue; int r = sqr(s) + dr; if (r < 0 || r >= H) continue;
    int t = mk(sqf(s) + df, r); if (t != s && find(nbrs[s].begin(), nbrs[s].end(), t) == nbrs[s].end()) nbrs[s].push_back(t);
  }
  FILE* rf = reachf ? fopen(reachf, "w") : nullptr;
  if (allfiles) {
    // every layer with at most 3 white and 3 black pawns on ranks 2..H-1 of the given files (the search space of implementation A)
    vector<int> fl; { string t = allfiles; size_t p = 0; while (p < t.size()) { size_t q = t.find(',', p); if (q == string::npos) q = t.size(); fl.push_back(atoi(t.substr(p, q - p).c_str())); p = q + 1; } }
    vector<int> sqs; for (int f : fl) for (int r = 1; r <= H - 2; r++) sqs.push_back(mk(f, r));
    int P = sqs.size(); vector<unsigned> subs; for (unsigned m = 0; m < (1u << P); m++) if (__builtin_popcount(m) <= 3) subs.push_back(m);
    for (unsigned wm : subs) for (unsigned bm : subs) {
      if (wm & bm) continue;
      vector<int> w, b; for (int i = 0; i < P; i++) { if (wm >> i & 1) w.push_back(sqs[i]); if (bm >> i & 1) b.push_back(sqs[i]); }
      getLayer(w, b);
    }
    printf("G %s layers=%zu\n", allfiles, created.size());
    for (size_t i = 0; i < created.size(); i++) {
      Layer* L = created[i];
      bool blocked = !L->pawns[0].empty() && L->pawns[0].size() == L->pawns[1].size();
      for (int s : L->pawns[0]) if (!(s + W < N && L->occ[s + W] == 2)) blocked = false;
      for (int sh = 0; sh < 2; sh++) {
        Cnt c = testLayer(*L, sh);
        if (c.f1 > 0 || blocked)
          printf("LAYER %s sh=%d%s pl=%lld f1=%lld nofz=%lld promo=%lld f2=%lld f3=%lld f4=%lld\n", L->key.c_str(), sh, blocked ? " B" : "", c.pl, c.f1, c.nofz, c.promo, c.f2, c.f3, c.f4);
      }
      for (auto& h : hitLines) printf("%s\n", h.c_str());
      hitLines.clear();
    }
    return 0;
  }
  string line; string curgroup;
  while (getline(cin, line)) {
    if (line.empty() || line[0] == '#') continue;
    if (line[0] == 'G') {   // group line: clear the layer cache (new file triple)
      for (auto* L : created) delete L; created.clear(); cache.clear();
      printf("%s\n", line.c_str()); fflush(stdout); continue;
    }
    if (line[0] == 'D') { diagLine(line); fflush(stdout); continue; }
    istringstream ss(line); string tok; vector<int> w, b;
    while (ss >> tok) { int f, r; sscanf(tok.c_str(), "%d:%d", &f, &r); w.push_back(mk(f, r - 1)); b.push_back(mk(f, r)); }
    size_t before = created.size();
    getLayer(w, b);
    // test every layer created since (children first); each layer once
    for (size_t i = 0; i < created.size(); i++) {
      Layer* L = created[i];
      if (L->testedDone) continue;
      L->testedDone = true;
      if (rf) fprintf(rf, "%s\n", L->key.c_str());
      bool blocked = !L->pawns[0].empty() && L->pawns[0].size() == L->pawns[1].size();
      for (int s : L->pawns[0]) if (!(s + W < N && L->occ[s + W] == 2)) blocked = false;
      for (int sh = 0; sh < 2; sh++) {
        Cnt c = testLayer(*L, sh);
        if (c.f1 > 0 || blocked)
          printf("LAYER %s sh=%d%s pl=%lld f1=%lld nofz=%lld promo=%lld f2=%lld f3=%lld f4=%lld\n", L->key.c_str(), sh, blocked ? " B" : "", c.pl, c.f1, c.nofz, c.promo, c.f2, c.f3, c.f4);
      }
    }
    (void)before;
    fflush(stdout);
  }
  if (rf) fclose(rf);
  return 0;
}

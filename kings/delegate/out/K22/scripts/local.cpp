// local.cpp -- solver for the local game L(Q_Z) of Definition 2.6 (LOOPY.md), unbounded time T.
// s-bar = White (promoter, moves up).  s = Black (defender; may pass whenever not in check).
//  * first promotion ends the game.  White promotion = win for White (L1_P) or, with --safe, only if
//    the black king cannot capture the new queen at once (L1); unsafe promotion = failure for White.
//    Black promotion = failure for White.
//  * White's king may only step onto files of F_Z (including captures).  Black's king is free.
//  * Mate of Black (in check, no legal move) = win for White.  White without a legal move = failure.
//  * Infinite play = failure for White (T finite).
// Value of a state = least n such that White forces a win using n White moves (255 = no win).
// Written for task K22 (kings/delegate/out/K22).  No part of kpsolve.c is used.
//
// usage:
//   local --board flat|cyl WxH --fz lo hi [--safe] [--noep] pos      < positions   (reads "Ka1 ka6 Pc2 pd3 b -")
//   local --board flat|cyl WxH --fz lo hi [--safe] [--noep] enum --f F --wmax A --bmax B [--bfiles lo hi]
//         [--kmode any|nearby] [--ep]
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;
typedef uint64_t u64;

static int W, H, N, WRAP = 0, SAFE = 0, EPON = 1, SHOWMOVES = 0;
static bool FZ[16];
static int kingAdj[64][8], kingAdjN[64];
static u64 kingAdjMask[64];
static u64 attBy[2][64];   // attBy[col][sq]: squares from which a pawn of colour col attacks sq
static int fileOf(int s) { return s % W; }
static int rankOf(int s) { return s / W; }
static inline u64 bit(int s) { return 1ULL << s; }

static int stepsq(int s, int df, int dr) {
  int f = fileOf(s) + df, r = rankOf(s) + dr;
  if (r < 0 || r >= H) return -1;
  if (WRAP) f = ((f % W) + W) % W; else if (f < 0 || f >= W) return -1;
  return r * W + f;
}
static void initGeom() {
  N = W * H;
  for (int s = 0; s < N; s++) {
    kingAdjN[s] = 0; kingAdjMask[s] = 0; attBy[0][s] = attBy[1][s] = 0;
    for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
      if (!df && !dr) continue;
      int t = stepsq(s, df, dr);
      if (t >= 0 && t != s && !(kingAdjMask[s] & bit(t))) { kingAdj[s][kingAdjN[s]++] = t; kingAdjMask[s] |= bit(t); }
    }
    // white pawn at q attacks q+(±1,+1). squares attacking s: s+(∓1,-1)
    for (int df = -1; df <= 1; df += 2) {
      int q = stepsq(s, df, -1); if (q >= 0) attBy[0][s] |= bit(q);
      q = stepsq(s, df, +1); if (q >= 0) attBy[1][s] |= bit(q);
    }
  }
}

struct Pos { u64 wp, bp; int ep, epc; int wk, bk, stm; };  // ep = target square or -1; epc = colour of pawn that double-stepped
struct Mv { int kind; Pos p; string d; };  // kind 0 child, 1 terminal win for White, 2 terminal failure

static string sqName(int s) { string r; r += char('a' + fileOf(s)); r += to_string(rankOf(s) + 1); return r; }

static void gen(const Pos& s, vector<Mv>& out, bool desc) {
  out.clear();
  int c = s.stm;
  u64 own = c ? s.bp : s.wp, en = c ? s.wp : s.bp;
  int ok = c ? s.bk : s.wk, ek = c ? s.wk : s.bk;
  u64 occ = s.wp | s.bp | bit(s.wk) | bit(s.bk);
  int ec = 1 - c;
  auto mk = [&](u64 nown, u64 nen, int nok, int nep, int nepc) {
    Pos q; q.wp = c ? nen : nown; q.bp = c ? nown : nen; q.ep = nep; q.epc = nepc;
    q.wk = c ? ek : nok; q.bk = c ? nok : ek; q.stm = ec; return q;
  };
  // king moves
  for (int i = 0; i < kingAdjN[ok]; i++) {
    int t = kingAdj[ok][i];
    if (own & bit(t)) continue;
    if (kingAdjMask[ek] & bit(t)) continue;
    if (t == ek) continue;
    if (c == 0 && !FZ[fileOf(t)]) continue;
    u64 en2 = en & ~bit(t);
    if (attBy[ec][t] & en2) continue;
    Mv m; m.kind = 0; m.p = mk(own, en2, t, -1, -1);
    if (desc) m.d = string(c ? "k" : "K") + (en & bit(t) ? "x" : "") + sqName(t);
    out.push_back(m);
  }
  // pawn moves
  int dr = c ? -1 : 1, startR = c ? H - 2 : 1, lastR = c ? 0 : H - 1;
  bool inChk = (attBy[ec][ok] & en) != 0;
  for (int p = 0; p < N; p++) if (own & bit(p)) {
    int f = fileOf(p), r = rankOf(p);
    auto emit = [&](int t, u64 en2, bool cap, int nep, int nepc, bool epcap) {
      if (attBy[ec][ok] & en2) return;   // own king attacked afterwards
      u64 own2 = (own & ~bit(p));
      bool promo = (rankOf(t) == lastR);
      Mv m; m.p = mk(own2, en2, ok, nep, nepc);
      if (!promo) { own2 |= bit(t); m.p = mk(own2, en2, ok, nep, nepc); m.kind = 0; }
      else if (c == 1) m.kind = 2;
      else {
        m.kind = 1;
        if (SAFE) {
          // black king captures the new queen on t?
          if ((kingAdjMask[s.bk] & bit(t)) && !(kingAdjMask[s.wk] & bit(t)) && !(attBy[0][t] & own2)) m.kind = 2;
        }
      }
      if (desc) {
        m.d = string(c ? "p" : "P") + sqName(p) + (cap ? "x" : "-") + sqName(t) + (epcap ? "ep" : "") + (promo ? "=Q" : "");
      }
      out.push_back(m);
    };
    int t1 = stepsq(p, 0, dr);
    if (t1 >= 0 && !(occ & bit(t1))) {
      emit(t1, en, false, -1, -1, false);
      if (r == startR) {
        int t2 = stepsq(p, 0, 2 * dr);
        if (t2 >= 0 && !(occ & bit(t2))) {
          int nep = -1;
          if (EPON && rankOf(t2) != lastR) {
            for (int df = -1; df <= 1; df += 2) { int a = stepsq(t2, df, 0); if (a >= 0 && (en & bit(a))) nep = t1; }
          }
          if (rankOf(t2) == lastR) { emit(t2, en, false, -1, -1, false); }
          else emit(t2, en, false, nep, nep >= 0 ? c : -1, false);
        }
      }
    }
    for (int df = -1; df <= 1; df += 2) {
      int t = stepsq(p, df, dr);
      if (t < 0) continue;
      if (en & bit(t)) emit(t, en & ~bit(t), true, -1, -1, false);
      else if (s.ep == t && s.epc == ec && EPON) {
        int vp = stepsq(t, 0, -dr);  // victim square: same rank as p, file of t
        if (vp >= 0 && (en & bit(vp))) emit(t, en & ~bit(vp), true, -1, -1, true);
      }
    }
  }
  if (c == 1 && !inChk) {
    Mv m; m.kind = 0; m.p = s; m.p.ep = -1; m.p.epc = -1; m.p.stm = 0; if (desc) m.d = "pass"; out.push_back(m);
  }
}

struct Key { u64 a, b; int ep, epc; bool operator==(const Key& o) const { return a == o.a && b == o.b && ep == o.ep && epc == o.epc; } };
struct KH { size_t operator()(const Key& k) const { return (k.a * 0x9E3779B97F4A7C15ULL) ^ (k.b * 0xC2B2AE3D27D4EB4FULL) ^ (size_t)(k.ep + 3) * 1315423911u ^ (size_t)(k.epc + 3) * 2654435761u; } };
struct Layer { vector<uint8_t> R; };
static unordered_map<Key, Layer*, KH> memo;
static const uint8_t INF = 255, INV = 254;

static inline int sid(int stm, int wk, int bk) { return (stm * N + wk) * N + bk; }

static bool validState(u64 wp, u64 bp, int ep, int epc, int stm, int wk, int bk) {
  if (wk == bk) return false;
  if ((wp | bp) & (bit(wk) | bit(bk))) return false;
  if (kingAdjMask[wk] & bit(bk)) return false;
  if (stm == 0 && (attBy[0][bk] & wp)) return false;   // black not to move must not be in check
  if (stm == 1 && (attBy[1][wk] & bp)) return false;
  if (!FZ[fileOf(wk)]) return false;                  // White king stays on F_Z
  if (ep >= 0) {
    if (stm != 1 - epc) return false;
    int dr = epc ? -1 : 1;
    int orig = stepsq(ep, 0, -dr), t2 = stepsq(ep, 0, dr);
    if (wk == ep || bk == ep || wk == orig || bk == orig) return false;
    u64 pawnsOfEpc = epc ? bp : wp;
    if (!(pawnsOfEpc & bit(t2))) return false;
    if ((wp | bp) & (bit(ep) | bit(orig))) return false;
  }
  return true;
}

static Layer* solveLayer(u64 wp, u64 bp, int ep, int epc);

static uint8_t extVal(const Pos& q) {
  Layer* L = solveLayer(q.wp, q.bp, q.ep, q.epc);
  return L->R[sid(q.stm, q.wk, q.bk)];
}

static Layer* solveLayer(u64 wp, u64 bp, int ep, int epc) {
  Key k{wp, bp, ep, epc};
  auto it = memo.find(k);
  if (it != memo.end()) return it->second;
  Layer* L = new Layer; L->R.assign(2 * N * N, INV);
  struct Rec { uint8_t cst; bool mate; vector<int> kids; };
  vector<Rec> recs(2 * N * N);
  vector<int> act;
  vector<Mv> mv;
  for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) {
    if (!validState(wp, bp, ep, epc, stm, wk, bk)) continue;
    int id = sid(stm, wk, bk);
    Pos s{wp, bp, ep, epc, wk, bk, stm};
    gen(s, mv, false);
    Rec& r = recs[id];
    r.mate = false;
    if (stm == 0) r.cst = INF; else r.cst = 0;   // white: min of items; black: max of items
    bool any = false;
    for (auto& m : mv) {
      any = true;
      if (m.kind == 1) { if (stm == 0) r.cst = 0; else {} }               // terminal win: value 0 item
      else if (m.kind == 2) { if (stm == 1) r.cst = INF; }                // failure: infinite item (white: ignore)
      else {
        bool intra = (m.p.wp == wp && m.p.bp == bp && m.p.ep == ep && m.p.epc == epc);
        if (intra) r.kids.push_back(sid(m.p.stm, m.p.wk, m.p.bk));
        else {
          uint8_t v = extVal(m.p);
          if (stm == 0) r.cst = min(r.cst, v); else r.cst = max(r.cst, v);
        }
      }
    }
    if (stm == 1 && !any) { r.mate = true; r.cst = 0; }  // no moves: only possible in check (pass otherwise) => mate
    L->R[id] = INF;
    act.push_back(id);
  }
  // Jacobi iteration
  vector<uint8_t> nr(L->R.size());
  while (true) {
    bool ch = false;
    nr = L->R;
    for (int id : act) {
      Rec& r = recs[id];
      int stm = id / (N * N);
      uint8_t v;
      if (stm == 0) {
        int best = r.cst;
        for (int kid : r.kids) best = min<int>(best, L->R[kid]);
        v = best >= INF ? INF : (uint8_t)(best + 1);
      } else {
        int worst = r.cst;
        for (int kid : r.kids) worst = max<int>(worst, L->R[kid]);
        v = (uint8_t)worst;
      }
      if (v != L->R[id]) { nr[id] = v; ch = true; }
    }
    L->R.swap(nr);
    if (!ch) break;
  }
  memo[k] = L;
  return L;
}

// ---- positions ----
static bool parsePos(const char* line, Pos& p, string& err) {
  p.wp = p.bp = 0; p.ep = -1; p.epc = -1; p.wk = p.bk = -1; p.stm = 0;
  char buf[256]; strncpy(buf, line, 255); buf[255] = 0;
  vector<string> tok; char* sv; for (char* t = strtok_r(buf, " \t\r\n", &sv); t; t = strtok_r(NULL, " \t\r\n", &sv)) tok.push_back(t);
  if (tok.size() < 3) { err = "short"; return false; }
  size_t n = tok.size();
  string stm = tok[n - 2], ep = tok[n - 1];
  p.stm = (stm == "b") ? 1 : 0;
  for (size_t i = 0; i + 2 < n; i++) {
    string t = tok[i]; char pc = t[0]; int f = t[1] - 'a', r = atoi(t.c_str() + 2) - 1;
    if (f < 0 || f >= W || r < 0 || r >= H) { err = "range"; return false; }
    int s = r * W + f;
    if (pc == 'K') p.wk = s; else if (pc == 'k') p.bk = s; else if (pc == 'P') p.wp |= bit(s); else if (pc == 'p') p.bp |= bit(s);
    else { err = "piece"; return false; }
  }
  if (ep != "-") { int f = ep[0] - 'a', r = atoi(ep.c_str() + 1) - 1; p.ep = r * W + f; p.epc = p.stm ? 0 : 1; }
  return p.wk >= 0 && p.bk >= 0;
}
static string posStr(const Pos& p) {
  string s = "K" + sqName(p.wk) + " k" + sqName(p.bk);
  for (int q = 0; q < N; q++) if (p.wp & bit(q)) s += " P" + sqName(q);
  for (int q = 0; q < N; q++) if (p.bp & bit(q)) s += " p" + sqName(q);
  s += p.stm ? " b " : " w ";
  s += p.ep >= 0 ? sqName(p.ep) : "-";
  return s;
}
static uint8_t valOf(const Pos& p) { return extVal(p); }

static void printPV(Pos p, int maxPlies) {
  vector<Mv> mv;
  string line;
  for (int ply = 0; ply < maxPlies; ply++) {
    uint8_t v = valOf(p);
    if (v == INF) break;
    gen(p, mv, true);
    if (mv.empty()) { line += " #mate"; break; }
    const Mv* best = nullptr; int bestv = p.stm == 0 ? 1000 : -1;
    for (auto& m : mv) {
      int mvv;
      if (m.kind == 1) mvv = 0; else if (m.kind == 2) mvv = INF; else mvv = valOf(m.p);
      if (p.stm == 0) { if (mvv < bestv) { bestv = mvv; best = &m; } }
      else { if (mvv > bestv) { bestv = mvv; best = &m; } }
    }
    if (!best) break;
    line += (p.stm == 0 ? " W:" : " B:") + best->d;
    if (best->kind != 0) { line += (best->kind == 1 ? " [promotion wins]" : ""); break; }
    p = best->p;
  }
  printf("   PV:%s\n", line.c_str());
}

int main(int argc, char** argv) {
  string mode;
  int lo = 0, hi = -1, Fp = -1, wmax = 2, bmax = 2, blo = -1, bhi = -1, nex = 20, wmin = 1, bmin = 0, kmode = 0, withEp = 0;
  string boardKind = "flat";
  int i = 1;
  for (; i < argc; i++) {
    string a = argv[i];
    if (a == "--board") { boardKind = argv[++i]; W = atoi(argv[++i]); H = atoi(argv[++i]); WRAP = (boardKind == "cyl"); }
    else if (a == "--fz") { lo = atoi(argv[++i]); hi = atoi(argv[++i]); }
    else if (a == "--safe") SAFE = 1;
    else if (a == "--noep") EPON = 0;
    else if (a == "--moves") SHOWMOVES = 1;
    else if (a == "pos" || a == "enum") { mode = a; i++; break; }
    else { fprintf(stderr, "bad arg %s\n", a.c_str()); return 1; }
  }
  if (hi < 0) hi = W - 1;
  for (int f = 0; f < 16; f++) FZ[f] = (f >= lo && f <= hi);
  initGeom();
  for (; i < argc; i++) {
    string a = argv[i];
    if (a == "--f") Fp = atoi(argv[++i]);
    else if (a == "--wmax") wmax = atoi(argv[++i]);
    else if (a == "--wmin") wmin = atoi(argv[++i]);
    else if (a == "--bmax") bmax = atoi(argv[++i]);
    else if (a == "--bmin") bmin = atoi(argv[++i]);
    else if (a == "--bfiles") { blo = atoi(argv[++i]); bhi = atoi(argv[++i]); }
    else if (a == "--ex") nex = atoi(argv[++i]);
    else if (a == "--ep") withEp = 1;
    else { fprintf(stderr, "bad arg %s\n", a.c_str()); return 1; }
  }
  if (mode == "pos") {
    char line[512];
    while (fgets(line, sizeof line, stdin)) {
      Pos p; string err;
      // allow trailing " | ..." comments
      char* bar = strchr(line, '|'); if (bar) *bar = 0;
      if (!parsePos(line, p, err)) { printf("X %s\n", line); continue; }
      if (!validState(p.wp, p.bp, p.ep, p.epc, p.stm, p.wk, p.bk)) { printf("%s | ILLEGAL\n", posStr(p).c_str()); continue; }
      uint8_t v = valOf(p);
      if (v == INF) printf("%s | no-win\n", posStr(p).c_str()); else printf("%s | WHITE-WINS T=%d\n", posStr(p).c_str(), (int)v);
      if (v != INF) printPV(p, 40);
      if (SHOWMOVES) {
        vector<Mv> mv; gen(p, mv, true);
        for (auto& m : mv) {
          string r;
          if (m.kind == 1) r = "promotes and wins (T=1)"; else if (m.kind == 2) r = "terminal, no White win";
          else { uint8_t w = valOf(m.p); r = (w == INF) ? "no White win" : "White wins, T=" + to_string((int)w) + " more White moves"; }
          printf("   move %-14s -> %s\n", m.d.c_str(), r.c_str());
        }
      }
    }
    fprintf(stderr, "layers=%zu\n", memo.size());
    return 0;
  }
  // enumeration of roots: White pawns on file Fp only (ranks 2..H-1), Black pawns on files blo..bhi, ranks 2..H-1 (idx 1..H-2).
  if (Fp < 0) Fp = (lo + hi) / 2;
  if (blo < 0) { blo = lo; bhi = hi; }
  vector<int> wsq, bsq;
  for (int r = 1; r <= H - 2; r++) wsq.push_back(r * W + Fp);
  for (int f = blo; f <= bhi; f++) for (int r = 1; r <= H - 2; r++) bsq.push_back(r * W + f);
  long roots = 0, wins = 0, nprint = 0;
  long rootsBy[3] = {0, 0, 0}, winsBy[3] = {0, 0, 0};   // by number of s-bar pawns attacked by an s pawn: 0, 1, >=2
  long rootsNear = 0, winsNear = 0;                     // roots with an s pawn on f+-1 (the LOOPY hypothesis fails)
  long viol = 0;
  int nw = wsq.size(), nb = bsq.size();
  for (u64 wm = 1; wm < (1ULL << nw); wm++) {
    int pw = __builtin_popcountll(wm); if (pw < wmin || pw > wmax) continue;
    u64 wp = 0; int front = -1;
    for (int j = 0; j < nw; j++) if (wm >> j & 1) { wp |= bit(wsq[j]); front = rankOf(wsq[j]); }
    for (u64 bm = 0; bm < (1ULL << nb); bm++) {
      int pb = __builtin_popcountll(bm); if (pb < bmin || pb > bmax) continue;
      u64 bp = 0; bool nearPawn = false;
      for (int j = 0; j < nb; j++) if (bm >> j & 1) {
        bp |= bit(bsq[j]);
        int f = fileOf(bsq[j]);
        int d = f - Fp; if (WRAP) { d = ((d % W) + W) % W; if (d > W / 2) d -= W; }
        if (d == 1 || d == -1 || (WRAP && W == 2 && f != Fp)) nearPawn = true;
      }
      if (wp & bp) continue;
      int att = 0;
      for (int q = 0; q < N; q++) if ((wp & bit(q)) && (attBy[1][q] & bp)) att++;
      int cls = att >= 2 ? 2 : att;
      // roots without and (with --ep) with an e.p. right created by a White double step to rank 4 (idx 3) on file f
      for (int variant = 0; variant < 1 + (withEp ? 1 : 0); variant++) {
        int ep = -1, epc = -1;
        if (variant == 1) {
          int t2 = 3 * W + Fp, t1 = 2 * W + Fp, org = 1 * W + Fp;
          if (H < 6 || !(wp & bit(t2)) || (wp & (bit(t1) | bit(org))) || (bp & (bit(t1) | bit(org)))) continue;
          // some black pawn must be able to capture e.p.
          bool can = false;
          for (int df = -1; df <= 1; df += 2) { int a = stepsq(t2, df, 0); if (a >= 0 && (bp & bit(a))) can = true; }
          if (!can) continue;
          ep = t1; epc = 0;
        }
        Layer* L = solveLayer(wp, bp, ep, epc);
        for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) {
          if (fileOf(bk) != Fp || rankOf(bk) <= front) continue;
          int id = sid(1, wk, bk);
          uint8_t v = L->R[id];
          if (v == INV) continue;
          roots++; rootsBy[cls]++; if (nearPawn) rootsNear++;
          if (v != INF) {
            wins++; winsBy[cls]++; if (nearPawn) winsNear++;
            Pos p{wp, bp, ep, epc, wk, bk, 1};
            if (cls <= 1) { viol++; printf("VIOLATION (<=1 attacked pawn but White wins) T=%d %s\n", (int)v, posStr(p).c_str()); printPV(p, 40); }
            else if (nprint < nex) { printf("WIN T=%d %s\n", (int)v, posStr(p).c_str()); printPV(p, 40); nprint++; }
          }
        }
      }
    }
  }
  printf("SUMMARY board=%s:%dx%d FZ=%d..%d f=%d wmax=%d bmax=%d safe=%d ep=%d | roots=%ld wins=%ld | attacked s-bar pawns 0: %ld roots %ld wins; 1: %ld roots %ld wins; >=2: %ld roots %ld wins | s pawn on f+-1: %ld roots %ld wins | VIOLATIONS(<=1 attacked, White wins)=%ld | layers=%zu\n",
         boardKind.c_str(), W, H, lo, hi, Fp, wmax, bmax, SAFE, withEp, roots, wins, rootsBy[0], winsBy[0], rootsBy[1], winsBy[1], rootsBy[2], winsBy[2], rootsNear, winsNear, viol, memo.size());
  return 0;
}

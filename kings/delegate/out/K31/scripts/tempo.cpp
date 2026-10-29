// K31: tempo profiles and sums of +-1 roots.  Built on the referee's lk.cpp (K20/verify), included unchanged.
//   tempo profile <board> <pairs> <margin|free> <N>
//       for every root x (full pawn set): outcomes of x + (-n) and x + n, n = 0..N (integer reservoirs), histogram of the leads
//         Lw(x) = max n such that White wins x + (-n) with Black to move   (-1: none)   [White's lead when moving second]
//         Fw(x) = max n such that White wins x + (-n) with White to move   (-1: none)   [moving first]
//         Lb(x) = max n such that Black wins x + (+n) with White to move                [Black's lead when moving second]
//         Fb(x) = max n such that Black wins x + (+n) with Black to move
//   tempo pairs <board> <pairs> <margin|free> <N>
//       all ordered pairs (x, y) of roots named +1 or -1 by B34: outcome pair of x + y + c for every integer c = -N..N,
//       against the reference integers (sign x + sign y) + c.  Also x + (integer 1/-1) + c.
#define main lk_main
#include "../../K20/verify/lk.cpp"
#undef main

struct IntGame { Game g; int N; int node(int k) const { return k + N; } };
static IntGame buildInt(int N) {
  IntGame I; I.N = N; for (int k = -N; k <= N; k++) I.g.add();
  for (int k = 1; k <= N; k++) I.g.L[I.node(k)].push_back(I.node(k - 1));
  for (int k = -1; k >= -N; k--) I.g.R[I.node(k)].push_back(I.node(k + 1));
  return I;
}

// k-fold sum solver (implicit product), as lk.cpp's solvePlayer but for any number of components.
struct Multi {
  vector<const Game*> C; vector<size_t> mul; size_t NS = 0;
  vector<char> ww, bb;
  size_t idx(const vector<int>& v, int s) const { size_t x = 0; for (size_t i = 0; i < C.size(); i++) x += mul[i] * v[i]; return x * 2 + s; }
  void solvePlayer(int player, vector<char>& win) {
    size_t K = C.size();
    mul.assign(K, 1); NS = 1; for (size_t i = 0; i < K; i++) { mul[i] = NS; NS *= C[i]->n; }
    size_t tot = NS * 2; win.assign(tot, 0);
    vector<vector<vector<int>>> rev(2 * K);   // rev[m*K+i][t] = sources a of component i with t in opt_m(a)
    for (int m = 0; m < 2; m++) for (size_t i = 0; i < K; i++) {
      auto& rv = rev[m * K + i]; rv.assign(C[i]->n, {});
      const auto& o = m == 0 ? C[i]->L : C[i]->R;
      for (int a = 0; a < C[i]->n; a++) for (int t : o[a]) if (t >= 0) rv[t].push_back(a);
    }
    int winT = player == 0 ? TP : TM, loseT = player == 0 ? TM : TP;
    vector<int> cnt(tot, 0); vector<size_t> q;
    vector<int> v(K);
    for (size_t x = 0; x < NS; x++) {
      size_t r = x; for (size_t i = 0; i < K; i++) { v[i] = r % C[i]->n; r /= C[i]->n; }
      for (int s = 0; s < 2; s++) {
        size_t id = x * 2 + s;
        if (s == player) {
          bool hw = false;
          for (size_t i = 0; i < K && !hw; i++) for (int t : (s == 0 ? C[i]->L : C[i]->R)[v[i]]) if (t == winT) { hw = true; break; }
          if (hw) { win[id] = 1; q.push_back(id); }
        } else {
          int c = 0; bool bad = false;
          for (size_t i = 0; i < K; i++) for (int t : (s == 0 ? C[i]->L : C[i]->R)[v[i]]) { if (t == winT) continue; c++; if (t == loseT) bad = true; }
          cnt[id] = bad ? 1000000 : c;
          if (!bad && c == 0) { win[id] = 1; q.push_back(id); }
        }
      }
    }
    size_t head = 0;
    while (head < q.size()) {
      size_t id = q[head++]; int s = id & 1; size_t x = id >> 1; int m = 1 - s;
      size_t r = x; for (size_t i = 0; i < K; i++) { v[i] = r % C[i]->n; r /= C[i]->n; }
      for (size_t i = 0; i < K; i++) for (int pa : rev[m * K + i][v[i]]) {
        size_t p = (x - mul[i] * v[i] + mul[i] * pa) * 2 + m;
        if (win[p]) continue;
        if (m == player) { win[p] = 1; q.push_back(p); }
        else if (--cnt[p] == 0) { win[p] = 1; q.push_back(p); }
      }
    }
  }
  void solve() { solvePlayer(0, ww); solvePlayer(1, bb); for (size_t i = 0; i < ww.size(); i++) if (ww[i] && bb[i]) { fprintf(stderr, "BOTH\n"); exit(2); } }
  int res(const vector<int>& v, int s) const { size_t i = idx(v, s); return ww[i] ? 2 : (bb[i] ? 0 : 1); }  // 0 L, 1 D, 2 W (White's view)
};

int main(int argc, char** argv) {
  string mode = argv[1];
  if (mode != "profile" && mode != "pairs") { fprintf(stderr, "mode\n"); return 1; }
  Cfg cf = parseCfg(argv[2], argv[3], argv[4]);
  int N = atoi(argv[5]);
  LK lk; lk.build(cf);
  Battery B = buildBattery();
  vector<int> roots = lk.roots();
  vector<vector<uint8_t>> sig(roots.size());
  signatures(lk, B, roots, sig);
  map<vector<uint8_t>, string> refs;
  for (auto& nm : B.games) { vector<uint8_t> s = refSig(B.g, nm.start, B); if (!refs.count(s)) refs[s] = nm.name; else refs[s] += "=" + nm.name; }
  vector<string> label(roots.size());
  for (size_t k = 0; k < roots.size(); k++) { auto it = refs.find(sig[k]); label[k] = it == refs.end() ? "other" : it->second; size_t p = label[k].find('='); if (p != string::npos) label[k] = label[k].substr(0, p); }
  IntGame I = buildInt(N);
  if (mode == "profile") {
    Multi M; M.C = {&lk.g, &I.g}; M.solve();
    map<string, long> hist; map<string, string> ex; map<string, map<string, long>> bylabel;
    long total = 0;
    for (size_t k = 0; k < roots.size(); k++) {
      int Lw = -1, Fw = -1, Lb = -1, Fb = -1;
      for (int n = 0; n <= N; n++) {
        if (M.res({roots[k], I.node(-n)}, 1) == 2) Lw = n;   // White wins, Black to move, Black has n spare moves
        if (M.res({roots[k], I.node(-n)}, 0) == 2) Fw = n;
        if (M.res({roots[k], I.node(n)}, 0) == 0) Lb = n;    // Black wins, White to move, White has n spare
        if (M.res({roots[k], I.node(n)}, 1) == 0) Fb = n;
      }
      char buf[100]; snprintf(buf, sizeof buf, "Lw=%d Fw=%d Lb=%d Fb=%d", Lw, Fw, Lb, Fb);
      hist[buf]++; bylabel[buf][label[k]]++; total++;
      if (!ex.count(buf)) ex[buf] = lk.rootText(roots[k]);
    }
    printf("PROFILE %s %s %s N=%d roots %ld\n", argv[2], argv[3], argv[4], N, total);
    for (auto& kv : hist) { printf("  %-34s %8ld  e.g. [%s]  labels:", kv.first.c_str(), kv.second, ex[kv.first].c_str()); for (auto& l : bylabel[kv.first]) printf(" %s=%ld", l.first.c_str(), l.second); printf("\n"); }
  } else {
    vector<int> pm;   // roots named +1 or -1
    for (size_t k = 0; k < roots.size(); k++) if (label[k] == "+1" || label[k] == "-1") pm.push_back(k);
    // reference: integer sums (3 integer components)
    Multi R; R.C = {&I.g, &I.g, &I.g}; R.solve();
    // x + y + c : components (LK, LK, int): memory nA*nA*(2N+1)*2
    long checked = 0, mism = 0; map<string, long> mm; map<string, array<long, 3>> sumout;
    // restrict the first LK component to the nodes reachable (all), use the full lk.g twice.
    vector<int> nid; Game sub = subgame(lk.g, roots, nid);
    Multi P; P.C = {&sub, &sub, &I.g}; P.solve();
    Multi Q; Q.C = {&sub, &I.g, &I.g}; Q.solve();
    string firstbad;
    for (int a : pm) for (int b : pm) {
      int va = label[a] == "+1" ? 1 : -1, vb = label[b] == "+1" ? 1 : -1;
      for (int c = -N; c <= N; c++) for (int s = 0; s < 2; s++) {
        int got = P.res({nid[roots[a]], nid[roots[b]], I.node(c)}, s);
        int ref = R.res({I.node(va), I.node(vb), I.node(c)}, s);
        checked++; if (got != ref) { mism++; mm["x+y"]++; if (firstbad.empty()) firstbad = lk.rootText(roots[a]) + " + " + lk.rootText(roots[b]) + " + " + to_string(c); }
      }
      // outcome with no context, as exhibited
      char key[40]; snprintf(key, sizeof key, "%+d%+d s0=%d s1=%d", va, vb, P.res({nid[roots[a]], nid[roots[b]], I.node(0)}, 0), P.res({nid[roots[a]], nid[roots[b]], I.node(0)}, 1));
      sumout[key][0]++;
    }
    long c2 = 0, m2 = 0;
    for (int a : pm) for (int v1 : {1, -1}) {
      int va = label[a] == "+1" ? 1 : -1;
      for (int c = -N; c <= N; c++) for (int s = 0; s < 2; s++) {
        int got = Q.res({nid[roots[a]], I.node(v1), I.node(c)}, s);
        int ref = R.res({I.node(va), I.node(v1), I.node(c)}, s);
        c2++; if (got != ref) { m2++; if (firstbad.empty()) firstbad = lk.rootText(roots[a]) + " + int " + to_string(v1) + " + " + to_string(c); }
      }
    }
    printf("PAIRS %s %s %s N=%d: roots %zu, +-1 roots %zu, x+y+c outcomes checked %ld mismatches %ld; x+(+-1 integer)+c checked %ld mismatches %ld\n", argv[2], argv[3], argv[4], N, roots.size(), pm.size(), checked, mism, c2, m2);
    for (auto& kv : sumout) printf("  sum outcome (White to move s0, Black to move s1; 0 L, 1 D, 2 W) %s : %ld ordered pairs\n", kv.first.c_str(), kv.second[0]);
    if (!firstbad.empty()) printf("  first mismatch %s\n", firstbad.c_str());
  }
  return 0;
}

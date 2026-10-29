// K31 task 4 check: replays a line (list of states "root text|c|s") in the referee's lk.cpp game LK + integer reservoir.
//   linechk <board> <pairs> <N> <linefile>
// each state line: "<root text>|<c>|<s>"  (s = 0 White to move, 1 Black to move; c > 0 White spare moves, c < 0 Black spare moves)
// last line may be "EVENT|+" or "EVENT|-": the mover captures and the terminal must be among its options.
// prints for every state the outcome (W White forces the event, L Black forces it, D neither) and whether the step to
// the next state is a legal move of LK (king step with c unchanged, or a pass that spends one unit of the mover's reserve).
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
// two-component sum solver: reuse lk.cpp's solveSum (outcome of A+B with s to move: 0 L, 1 D, 2 W, White's view)
int main(int argc, char** argv) {
  Cfg cf = parseCfg(argv[1], argv[2], "free");
  int N = atoi(argv[3]);
  LK lk; lk.build(cf);
  IntGame I = buildInt(N);
  SumRes sr = solveSum(lk.g, I.g);
  auto res = [&](int a, int c, int s) { return sr.w[((size_t)a * sr.nB + I.node(c)) * 2 + s]; };
  FILE* f = fopen(argv[4], "r"); char buf[512];
  vector<tuple<string,int,int,int>> st;   // text, c, s, node
  string last;
  while (fgets(buf, sizeof buf, f)) {
    string l = buf; while (!l.empty() && (l.back() == '\n' || l.back() == '\r')) l.pop_back(); if (l.empty()) continue;
    size_t p1 = l.find('|'); string t = l.substr(0, p1);
    if (t == "EVENT") { last = l.substr(p1 + 1); continue; }
    size_t p2 = l.find('|', p1 + 1); int c = atoi(l.substr(p1 + 1, p2 - p1 - 1).c_str()); int s = atoi(l.c_str() + p2 + 1);
    int node = lk.parseRoot(t); if (node < 0) { printf("ILLEGAL position %s\n", t.c_str()); return 1; }
    st.emplace_back(t, c, s, node);
  }
  static const char* O = "LDW"; int bad = 0;
  for (size_t i = 0; i < st.size(); i++) {
    auto& [t, c, s, node] = st[i];
    printf("%2zu  %-28s reserve %+d  %s to move  outcome %c", i, lk.rootText(node).c_str(), c, s ? "Black" : "White", O[res(node, c, s)]);
    if (i + 1 < st.size()) {
      auto& [t2, c2, s2, node2] = st[i + 1];
      bool ok = false;
      if (s2 == 1 - s) {
        if (node2 != node && c2 == c) { for (int x : (s == 0 ? lk.g.L : lk.g.R)[node]) if (x == node2) ok = true; }
        else if (node2 == node) ok = (s == 0) ? (c > 0 && c2 == c - 1) : (c < 0 && c2 == c + 1);
      }
      printf("   step %s", ok ? "legal" : "ILLEGAL"); if (!ok) bad++;
    } else if (!last.empty()) {
      bool ok = false; int want = last == "+" ? TP : TM;
      for (int x : (s == 0 ? lk.g.L : lk.g.R)[node]) if (x == want) ok = true;
      printf("   final capture event %s: %s", last.c_str(), ok ? "available to the mover" : "NOT AVAILABLE"); if (!ok) bad++;
    }
    printf("\n");
  }
  printf("%s\n", bad ? "LINE CHECK FAILED" : "LINE CHECK OK: every step is a legal move of LK");
  return bad != 0;
}

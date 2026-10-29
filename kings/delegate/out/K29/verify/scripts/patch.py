import re
s = open('me/src/ref3d.cpp').read()
# 1. depth memo + wrapper: replace 'static Table compute' ... add depth after fixpoint
s = s.replace('static const Table& solve(const Key& k);',
'''static const Table& solve(const Key& k);
typedef vector<int16_t> DTable; // -1 unknown/none; plies to the end (mate = 0 for the loser, promotion: winner depth 1)
static unordered_map<Key, DTable, KH> memoD;
''')
# after 'return tab;' of compute: compute depth.  Replace the end of compute
s = s.replace('''      if (win) { tab[s.idx] = 1; ch = true; }
      else if (allw) { tab[s.idx] = 2; ch = true; }
    }
  }
  return tab;
}''','''      if (win) { tab[s.idx] = 1; ch = true; }
      else if (allw) { tab[s.idx] = 2; ch = true; }
    }
  }
  // ---- depth (own addition, level-synchronous) ----
  {
    DTable dep(2 * N * N, -1);
    vector<vector<Move>> mvs(2 * N * N);
    vector<int> live;
    for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) {
      int idx = (stm * N + wk) * N + bk;
      if (tab[idx] != 1 && tab[idx] != 2) continue;
      genMoves(stm, wk, bk, k.wp, k.bp, k.ep, mvs[idx]);
      if (mvs[idx].empty()) { dep[idx] = 0; continue; } // mated
      live.push_back(idx);
    }
    // child lookup: returns table value (0 draw,1 mover wins,2 mover loses) and depth
    auto child = [&](int stm, const Move& m, int& val, int& d) {
      if (m.kind == 0) { val = 2; d = 0; return; }       // promotion: the child "loses" at depth 0
      if (m.kind == 1) { val = 1; d = 0; return; }
      bool same = (m.kind == 3 && m.nk.wp == k.wp && m.nk.bp == k.bp && k.ep == -1);
      int ci = ((1 - stm) * N + m.nwk) * N + m.nbk;
      if (same) { val = tab[ci]; d = dep[ci]; return; }
      const Table& ct = solve(m.nk); auto it = memoD.find(m.nk);
      val = ct[ci]; d = it->second[ci];
    };
    for (int n = 1; n < 400; n++) {
      bool any = false; vector<pair<int,int>> assign;
      for (int idx : live) {
        if (dep[idx] >= 0) continue;
        int stm = idx / (N * N);
        if (tab[idx] == 1) {
          int best = 1 << 20;
          for (auto& m : mvs[idx]) { int v, d; child(stm, m, v, d); if (v == 2 && d >= 0 && d <= n - 1) best = min(best, d); }
          if (best < (1 << 20)) assign.push_back({idx, 1 + best});
        } else {
          int mx = -1; bool ok = true;
          for (auto& m : mvs[idx]) { int v, d; child(stm, m, v, d); if (m.kind == 1) continue; if (v != 1 || d < 0 || d > n - 1) { ok = false; break; } mx = max(mx, d); }
          if (ok) assign.push_back({idx, 1 + mx});
        }
      }
      for (auto& a : assign) { dep[a.first] = a.second; any = true; }
      if (!any) break;
    }
    memoD[k] = std::move(dep);
  }
  return tab;
}''')
# print depth in --moves output and results
s = s.replace('''    printf("%s | %c", line.c_str(), res);''','''    printf("%s | %c", line.c_str(), res);
    if (res != 'X') { solve(Key{wp, bp, ep}); int dd = memoD[Key{wp, bp, ep}][(stm * N + wk) * N + bk]; printf(" d=%d", dd); }''')
s = s.replace('''        printf(" %s:%c", d.c_str(), v);''','''        int dm = -1;
        if (m.kind == 0) dm = 0; else { solve(m.nk); dm = memoD[m.nk][((1 - stm) * N + m.nwk) * N + m.nbk]; }
        printf(" %s:%c:%d", d.c_str(), v, dm);''')
open('me/src/ref3d.cpp','w').write(s)

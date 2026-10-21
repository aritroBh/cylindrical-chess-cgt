#!/usr/bin/env python3
"""Adds MY_PATH (on top of make_src.py's MY_COUNT): print the root-to-node move path at every
Step-15 block entry (first 40 per search). Verifier diagnostic for the cgt148 position."""
import sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text()
old = """#ifdef MY_COUNT
            myc_s15++;
#endif
"""
new = old + """#ifdef MY_PATH
            if (myc_s15 <= 40)
            {
                std::string path;
                for (int k = ss->ply; k >= 1; --k)
                    path += UCIEngine::move((ss - k)->currentMove, false) + " ";
                sync_cout << "info string s15path ply " << ss->ply << " depth " << depth << " root "
                          << rootDepth << " path " << path << "move " << UCIEngine::move(move, false)
                          << sync_endl;
            }
#endif
"""
assert s.count(old) == 1
p.write_text(s.replace(old, new)); print("ok")

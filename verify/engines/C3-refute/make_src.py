#!/usr/bin/env python3
"""Independent (verifier-written) instrumentation of Stockfish 19 search.cpp for claim C3.

Copies nothing itself; expects verify/engines/C3-refute/sf/src to be a copy of the pristine sf_19 src
(see build.sh). Rewrites sf/src/search.cpp in place with #ifdef-guarded edits:
  MY_NONMP  : Step 10 (null move) guard replaced by `false`
  MY_NOS15  : Step 15 (shallow pruning) guard replaced by `false`
  MY_COUNT  : counters, printed as `info string myc ...` at the end of every completed iteration:
     npmnode = main-search node entries with non_pawn_material(side to move) > 0
     npmq    = qsearch node entries with non_pawn_material(side to move) > 0
     nmpexec = times the null-move block is entered (null move actually searched)
     nmpblk  = times every NMP condition except non_pawn_material(us) holds
     s15     = move-loop iterations entering the Step-15 block
     s15blk  = move-loop iterations where !rootNode && !is_loss(bestValue) hold but NPM(us) == 0
Without any macro the file compiles to the same code as pristine sf_19.
"""
import sys
from pathlib import Path

p = Path(sys.argv[1])
s = p.read_text()


def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)


rep("namespace Stockfish {\n",
    "namespace Stockfish {\n#ifdef MY_COUNT\nuint64_t myc_npmnode = 0, myc_npmq = 0, myc_nmpexec = 0, "
    "myc_nmpblk = 0, myc_s15 = 0, myc_s15blk = 0;\n#endif\n")

rep("""    if (cutNode && ss->staticEval >= beta - 13 * depth - 47 * improving + 365 && !excludedMove
        && pos.non_pawn_material(us) && ss->ply >= nmpMinPly && beta >= -2000)
    {
""", """#ifdef MY_COUNT
    if (cutNode && ss->staticEval >= beta - 13 * depth - 47 * improving + 365 && !excludedMove
        && !pos.non_pawn_material(us) && ss->ply >= nmpMinPly && beta >= -2000)
        myc_nmpblk++;
#endif
#ifdef MY_NONMP
    if (false)
#else
    if (cutNode && ss->staticEval >= beta - 13 * depth - 47 * improving + 365 && !excludedMove
        && pos.non_pawn_material(us) && ss->ply >= nmpMinPly && beta >= -2000)
#endif
    {
#ifdef MY_COUNT
        myc_nmpexec++;
#endif
""")

rep("""        if (!rootNode && pos.non_pawn_material(us) && !is_loss(bestValue))
        {
""", """#ifdef MY_COUNT
        if (!rootNode && !pos.non_pawn_material(us) && !is_loss(bestValue))
            myc_s15blk++;
#endif
#ifdef MY_NOS15
        if (false)
#else
        if (!rootNode && pos.non_pawn_material(us) && !is_loss(bestValue))
#endif
        {
#ifdef MY_COUNT
            myc_s15++;
#endif
""")

rep("    Color us      = pos.side_to_move();\n    ss->moveCount = 0;\n",
    "    Color us      = pos.side_to_move();\n    ss->moveCount = 0;\n"
    "#ifdef MY_COUNT\n    if (pos.non_pawn_material(us))\n        myc_npmnode++;\n#endif\n")

rep("""    static_assert(nodeType != Root);
    constexpr bool PvNode = nodeType == PV;
""", """    static_assert(nodeType != Root);
    constexpr bool PvNode = nodeType == PV;
#ifdef MY_COUNT
    if (pos.non_pawn_material(pos.side_to_move()))
        myc_npmq++;
#endif
""")

rep("""bool Search::Worker::iterative_deepening() {
""", """bool Search::Worker::iterative_deepening() {
#ifdef MY_COUNT
    myc_npmnode = myc_npmq = myc_nmpexec = myc_nmpblk = myc_s15 = myc_s15blk = 0;
#endif
""")

rep("""        const bool forgottenMate = lastBestMoveScore != -VALUE_INFINITE
""", """#ifdef MY_COUNT
        if (mainThread && !threads.stop)
            sync_cout << "info string myc depth " << rootDepth << " npmnode " << myc_npmnode << " npmq "
                      << myc_npmq << " nmpexec " << myc_nmpexec << " nmpblk " << myc_nmpblk << " s15 "
                      << myc_s15 << " s15blk " << myc_s15blk << sync_endl;
#endif
        const bool forgottenMate = lastBestMoveScore != -VALUE_INFINITE
""")

p.write_text(s)
print("patched", p)

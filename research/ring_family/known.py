import sys
KNOWN = {
 3: ["W: a2 a3 b2 / B: b7 c6 c7", "W: a2 a5 b2 b4 c2 / B: a7 b5 b6 c4 c7"],
 4: ["W: a4 b2 c2 / B: b6 c5 d6 d7"],
 5: """W: a2 a3 b3 d3 / B: a7 c5 e5 e6
W: a2 a3 c3 d2 / B: a4 b5 d5 e5
W: a2 a3 c3 d2 / B: b5 b6 d5 e5
W: a2 b2 c2 d2 / B: b5 b7 d6 e4
W: a2 b2 c2 d2 / B: b6 b7 d5 e4
W: a3 a4 c4 e2 / B: b6 d6 e6 e7
W: a3 b3 c2 e2 / B: a6 c5 d5 e3
W: a4 b3 c2 d2 / B: a7 b6 c7 e4
W: a4 b4 d3 d4 / B: a7 c6 c7 e6
W: a5 b2 c3 d2 / B: b5 c6 d7 e7
W: a5 b4 c4 e4 / B: a6 a7 c7 d6
W: a5 b4 d2 d3 / B: b7 c7 d7 e7
W: a5 c2 c4 e3 / B: b7 c7 d7 e7
W: a6 b4 c4 e3 / B: a7 c7 d6 e6""".split("\n"),
 6: ["W: a4 c4 d2 e2 / B: b6 b7 d6 e5 f6", "W: a5 b3 d4 e2 / B: c6 d7 e6 e7 f7", "W: a5 c4 d4 e3 / B: b7 d7 e4 e6 f7"],
 7: """W: a2 a3 c2 d3 f2 / B: b5 c6 e5 e6 g5
W: a2 a3 c3 e2 f2 / B: b5 d5 d6 f6 g5
W: a2 a3 c3 e3 f2 / B: a4 b5 d5 f5 g5
W: a2 a3 c3 e3 f2 / B: b5 d5 d6 f5 g5
W: a3 a4 c3 d3 f3 / B: b6 b7 d7 e5 g6
W: a3 a4 c4 e4 f3 / B: b6 d6 d7 f7 g7
W: a3 a4 c4 e4 f3 / B: b7 d6 d7 f7 g6
W: a3 b2 c2 d3 f2 / B: b5 b7 c5 e6 g5
W: a2 a4 b3 d2 g3 / B: b6 b7 c6 e4 f7
W: a2 a4 b3 d4 e2 / B: b5 c6 c7 f4 g6
W: a2 a4 b3 d4 f2 / B: b5 c6 c7 e4 g6
W: a2 a5 c4 e2 f2 / B: a7 b4 d6 e5 g7
W: a2 a5 c4 e2 f2 / B: a7 b4 d7 e5 g7
W: a2 a5 c5 e2 f2 / B: a7 b4 d7 e5 g7
W: a2 a6 b2 d3 f2 / B: a7 c7 e5 e6 g4
W: a2 a6 b3 e3 f2 / B: a3 a7 c7 d6 g6""".split("\n"),
}

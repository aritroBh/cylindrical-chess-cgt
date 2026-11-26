# Lemma B in first-promotion chess

**PROVED.** Black wins all 46 starts in the required set S.  
**PROVED.** On the full board Black wins 54 starts with γ on c2, 54 with γ on c3, and 53 with γ on c4.  
**PROVED.** The remaining start, White Kb4 and c4, draws. Only 1.c5+ holds.  
**PROVED.** The win proof is a finite case proof by descending variation numbers. The draw uses a king-and-pawn blockade and a closed list of defensive replies.  
**COMPUTED.** I used a search to discover the variations. A separate move enumerator checks the printed proof. The proof below can be checked with a board and the two variation tables.

## Black’s first reply

**PROVED.** Look at the board *after* White’s first move. Call the White king’s square x. No Black pawn can have been taken. Both are adjacent to Kb6. A White king move to d5 is illegal because c6 attacks it. A White pawn push with the king already on d5 leaves that attack in place. Thus d5 is included as an initial square, but never as x.

| White pawn after moving or waiting | White king x | Black plays |
|---|---|---|
| c2 or c3 | d6 | …Kb5 |
| c2 or c3 | all other possible x | …c5 |
| c4 | d4 or d6 | …Ka6 |
| c4 | d7 or e4, e5, e6, e7 | …Kc5 |
| c4 | all other possible x | …c5 |
| c5 | d4 or d6 | …Kb5, followed by …Kxc5 |
| c5 | b4 | the drawing case below |
| c5 | all other possible x | …Kxc5 |

**PROVED.** With a White pawn on c5 the last move must have been c4–c5+. Of the possible kings protecting c5, b5 and c6 were adjacent to the original Black king, c4 was occupied, and d5 was in check. That leaves b4, d4 and d6. Against d4 or d6 Black steps out of check on b5. The c-pawns now block one another. White must move the king. Black’s king takes away c4 and c6, while pc6 takes away d5. White therefore has to give up its defence of c5. Against b4 the same …Kb5 is illegal. This is the distinction that singles out the exception.

**PROVED.** The two king detours when the White pawn is on c4 serve different purposes.

- Against e4–e7 or d7, …Kc5 blocks c4 with the king. White has only a king move. List its destinations by putting the White king on each of those five squares and removing c4, Black’s king neighbourhood, and the Black pawn attacks. The only remaining destination defending c4 is **d3**. There Black plays …Kb4 and attacks c4 from the side. Every other destination permits …Kxc4. These are Black cases 448, 447 and 444.
- Against d4 or d6, …Ka6 keeps the b-pawn on its home square. If White plays Kc5, Black approaches by …Ka5. Every other king move allows …c5. If White plays c5 instead, …Kb5 again wins the pawn by the preceding argument. Case 451 lists the three continuations. For example, from d4 the legal king destinations are c3, d3, e3, e4, c5 and e5. From d6 they are c5, e5, e6, c7, d7 and e7. Only c5 blocks the pawn push.

**PROVED.** One apparent counterplay after …Kxc5 is Kxb7. With White Kb7, Black Kc5 and pc6, play …Kb5. The Black king protects c6 and bars a6, b6 and c6. White must stay on rank 7 or 8. Now …c5 wins by straight pushes. On White’s first turn against the running pawn the king is at least two ranks behind it. After every subsequent pair of turns that gap is at least as large. The c-file is clear. Until promotion White starts each turn on rank 4 or higher. A step straight up is safe, or a sideways step on rank 8. On ranks 4 through 6 every legal White king is already outside files a through c because of Kb5. This closes the capture branch of case 414 directly.

**PROVED.** A locked c-file also explains when Black spends the b-pawn tempo. With White Kb3, Pc4, one line from the required set is **1.Ka2 c5 2.Kb2 Kc6 3.Kb1 Kd6 4.Kc2 Ke5 5.Kd3 Kf4**. The White pawn on c4 prevents …Kd5, while the black pawn on c5 prevents Kd4. Going around via f4 takes e3 and e4 from White. White’s complete list is now Kc2, Kd2, Ke2 and Kc3. Black answers all four with **…Ke4**. The pawn is still locked, and after any White king move Black plays **…b6**. This is the sequence B388 → B380 → B376. The alternative when the White king is too far away occurs in B378. With Kc6 behind pc5, Black can play **…b5** in one move. After cxb5, …Kxb5 leaves the c-pawn. After any king move, …b4 gets the b-pawn past c4. B102 and B260 close those two branches.

## How the remaining winning variations are proved

**PROVED.** Table B gives Black’s strategy after the opening and after each subsequent White defence. Each row asserts a win with **Black to move**. The section heading gives all the pawns. The King column gives the **Black** king, and Zone gives the **White** king. In Table D the roles of the kings are reversed and **White moves**. The same square notation is used in both tables.

- A range such as `c4–f8` is the whole closed rectangle with those opposite corners. Commas mean union. A leading `!` excludes the **whole** union. A star admits every eligible square.
- In a zone, discard occupied squares, squares within one king step of the listed king, and squares where the **other** king would already be in pawn check on the listed player’s turn. The listed king itself may be in check. An `ep` annotation gives the available en-passant landing square. An absent annotation means there is no available en-passant capture.
- Make the move under Play. In Replies, `K` means any **noncapturing** king step by the other player. A king capture has its own entry, such as `Kxb7`. Pawn replies give their destinations or captures. The numbers following an arrow cover that reply. Choose the row whose pieces and zone match the resulting board.
- `end→P` means the prescribed move promotes immediately. In Table D, `0` means Black has only its king and `F` means the blockade proved below applies **after the prescribed White move**, before Black replies. If F applies, no further row is needed.

**PROVED.** Here is the local board argument for the entries. For a king reply, take the one-square border around each possible enemy king location after Play, excluding the location itself. Remove friendly pieces, the prescribed player’s king and its neighbours, and its pawn attacks. Split off captures of enemy pawns. The remaining destinations lie in the zones of the cited rows under K. For a pawn reply the enemy king stays at its old square. Remove positions where the pawn path is blocked or the move leaves its king attacked, then use the cited zones for that pawn move. These set inclusions, with their source squares, move and target rows printed together, are the individual cases of the proof. No legal reply may be omitted, even a capture that costs the last pawn. In Table B every nonterminal row leaves White a legal move throughout its zone, and every arrow points to a **smaller** number. Induction from promotion therefore gives a finite Black win and rules out both repetition and stalemate.

**PROVED.** For an example of the induction away from the opening, take B70. White’s only man is Kb7, Black has Kc5 and pc6. After …Kb5 the legal replies are Ka7, Kc7, Ka8, Kb8 and Kc8. All five are in B69. In B69, …c5 leaves White’s king at least on rank 7 before it moves. Every king reply is in B48, whose excluded rectangle is a1–c3. The straight-push proof above also closes these two rows. At the other end of the table B1 consists of Kd2 escorting pc2. Black plays …c1, and White never gets a reply. In particular, the rule at promotion is the one in game P.

**PROVED.** The following are the entry rows after each first White move. Each K entry is a quiet king move. These destinations are exactly covered by the opening rule. For the c4 starting pawn the c5 entry here excludes the separately proved Kb4 draw.

| Initial γ | White’s move and Black’s entry rows |
|---|---|
| c2 | K → 481, 486 · c3 → 475, 480 · c4 → 445, 448, 451 |
| c3 | K → 475, 480 · c4 → 445, 448, 451 |
| c4 | K → 445, 448, 451 · c5 → 414, 417 |

## Why Kb4 and c4 draw

**PROVED, Black can prevent a White win.** Initially Ka3, Kb3, Kc3 and Ka4 all enter B445. The only other move is 1.c5+. Black can answer …Kc7 and thereafter keep both pawns fixed. Keep the king on a7, a8, b8, c8 or c7. All five squares guard b7, and b7 guards c6. White’s pawn is blocked and can never capture anything. From c7 the king can always go to c8 since a White king attacking c8 would already be next to c7. From c8 use c7 if available. If the White king bars it, the White king must be on rank 6 and b8 is free. The a-file works by reflection. From b8 at least one of a8 and c8 is free of attack, since no legal White king can attack both. The White pawn attacks neither. This gives Black an indefinite defence.

**PROVED, a blockade used by White.** Suppose Black has a single c-pawn on rank r and it is Black’s turn. White may also have a pawn on b6 or b7. In the following descriptions a subscript denotes a rank, so c(r−1) is immediately in front of the black pawn. Each of the following positions holds for White.

| Shape | White king | Black king |
|---|---|---|
| A, for 3 ≤ r ≤ 6 | b(r−2) | b(r), or reflect both kings to the d-file |
| B, for 3 ≤ r ≤ 6 | c(r−1) | anywhere legal |
| C, for 3 ≤ r ≤ 6 | c(r−2) | b(r+1), c(r+1) or d(r+1) |
| Last rank, r = 2 | c1 | b3 or d3 |

**PROVED.** In A, White holds direct opposition. If Black advances the pawn with check, step sideways onto the c-file immediately in front of it. This gives B for the new rank, or the last-rank case. If the Black king moves, it cannot penetrate rank r−1. Its legal destinations on the b-file side are a(r), a(r+1), b(r+1) and c(r+1). White can step to c(r−1) against each, giving B. Reflect this argument for the d-file.

**PROVED.** In B the pawn cannot move. After a king move, take the pawn if it is loose. A king that still guards it must be on b, c or d of rank r+1, since the White king excludes all the closer guarding squares. Step back along the c-file to c(r−2), giving C. In C an immediate pawn push loses the pawn to the White king. If the Black king comes to b(r) or d(r), take direct opposition on that file, giving A. Every other king move allows c(r−1), giving B. The stated White king steps never need b6 or b7. Checks by an extra White pawn can only reduce Black’s choices in these cases.

**PROVED.** In the last-rank case the pawn is blocked. A king move other than …Kc3 leaves c2 available for capture. After …Kc3 the bare White king is stalemated. If White has a b-pawn instead, b7–b8 promotes immediately from b7. From b6, play b7 and then b8. The king on c3 cannot reach the runner in time, and White’s king on c1 still blocks the black pawn. This proves the blockade, including the possible effect of White’s spare tempo.

**PROVED, White can prevent a Black win.** Play **1.c5+**. Black has exactly …Ka6, …Ka7 and …Kc7. Answer the two a-file moves by **Ka4**, and …Kc7 by **Kc4**. While the c-pawns are locked, White maintains the zones in D80–97. In particular, against either …b6 or …b5, play **cxb6**. Against the double push it is en passant. If the Black king wanders away to the east, White can instead approach via d6 and c7 and capture b7. D80–97 specify the waiting moves as well as the approach.

**PROVED.** For example, after 1.c5+ Ka6 2.Ka4 b5+ 3.cxb6 e.p. Kxb6, the precise move is **4.Kb4**. This is blockade A with r = 6. The same answer holds after 2…b6 3.cxb6 Kxb6. If Black declines to capture on b6, the b-pawn threatens to promote. D61 and D71 give the continuations for every king retreat and for …c5. This distinction matters because …c5 can give a check against a king on b4 or d4.

**PROVED.** Table D is a closed defensive strategy. At each row White makes the prescribed move. Every legal Black move then enters a cited White row, or White has already secured a promotion, a bare Black king or the proved blockade. No Black promotion occurs on a listed reply. Unlike the win proof, a cycle here is a successful defence because infinite play draws. Together with Black’s fixed-pawn defence, this proves the draw. Table B proves its uniqueness.

## Table B · Black to move

**PROVED by descending induction.** Read the numbered continuations within this table.

**White pawn - · Black pawns c2, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 1 | d2 | * | c1 | end→P |
| 2 | b3 | !c1,a1 | c1 | end→P |
| 3 | c4 | !a1–c3 | c1 | end→P |

**White pawn - · Black pawns c3, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 4 | d2 | a2–g8,a1,b1 | c2 | K→1 |
| 5 | c2 | a4–f8,f3,a2–a3 | Kd2 | K→4 |
| 6 | b3 | !d1,a1,b1 | c2 | K→2 |
| 7 | d3 | a2–d8,a1,b1 | Kd2 | K→4 |
| 8 | c4 | !a1–d4 | c2 | K→3 |
| 9 | b3 | a1 | Kc2 | K→5 |
| 10 | c4 | d1 | Kb3 | K→6 |
| 11 | b4 | !a1–d5 | Kc4 | K→8,10 |
| 12 | b4 | d1–d5 | Kb3 | K→6 |
| 13 | a3 | !a1–c5,h6–h8,d1–d3 | Kb4 | K→11,12 |
| 14 | a3 | a5–c5,d3,d1 | Kb3 | K→6 |
| 15 | b2 | a6–f8,e1–g4,a5,e5,f5 | Ka3 | K→13,14 |
| 16 | b2 | d1–d5,b5,c5 | Kb3 | K→6 |
| 17 | b2 | a4–c4 | Kc2 | K→5 |
| 18 | c2 | e3 | Kb2 | K→15,16 |
| 19 | b3 | d1 | Kb2 | K→15 |

**White pawn - · Black pawns c4, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 20 | b2 | a5–e8,d1–f3,a4,b4 | c3 | K→15,16,17 |
| 21 | d2 | a1–b4,b5 | c3 | K→4 |
| 22 | b3 | !a1,c1 | c3 | K→6,9,19 |
| 23 | c2 | b5–b6 | Kb3 | K→22 |
| 24 | d3 | a3–c7,a1–a2 | c3 | K→7 |
| 25 | c3 | a6–d8,d1–e2,a4,a5 | Kb2 | K→20 |
| 26 | c3 | a1–b3 | Kd2 | K→21 |
| 27 | c3 | b5–d5,c1 | Kb3 | K→22 |
| 28 | d3 | b1–d1 | Kc3 | K→25,26,27 |
| 29 | b3 | a1,c1 | Kc3 | K→25,26 |
| 30 | b4 | !a1–c2 | Kb3 | K→22,29 |
| 31 | d3 | b2 | Kd2 | K→21 |

**White pawn b6 · Black pawns c2, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 32 | f4 | f1–f2 | c1 | end→P |

**White pawn - · Black pawns b2, c4**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 33 | c3 | !b1 | b1 | end→P |
| 34 | d3 | !b1 | b1 | end→P |
| 35 | c5 | !a2,b1 | b1 | end→P |
| 36 | e4 | c1–f3 | b1 | end→P |
| 37 | c3 | b1 | Kd3 | K→34 Kxb2→31 |
| 38 | d3 | b1 | Kc3 | K→33 |

**White pawn - · Black pawns c5, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 39 | b3 | * | c4 | K→22,29 |
| 40 | d3 | a1–c4,b6 | c4 | K→24,28,31 |
| 41 | c4 | a7–c8,b1–d1,a5,a6,d2 | Kb3 | K→39 |
| 42 | b4 | !b5–d6,a1–b2,c2 | Kb3 | K→39 |
| 43 | d4 | b3 | Kd3 | K→40 |
| 44 | b4 | b5–d6 | c4 | K→30 |
| 45 | c4 | b2 | Kd3 | K→40 |
| 46 | c4 | b6,c6 | Kb4 | K→42,44 |
| 47 | b4 | c2 | Kc4 | K→41,45 |
| 48 | b5 | !a1–c3 | Kb4 | K→42,44,47 |

**White pawn b5 · Black pawns c2, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 49 | d2 | a1–b3 | c1 | end→P |
| 50 | f4 | e1–g2 | c1 | end→P |

**White pawn - · Black pawns c2, b5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 51 | b2 | c1–g7 | c1 | end→P |
| 52 | d2 | * | c1 | end→P |

**White pawn - · Black pawns b3, c4**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 53 | c3 | * | b2 | K→33,37 |
| 54 | d3 | !b2 | b2 | K→34,38 Kxb2→31 |
| 55 | d2 | b1,a1,a3 | Kc3 | K→53 |
| 56 | c5 | !a1–c3 | b2 | K→35 |
| 57 | e4 | d2,e2,e1 | b2 | K→36 |
| 58 | d3 | b2 | Kd2 | K→55 |
| 59 | d4 | !h8,d2,e2 | Kd3 | K→54,58 |
| 60 | e4 | a1,b2,c1 | Kd3 | K→54,58 |
| 61 | d5 | b1,d1 | Ke4 | K→57,60 |
| 62 | d5 | b2,b4 | Kd4 | K→59 |
| 63 | c5 | a1–b3 | Kd4 | K→59 |
| 64 | d4 | e2 | Kc5 | K→56 |
| 65 | d5 | d2 | Kd4 | K→59,64 |
| 66 | c5 | c3,c1 | Kd5 | K→61,62,65 |
| 67 | d4 | d2 | Kc5 | K→56,66 |

**White pawn - · Black pawns c6, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 68 | c4 | b7 | c5 | K→41,46 |
| 69 | b5 | a7–c8 | c5 | K→48 |
| 70 | c5 | b7 | Kb5 | K→69 |

**White pawn b4 · Black pawns c2, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 71 | d2 | a1–c4 | c1 | end→P |
| 72 | f4 | d1–h3 | c1 | end→P |

**White pawn b5 · Black pawns c3, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 73 | f4 | f1–f2 | c2 | K→50 b6→32 |
| 74 | d2 | b1 | c2 | K→49 |

**White pawn - · Black pawns b3, c5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 75 | c3 | d2–f6 | c4 | K→53 |
| 76 | d4 | !g7–h8 | c4 | K→59,64,67 |
| 77 | c4 | !f6–h8,e3–e5 | Kd4 | K→76 Kxb3→43 |
| 78 | c4 | e3–e5 | Kc3 | K→75 |

**White pawn - · Black pawns c3, b5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 79 | d2 | a1–g8 | c2 | K→52 Kxb5→1 |
| 80 | c2 | !g1–h8,e1–e3 | Kd2 | K→79 Kxb5→4 |
| 81 | b2 | d1–f6 | c2 | K→51 |
| 82 | b2 | b4–c6,a6 | Kc2 | K→80 Kxb5→5 |
| 83 | c2 | e1–e3 | Kb2 | K→81 |

**White pawn - · Black pawns b4, c4**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 84 | c3 | * | b3 | K→53 |
| 85 | c5 | * | b3 | K→56,63,66 |
| 86 | c2 | a1–f3 | Kc3 | K→84 |

**White pawn b4 · Black pawns c3, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 87 | d2 | a1–b3 | c2 | K→71 b5→49 |
| 88 | f4 | e1–g2 | c2 | K→72 b5→50 |

**White pawn - · Black pawns b4, c5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 89 | c4 | a1–h4,a5–d7 | b3 | K→77,78 |

**White pawn - · Black pawns c4, b5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 90 | c3 | * | b4 | K→84 |
| 91 | c5 | * | b4 | K→85 |
| 92 | b2 | a5–e5,e3,e4 | c3 | K→81,82 Kxb5→16 |
| 93 | d2 | a1–a5,b1,c5 | c3 | K→79 Kxb5→4 |
| 94 | b3 | e1–e5,a7–d7,a5–d5,d1,c1,d6,b6 | Kc3 | K→90 Kxb5→27 |
| 95 | d3 | !g1–h8,d1–f3,b4,b2 | Kc3 | K→90 Kxb5→27 |
| 96 | c2 | !b4,d4,h7–h8 | Kc3 | K→90 Kxb5→27 |
| 97 | d3 | b4,b2 | Kd2 | K→93 Kxb5→21 |
| 98 | c2 | b4,d4 | Kb2 | K→92 Kxb5→20 |

**White pawn b4 · Black pawns c4, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 99 | c5 | !a1–d5 | Kxb4 | K→30 |
| 100 | f4 | f1–f2 | c3 | K→88 b5→73 |
| 101 | d2 | b1–b2 | c3 | K→87 b5→74 |

**White pawn b5 · Black pawns c5, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 102 | c6 | !a1–d6 | Kxb5 | K→48 |

**White pawn - · Black pawns c4, b6**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 103 | c5 | * | b5 | K→91 |
| 104 | c3 | d1–g8,a6–c8,a4 | b5 | K→90 Kxb5→27 |
| 105 | d3 | !f1–h8,a1–e1,b5 | b5 | K→95,97 Kxb5→24 |
| 106 | c2 | !g5–h8,h1–h4,b5 | b5 | K→96,98 Kxb5→23 |
| 107 | b5 | !d4–d6 | Kc5 | K→103 |
| 108 | b3 | e2–f8,a7–d8,d5,b5,d6 | Kc3 | K→104 Kxb6→25 |
| 109 | b3 | a6,c6,d2–d4 | b5 | K→94 Kxb5→22 |
| 110 | b4 | a3–e8 | Kb3 | K→108,109 Kxb6→22 |
| 111 | b5 | d4–d6 | Kb4 | K→110 |
| 112 | c2 | b5 | Kb3 | K→109 Kxb6→22 |

**White pawn c2 · Black pawns c3, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 113 | b2 | a4–e8 | Kxc2 | K→5,18 |
| 114 | d2 | a4–a6,c4–c6,b4,b6 | Kxc2 | K→5 |
| 115 | a3 | a5–d8 | Kb2 | K→113 |
| 116 | b4 | a7–c7,a6,c6 | Ka3 | K→115 |

**White pawn b3 · Black pawns c4, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 117 | c3 | !a2–a4,b1,d1 | Kxb3 | K→22 |

**White pawn c3 · Black pawns c4, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 118 | b3 | a5–c7 | Kxc3 | K→25,27 |
| 119 | d3 | b5–b6 | Kxc3 | K→25,27 |
| 120 | d2 | a1–a3,b1,b5 | Kxc3 | K→25,26,27 |
| 121 | b2 | b5–b6 | Kb3 | K→118 |
| 122 | c2 | b5 | Kb3 | K→118 |
| 123 | d3 | b2 | Kd2 | K→120 |

**White pawn c4 · Black pawns c5, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 124 | b4 | b6–b7 | Kxc4 | K→41,46 |
| 125 | d4 | b6 | Kxc4 | K→41,46 |

**White pawn - · Black pawns c5, b6**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 126 | b5 | * | c4 | K→107,111 |
| 127 | c4 | !a4–c6 | Kb5 | K→126 |
| 128 | d3 | a7–d7,b3–d5,a3,d6 | c4 | K→105 Kxb6→24 |
| 129 | b4 | a8–d8,a6–d6,d7,b7 | c4 | K→110 Kxb6→30 |
| 130 | c4 | a4–c6 | Kd3 | K→128 Kxb6→40 |

**White pawn c2 · Black pawns c4, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 131 | b2 | a5–a7,c5–c7,b5,b7 | c3 | K→113 |
| 132 | d2 | b5 | c3 | K→114 |
| 133 | c3 | b6 | Kb2 | K→131 c3→121 |
| 134 | b4 | b6 | c3 | K→116 |

**White pawn c3 · Black pawns b2, c4**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 135 | d3 | a2–c5,d1,e1 | b1 | end→P |
| 136 | c5 | !a2,b1 | b1 | end→P |
| 137 | e4 | d1–h5,c2 | b1 | end→P |
| 138 | d3 | b1 | Kxc3 | K→33 |

**White pawn c3 · Black pawns c5, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 139 | b3 | b6 | c4 | K→118 |

**White pawn c4 · Black pawns b2, c5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 140 | c6 | !a2,b1 | b1 | end→P |
| 141 | e5 | c1–h5,g6,h6 | b1 | end→P |
| 142 | c7 | c1–h5 | b1 | end→P |

**White pawn - · Black pawns c5, b7**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 143 | b5 | * | b6 | K→126 |
| 144 | c4 | !a1,b6 | b6 | K→127,130 Kxb6→46 |
| 145 | b4 | a7,c7 | b6 | K→129 Kxb6→44 |
| 146 | c4 | b6 | Kb4 | K→145 Kxb7→42 |

**White pawn c2 · Black pawns b2, c4**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 147 | c3 | !b1 | b1 | end→P |

**White pawn c3 · Black pawns b3, c4**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 148 | d3 | a1–d1,a3–b4 | b2 | K→135,138 Kxb2→123 |
| 149 | b2 | e1–e3,d1 | Kxc3 | K→53 |
| 150 | d2 | b1,a1,a3 | Kxc3 | K→53 |
| 151 | c5 | !a1–c3 | b2 | K→136 |
| 152 | e4 | d1–h4 | b2 | K→137 |
| 153 | d3 | b2 | Kd2 | K→150 |
| 154 | e4 | a1–c3 | Kd3 | K→148,153 |
| 155 | d5 | b2,b1,d2,d1 | Ke4 | K→152,154 |
| 156 | f4 | d1–h3 | Ke4 | K→152,154 |
| 157 | c5 | c1 | Kd5 | K→155 |

**White pawn c4 · Black pawns b3, c5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 158 | d4 | a4–a6,b6,c6 | Kxc4 | K→77 |
| 159 | c6 | !a1–c3 | b2 | K→140 |
| 160 | c7 | d1–g4 | b2 | K→142 |
| 161 | e5 | d1–h5 | b2 | K→141 |

**White pawn - · Black pawns c6, b7**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 162 | b5 | * | c5 | K→143 Kxb7→48 |
| 163 | c4 | d2–g8,a3–b6,b7–c8 | c5 | K→144,146 Kxb7→41 |
| 164 | c5 | !a4–a5 | Kb5 | K→162 Kxb7→69 |
| 165 | c5 | a4–a5 | Kc4 | K→163 |

**White pawn c2 · Black pawns b3, c4**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 166 | c3 | !a3,a1,c1 | b2 | K→147 |

**White pawn c3 · Black pawns b4, c4**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 167 | d2 | b1,a1,a2 | Kxc3 | K→84 |
| 168 | c5 | !a1–c4 | b3 | K→151,157 |
| 169 | b2 | d2 | b3 | K→149 |
| 170 | f4 | e1–g2 | b3 | K→156 |
| 171 | d2 | b2 | b3 | K→150 |

**White pawn c4 · Black pawns b4, c5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 172 | d4 | a1–g2,a6–c6,a4,f3,g3,a5 | Kxc4 | K→89 |
| 173 | d3 | b2,a2,a4 | Kxc4 | K→89 |
| 174 | c6 | !a1–d4 | b3 | K→159 |
| 175 | c7 | e1–f3 | b3 | K→160 |
| 176 | e5 | e2–g4,e1,f1 | b3 | K→161 |
| 177 | d4 | b5 | b3 | K→158 |
| 178 | d4 | b3 | Kd3 | K→173 |
| 179 | e4 | b1–f3 | Kd4 | K→172,178 |
| 180 | f4 | c2–e2 | Ke4 | K→179 |
| 181 | e5 | a1–c5,d1–d2 | Kd4 | K→172,177,178 |
| 182 | e5 | d3 | Kf4 | K→180 |
| 183 | d6 | a1–e3,f3,a4 | Ke5 | K→176,181,182 |
| 184 | c7 | b1–d2,a2,b3 | Kd6 | K→183 |
| 185 | c6 | a1–d2,b3 | Kd6 | K→183 |
| 186 | b6 | a1–e1,b2,d3,a2,a4 | Kc6 | K→174,185 |
| 187 | c7 | a4,d3 | Kc6 | K→174,185 |
| 188 | b6 | c2–e2,b3 | Kc7 | K→175,184,187 |
| 189 | a6 | a1–c4,d1 | Kb6 | K→186,188 |
| 190 | d6 | f5,f4 | Kc6 | K→174 |
| 191 | c7 | e4 | Kd6 | K→183,190 |
| 192 | c6 | d3 | Kc7 | K→175,184,191 |
| 193 | b6 | e4,e3 | Kc6 | K→174,185,192 |
| 194 | a6 | d3,d2 | Kb6 | K→186,188,193 |
| 195 | c6 | a4 | Kb6 | K→188 |

**White pawn c2 · Black pawns c3, b5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 196 | b2 | a4–e8,e2,e1 | Kxc2 | K→80,83 Kxb5→5 |
| 197 | d2 | a2,a1 | Kxc2 | K→80 |
| 198 | a3 | a5–d8 | Kb2 | K→196 Kxb5→113 |
| 199 | b4 | a6–c7 | Ka3 | K→198 Kxb5→115 |

**White pawn c2 · Black pawns b4, c4**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 200 | c3 | !b1,d1,a2–a4 | b3 | K→166 cxb3→117 |
| 201 | b2 | d1,e3 | Kc3 | K→200 |
| 202 | d2 | a1–a2 | Kxc2 | K→86 |
| 203 | b2 | e1–e2 | Kxc2 | K→86 |
| 204 | c3 | a2 | Kxc2 | K→86 |
| 205 | d2 | b1 | Kc3 | K→200,204 |

**White pawn c3 · Black pawns c4, b5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 206 | b3 | !d2–d4 | Kxc3 | K→90 Kxb5→27 |
| 207 | b4 | !a1–c2,d2–d7,c7,b7,b6 | Kxc3 | K→90 Kxb5→27 |
| 208 | d3 | !a6,a8,b4,b2 | Kxc3 | K→90 Kxb5→27 |
| 209 | c2 | a5–d6,e3–e5,a1–a3 | Kxc3 | K→90 Kxb5→27 |
| 210 | b2 | e1–g4,a5–e5,d1 | Kxc3 | K→90 Kxb5→27 |
| 211 | c5 | !a1–d5 | b4 | K→168 cxb4→99 |
| 212 | f4 | f1–f2 | b4 | K→170 cxb4→100 |
| 213 | d2 | b1–b2 | b4 | K→167,171 cxb4→101 |
| 214 | b3 | d2–d4 | Kb2 | K→210 |
| 215 | a3 | d1–e5,f1–f3,c1,b1,c5 | Kb3 | K→206,214 Kxb5→118 |
| 216 | a4 | !a1–c2 | Kb3 | K→206,214 Kxb5→118 |
| 217 | a2 | d1–e3,c1 | Kb3 | K→206,214 |
| 218 | a5 | !a1–d3 | Ka4 | K→216 |
| 219 | b2 | d4,b4 | Kc2 | K→209 Kxb5→122 |
| 220 | c2 | b4,d4 | Kb2 | K→210 Kxb5→121 |
| 221 | d2 | a1–a5,b4,d4,c5 | Kc2 | K→209,220 Kxb5→122 |
| 222 | d3 | b4,b2 | Kd2 | K→213,221 Kxb5→120 |
| 223 | e3 | d4–g8,a1–f1,a2–b3,c7–c8 | Kd3 | K→208,222 |
| 224 | e4 | a1–g1,a2–b4,f2–g3 | Kd3 | K→208,222 Kxb5→119 |
| 225 | e2 | c1,b1,b2 | Kd3 | K→208,222 |
| 226 | a3 | c2 | Ka2 | K→217 |
| 227 | b4 | d4,d2 | Ka3 | K→215,226 |
| 228 | e3 | c2 | Ke2 | K→225 |
| 229 | d4 | e5–f8,a1–b2,d8 | Ke3 | K→223,228 |
| 230 | f3 | c1–e1,c2 | Ke3 | K→223,228 |
| 231 | f4 | b1–e1,b2 | Ke3 | K→223,228 |
| 232 | e4 | d2 | Kf3 | K→230 |
| 233 | a2 | c2 | Ka3 | K→215 |
| 234 | b2 | d2 | Ka2 | K→217,233 |
| 235 | f4 | d2 | Kf3 | K→230 |
| 236 | e4 | c2,e2 | Kf4 | K→212,231,235 |
| 237 | d5 | a1–f2,a3 | Ke4 | K→224,232,236 |
| 238 | b6 | d4–f5,f1–f3 | Ka5 | K→218 |
| 239 | c6 | !a1–e3,a6,b4,d4 | Kc5 | K→211 |
| 240 | d6 | f2–f4,e4 | Kc5 | K→211 |
| 241 | c6 | a1–c2,d1,e1 | Kd5 | K→237 |
| 242 | c5 | a1–c2,d1 | Kd5 | K→237 |
| 243 | b6 | a1,b1,a3,d2 | Kc5 | K→211,242 |
| 244 | d5 | f4,f3 | Kc5 | K→211 |
| 245 | d6 | d2 | Kc5 | K→211,242 |
| 246 | c6 | a3,d2 | Kc5 | K→211,242 |
| 247 | b6 | a2–c2,b4,c1 | Kc6 | K→239,241,246 |
| 248 | a6 | a1–b4 | Kb6 | K→243,247 |
| 249 | a5 | a1–b3 | Kb6 | K→243,247 |
| 250 | c6 | e3 | Kd5 | K→237,244 |
| 251 | d6 | e2,d4 | Kc6 | K→239,241,246,250 |
| 252 | d5 | e3 | Kd6 | K→240,245,251 |
| 253 | c6 | e2 | Kd5 | K→237,244,252 |
| 254 | c5 | d2 | Kd5 | K→237,252 |
| 255 | b6 | e1–e3,d1 | Kc5 | K→211,242,254 |
| 256 | a6 | c1–e4 | Kb6 | K→238,243,247,255 |
| 257 | a5 | c1–d2 | Kb6 | K→243,247,255 |
| 258 | c6 | b4,d4 | Kb6 | K→238,243,255 |
| 259 | c5 | a3 | Kb6 | K→247 |

**White pawn c4 · Black pawns b5, c5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 260 | c6 | !c3 | b4 | K→174,185,192,195 |
| 261 | a6 | a1–c2,a3,b3 | b4 | K→189,194 |

**White pawn c2 · Black pawns c4, b5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 262 | b2 | e1–h5,b4–f6,a5 | Kxc2 | K→96,98 Kxb5→23 |
| 263 | d2 | a1–a5,c5–e5,b4,e4 | Kxc2 | K→96,98 Kxb5→23 |
| 264 | c3 | !a1–a5,e2,e1,c1 | b4 | K→200,204 |
| 265 | b4 | !d1–f3,a1–b6,d4,c6 | Kc3 | K→264 |
| 266 | d4 | d4–g8,c1,c7–c8 | Kc3 | K→264 |
| 267 | b4 | a6,b6 | c3 | K→199 |
| 268 | b2 | d1 | c3 | K→196 |
| 269 | b2 | d2 | b4 | K→201,203 c3→169 |
| 270 | a2 | d1–d4,b4 | Kb2 | K→262,268,269 Kxb5→131 c3→210,219,234 |
| 271 | a3 | d1–g4,c5–e5 | Kb2 | K→262,268,269 Kxb5→131 c3→210,219,234 |
| 272 | a3 | c3,c1 | Ka2 | K→270 c3→217 |
| 273 | b4 | d1–f3,d4 | Ka3 | K→271,272 c3→215 |
| 274 | a5 | d1–d4 | Kb4 | K→265,273 c3→207,227 |
| 275 | c5 | e1–h8,d2,d1 | Kb4 | K→265,273 c3→207,227 |
| 276 | d2 | b1 | c3 | K→197 |
| 277 | d2 | b2 | b4 | K→202,205 c3→171 |
| 278 | e2 | b1–b4,d4 | Kd2 | K→263,276,277 Kxb5→132 c3→213,221 |
| 279 | e3 | a1–b4 | Kd2 | K→263,276,277 Kxb5→132 c3→213,221 |
| 280 | e3 | c3,c1 | Ke2 | K→278 c3→225 |
| 281 | d4 | a1–b3 | Ke3 | K→279,280 c3→223 |
| 282 | d5 | a1–b2 | Kd4 | K→266,281 c3→229 |
| 283 | c5 | a2,b2,b1 | Kd4 | K→266,281 c3→229 |
| 284 | c6 | a1,a3,c3,c1 | Kc5 | K→275,283 c3→242,259 |
| 285 | b6 | a1,a3,c3,c1 | Kc5 | K→275,283 c3→242,259 |
| 286 | d5 | a3,c3,c1 | Kc5 | K→275,283 c3→242,259 |
| 287 | c6 | a2,b2,b1 | Kd5 | K→282,286 c3→237 |
| 288 | b6 | a2,b2,b1 | Kc6 | K→284,287 c3→241 |
| 289 | a6 | a1–b2,b4 | Kb6 | K→285,288 c3→243,247 |
| 290 | a5 | a2,b2,b1 | Kb6 | K→285,288 c3→243,247 |
| 291 | a6 | a3,c3,c1 | Ka5 | K→274,290 c3→249,257 |
| 292 | c6 | b4 | Kb6 | K→285 c3→247 |

**White pawn c3 · Black pawns c4, b6**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 293 | a5 | * | b5 | K→218,249,257 |
| 294 | b3 | !b5 | b5 | K→206,214 Kxb5→118 |
| 295 | d3 | d5–f8,a1–d4,a6,c6 | b5 | K→208,222 Kxb5→119 |
| 296 | b5 | !d4–d5 | Ka5 | K→293 |
| 297 | c6 | !a6–c8 | b5 | K→239,241,246,250,253,258 |
| 298 | b2 | d1 | b5 | K→210,234 |
| 299 | d2 | b1 | b5 | K→213,221 |
| 300 | c5 | !a6–d8 | Kc6 | K→297 |
| 301 | b4 | !a6–e8,g1–h2,c2,d4–d5 | Kc5 | K→300 |
| 302 | d5 | a3 | Kc5 | K→300 |
| 303 | d4 | a2,b2,b1,d2 | Kc5 | K→300 |
| 304 | b3 | b5 | Kxc3 | K→104 Kxb6→25 |
| 305 | b4 | b6–e8,a7–a8,d4–d5 | Kb3 | K→294,304 Kxb6→118 |
| 306 | d3 | b5 | Kxc3 | K→104 Kxb6→25 |
| 307 | d4 | e6–e8,b4 | Kd3 | K→295,306 |

**White pawn c3 · Black pawns b5, c5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 308 | c6 | !a5,a7,a8 | c4 | K→239,241,246,250,253,258 |
| 309 | a6 | a1–d3 | c4 | K→248,256 |

**White pawn c4 · Black pawns c5, b6**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 310 | b4 | !d3–d5 | Kxc4 | K→127,130 Kxb6→46 |
| 311 | b5 | !b3–d5,a7–b8 | Kxc4 | K→127,130 Kxb6→46 |
| 312 | d4 | !a7–h8,b5,b3,d6,e6 | Kxc4 | K→127,130 Kxb6→46 |
| 313 | b3 | e1–f7,a1–d2,c6–d7 | Kxc4 | K→127,130 Kxb6→46 |
| 314 | d3 | a2–a4,b2 | Kxc4 | K→127,130 |
| 315 | c6 | a7 | b5 | K→260 cxb5→102 |
| 316 | b5 | d5,d3 | Kb4 | K→310 |
| 317 | b4 | d3–d5 | Kb3 | K→313 |
| 318 | a5 | !a3–c3 | Kb4 | K→310,317 Kxb6→124 |
| 319 | a6 | !a2–d4,h1–h8,d1 | Ka5 | K→318 |
| 320 | b3 | d3,d5 | Kb4 | K→310 |
| 321 | d4 | b3 | Kd3 | K→314 |
| 322 | d5 | b3 | Kd4 | K→312 |
| 323 | e4 | a1–g2,b5,a3,g3,b3 | Kd4 | K→312,321 Kxb6→125 |
| 324 | e3 | b2–b5,a3,c2 | Kd4 | K→312,321 Kxb6→125 |
| 325 | e5 | !a6–h8,c3–e3,a4 | Kd4 | K→312,321 Kxb6→125 |
| 326 | e4 | a4,c3 | Ke3 | K→324 |
| 327 | f4 | c2–e2,c3 | Ke4 | K→323,326 |
| 328 | e5 | a4,c3 | Ke4 | K→323 |
| 329 | e5 | d3 | Kf4 | K→327 |
| 330 | d6 | a1–c4 | Ke5 | K→325,328,329 |
| 331 | c6 | a1–b3 | Kd6 | K→330 |
| 332 | c7 | a4,a6 | Kc6 | K→315,331 |

**White pawn c2 · Black pawns c4, b6**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 333 | b2 | d2,e2,e1 | b5 | K→262,268,269 c3→210,234 |
| 334 | d2 | b2,a2,a1 | b5 | K→263,276,277 c3→213,221 |
| 335 | c3 | !g1–h8,f4–f8,b1–d5 | Kxc2 | K→106,112 Kxb6→23 |
| 336 | b4 | !a1–c2,b7–d7,h1,d5,d6 | b5 | K→265,267,273 c3→207,227 |
| 337 | c5 | !a6–e8,a2–d2,a4,b1,d1 | b5 | K→275,283 c3→211,242,259 |
| 338 | d4 | e5–f8,a1–b2,d8 | b5 | K→266,281 c3→229 |
| 339 | c3 | d5,c1 | b5 | K→264 |
| 340 | c3 | d1 | Kb2 | K→333 c3→298 |
| 341 | c3 | b1 | Kd2 | K→334 c3→299 |
| 342 | d4 | c1–e1,a3,b5,e2,d6–d7 | Kc3 | K→335,339,340,341 Kxb6→133 |
| 343 | c5 | e6–e8,a2–d2,b1 | Kd4 | K→338,342 c3→303,307 |
| 344 | b5 | f1–h8,a1–b2,e3–e5,d1,c3 | Kc5 | K→337,343 c3→300 |
| 345 | d5 | a2,a4,b2 | Kc5 | K→337,343 c3→300 |
| 346 | b4 | a1–c1,b7–d7,d5,d6,a2 | Kc3 | K→335,339,340,341 Kxb6→133 |
| 347 | b4 | b2 | Kc5 | K→337,343 c3→300 |
| 348 | a5 | !g1–h2,c3,a3 | Kb4 | K→336,346,347 c3→301,305 Kxb6→134 |
| 349 | b5 | a6–e8,d2–d5,c1,e2,e1 | Kb4 | K→336,346,347 Kxb6→134 c3→301,305 |
| 350 | b5 | a3 | Ka5 | K→348 c3→293 |
| 351 | d4 | a4 | Kc5 | K→337 c3→300 |
| 352 | d5 | b4,d2 | Kd4 | K→342,351 c3→303,307 |

**White pawn c2 · Black pawns b5, c5**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 353 | c6 | a2,b2,b3 | c4 | K→284,287,292 c3→241 |
| 354 | a6 | a1–b3 | c4 | K→289,291 c3→248 |

**White pawn c3 · Black pawns c5, b6**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 355 | a5 | a6–g8,e4–g5,a1–d1,c2–e2,e3 | c4 | K→293 |
| 356 | b3 | b1–g8,a1 | c4 | K→294,304 Kxb6→118 |
| 357 | d3 | a1–c5 | c4 | K→295,306 Kxb6→119 |
| 358 | b4 | d1–e3,a1–c1,d5 | Kb3 | K→356 c4→313,320 |
| 359 | c4 | d1–f7,a1–c1,c6,c7 | Kb3 | K→356 Kxb6→139 c4→313 |
| 360 | c6 | a1–b2,c2,a3,c4 | b5 | K→308 c4→260 |
| 361 | b5 | !d3–e6,a7–a8 | c4 | K→296 |
| 362 | a6 | a1–c1,b3 | b5 | K→309 c4→261 |
| 363 | b5 | e3–e6,d6 | Kc4 | K→359 |
| 364 | c4 | a2–b4 | Kd3 | K→357 c4→314 |
| 365 | a5 | d5 | Kb5 | K→363 c4→316 |
| 366 | c6 | a4 | c4 | K→297 |
| 367 | d5 | b3 | Kc6 | K→360,366 c4→331 |
| 368 | a6 | a6–f8,e5,f5 | Ka5 | K→355,365 c4→318 |
| 369 | a6 | d3,d5 | Kb5 | K→361,363 c4→316 |
| 370 | a5 | c4 | Ka6 | K→362,369 |
| 371 | b5 | d5,d3 | Ka5 | K→355,370 c4→318 |
| 372 | c4 | c2 | Kb5 | K→361,371 c4→311 |
| 373 | b4 | a2,b2 | Kc4 | K→359,364,372 |

**White pawn c4 · Black pawns c5, b7**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 374 | b4 | !b6,a7,a8 | b6 | K→310,317 Kxb6→124 |
| 375 | d4 | c1–g4,a4,b6,a5 | Kxc4 | K→144,146 Kxb7→41 |
| 376 | e4 | b1–f3 | b6 | K→323,326 |
| 377 | e5 | a1–c4,d1–g1,g2–g4,e3 | b6 | K→325,328,329 |
| 378 | c6 | !a1–d5 | b5 | K→260 cxb5→102 |
| 379 | a6 | a5–f8,f2–f4 | b6 | K→319 |
| 380 | f4 | c2–e2,c3 | Ke4 | K→376 |
| 381 | c7 | b5 | b6 | K→332 |
| 382 | c6 | a4,a1–a2 | b6 | K→331 |
| 383 | d4 | b5 | b6 | K→312 Kxb6→125 |
| 384 | e5 | d2–f2,a5,b5,f3 | Kd4 | K→375,383 |
| 385 | b4 | b6 | Kxc4 | K→144 Kxb7→41 |
| 386 | a5 | !a3–b8,c3 | Kb4 | K→374,385 Kxb7→124 |
| 387 | b5 | !a2–c8 | Kb4 | K→374 |
| 388 | e5 | d3 | Kf4 | K→380 |
| 389 | d6 | a1–f3,a4 | Ke5 | K→377,384,388 |
| 390 | b6 | !a2–d6,a8–c8 | Ka5 | K→386 |
| 391 | d7 | f2–f4 | Kc6 | K→378 |
| 392 | c7 | c2–e2,c3 | Kd6 | K→389 |
| 393 | d7 | d2,e2 | Kd6 | K→389 |
| 394 | c6 | b1–d2,a3–c3 | Kd6 | K→389 |
| 395 | b6 | a2–b3,a8–c8,d3 | Kc6 | K→378,382,394 |
| 396 | a6 | e2–e4 | Ka5 | K→386 |
| 397 | d6 | f5,f4 | Kc6 | K→378 |
| 398 | c7 | a4 | Kb6 | K→395 |
| 399 | a6 | a2,a4 | Kb6 | K→390,395 |
| 400 | c7 | e4 | Kd6 | K→389,397 |
| 401 | c6 | a5 | Kc7 | K→381,398 |
| 402 | d7 | d3 | Kc6 | K→378,394 |
| 403 | b6 | a4 | Kc6 | K→394,401 |
| 404 | a5 | a3 | Kb6 | K→395,403 |
| 405 | a6 | a3 | Kb6 | K→395,403 |
| 406 | d7 | e4 | Kd6 | K→389,397 |
| 407 | c7 | e3 | Kd7 | K→391,393,402,406 |
| 408 | c6 | d3 | Kc7 | K→392,400,407 |
| 409 | b6 | d2,c2,c3 | Kc6 | K→378,394,408 |
| 410 | a6 | b2–d3 | Kb6 | K→390,395,403,409 |
| 411 | b5 | a3,b3 | Ka6 | K→399,405,410 |
| 412 | a5 | b3 | Kb6 | K→395,403,409 |

**White pawn c5 · Black pawns c6, b7**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 413 | b5 | e3–e7,d3,d7,c3,c7 | Kxc5 | K→164 Kxb7→70 |
| 414 | b6 | !b4–d6 | Kxc5 | K→164,165 Kxb7→70 |
| 415 | b4 | d3 | Kxc5 | K→164 |
| 416 | a6 | d6,d4 | Kb5 | K→413 |
| 417 | b6 | d6,d4 | Kb5 | K→413 |
| 418 | b4 | d4,d6 | Kb5 | K→413 |

**White pawn c2 · Black pawns c5, b6**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 419 | b5 | !d5,a7–a8 | c4 | K→344,349,350 c3→296 |
| 420 | b4 | a1–f4,c6–e6,e5 | c4 | K→336,346,347 Kxb6→134 c3→301,305 |
| 421 | a5 | a6–g8,e4–g5,a1–e1,e2 | c4 | K→348 c3→293 |
| 422 | d5 | a3,c3 | c4 | K→345,352 c3→302 |
| 423 | a5 | a2–d2,d5 | Kb4 | K→420 c3→358,373 c4→310,317 |
| 424 | a6 | a6–f8,a1–d1,e5,f5 | Ka5 | K→421,423 c3→355 c4→318 |
| 425 | a6 | a2–d2,d5 | Kb5 | K→419 c3→361,371 c4→311,316 |
| 426 | b5 | d5 | Kb4 | K→420 c3→358 c4→317 |
| 427 | c4 | a1–c3 | Kb5 | K→419 c3→361 c4→311 |
| 428 | c6 | a1–c2,a3,c3,d3 | Kb5 | K→419 c3→361,371 c4→311,316 |
| 429 | d5 | a2,b2,a4 | Kc4 | K→427 c3→364 |
| 430 | c6 | b3 | Kd5 | K→422,429 c3→367 c4→322 |

**White pawn c3 · Black pawns c5, b7**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 431 | b5 | !a7–b8,b3 | b6 | K→361,363,371 c4→311,316 |
| 432 | c6 | !a7–b8,a4 | b5 | K→308 c4→260 |
| 433 | c4 | a1–c3,e1–e3,d1 | b6 | K→359,364,372 |
| 434 | a6 | a6–e8,c4 | b6 | K→362,368,369 c4→319 |
| 435 | b6 | !d5–d7,a8–c8,a3,b3 | Kc6 | K→432 c4→378,382,394,408 |
| 436 | b4 | d2,b2,a2 | Kc4 | K→433 |
| 437 | a6 | a2–c3,a4 | b5 | K→309 c4→261 |
| 438 | b6 | a8–c8,a3,d7,b3 | Ka6 | K→434,437 c4→379,405,410 |
| 439 | b6 | d5–d6 | Kb5 | K→431 c4→387 |
| 440 | b5 | b3 | Ka6 | K→434,437 c4→410 |
| 441 | a5 | b3,a3 | Kb5 | K→431,440 c4→411 |

**White pawn c4 · Black pawns c6, b7**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 442 | a6 | e3–e7,d3,d7,c3,c7 | c5 | K→379,396,410 |
| 443 | b4 | c2–e5,c7–e7,e6 | c5 | K→374,385 Kxb7→124 |
| 444 | c5 | c4–f8,e3,f3 | Kxc4 | K→163 Kxb7→68 |
| 445 | b6 | !d4–e7 | c5 | K→390,395,403,409 |
| 446 | a5 | d4,d6 | Kb4 | K→443 c5→418 |
| 447 | c5 | d3 | Kb4 | K→443 c5→415 |
| 448 | b6 | e4–e7,d7 | Kc5 | K→444,447 |
| 449 | a6 | c5 | Ka5 | K→446 |
| 450 | b5 | d6 | Ka6 | K→442,449 c5→416 |
| 451 | b6 | d6,d4 | Ka6 | K→442,449 c5→416 |

**White pawn c2 · Black pawns c5, b7**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 452 | b5 | !a7–b8,b3 | b6 | K→419,426 c3→361,363,371 c4→311,316 |
| 453 | b4 | !a4–h8,f1–h3,d2 | b6 | K→420 c3→358,373 c4→310,317 |
| 454 | a6 | a6–e8,a1–c1 | b6 | K→424,425 c3→362,368 c4→319 |
| 455 | c6 | a1,b1,b2,c4 | b6 | K→428,430 c3→360 c4→331 |
| 456 | a5 | a2–d2 | Kb4 | K→453 c3→436 c4→374 |
| 457 | a6 | a2–a4 | b5 | K→354 c3→309 c4→261 |
| 458 | c6 | a3 | b5 | K→353 c3→308 c4→260 |
| 459 | b6 | d1–h8,a1–c1,b3 | Kb5 | K→452 c3→431,440 c4→387,411 |
| 460 | a5 | d3,b3 | Kb5 | K→452 c3→431,440 c4→387,411 |
| 461 | c6 | d2,b3,d3 | Kb5 | K→452 c3→431,440 c4→387,411 |
| 462 | b6 | a8–c8 | Ka6 | K→454 c3→434 c4→379 |
| 463 | b6 | a2,c3 | Kc6 | K→455,458,461 c3→432 c4→382 |
| 464 | a6 | c4 | Kb6 | K→459,463 c3→435 |
| 465 | b6 | a3 | Ka5 | K→456,460 c3→441 c4→404 |
| 466 | a5 | c4 | Kb6 | K→459,463 c3→435 |
| 467 | a6 | c3 | Ka5 | K→456,460,466 |
| 468 | a6 | b2 | Kb6 | K→459,463,465 c3→435 c4→395 |
| 469 | b5 | b3 | Ka6 | K→457,464,467,468 c3→437 c4→410 |
| 470 | a5 | c3,a3 | Kb5 | K→452,469 c3→431 c4→411 |
| 471 | a6 | b3 | Ka5 | K→456,466,470 c3→441 c4→412 |
| 472 | b6 | b2,a4 | Ka6 | K→454,457,467,471 c3→437 c4→399,410 |
| 473 | c6 | c3 | Kb5 | K→452,469 |
| 474 | b6 | c4 | Kc6 | K→461,473 c3→432 |

**White pawn c3 · Black pawns c6, b7**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 475 | b6 | !d6 | c5 | K→435,438,439 c4→390,395,403,409 |
| 476 | b5 | d5–e7 | c5 | K→431 c4→387 |
| 477 | a6 | b7–d8 | c5 | K→434 c4→379 |
| 478 | a6 | d6 | Kb6 | K→475 c4→451 |
| 479 | b5 | c7 | Ka6 | K→477,478 c4→442 |
| 480 | b6 | d6 | Kb5 | K→476,479 c4→450 |

**White pawn c2 · Black pawns c6, b7**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 481 | b6 | !d6 | c5 | K→459,462,463,465,472,474 c3→435,438 c4→390,395,403,409 |
| 482 | b5 | e5–e7,d7 | c5 | K→452 c3→431 c4→387 |
| 483 | a6 | b8–d8,d7 | c5 | K→454 c3→434 c4→379 |
| 484 | a6 | d6 | Kb6 | K→481 c3→480 c4→451 |
| 485 | b5 | c7 | Ka6 | K→483,484 c3→477 c4→442 |
| 486 | b6 | d6 | Kb5 | K→482,485 c3→476 c4→450 |

## Table D · White to move

**PROVED by closure.** Enter at D80 after …Ka6 or …Ka7, or at D81 after …Kc7. Numbers in this table refer to other D rows.

**White pawn - · Black pawns c5, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 1 | b3 | b6–b7 | Kc4 | end→F |
| 2 | c4 | b6 | Kc3 | end→F |

**White pawn b7 · Black pawns c4, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 3 | b3 | a6 | Kc3 | end→F |
| 4 | d3 | f5–h8,d7–e8,e5,d6 | Kc3 | end→F |
| 5 | c7 | f2–h7 | b8 | end→P |
| 6 | f4 | e8–h8,h5–h7,f6 | b8 | end→P |
| 7 | f5 | e7–g7,h5 | b8 | end→P |

**White pawn - · Black pawns c6, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 8 | b4 | b6,b7 | Kc4 | K→10 c5→2 end→F |
| 9 | a4 | b6 | Kb4 | end→F |
| 10 | c4 | a5–a7,b7,c7 | Kc5 | end→F |
| 11 | d4 | b6 | Kc4 | K→10 c5→2 |

**White pawn b6 · Black pawns c4, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 12 | b3 | a6–b8 | Kc3 | end→F |
| 13 | d3 | g6–h8,e6,e8,f8 | Kc3 | end→F |
| 14 | d5 | d7–h8,g5–h6,h4 | Kxc4 | end→0 |

**White pawn b7 · Black pawns c5, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 15 | b4 | a6 | Kb3 | K→16 Kxb7→1 c4→3 |
| 16 | b3 | a7,a5,b5,b6 | b8 | end→P |
| 17 | c4 | d6 | Kc3 | end→F |
| 18 | d3 | c4–h8 | b8 | end→P |
| 19 | d6 | f2–h7 | Kxc5 | end→0 |
| 20 | e4 | f5–h8,d7–e8,d6 | Kd3 | K→18 c4→4 |
| 21 | c7 | e1–h8 | b8 | end→P |
| 22 | f4 | d7–h8,g4–h6,e6 | b8 | end→P |
| 23 | f5 | d6–h8,h4 | b8 | end→P |

**White pawn b6 · Black pawns c5, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 24 | b4 | a6–b8 | Kb3 | K→25,26 Kxb6→1 c4→12 |
| 25 | b3 | a6–c8,a5 | Kc4 | end→F |
| 26 | b3 | b5 | b7 | end→F |
| 27 | a4 | a6,a8 | Kb3 | K→25,26 Kxb6→1 c4→12 |
| 28 | c4 | f2–h8,a8–e8,d6,e6,e7 | b7 | end→F |
| 29 | d3 | !a1–h4,a5–c8,e6 | b7 | end→F K→18 c4→4 |
| 30 | d4 | g3–h8,c7–f8 | Kc4 | end→F |
| 31 | d5 | c4–h8,g3,h3 | Kc4 | end→F |
| 32 | d6 | g3–g6,h3–h4 | Kxc5 | end→0 |
| 33 | e4 | g6–h8,e8,f8,e6 | Kd3 | K→29 c4→13 |
| 34 | e5 | d5–h8,h4 | Kd5 | K→31 c4→14 |
| 35 | c7 | f2–h7 | b7 | K→21 c4→5 |
| 36 | f4 | e8–h8,h5–h7,f6 | b7 | K→22 c4→6 |
| 37 | f5 | e7–g7,h5 | b7 | K→23 c4→7 |

**White pawn b7 · Black pawns c6, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 38 | b4 | a7,b6 | b8 | end→P |
| 39 | c4 | c7–e7,e5,e6 | Kc5 | end→F |
| 40 | d6 | e1–h8 | b8 | end→P |
| 41 | e4 | c5–h8,g4,h4 | b8 | end→P |
| 42 | c7 | d1–h8 | b8 | end→P |
| 43 | f4 | d5–h8,c7,h3–h4 | b8 | end→P |
| 44 | f5 | c5–h8,h3,g3 | b8 | end→P |

**White pawn b6 · Black pawns c6, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 45 | b4 | a7–c8 | Kc4 | end→F K→48 c5→28 |
| 46 | b4 | a6 | b7 | K→38 Kxb7→8 c5→15 |
| 47 | a4 | a6–b8 | Kb4 | K→45,46 Kxb6→8 c5→24 |
| 48 | c4 | !a1–d6 | Kc5 | end→F |
| 49 | c4 | d6 | b7 | K→39 c5→17 |
| 50 | d4 | c3–h8,f2–h2,b7,b8 | Kc4 | end→F K→48,49 c5→28 |
| 51 | d6 | f2–h7 | b7 | K→40 c5→19 |
| 52 | e4 | f5–h8,d7–e8,d6 | b7 | K→41 c5→20 |
| 53 | e5 | d4–h8,c8,g3,h3 | Kd4 | K→50 c5→30 |
| 54 | c7 | e1–h8 | b7 | K→42 c5→21 |
| 55 | f4 | d7–h8,g4–h6,e6 | b7 | K→43 c5→22 |
| 56 | f5 | d6–h8,h4 | b7 | K→44 c5→23 |

**White pawn c5 · Black pawns c6, -**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 57 | b6 | !a1–b8,d5–d7 | Kxc6 | end→0 |
| 58 | b7 | f1–h8,d1–e3,d7,d5 | Kb6 | K→57 |
| 59 | b7 | e4–e8,d4,d8 | Kxc6 | end→0 |

**White pawn c5 · Black pawns b5, c6**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 60 | b4 (ep b6) | a6–a8,b8 | cxb6 | K→45,46 Kxb6→8 c5→24 |
| 61 | a4 (ep b6) | a6–a8 | cxb6 | K→47 Kxb6→9 c5→27 |
| 62 | c4 (ep b6) | b8,c8,c7 | cxb6 | end→F K→48 c5→28 |
| 63 | d4 (ep b6) | c8–h8,c7,d7,h6–h7 | cxb6 | K→50 c5→30 Kxb6→11 |
| 64 | e4 (ep b6) | g6–h8,e8,f8,e6 | cxb6 | K→52 c5→33 |
| 65 | e5 (ep b6) | d5–h8,h4 | cxb6 | K→53 c5→34 |
| 66 | c7 (ep b6) | f2–h7 | cxb6 | K→54 c5→35 |
| 67 | f4 (ep b6) | e8–h8,h5–h7,f6 | cxb6 | K→55 c5→36 |
| 68 | f5 (ep b6) | e7–g7,h5 | cxb6 | K→56 c5→37 |
| 69 | d6 (ep b6) | g3–g6,h3–h4 | cxb6 | K→51 c5→32 |

**White pawn c5 · Black pawns b6, c6**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 70 | b4 | a6–a8,b8 | cxb6 | K→45,46 Kxb6→8 c5→24 |
| 71 | a4 | a6–a8 | cxb6 | K→47 Kxb6→9 c5→27 |
| 72 | c4 | b8,c8,c7 | cxb6 | end→F K→48 c5→28 |
| 73 | d4 | c8–h8,c7,d7,h6–h7 | cxb6 | K→50 c5→30 Kxb6→11 |
| 74 | e4 | g6–h8,e8,f8,e6 | cxb6 | K→52 c5→33 |
| 75 | e5 | d5–h8,h4 | cxb6 | K→53 c5→34 |
| 76 | c7 | f2–h7 | cxb6 | K→54 c5→35 |
| 77 | f4 | e8–h8,h5–h7,f6 | cxb6 | K→55 c5→36 |
| 78 | f5 | e7–g7,h5 | cxb6 | K→56 c5→37 |
| 79 | d6 | g3–g6,h3–h4 | cxb6 | K→51 c5→32 |

**White pawn c5 · Black pawns c6, b7**

| # | King | Zone | Play | Replies |
|---:|:---:|:---|:---|:---|
| 80 | b4 | a6–a8 | Ka4 | K→82 b6→71 b5→61 |
| 81 | b4 | b7–c8 | Kc4 | K→83,84 b6→72 b5→62 |
| 82 | a4 | a6–b8 | Kb4 | K→80,81 b6→70 b5→60 |
| 83 | c4 | a7–b8 | Kb4 | K→80,81 b6→70 b5→60 |
| 84 | c4 | c7–d8 | Kd4 | K→85,86,87 b6→73 b5→63 |
| 85 | d4 | b7–c8 | Kc4 | K→83,84 b6→72 b5→62 |
| 86 | d4 | g6–h8,e8,f8,e6 | Ke4 | K→88,89 b6→74 b5→64 |
| 87 | d4 | d7–f7,g5,h5,d8 | Ke5 | K→90,91,92 b6→75 b5→65 |
| 88 | e4 | e8–h8,h5–h7,f6 | Kf4 | K→94,95 b6→77 b5→67 |
| 89 | e4 | d7–g7,g5,g6,d8 | Ke5 | K→90,91,92 b6→75 b5→65 |
| 90 | e5 | c8–h8,c7,d7,h6–h7 | Kd4 | K→85,86,87 b6→73 b5→63 |
| 91 | e5 | e7–g7,h5 | Kf5 | K→96 b6→78 b5→68 |
| 92 | e5 | g3–g6,h4,h3 | Kd6 | K→97 b6→79 b5→69 |
| 93 | c7 | e1–h8 | Kxb7 | K→58,59 |
| 94 | f4 | g6–h8,e8,f8,e6 | Ke4 | K→88,89 b6→74 b5→64 |
| 95 | f4 | d7–f7,d8,h4–h5 | Ke5 | K→90,91,92 b6→75 b5→65 |
| 96 | f5 | d6–h8,h4 | Ke5 | K→90,91,92 b6→75 b5→65 |
| 97 | d6 | f2–h7 | Kc7 | K→93 b6→76 b5→66 |


## Reproduction

**COMPUTED.** Run the following from the project root. The checker reads the rectangles and reply references directly from this file, generates chess moves square by square, and checks every indicated inclusion, entry and descent. It then builds a separate unrestricted king-and-pawn solver in a temporary directory under K70. That solver uses first promotion, ordinary en passant, checkmate and stalemate. The pawn-group passed-pawn convention and its race rule have no role in game P.

```sh
PYTHONPATH=. .venv/bin/python -B kings/delegate/out/K70/src/check.py
```

**COMPUTED.** The checker covers 486 Black rows with 6,742 positions and 36,408 nonterminal replies, and 97 White rows with 1,088 positions and 3,902 nonterminal replies. It also tests all 716 legal instances of the stated blockade shapes with the allowed pawn material. The unrestricted calculation reproduces the starting outcomes. Its longest optimal Black win takes **38 plies, or 19 Black moves**. This distance is a computed result. The descending proof establishes finiteness without claiming that its moves are fastest.

**COMPUTED.** The commands below regenerate the two sets of printed variations from the saved repertoires, or independently repeat the search that selected each repertoire. They print to standard output.

```sh
PYTHONPATH=. .venv/bin/python -B kings/delegate/out/K70/src/certificate.py
PYTHONPATH=. .venv/bin/python -B kings/delegate/out/K70/src/certificate.py --draw
PYTHONPATH=. .venv/bin/python -B kings/delegate/out/K70/src/repertoire.py
PYTHONPATH=. .venv/bin/python -B kings/delegate/out/K70/src/repertoire.py --draw
```

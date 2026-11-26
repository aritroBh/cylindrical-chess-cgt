# K67 review (coordinator, 2026-11-26)

Question: the other two file classes of the known shape on flat 8×8, {a,b,e} and {a,d,e}; is there a group that
needs a ladder longer than 3?

Investigator: `findings.txt`. Referee (K77, independent; own sum solver s77 and the K74 referee's P solver p74):
`verify/VERIFY.md`. The census paragraph of Corollary 4.17 is the referee's text (`verify/EDITS.md`).

| Statement | Label |
|---|---|
| {a,b,e}: 4,018,737,400 placements, 10 exact over groups; {a,d,e}: 3,992,135,379 placements, 3 | CHECKED-2 (p45a, r48: same six counters, same groups) |
| Each of the 13 is exact (Definition 4.8); 30 near misses are not | five programs on the 13 (ref3m, kp_p, ax65, p74, s77) |
| Four classes: 48 distinct groups, 27 up to reflection and file translation; 5, 19, 24 with 6, 7, 8 men; 10 new; one new shape, `Ka5 kc4/kc5 Pa4 Pa6 Pb2 pa7` | recount by the referee from CHECKED-2 lists |
| Of the 10 new: (B1) for 7; Aux won for 2 (C014_04, C014_09); Aux lost for 1, `Kd5 kf4/kf5 Pa2 Pb3 Pe2 pa5 pb4 pe5` at …e5–e4, N\* = 2 | CHECKED-2 (ax65, pk_sum, s77; two authors) |
| Over all 48: (B1) 34; Aux won 9; Aux lost 5 (N\* = 3 once, 2 four times). No group with N\* ≥ 4 | CHECKED-2 |
| In chess `Kc4 ke4/ke5 Pd2 Pd5 Pe6 pd6 pe7` and `Kf4 kd4/kd5 Pd6 Pe2 Pe5 pd7 pe6` are exact over groups; C014_01, C014_04, C014_05 are not | KNOWN (tablebase; two evaluations) |
| 7 of the 24 groups with at most seven men are exact in chess | KNOWN |

Correction by the referee, taken over: the seven chess-exact groups are two shapes, not five (C125_05, C145_07,
C145_09, C034_01, C034_02 are one shape up to reflection and translation; C125_08, C125_10 the other).

Not done: the seven two-file classes that lie in none of the four classes ({a,c}, {a,f}, {a,g}, {a,h}, {b,d},
{b,g}, {c,e} up to reflection); other shapes; other boards.

Process notes. Investigator: an early hand-back stopped its first search after two minutes (own PIDs; redone
from the start); 11.3 h of solver time against a budget of 10; its two long searches held both slots for an
hour and a half. Referee: one five-second run started without recording its PID.

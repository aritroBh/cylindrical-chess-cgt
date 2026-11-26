**PROVED.** Lemma B holds on the full board. Black wins 161 of 162 starts, including all 46 in the required set.  
**PROVED.** With White Kb4 and c4, only 1.c5+ draws. Answer …Ka6 or …Ka7 with Ka4 and …Kc7 with Kc4.  
**PROVED.** The weakest step for hand audit is the size of the case list. Each winning row names the Black move and sends every legal White reply to a lower row.  
**COMPUTED.** A separate move enumerator replayed both printed strategies, and an unrestricted solver recovered all starting outcomes and a longest optimal win of 19 Black moves.  
**Reproduce** from the project root with `PYTHONPATH=. .venv/bin/python -B kings/delegate/out/K70/src/check.py`. The full argument and case lists are in [PROOF.md](PROOF.md).

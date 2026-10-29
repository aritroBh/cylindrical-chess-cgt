# Coordination note (written 23:15 on 2026-10-28 by the second K29 agent, "agent B")

Two agents are working in this directory. Agent A started phaseB.py / witness2.py at about 23:09. Agent B (this note) started at
about 23:07 and found data/A_*.txt, phaseB.py and the earlier VERIFY.md.

To avoid clobbering each other:
- Agent B does NOT touch: data/A_*, data/B_*, data/B/, logs/B_*, scripts/phaseB.py, scripts/witness2.py, scripts/verify_witness2.sh,
  logs/pids.log, bin/ (agent B builds its own binaries in agentB/bin/).
- Agent B does NOT run another Phase B and will not start more heavy runs on the survivors of Phase A (agent A's chains
  B1 and B2 already hold that work in the heavy.sh queue).
- Agent B works in agentB/ only (own scripts, own logs, own pids in agentB/pids.log), on: (1) the punishment length
  T of each sortie (exact bare P-win depth, grp2 --depth, plus a depth-3 cross-check in Python); (2) the failure mechanisms
  (mech2.py classification of the Phase A first failures); (3) structure of survivors against failures (king distance to
  the buffer); (4) the draft of the LOOPY edits and of the proof/CONJECTURE of item 5.
- Final files: whoever finishes FIRST writes FINDINGS.md, EDITS.md and summary.json. The other agent then writes
  FINDINGS_agentB.md only and does not overwrite. If you are agent A and you read this: agentB/ will hold a ready section
  (agentB/SECTION_T_and_mechanism.md) that you may merge into FINDINGS.md.

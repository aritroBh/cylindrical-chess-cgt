# T55: Q-family coverage for the even n+2 ring proof

Read delegate/COMMON.md first and obey it (no pattern kills, kill only your own PIDs, max 2 processes, nice -n 15, under 4GB each, label claims COMPUTED-1 vs CHECKED-2, never claim a number your own run did not print, no git commit or push).

## Background
research/ring_family_proof/PROOF.md proves the even n+2 ring family is *2, but only states the NNPN and NNPP cases. The T53 referee report (research/ring_n_plus_2_check/REPORT.md) found the proof SOUND conditional on its finite check C1', and flagged that research/ring_family_proof/run_all.sh also runs Q-family configurations that PROOF.md never describes.

## Task
Work in a new folder research/ring_q_family_check/.
1. Read PROOF.md, run_all.sh, and the T53 REPORT.md. List exactly which Q-family configurations run_all.sh exercises and what outcomes were computed for them.
2. Decide which gap this is: (a) the proof argument already covers the Q family but was never written down, (b) the Q family needs its own induction or base cases, or (c) the computed Q outcomes are not actually *2 / not covered at all.
3. Close it: either write PROOF_Q.md extending the argument rigorously to the Q family, or run the finite verification the induction needs (each base case evaluated with the cylcgt whole-board solver, cross-checked per COMMON.md labelling).
4. Write research/ring_q_family_check/REPORT.md with your verdict, the evidence, and every number traceable to a run you executed (include the scripts you used in the folder).

Do not edit PROOF.md, RESULTS.md, or the paper. Report only.
# K41: post-commit check of 2061cea4, 8eba35c5, 80bae8e1 (K28, K15b+K26, K29)

Check `git show` of the three commits (kings/theory/LOOPY.md, kings/REPORT.md) against their sources in
`kings/delegate/out/K28/`, `K15/`, `K26/`, `K15K26/`, `K29/`. For each changed passage: numbers match the VERIFY files,
labels follow LOOPY's label rule, no surviving text contradicts the new results, table cells unchanged. Write no file
except `kings/delegate/out/K41/CHECK.md`; edit nothing; one permitted git command: `git show`.

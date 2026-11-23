# K46: post-commit check of 3cc612a8, dc9c51a6 and a85b211a

For each commit, check that the edit files named in the item REVIEW.md files (K38, K40, K41, K39, K42, K43, K44) were
applied exactly to the parent LOOPY.md, that table cell counts are unchanged except K42's new row, and that every number
and label in the new LOOPY and REPORT text matches its VERIFY.md (VERIFY takes precedence over investigator files).
Also flag text made stale by later items (for example §8 item 2 vs K44's over roots). Read-only except
out/K46/CHECK.md. Report each finding as file:line, severity, OLD, NEW. Use only `git show` for git.

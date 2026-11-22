"""Post-pass on the proof notes before typesetting (Sections S12-S16 of the supplement).
Removes working-note residue without touching mathematics:
  - task and agent IDs (K7, K13b, T50, T62, ...): a parenthetical that names one is dropped
    ("(revised after K7, 2026-10-22)"); a sentence that names one and has no math is dropped;
    in a sentence with math the ID is replaced by a neutral word; T50 (the wall-ring proof) becomes "Section S13";
  - shell command lines (code blocks and inline code with python, .venv, nice, cd ...), and sentences that only
    give where logs or scripts live;
  - repository paths that are not needed to state a result (the proof notes that are typeset here are renamed
    to their supplement section);
  - the repeated status lines about human checking (one statement at the head of the proofs part replaces them).
Hypothesis names such as (K1), (K2), (T1)-(T4) are not IDs and are kept. Math ($...$) is never edited: a
sentence that contains math is never dropped, only its non-math ID/path tokens are replaced."""
import re

ID = r'\b(?:K(?:[3-9]|\d{2,})[a-z]*|K[12][a-z]+|T\d{2,}[a-z]*)\b'
ID_RE = re.compile(ID)
SHELL = re.compile(r'(\.venv|python|PYTHONPATH|nice -n|/usr/bin/time|\bcd |run_all\.sh|\bsh research|tectonic )')
NOTES = [  # paths of notes that are typeset in this supplement -> their section
    (r'research/ring_family_proof/proof\.tex', 'Section S13'),
    (r'research/ring_n_plus_2_proof/PROOF\.md', 'Note 1 of Section S15'),
    (r'PROOF\.md', 'Note 1 of Section S15'),
    (r'research/ring_n_plus_2_proof/PROOF_Q\.md', 'Note 2 of Section S15'),
    (r'research/ring_n_plus_2_proof/PROOF_odd\.md', 'Note 3 of Section S15'),
    (r'PROOF_odd\.md', 'Note 3 of Section S15'),
    (r'research/star3_proof/PROOF_S3T3\.md', 'Note 4 of Section S15'),
    (r'research/ring_n_proof/PROOF_N\.md', 'Section S14'),
    (r'proof\.tex', 'Section S13'),
]
PATHLIKE = re.compile(r'`[^`]*(?:/|\.py|\.log|\.txt|\.c\b|\.md|\.sh)[^`]*`')
HUMAN = re.compile(r'(?i)\bhuman\b')
MATH = re.compile(r'\$[^$]*\$')
LOGSENT = re.compile(r'^\s*(Logs?|Rerun|Scripts?|Raw output|Output|Command)\b', re.I)

def _protect(s):
    keep = []
    def f(m):
        keep.append(m.group(0)); return '\x02%d\x03' % (len(keep) - 1)
    return MATH.sub(f, s), keep

def _restore(s, keep):
    return re.sub('\x02(\\d+)\x03', lambda m: keep[int(m.group(1))], s)

IMPERSONAL = [  # first person and "the author" in the notes (anonymous supplement)
    ('has not yet been refereed by a model other than the author', 'has not yet been refereed by a second model'),
    ('I rebuilt the raw-flag graph', 'The raw-flag graph was rebuilt'),
    ('I checked the numbers this note cites', 'The numbers this note cites were checked'),
    ('by my own rebuild', 'by a separate rebuild'),
    ('and my spot runs', 'and spot runs'),
    ('My own re-check', 'A separate re-check'),
    ('and my rerun', 'and a rerun'),
    ('my rerun', 'a rerun'),
    ('my own re-check', 'a separate re-check'),
]

import unicodedata
KEEPWORDS = re.compile(r'\*\*|\b(Theorem|Lemma|Proposition|Corollary|Definition|Remark|Proof|PROVED|FALSE|GAP|'
                       r'CONJECTURE|CHECKED-2|COMPUTED-1|Claim|Step|Case|instance|hypothes[ie]s|implies|iff|if and only if)\b|\d{2,}')

def _mathy(s):
    # LOOPY.md writes its mathematics in Unicode, not $...$: any math symbol, Greek letter or '=' counts
    return '$' in s or '=' in s or any(ord(ch) > 127 and (unicodedata.category(ch) == 'Sm'
                                       or 'GREEK' in unicodedata.name(ch, '')) for ch in s)

def _clean_sentence(s):
    for a, b in IMPERSONAL:
        s = s.replace(a, b)
    s = re.sub(r'\s*\(an AI check; no human has re-derived it\)', ' (an AI check)', s)
    s = re.sub(r'[;,]\s*no human has re-derived (?:it|them|any of them)', '', s)
    s = re.sub(r'[;,]\s*human check pending', '', s, flags=re.I)
    if 'did not write a REPORT' in s:
        return ''
    has_math = _mathy(s) or bool(KEEPWORDS.search(s))
    if not has_math and (HUMAN.search(s) or LOGSENT.match(s)):
        return ''
    t, keep = _protect(s)
    # notes typeset here: name their section instead of the path
    for pat, rep in NOTES:
        t = re.sub(r'`' + pat + r'`', rep, t)
        t = re.sub(r'(?<![\w/])' + pat, rep, t)
    t = re.sub(r"\bT50's\b", "Section S13's", t)
    t = re.sub(r'\bT50\b', 'Section S13', t)
    # inline shell commands
    if SHELL.search(t):
        if not has_math:
            return ''
        t = re.sub(r'`[^`]*`', lambda m: '' if SHELL.search(m.group(0)) else m.group(0), t)
        t = re.sub(r'`\.\.\.[^`]*`', '', t)
    # parentheticals that only carry IDs, dates or paths
    def paren(m):
        inner = m.group(1)
        if '\x02' in inner:
            return m.group(0)
        if ID_RE.search(inner) or PATHLIKE.search(inner) or re.search(r'\b20\d\d-\d\d-\d\d\b', inner):
            return ''
        return m.group(0)
    for _ in range(3):
        t = re.sub(r'\s?\(([^()]*)\)', paren, t)
    if ID_RE.search(t):
        if not has_math:
            return ''
        t = re.sub(r"(^|(?<=[.:] ))" + ID + r"('s)?\b", lambda m: m.group(1) + ('A referee' + (m.group(2) or '')), t)
        t = re.sub(r"\s*" + ID + r"'s\b", " a referee's", t)
        t = re.sub(r'\s*' + ID, '', t)
    # remaining path-like code spans not needed to state a result
    t = PATHLIKE.sub(lambda m: '' if re.search(r'(logs?/|\.log|\.py|\.sh|\.txt|\.json|scripts?/|delegate/|REPORT|VERIFY|_check)', m.group(0)) else m.group(0), t)
    t = re.sub(r'`\.\.\.[^`]*`', '', t)
    t = re.sub(r'`[^`]*\b(?:K|T)\d+_[^`]*`', '', t)          # environment switches named after tasks
    t = re.sub(r'\s*=\s*,', ' =', t)
    t = re.sub(r',\s*,', ',', t)
    t = re.sub(r'\b(with|against)\s+(?=(on|and|for|in)\b)', '', t)
    t = re.sub(r'\s+(in|via)(?=[;,)])', '', t)
    t = re.sub(r'(\s*->\s*)+(?=[:;,.)]|$)', '', t)
    t = re.sub(r'^\s*->\s*', '', t)
    t = re.sub(r'(?<=[:;,])\s*->\s+', ' ', t)
    t = re.sub(r'\*\*(\w)\*\* = \(', r'**\1** (', t)
    t = re.sub(r'[;,]\s*\)', ')', t)
    t = re.sub(r'\(\s*\)', '', t)
    t = re.sub(r'::', ':', t)
    t = re.sub(r'\bby \(', 'by a referee (', t)
    t = re.sub(r',\s*:', ':', t)
    t = re.sub(r'[;,]?\s*\b(?:[Rr]evised|[Rr]estored|[Ww]ording corrected)\s+after[^;:()]*?(?:\d{4}-\d\d-\d\d|referee)', '', t)
    t = re.sub(r',?\s*\b20\d\d-\d\d-\d\d\b', '', t)
    t = re.sub(r'\(\s*[;,:]+\s*', '(', t)
    t = re.sub(r"\s+(?:in|by|is in)\s*\)", ')', t)
    t = re.sub(r'(?:\s*[;,]){2,}', ';', t)
    t = re.sub(r'\s+(?:of|by|from) and\b', '', t)
    t = re.sub(r'\(\s*(?:new)?\s*\)', '', t)
    t = re.sub(r'\(\s*\)', '', t)
    t = re.sub(r'\s+([,;.:])', r'\1', t)
    t = re.sub(r'  +', ' ', t)
    return _restore(t, keep)

SPLIT = re.compile(r'(?<=[.])\s+(?=[A-Z(*])')

def _clean_text(text):
    t, keep = _protect(text)
    parts = SPLIT.split(t)
    out = [_clean_sentence(_restore(p, keep)) for p in parts]
    return ' '.join(p for p in out if p.strip())

LISTSTART = re.compile(r'^\s*(?:[-*+]|\d+[.)])\s+')

def clean(lines):
    """Clean whole paragraphs and list items (their wrapped lines joined), so that a sentence is never cut at a
    line break; tables, headings and code blocks are handled line by line."""
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith('```'):
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith('```'):
                j += 1
            block = lines[i:j + 1]
            if not SHELL.search('\n'.join(block)):
                out += block
            i = j + 1
            continue
        if ln.strip().startswith('|'):
            cells = ln.split('|')
            out.append('|'.join(_clean_text(c) if c.strip() and not re.fullmatch(r'\s*:?-{2,}:?\s*', c) else c
                                for c in cells))
            i += 1
            continue
        mh = re.match(r'^(\s*#+\s+)(.*)$', ln)
        if mh:
            h = re.sub(r'\s*\((?:rerun|reruns|logs?|scripts?)\b[^()]*\)', '', mh.group(2), flags=re.I)
            out.append(mh.group(1) + (_clean_text(h) or h))
            i += 1
            continue
        if not ln.strip():
            out.append(ln)
            i += 1
            continue
        m = LISTSTART.match(ln)
        lead = m.group(0) if m else ''
        body = [ln[len(lead):].strip() if m else ln.strip()]
        indent = ln[:len(ln) - len(ln.lstrip())]
        j = i + 1
        while j < len(lines):
            nx = lines[j]
            if (not nx.strip() or LISTSTART.match(nx) or nx.strip().startswith(('|', '```')) or
                    re.match(r'^\s*#+\s+', nx)):
                break
            body.append(nx.strip())
            j += 1
        c = _clean_text(' '.join(body))
        if c.strip():
            out.append((lead if m else indent) + c)
        i = j
    return out

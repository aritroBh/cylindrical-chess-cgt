r"""Minimal Markdown -> LaTeX converter for the proof notes (pandoc is not installed).
Typesets only: headings, paragraphs, nested lists, pipe tables, code blocks, inline code, bold/italic, links,
and passes $...$ / $$...$$ math through unchanged. Unicode is left as is (the supplement uses XeTeX with
STIX Two Text / STIX Two Math). Usage: md2tex.py in.md out.tex [first_line last_line] [--top-level N]
Heading levels: '#' -> \subsection*, '##' -> \subsubsection*, '###' and deeper -> \paragraph*."""
import re, sys

def esc_text(t):
    rep = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}', '#': r'\#', '%': r'\%', '&': r'\&',
           '_': r'\_', '^': r'\textasciicircum{}', '~': r'\textasciitilde{}', '$': r'\$'}
    return ''.join(rep.get(c, c) for c in t)

import unicodedata

def _sym(c, wrap):
    return wrap % c if ord(c) > 127 and unicodedata.category(c) in ('Sm', 'So') else c

SUPSUB = {'⁰': r'\textsuperscript{0}', '⁺': r'\textsuperscript{+}', '₀': r'\textsubscript{0}',
          '₁': r'\textsubscript{1}', 'ȳ': r'\ensuremath{\bar{y}}', '′': r'\ensuremath{{}^{\prime}}',
          '″': r'\ensuremath{{}^{\prime\prime}}', '‴': r'\ensuremath{{}^{\prime\prime\prime}}'}

def text_glyphs(s):
    # glyphs that the text fonts lack: math symbols go to the math font, super/subscripts to \textsuper/subscript
    s = re.sub('(.)\u0304', lambda m: r'\ensuremath{\bar{%s}}' % m.group(1), s)
    return ''.join(SUPSUB.get(c) or _sym(c, r'\ensuremath{%s}') for c in s)

def esc_code(t):
    s = ''.join(_sym(c, r'\textrm{%s}') for c in esc_text(t))
    return r'\texttt{' + s.replace('-', '-{}').replace('<', r'\textless{}').replace('>', r'\textgreater{}') + '}'

SUB = str.maketrans({'₀': '_0', '₁': '_1', '₂': '_2', '₃': '_3', '₄': '_4', '₅': '_5', '₆': '_6', '₇': '_7',
                     '₈': '_8', '₉': '_9'})

def fix_math(m):
    m = m.translate(SUB)
    m = m.replace('\u2223', r'\mid ')
    return m

def emph(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'\\emph{\1}', s)
    return s

TOK = re.compile(r'(\$\$.+?\$\$|\$[^$\n]+?\$|`[^`]+`|\[[^\]]+\]\([^)]+\))')

def inline(s):
    toks = []
    def keep(m):
        part = m.group(0)
        if part.startswith('$$'):
            r = r'\[' + fix_math(part[2:-2]) + r'\]'
        elif part.startswith('$'):
            r = '$' + fix_math(part[1:-1]) + '$'
        elif part.startswith('`'):
            r = esc_code(part[1:-1])
        else:
            mm = re.match(r'\[([^\]]+)\]\(([^)]+)\)', part)
            r = inline(mm.group(1)) + ' (' + esc_code(mm.group(2)) + ')'
        toks.append(r)
        return '\x00%d\x01' % (len(toks) - 1)
    s = TOK.sub(keep, s)
    s = esc_text(s).replace('<', r'\textless{}').replace('>', r'\textgreater{}')
    s = text_glyphs(s)
    s = emph(s)
    s = s.replace('*', r'\textasteriskcentered{}')
    return re.sub('\x00(\\d+)\x01', lambda m: toks[int(m.group(1))].replace('\\', '\\\\'), s).replace('\\\\', '\\') if False else re.sub('\x00(\\d+)\x01', lambda m: toks[int(m.group(1))], s)

def table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r':?-{2,}:?', c) or c == '' for c in r)]
    n = max(len(r) for r in cells)
    lens = [max(1, sum(len(r[j]) if j < len(r) else 0 for r in cells)) for j in range(n)]
    tot = sum(min(l, 4 * sum(lens) / n) for l in lens)
    widths = [max(0.08, min(l, 4 * sum(lens) / n) / tot) * (0.98 - 0.02 * n) for l in lens]
    spec = ''.join(r'>{\raggedright\arraybackslash}p{%.3f\linewidth}' % w for w in widths)
    # longtable is not in the offline TeX bundle: long tables are split into chunks of at most 18 rows,
    # each a tabular that repeats the header row
    head = ' & '.join(inline(c) for c in cells[0] + [''] * (n - len(cells[0]))) + r' \\'
    body = [' & '.join(inline(c) for c in r + [''] * (n - len(r))) + r' \\' for r in cells[1:]]
    out = []
    for k in range(0, max(1, len(body)), 18):
        out += [r'\par\noindent{\small\setlength{\tabcolsep}{3pt}\begin{tabular}{@{}' + spec + '@{}}', r'\toprule', head,
                r'\midrule'] + body[k:k + 18] + [r'\bottomrule', r'\end{tabular}}\par\smallskip']
    return out

def convert(lines):
    out, i, stack, para = [], 0, [], []
    def flush():
        if para:
            out.append(inline(' '.join(para)))
            out.append('')
            para.clear()
    def close_lists(indent=-1):
        while stack and stack[-1][0] > indent:
            out.append(r'\end{%s}' % stack.pop()[1])
    while i < len(lines):
        ln = lines[i].rstrip('\n')
        if ln.strip().startswith('```'):
            flush(); close_lists()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith('```'):
                j += 1
            out.append(r'\begin{small}\begin{verbatim}')
            out += [l.rstrip('\n') for l in lines[i + 1:j]]
            out.append(r'\end{verbatim}\end{small}')
            i = j + 1
            continue
        if ln.strip().startswith('|'):
            flush(); close_lists()
            j = i
            while j < len(lines) and lines[j].strip().startswith('|'):
                j += 1
            out += table(lines[i:j])
            i = j
            continue
        m = re.match(r'^(#{1,6})\s+(.*)', ln)
        if m:
            flush(); close_lists()
            lev = len(m.group(1))
            cmd = {1: 'subsection*', 2: 'subsubsection*'}.get(lev, 'paragraph*')
            out.append('\\%s{%s}' % (cmd, inline(m.group(2))))
            i += 1
            continue
        if re.fullmatch(r'\s*(---+|\*\*\*+)\s*', ln):
            flush(); close_lists()
            out.append(r'\medskip\hrule\medskip')
            i += 1
            continue
        m = re.match(r'^(\s*)([-*+]|\d+[.)])\s+(.*)', ln)
        if m:
            flush()
            ind = len(m.group(1).expandtabs(4))
            kind = 'itemize' if m.group(2) in '-*+' else 'enumerate'
            close_lists(ind)
            if not stack or stack[-1][0] < ind:
                out.append(r'\begin{%s}' % kind)
                stack.append((ind, kind))
            text = [m.group(3)]
            i += 1
            while i < len(lines):
                nx = lines[i].rstrip('\n')
                if not nx.strip() or re.match(r'^\s*([-*+]|\d+[.)])\s+', nx) or nx.strip().startswith(('|', '```', '#')):
                    break
                text.append(nx.strip())
                i += 1
            out.append(r'\item ' + inline(' '.join(text)))
            continue
        if not ln.strip():
            flush()
            # a blank line ends a list only if the next line is not indented list content
            if stack and i + 1 < len(lines) and not re.match(r'^\s+\S|^\s*([-*+]|\d+[.)])\s+', lines[i + 1]):
                close_lists()
            i += 1
            continue
        if stack and re.match(r'^\s+\S', ln):  # continuation paragraph inside a list item
            out.append(inline(ln.strip()))
            i += 1
            continue
        close_lists()
        para.append(ln.strip())
        i += 1
    flush(); close_lists()
    return out

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    lines = open(src, encoding='utf-8').read().split('\n')
    if len(sys.argv) > 4:
        lines = lines[int(sys.argv[3]) - 1:int(sys.argv[4])]
    open(dst, 'w', encoding='utf-8').write('\n'.join(convert(lines)) + '\n')

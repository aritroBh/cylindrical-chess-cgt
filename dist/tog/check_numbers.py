"""Number check for the ToG version (dist/tog).
Extracts every number from the long version's abstract, introduction, Section VIII (the *2 question) and
conclusion (paper/ieee/sections/00_abstract, 01_intro, 08_star2, 14_conclusion): integers with at least two
digits (thousands separators allowed), percentages and decimals. Checks that each still appears in the
anonymous main PDF (build/tog_review.pdf) or in the supplement (build/supplement_review.pdf).
Run from dist/tog after sbuild.sh:  python3 check_numbers.py > check_numbers.out"""
import re, subprocess, sys

SRC = ['00_abstract', '01_intro', '08_star2', '14_conclusion']
PDFS = ['build/tog_review.pdf', 'build/supplement_review.pdf']

def strip_tex(s):
    s = re.sub(r'(?m)(?<!\\)%.*$', '', s)                                  # comments
    s = re.sub(r'\\(label|ref|cite|includegraphics|begin|end|setlength)\*?(\[[^\]]*\])?\{[^}]*\}', ' ', s)
    s = re.sub(r'\[[^\]]*\\(column|text|line)width[^\]]*\]', ' ', s)       # widths in optional args
    s = re.sub(r'\{[0-9.]+\\(column|text|line)width\}', ' ', s)
    s = s.replace('{,}', ',')
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)                                  # control words (\le60 -> ' 60')
    return s

NUM = re.compile(r'(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+\.\d+|\d+)(\\?%)?(?![\w])')

def numbers(text):
    out = []
    for m in NUM.finditer(text):
        n, pct = m.group(1), m.group(2)
        if pct or '.' in n or len(n.replace(',', '')) >= 2:
            out.append(n + ('%' if pct else ''))
    return out

def pdf_text(p):
    t = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True).stdout
    t = t.replace('\u2009', '').replace('\u202f', '')
    t = re.sub(r'-\n\s*', '', t)          # hyphenation at line ends
    return t

def found(num, text):
    core = num.rstrip('%')
    variants = {core, core.replace(',', '')}
    for v in variants:
        pat = r'(?<![\d.,])' + re.escape(v) + r'(?![\d])' + (r'\s*%' if num.endswith('%') else '')
        if re.search(pat, text):
            return True
    return False

def main():
    texts = {p: pdf_text(p) for p in PDFS}
    allok = True
    print('number check: long-version numbers from', ', '.join(SRC))
    print('searched in', ', '.join(PDFS))
    print()
    for sec in SRC:
        src = strip_tex(open('../../paper/ieee/sections/%s.tex' % sec).read())
        nums = list(dict.fromkeys(numbers(src)))
        print('== %s: %d distinct numbers (two-digit integers are weak tests: they occur everywhere)' % (sec, len(nums)))
        for n in nums:
            where = [p.split('/')[-1].replace('.pdf', '') for p in PDFS if found(n, texts[p])]
            status = 'OK  ' if where else 'MISSING'
            allok &= bool(where)
            print('  %-8s %-14s %s' % (status, n, ', '.join(where)))
        print()
    print('RESULT:', 'all numbers found' if allok else 'some numbers missing (see MISSING lines)')

if __name__ == '__main__':
    main()

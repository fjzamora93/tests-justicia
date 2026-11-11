import fitz, re, json, sys
QRE = re.compile(r'^\s*(\d{1,3})\s*(?:\.-|\.|-|\))\s*(.*)$')
ORE = re.compile(r'^\s*([a-dA-D])\s*\)\s*(.*)$')
def lines(path):
    d = fitz.open(path)
    for pno, p in enumerate(d):
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                spans = [(s['text'], ('Bold' in s['font']) or bool(s['flags'] & 16)) for s in l['spans']]
                txt = ''.join(t for t, _ in spans)
                if not txt.strip(): continue
                if re.fullmatch(r'\s*\d+\s*', txt) and l['bbox'][1] > p.rect.height*0.85: continue
                yield pno+1, txt, spans
def parse(path):
    qs, cur, opt, header = [], None, None, ''
    for pno, txt, spans in lines(path):
        m = QRE.match(txt); o = ORE.match(txt)
        nonblank = [(t, b) for t, b in spans if t.strip()]
        allbold = nonblank and all(b for _, b in nonblank)
        firstbold = nonblank[0][1] if nonblank else False
        n = int(m.group(1)) if m else -1
        if m and not firstbold and (cur is None or len(cur['opts']) == 4 or n == cur['n'] + 1 or n == 1 or (not cur['opts'] and n > cur['n'])):
            if cur: qs.append(cur)
            cur = {'n': int(m.group(1)), 'page': pno, 'header': header, 'stem_spans': list(spans), 'opts': [], 'bold': []}
            opt = None
            continue
        if cur is None:
            header += ' ' + txt.strip(); continue
        if o and len(cur['opts']) < 4 and o.group(1).lower() == 'abcd'[len(cur['opts'])]:
            cur['opts'].append(o.group(2).strip()); cur['bold'].append(bool(allbold)); opt = len(cur['opts'])-1
            continue
        if opt is not None and len(cur['opts']) == 4 and opt == 3 and allbold and not cur['bold'][3] and txt.strip().isupper():
            # likely a section header after the question
            qs.append(cur); cur = None; header = txt.strip(); continue
        if opt is None:
            cur['stem_spans'] += [(' ', False)] + spans
        else:
            cur['opts'][opt] += ' ' + txt.strip()
            cur['bold'][opt] = cur['bold'][opt] and bool(allbold) if False else (cur['bold'][opt] or bool(allbold))
    if cur: qs.append(cur)
    out = []
    for q in qs:
        plain = ''.join(t for t, b in q['stem_spans'] if not b)
        bold = ' '.join(t.strip() for t, b in q['stem_spans'] if b and t.strip())
        out.append({'n': q['n'], 'page': q['page'], 'stem': re.sub(r'\s+', ' ', plain).strip(),
                    'ref': re.sub(r'\s+', ' ', bold).strip(), 'options': [re.sub(r'\s+',' ',x) for x in q['opts']],
                    'bold': q['bold']})
    return out
if __name__ == '__main__':
    res = parse(sys.argv[1]); json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    ok = [q for q in res if len(q['options']) == 4 and sum(q['bold']) == 1]
    print(sys.argv[1], 'total', len(res), 'ok', len(ok))

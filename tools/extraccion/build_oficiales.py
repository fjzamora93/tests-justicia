import json, sys, re, glob, os, collections
sys.path.insert(0, os.path.dirname(__file__)); from temas import *
SP = os.path.dirname(os.path.abspath(__file__))  # raw_*.json (salida de parse.py) y lopj_part*.json
OUT = '/home/javier/Desktop/Projects/AngularAplicacionTests/src/assets/examenes_oficiales/preguntas_oficiales.json'
CUERPOS = {'auxilio_judicial': 'Auxilio Judicial', 'gestion_procesal': 'Gestión Procesal', 'trami_libre': 'Tramitación Procesal'}
def clean(s): return re.sub(r'[⁠​]', '', re.sub(r'\s+', ' ', s)).strip()
def strip_num(stem): return re.sub(r'^\s*\d{1,3}\s*(?:\.-|\.|-|\))\s*', '', stem).strip()
def key(stem): return re.sub(r'[^a-z0-9]', '', norm(strip_num(stem)).lower())
out, seen, stats = [], set(), collections.Counter()
for f, cuerpo in CUERPOS.items():
    exam = 0
    for q in json.load(open(f'{SP}/raw_{f}.json')):
        if q['n'] == 1: exam += 1
        if EXCLUDE.search(norm(q['ref'])): stats['excluida_derogada_anulada'] += 1; continue
        if len(q['options']) != 4 or sum(q['bold']) != 1: stats['formato_incompleto'] += 1; continue
        stem = clean(strip_num(q['stem'])).rstrip(' :') + ':' if not clean(q['stem']).endswith('?') else clean(strip_num(q['stem']))
        stem = re.sub(r'\(\s*Pregunta de reserva[^)]*\)\s*', '', stem, flags=re.I)
        k = key(stem) + '|' + key(' '.join(q['options']))
        if k in seen: stats['duplicada'] += 1; continue
        seen.add(k)
        out.append({'id': f'of-{f}-{exam}-{q["n"]}', 'origen': 'oficial', 'tema': classify(q['ref'], q['stem']),
                    'bloque': bloque(q['ref']), 'articulo': articulo(q['ref']), 'enunciado': stem,
                    'opciones': [clean(o) for o in q['options']], 'correcta': q['bold'].index(True),
                    'fuente': f'{cuerpo} · Examen oficial {exam}'})
for p in sorted(glob.glob(f'{SP}/lopj_part*.json')):
    for q in json.load(open(p)):
        if q.get('uncertain') or len(q.get('options', [])) != 4: stats['lopj_incierta'] += 1; continue
        stem = clean(q['stem']); k = key(stem) + '|' + key(' '.join(q['options']))
        if k in seen: stats['duplicada'] += 1; continue
        seen.add(k)
        out.append({'id': f'of-tests_lopj-{q["page"]}-{q["n"]}', 'origen': 'oficial', 'tema': classify(q.get('section', ''), stem) if 'LOPJ' in norm(q.get('section', '')) and 'SECRETARIOS' not in norm(q.get('section', '')) else classify(q['ref'] + ' ' + q.get('section', ''), stem),
                    'bloque': bloque(q.get('section') or q['ref']), 'articulo': articulo(q['ref']), 'enunciado': stem,
                    'opciones': [re.sub(r'^[a-dA-D]\) ', '', clean(o)) for o in q['options']], 'correcta': q['correct'],
                    'fuente': 'Tests LOPJ y reglamentos'})
ids = collections.Counter(q['id'] for q in out)
for q in out:
    if ids[q['id']] > 1: q['id'] += '-' + key(q['enunciado'])[:6]
json.dump(out, open(OUT, 'w'), ensure_ascii=False, indent=1)
json.dump([{'id': i, 'nombre': n} for i, n in TEMAS], open('/home/javier/Desktop/Projects/AngularAplicacionTests/src/assets/temas.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), dict(stats)); print(collections.Counter(q['tema'] for q in out).most_common())

"""Valida los lotes de tests_claude y regenera index.json."""
import json, glob, os, re, collections
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../src/assets')
temas = {t['id'] for t in json.load(open(f'{BASE}/temas.json'))}
oficiales = {re.sub(r'\W', '', q['enunciado'].lower()) for q in json.load(open(f'{BASE}/examenes_oficiales/preguntas_oficiales.json'))}
lotes, ids, vistos = [], set(), set()
for p in sorted(glob.glob(f'{BASE}/tests_claude/lote_*.json')):
    qs = json.load(open(p)); errores = []
    for q in qs:
        k = re.sub(r'\W', '', q['enunciado'].lower())
        if q['id'] in ids: errores.append(f"id duplicado {q['id']}")
        if q['tema'] not in temas: errores.append(f"tema desconocido {q['tema']} ({q['id']})")
        if len(q['opciones']) != 4 or not 0 <= q['correcta'] <= 3: errores.append(f"formato {q['id']}")
        if k in oficiales: errores.append(f"repite oficial {q['id']}")
        if k in vistos: errores.append(f"repite generada {q['id']}")
        ids.add(q['id']); vistos.add(k)
    pos = collections.Counter('abcd'[q['correcta']] for q in qs)
    print(os.path.basename(p), len(qs), dict(collections.Counter(q['tema'] for q in qs)), 'pos', dict(sorted(pos.items())), errores or 'OK')
    lotes.append(os.path.basename(p))
json.dump({'lotes': lotes}, open(f'{BASE}/tests_claude/index.json', 'w'), ensure_ascii=False, indent=1)
print('index.json ->', lotes)

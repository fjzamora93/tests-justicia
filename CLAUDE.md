# AngularAplicacionTests

Aplicación Angular 21 (standalone + signals, SCSS, Tailwind) de tests para oposiciones de Justicia
(Auxilio Judicial, Tramitación Procesal, Gestión Procesal).

Especificaciones funcionales del proyecto (fuentes, temas, modalidades, estilo):
@INSTRUCCIONES.md

## Código

- `src/app/features/tests/data/preguntas.service.ts`: carga `temas.json`, las preguntas oficiales y los lotes de `tests_claude/` (vía `index.json`); filtra por tema/modalidad y baraja.
- `src/app/features/tests/pages/test-library.component.*`: selector de modalidad, tema (norma) y número de preguntas.
- `src/app/features/tests/pages/test-player.component.*`: test; preselección + botón «Ver respuesta» por pregunta.
- Arranque: `npm start` (http://localhost:4200). Build: `npm run build`. El aviso de presupuesto del bundle inicial viene de Firebase (ya existía).
- Despliegue: `npm run deploy` publica en https://fjzamora93.github.io/tests-justicia/ (rama `gh-pages`, sin PDFs).

## Generar preguntas nuevas (procedimiento)

1. Extraer texto del material: `pdftotext -layout src/assets/material/<pdf> <scratchpad>/<nombre>.txt`.
2. Revisar `src/assets/examenes_oficiales/preguntas_oficiales.json` (modelo de estilo y jerga) y **todos** los `src/assets/tests_claude/lote_*.json` existentes para no repetir preguntas ni artículos ya cubiertos.
3. Redactar en el formato de pregunta de INSTRUCCIONES.md: 4 opciones, una correcta, respuesta verificada contra el texto del material, artículo citado en `explicacion`, posición de la correcta repartida entre a/b/c/d. `tema` debe ser un id de `src/assets/temas.json`.
4. Guardar como nuevo lote `src/assets/tests_claude/lote_<AAAA-MM-DD>_<materia>.json` y ejecutar `python3 tools/extraccion/validar_lotes.py`: comprueba ids, temas, formato, repeticiones con oficiales/generadas y reparto a/b/c/d, y **regenera `src/assets/tests_claude/index.json`**.

## Re-extraer las preguntas oficiales

Scripts en `tools/extraccion/` (ejecutar desde esa carpeta):

```bash
for f in auxilio_judicial gestion_procesal trami_libre; do
  python3 parse.py ../../src/assets/examenes_oficiales/${f}_completo.pdf raw_$f.json
done
python3 build_oficiales.py   # escribe preguntas_oficiales.json y temas.json
```

`temas.py` define los temas (normas) y las reglas de clasificación. `lopj_part*.json` es la transcripción del PDF escaneado.

- En los PDFs de `examenes_oficiales/` la respuesta correcta y la referencia normativa están en **negrita**; se extraen con PyMuPDF (`fitz`) leyendo la fuente de cada span (no se ve con `pdftotext`).
- Cada examen tiene 104 preguntas (100 + 4 de reserva); al final de algunos PDFs hay secciones de análisis que repiten preguntas → deduplicar.
- Excluir las preguntas cuya referencia indica ANULADA, DEROGADA o ELIMINADA.
- `tests_lopj_y_reglamentos_completo.pdf` está escaneado (sin texto ni OCR instalado): se transcribió leyendo las imágenes de las páginas.
- El tema se asigna por la referencia en negrita (p. ej. «LEC. ACTOS DE COMUNICACIÓN Art. 152» → `lec`); «TEMA 2» se reparte entre igualdad / violencia de género / Ley 15/2022 según el enunciado.

# Instrucciones – Aplicación de tests

## 1. Fuentes de contenido

- **Material de estudio**: `src/assets/material/`
  Contiene el contenido susceptible de caer en un examen (temarios en PDF).
- **Exámenes oficiales**: `src/assets/examenes_oficiales/`
  Contiene preguntas que han caído en convocatorias anteriores. **Estas preguntas deben estar incluidas en la aplicación de tests.**

## 2. Selección por tema

- La aplicación debe permitir seleccionar el **tema**.
- Un tema **no** corresponde a un PDF concreto. Un tema es una **norma** (reglamento, ley...).
  - Ejemplo: todo lo relacionado con una ley concreta (LOPJ, LEC, LECrim, LJCA, LRJS, Constitución...) forma un único tema seleccionable, aunque su contenido esté repartido entre varios PDFs y varios tests.
- Cada pregunta debe ir etiquetada con el tema (norma) al que pertenece.

## 3. Redacción de preguntas

- Redactar tests a partir del **material** y de los **exámenes oficiales**, siguiendo el modelo de los exámenes oficiales: **misma estructura** (enunciado + 4 opciones a/b/c/d, una sola correcta) y **misma jerga**.
- Todas las preguntas generadas se guardan en JSON dentro de `src/assets/tests_claude/`, para que quede constancia de las preguntas ya sacadas y evitar repetirlas en el futuro.
- Antes de generar preguntas nuevas, revisar los JSON existentes en `src/assets/tests_claude/` para no duplicar.
- Indicar en cada pregunta su origen (`oficial` o `generada`) y, si se conoce, la referencia normativa (artículo).

### Ficheros de datos

| Fichero | Contenido |
|---|---|
| `src/assets/temas.json` | Lista de temas (normas): `{ id, nombre }` |
| `src/assets/examenes_oficiales/preguntas_oficiales.json` | Preguntas oficiales extraídas de los PDFs (respuesta correcta = opción en **negrita** del PDF). Se excluyen las marcadas como ANULADA / DEROGADA / ELIMINADA. |
| `src/assets/tests_claude/lote_<fecha>_<materia>.json` | Preguntas generadas por Claude, un fichero por lote |
| `src/assets/tests_claude/index.json` | `{ "lotes": [...] }`: lista de lotes que carga la app. **Añadir aquí cada lote nuevo.** |

Formato de cada pregunta:

```json
{
  "id": "cl-lec-lec-001",
  "origen": "oficial | claude",
  "tema": "lec",
  "bloque": "LEC. ACTOS DE COMUNICACIÓN",
  "articulo": "Art. 152.1",
  "enunciado": "...:",
  "opciones": ["...", "...", "...", "..."],
  "correcta": 0,
  "explicacion": "(solo generadas) justificación citando el artículo",
  "fuente": "Gestión Procesal · Examen oficial 3 | Material: lec_temario_completo.pdf",
  "fecha": "2026-11-11"
}
```

## 4. Modalidades de test

Además de filtrar por tema, el usuario elige el origen de las preguntas:

- **Todas**: oficiales + generadas.
- **Solo preguntas oficiales**: únicamente las extraídas de `examenes_oficiales/` (sin las generadas).
- **Solo preguntas de Claude**: únicamente las generadas y guardadas en `tests_claude/`.

## 5. Compilación y arranque

Una vez preparado el contenido, compilar y arrancar el proyecto en local:

```bash
npm run build
npm start        # ng serve → http://localhost:4200/
```

## 6. Estilo e interacción

- **Responsive**: debe funcionar bien en móvil y en pantallas pequeñas.
- **No mostrar el resultado inmediatamente**: al pulsar una opción, solo queda *preseleccionada*.
- Debajo de cada pregunta hay un botón **«Ver respuesta»**. Al pulsarlo se desvela si es correcta o no, y cuál es la correcta, **solo de esa pregunta concreta**; el resto siguen ocultas.

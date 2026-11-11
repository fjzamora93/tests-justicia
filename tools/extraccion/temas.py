import re, unicodedata
def norm(s):
    s = unicodedata.normalize('NFD', s.upper())
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')
TEMAS = [
 ('constitucion','Constitución Española'),
 ('ue','Unión Europea (Tratados)'),
 ('gobierno','Ley 50/1997, del Gobierno'),
 ('ley40','Ley 40/2015, de Régimen Jurídico del Sector Público'),
 ('ley39','Ley 39/2015, del Procedimiento Administrativo Común'),
 ('regimen_local','Ley 7/1985, de Bases del Régimen Local'),
 ('igualdad','LO 3/2007, para la igualdad efectiva de mujeres y hombres'),
 ('violencia_genero','LO 1/2004, de Medidas de Protección Integral contra la Violencia de Género'),
 ('igualdad_trato','Ley 15/2022, integral para la igualdad de trato y la no discriminación'),
 ('tecnologias','Tecnologías en la Administración de Justicia (Ley 18/2011 / RDL 6/2023)'),
 ('lopj','LOPJ – Ley Orgánica del Poder Judicial'),
 ('reglamento_ingreso','Reglamento de Ingreso (RD 1451/2005)'),
 ('reglamento_disciplinario','Reglamento Disciplinario (RD 796/2005)'),
 ('permisos','Jornada, permisos y licencias'),
 ('ebep','EBEP y libertad sindical'),
 ('reglamento_laj','Reglamento Orgánico del Cuerpo de LAJ'),
 ('reglamentos_cgpj','Reglamentos del CGPJ'),
 ('carta_derechos','Carta de Derechos de los Ciudadanos ante la Justicia'),
 ('estatuto_fiscal','Estatuto Orgánico del Ministerio Fiscal'),
 ('registro_civil','Registro Civil'),
 ('archivos','Archivos judiciales y expurgo (RD 937/2003)'),
 ('asistencia_juridica','Ley 1/1996, de Asistencia Jurídica Gratuita'),
 ('cooperacion','Ley 29/2015, de Cooperación Jurídica Internacional'),
 ('lec','LEC – Ley de Enjuiciamiento Civil'),
 ('jurisdiccion_voluntaria','Ley 15/2015, de la Jurisdicción Voluntaria'),
 ('concursal','Ley Concursal'),
 ('lecrim','LECrim – Ley de Enjuiciamiento Criminal'),
 ('jurado','LO 5/1995, del Tribunal del Jurado'),
 ('menores','LO 5/2000, de Responsabilidad Penal de los Menores'),
 ('ljca','LJCA – Jurisdicción Contencioso-administrativa'),
 ('lrjs','LRJS – Jurisdicción Social'),
 ('otros','Otras normas'),
]
REF_RULES = [  # (regex on normalized ref, tema)
 (r'LECRIM|LECRIN|^ECRIM|LEY DE ENJUICIAMIENTO CRIMINAL', 'lecrim'), (r'MONITORIO EUROPEO', 'lec'), (r'SECRETARIOS', 'reglamento_laj'), (r'JUECES (DE )?PAZ', 'reglamentos_cgpj'),
 (r'JURADO', 'jurado'), (r'MENORES', 'menores'),
 (r'CONTENCIOSO|LJCA', 'ljca'), (r'^SOCIAL|LRJS|SOCIAL\.', 'lrjs'),
 (r'VOLUNTARIA', 'jurisdiccion_voluntaria'), (r'CONCURS', 'concursal'),
 (r'\bLEC\b', 'lec'),
 (r'CONSTITUCION', 'constitucion'), (r'EUROPA|TFUE|\bTUE\b', 'ue'),
 (r'GOBIERNO', 'gobierno'), (r'40/15|40/2015', 'ley40'), (r'39/15|39/2015', 'ley39'),
 (r'REGISTRO CIVIL', 'registro_civil'), (r'ARCHIVO|EXPURGO', 'archivos'),
 (r'CARTA', 'carta_derechos'), (r'FISCAL', 'estatuto_fiscal'),
 (r'ASISTENCIA JURIDICA', 'asistencia_juridica'), (r'COOPERACION', 'cooperacion'),
 (r'INGRESO', 'reglamento_ingreso'), (r'DIS?CIPLINARIO', 'reglamento_disciplinario'),
 (r'PERMISO|JORNADA|EXCEDENCIA', 'permisos'), (r'SINDICAT|EBEP', 'ebep'),
 (r'REGLAMENTO (DEL )?SECRETARIO|ROLAJ|REGLAMENTO LAJ', 'reglamento_laj'),
 (r'REGLAMENTO \d+/\d+|CGPJ', 'reglamentos_cgpj'),
 (r'LOPJ|PODER JUDICIAL', 'lopj'),
 (r'TEMA 4|7/1985|REGIMEN LOCAL', 'regimen_local'),
 (r'TEMA 10|18/2011|6/2023', 'tecnologias'),
]
STEM_RULES = [
 (r'ENJUICIAMIENTO CRIMINAL|LECRIM', 'lecrim'), (r'ENJUICIAMIENTO CIVIL|\bLEC\b', 'lec'),
 (r'1/2004|VIOLENCIA (DE GENERO|SOBRE LA MUJER)', 'violencia_genero'),
 (r'15/\s?2022|IGUALDAD DE TRATO', 'igualdad_trato'),
 (r'3/\s?2007|IGUALDAD EFECTIVA', 'igualdad'),
 (r'7/1985|REGIMEN LOCAL|AYUNTAMIENTO|ALCALDE|MUNICIPIO|CONCEJAL', 'regimen_local'),
 (r'18/2011|6/2023|TABLON EDICTAL|ELECTRONIC|TECNOLOGIA', 'tecnologias'),
 (r'40/\s?2015', 'ley40'), (r'39/\s?2015', 'ley39'), (r'50/\s?1997|DEL GOBIERNO', 'gobierno'),
 (r'CONSTITUCION', 'constitucion'), (r'PODER JUDICIAL|LOPJ', 'lopj'),
 (r'JURISDICCION SOCIAL|JUZGADO DE LO SOCIAL|DESPIDO', 'lrjs'),
 (r'CONTENCIOSO', 'ljca'), (r'REGISTRO CIVIL', 'registro_civil'),
 (r'INTERES DE LEY|RECONVENCION|DEMANDA|EJECUCION|EMBARGO|JUICIO VERBAL|LETRADO DE LA ADMINISTRACION', 'lec'),
]
def classify(ref, stem):
    r = norm(ref); s = norm(stem)
    if r.startswith('TEMA 2') or 'IGUALDAD' in r:
        for rx, t in STEM_RULES[2:5]:
            if re.search(rx, s) or re.search(rx, r): return t
        return 'igualdad'
    for rx, t in REF_RULES:
        if re.search(rx, r): return t
    for rx, t in STEM_RULES:
        if re.search(rx, s): return t
    return 'otros'
EXCLUDE = re.compile(r'ANULAD|DEROGAD|ELIMINAD')
def bloque(ref):
    r = re.sub(r'\s+', ' ', ref).strip(' :.')
    r = re.split(r'(?i)\bart[\.\s]', r)[0].strip(' .,')
    r = re.sub(r'(?i)\b(NUEVA PURA|NUEVA|PURA|DIF[IÍ]CIL|REPETIDA.*|FUERA.*)$', '', r).strip(' .,')
    return r
def articulo(ref):
    m = re.search(r'(?i)\bart[íi]?c?u?l?o?s?\.?\s*([\d][\w\.\sº,ª\-\)\(]*)', ref)
    if not m: return ''
    a = re.split(r'\s(?=NUEVA|NUEV|PURA|DIF|REPETIDA|FUERA|TRAMI|GESTI|AUXILIO|LOPJ|LEC|CONST|[A-ZÁÉÍÓÚ]{4,})', m.group(1))[0]
    return 'Art. ' + a.strip(' .,')

export type Origen = 'oficial' | 'claude';

/** Modalidad de test: qué origen de preguntas se incluye. */
export type Modalidad = 'todas' | 'oficiales' | 'claude';

export interface Tema {
  id: string;
  nombre: string;
}

export interface Pregunta {
  id: string;
  origen: Origen;
  /** Id del tema (norma) al que pertenece, ver assets/temas.json. */
  tema: string;
  bloque: string;
  articulo: string;
  enunciado: string;
  opciones: string[];
  correcta: number;
  explicacion?: string;
  fuente: string;
}

export interface TemaConRecuento extends Tema {
  oficiales: number;
  claude: number;
}

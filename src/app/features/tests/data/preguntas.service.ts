import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { Modalidad, Pregunta, Tema, TemaConRecuento } from '../models/test.model';

const RUTA_TEMAS = 'assets/temas.json';
const RUTA_OFICIALES = 'assets/examenes_oficiales/preguntas_oficiales.json';
/** Índice con los lotes de preguntas generadas por Claude (assets/tests_claude). */
const RUTA_INDICE_CLAUDE = 'assets/tests_claude/index.json';

@Injectable({ providedIn: 'root' })
export class PreguntasService {
  private readonly http = inject(HttpClient);
  private carga?: Promise<void>;

  readonly temas = signal<Tema[]>([]);
  readonly preguntas = signal<Pregunta[]>([]);
  readonly error = signal<string | null>(null);
  readonly cargado = signal(false);

  readonly temasConRecuento = computed<TemaConRecuento[]>(() => {
    const recuento = new Map<string, { oficiales: number; claude: number }>();
    for (const p of this.preguntas()) {
      const r = recuento.get(p.tema) ?? { oficiales: 0, claude: 0 };
      if (p.origen === 'oficial') r.oficiales++;
      else r.claude++;
      recuento.set(p.tema, r);
    }
    return this.temas()
      .map((t) => ({ ...t, ...(recuento.get(t.id) ?? { oficiales: 0, claude: 0 }) }))
      .filter((t) => t.oficiales + t.claude > 0);
  });

  cargar(): Promise<void> {
    this.carga ??= this.cargarDatos();
    return this.carga;
  }

  /** Preguntas disponibles para un tema ('todos' = cualquiera) y una modalidad. */
  filtrar(tema: string, modalidad: Modalidad): Pregunta[] {
    return this.preguntas().filter(
      (p) =>
        (tema === 'todos' || p.tema === tema) &&
        (modalidad === 'todas' ||
          (modalidad === 'oficiales' && p.origen === 'oficial') ||
          (modalidad === 'claude' && p.origen === 'claude')),
    );
  }

  /** Selección aleatoria de `cantidad` preguntas (0 = todas). */
  generarTest(tema: string, modalidad: Modalidad, cantidad: number): Pregunta[] {
    const pool = [...this.filtrar(tema, modalidad)];
    for (let i = pool.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [pool[i], pool[j]] = [pool[j], pool[i]];
    }
    return cantidad > 0 ? pool.slice(0, cantidad) : pool;
  }

  private async cargarDatos(): Promise<void> {
    try {
      const [temas, oficiales, indice] = await Promise.all([
        firstValueFrom(this.http.get<Tema[]>(RUTA_TEMAS)),
        firstValueFrom(this.http.get<Pregunta[]>(RUTA_OFICIALES)),
        firstValueFrom(this.http.get<{ lotes: string[] }>(RUTA_INDICE_CLAUDE)).catch(() => ({ lotes: [] })),
      ]);
      const lotes = await Promise.all(
        indice.lotes.map((lote) =>
          firstValueFrom(this.http.get<Pregunta[]>(`assets/tests_claude/${lote}`)).catch(() => [] as Pregunta[]),
        ),
      );
      const generadas = lotes.flat().map((p) => ({ ...p, origen: 'claude' as const }));
      this.temas.set(temas);
      this.preguntas.set([...oficiales, ...generadas]);
      this.cargado.set(true);
    } catch {
      this.error.set('No se han podido cargar las preguntas.');
      this.carga = undefined;
    }
  }
}

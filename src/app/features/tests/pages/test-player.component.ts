import { Component, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { PreguntasService } from '../data/preguntas.service';
import { Modalidad, Pregunta } from '../models/test.model';

const LETRAS = 'abcd';

@Component({
  selector: 'app-test-player',
  imports: [RouterLink],
  templateUrl: './test-player.component.html',
  styleUrl: './test-player.component.scss',
})
export class TestPlayerComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly datos = inject(PreguntasService);

  readonly letras = LETRAS;
  readonly cargando = signal(true);
  readonly preguntas = signal<Pregunta[]>([]);
  /** Opción preseleccionada por pregunta (id → índice). */
  readonly seleccion = signal<Record<string, number>>({});
  /** Preguntas cuya respuesta se ha desvelado. */
  readonly reveladas = signal<Record<string, boolean>>({});

  private readonly params = this.route.snapshot.queryParamMap;
  readonly tema = this.params.get('tema') ?? 'todos';
  readonly modalidad = (this.params.get('modo') ?? 'todas') as Modalidad;
  readonly cantidad = Number(this.params.get('n') ?? 25);

  readonly nombreTema = computed(() =>
    this.tema === 'todos' ? 'Todos los temas' : (this.datos.temas().find((t) => t.id === this.tema)?.nombre ?? this.tema),
  );
  readonly nombreModalidad = { todas: 'Oficiales + Claude', oficiales: 'Solo oficiales', claude: 'Solo Claude' }[this.modalidad];

  readonly totalReveladas = computed(() => Object.keys(this.reveladas()).length);
  readonly aciertos = computed(
    () => this.preguntas().filter((p) => this.reveladas()[p.id] && this.seleccion()[p.id] === p.correcta).length,
  );

  constructor() {
    this.datos.cargar().then(() => {
      this.nuevoTest();
      this.cargando.set(false);
    });
  }

  nuevoTest(): void {
    this.preguntas.set(this.datos.generarTest(this.tema, this.modalidad, this.cantidad));
    this.seleccion.set({});
    this.reveladas.set({});
    window.scrollTo({ top: 0 });
  }

  seleccionar(p: Pregunta, opcion: number): void {
    if (this.reveladas()[p.id]) return;
    this.seleccion.update((s) => ({ ...s, [p.id]: opcion }));
  }

  verRespuesta(p: Pregunta): void {
    this.reveladas.update((r) => ({ ...r, [p.id]: true }));
  }

  estadoOpcion(p: Pregunta, opcion: number): string {
    const elegida = this.seleccion()[p.id] === opcion;
    if (!this.reveladas()[p.id]) return elegida ? 'elegida' : '';
    if (opcion === p.correcta) return 'correcta';
    return elegida ? 'fallo' : 'apagada';
  }
}

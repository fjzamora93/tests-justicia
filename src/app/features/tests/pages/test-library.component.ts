import { Component, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { PreguntasService } from '../data/preguntas.service';
import { Modalidad } from '../models/test.model';

@Component({
  selector: 'app-test-library',
  templateUrl: './test-library.component.html',
  styleUrl: './test-library.component.scss',
})
export class TestLibraryComponent {
  private readonly router = inject(Router);
  readonly datos = inject(PreguntasService);

  readonly modalidades: { id: Modalidad; nombre: string; detalle: string }[] = [
    { id: 'todas', nombre: 'Todas', detalle: 'Oficiales + Claude' },
    { id: 'oficiales', nombre: 'Solo oficiales', detalle: 'Exámenes de convocatorias' },
    { id: 'claude', nombre: 'Solo Claude', detalle: 'Preguntas generadas' },
  ];
  readonly cantidades = [10, 25, 50, 100, 0];

  readonly tema = signal('todos');
  readonly modalidad = signal<Modalidad>('todas');
  readonly cantidad = signal(25);

  readonly disponibles = computed(() =>
    this.datos.cargado() ? this.datos.filtrar(this.tema(), this.modalidad()).length : 0,
  );

  constructor() {
    this.datos.cargar();
  }

  recuento(t: { oficiales: number; claude: number }): number {
    const m = this.modalidad();
    return m === 'oficiales' ? t.oficiales : m === 'claude' ? t.claude : t.oficiales + t.claude;
  }

  empezar(): void {
    this.router.navigate(['/test'], {
      queryParams: { tema: this.tema(), modo: this.modalidad(), n: this.cantidad() },
    });
  }
}

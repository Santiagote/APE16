import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AnalizadorService, ResultadoAnalisis } from './analizador.service';

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  oracion = signal('');
  motor = signal('stanza');
  resultado = signal<ResultadoAnalisis | null>(null);
  cargando = signal(false);
  error = signal('');
  seccionAbierta = signal<string | null>(null);

  oracionesEjemplo = [
    'María estudia porque mañana tiene un examen.',
    'Pedro llegó y Ana salió.',
    'Aunque llueve iremos al parque.',
    'Si estudias aprobarás.',
    'Juan cocina mientras Ana limpia.',
    'Pedro compró un automóvil.',
    'Ana cocina la cena.',
    'Luis juega fútbol.',
  ];

  constructor(private analizador: AnalizadorService) {}

  analizar(): void {
    const texto = this.oracion().trim();
    if (!texto) return;

    this.cargando.set(true);
    this.error.set('');
    this.resultado.set(null);

    this.analizador.analizar(texto, this.motor()).subscribe({
      next: (res) => {
        this.resultado.set(res);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('Error al conectar con el backend. Verifica que el servidor esté corriendo en el puerto 5000.');
        this.cargando.set(false);
      },
    });
  }

  seleccionarEjemplo(ejemplo: string): void {
    this.oracion.set(ejemplo);
    this.analizar();
  }

  toggle(seccion: string): void {
    this.seccionAbierta.set(
      this.seccionAbierta() === seccion ? null : seccion
    );
  }

  clasePos(pos: string): string {
    const mapa: Record<string, string> = {
      NOUN: 'pos-noun', VERB: 'pos-verb', ADJ: 'pos-adj',
      ADV: 'pos-adv', DET: 'pos-det', ADP: 'pos-adp',
      CONJ: 'pos-conj', PRON: 'pos-pron', PUNCT: 'pos-punct',
      PROPN: 'pos-noun', SCONJ: 'pos-conj', NUM: 'pos-num',
    };
    return mapa[pos] || '';
  }

  arbolPlano(raw: string): NodoArbol[] {
    const tokens: string[] = [];
    let buf = '';
    for (const ch of raw) {
      if (ch === '(' || ch === ')') {
        if (buf.trim()) tokens.push(buf.trim());
        tokens.push(ch);
        buf = '';
      } else if (ch === ' ' || ch === '\t' || ch === '\n') {
        if (buf.trim()) tokens.push(buf.trim());
        buf = '';
      } else {
        buf += ch;
      }
    }
    if (buf.trim()) tokens.push(buf.trim());

    const nodes: NodoArbol[] = [];
    let i = 0;

    const parse = (depth: number): void => {
      while (i < tokens.length) {
        const t = tokens[i];
        if (t === ')') { i++; return; }
        if (t === '(') {
          i++;
          const label = tokens[i++];
          nodes.push({ label, depth, esRama: true });
          parse(depth + 1);
        } else {
          nodes.push({ label: t, depth, esRama: false });
          i++;
          return;
        }
      }
    };

    parse(0);

    for (let idx = 0; idx < nodes.length; idx++) {
      const n = nodes[idx];
      let esUltimo = true;
      for (let j = idx + 1; j < nodes.length; j++) {
        if (nodes[j].depth < n.depth) break;
        if (nodes[j].depth === n.depth) { esUltimo = false; break; }
      }
      n.esUltimo = esUltimo;
    }

    return nodes;
  }
}

interface NodoArbol {
  label: string;
  depth: number;
  esRama: boolean;
  esUltimo?: boolean;
}

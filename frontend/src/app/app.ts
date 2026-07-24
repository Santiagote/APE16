/**
 * @fileoverview Componente principal de la aplicación Angular (Analizador Sintáctico APE16).
 * Gestiona el estado reactivo mediante Angular Signals, interactúa con el servicio backend,
 * asigna estilos a las etiquetas POS y reconstruye visualmente el árbol sintáctico.
 */

import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AnalizadorService, ResultadoAnalisis } from './analizador.service';

/**
 * Estructura de nodo plano para renderizar árboles jerárquicos sintácticos con sangría e identadores.
 */
interface NodoArbol {
  /** Etiqueta o texto del nodo (ej. 'SBAR', 'NP', 'NOUN', 'estudiante') */
  label: string;
  /** Nivel de profundidad en la jerarquía del árbol */
  depth: number;
  /** Indica si el nodo es una rama sintáctica (true) o una palabra/hoja terminal (false) */
  esRama: boolean;
  /** Indica si es el último nodo hijo dentro de su mismo nivel de profundidad */
  esUltimo?: boolean;
}

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  /** Signal reactivo para el texto de la oración ingresada por el usuario */
  oracion = signal('');
  
  /** Signal reactivo para la selección del motor NLP ('stanza' o 'spacy') */
  motor = signal('stanza');
  
  /** Signal reactivo que almacena los resultados devueltos por la API */
  resultado = signal<ResultadoAnalisis | null>(null);
  
  /** Signal reactivo de estado de carga mientras la API procesa la solicitud */
  cargando = signal(false);
  
  /** Signal reactivo para mensajes de error de red o backend */
  error = signal('');
  
  /** Signal reactivo para controlar el colapso/despliegue de secciones de detalles en la interfaz */
  seccionAbierta = signal<string | null>(null);

  /** Lista de oraciones de ejemplo prediseñadas para pruebas rápidas del usuario */
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

  /**
   * Ejecuta el análisis sintáctico enviando la oración actual y motor seleccionado al servicio.
   */
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

  /**
   * Carga una oración de ejemplo en el campo de texto e inicia inmediatamente el análisis.
   * 
   * @param ejemplo Oración de prueba seleccionada por el usuario.
   */
  seleccionarEjemplo(ejemplo: string): void {
    this.oracion.set(ejemplo);
    this.analizar();
  }

  /**
   * Alterna la visibilidad de una sección colapsable en la interfaz de usuario.
   * 
   * @param seccion Identificador de la sección (ej. 'tokens', 'dependencias', 'arbol').
   */
  toggle(seccion: string): void {
    this.seccionAbierta.set(
      this.seccionAbierta() === seccion ? null : seccion
    );
  }

  /**
   * Devuelve la clase CSS correspondiente según la etiqueta de categoría gramatical (UPOS Tag).
   * 
   * @param pos Código de categoría gramatical (ej. NOUN, VERB, ADJ).
   * @returns Nombre de la clase CSS declarada en app.css.
   */
  clasePos(pos: string): string {
    const mapa: Record<string, string> = {
      NOUN: 'pos-noun', VERB: 'pos-verb', ADJ: 'pos-adj',
      ADV: 'pos-adv', DET: 'pos-det', ADP: 'pos-adp',
      CONJ: 'pos-conj', PRON: 'pos-pron', PUNCT: 'pos-punct',
      PROPN: 'pos-noun', SCONJ: 'pos-conj', NUM: 'pos-num',
    };
    return mapa[pos] || '';
  }

  /**
   * Parsea la notación jerárquica entre paréntesis (Penn Treebank / LISP format, ej. "(ROOT (S (NP ...)))")
   * y la transforma en un arreglo plano de nodos con niveles de profundidad (`depth`) y marcas de jerarquía.
   * 
   * @param raw Cadena de texto con la notación de árbol entre paréntesis.
   * @returns Lista de nodos estructurados (`NodoArbol[]`).
   */
  arbolPlano(raw: string): NodoArbol[] {
    // 1. Tokenizador léxico simple: separa paréntesis y palabras clave
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

    // 2. Parser recursivo descendente para construir la lista de nodos con profundidad
    const nodes: NodoArbol[] = [];
    let i = 0;

    const parse = (depth: number): void => {
      while (i < tokens.length) {
        const t = tokens[i];
        if (t === ')') { 
          i++; 
          return; 
        }
        if (t === '(') {
          i++;
          const label = tokens[i++];
          nodes.push({ label, depth, esRama: true });
          parse(depth + 1); // Recurrencia para los sub-elementos hijos
        } else {
          nodes.push({ label: t, depth, esRama: false });
          i++;
          return;
        }
      }
    };

    parse(0);

    // 3. Determinar si un nodo es el último hijo en su nivel para renderizar líneas conectoras visuales
    for (let idx = 0; idx < nodes.length; idx++) {
      const n = nodes[idx];
      let esUltimo = true;
      for (let j = idx + 1; j < nodes.length; j++) {
        if (nodes[j].depth < n.depth) break;
        if (nodes[j].depth === n.depth) { 
          esUltimo = false; 
          break; 
        }
      }
      n.esUltimo = esUltimo;
    }

    return nodes;
  }
}


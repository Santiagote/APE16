/**
 * @fileoverview Servicio de Angular para comunicarse con el backend REST API de Flask.
 * Permite enviar oraciones en español para su análisis morfosintáctico y clasificación gramatical.
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

/**
 * Representa una unidad léxica o palabra analizada con su lema y categoría gramatical.
 */
export interface Token {
  /** Palabra original en la oración */
  palabra: string;
  /** Forma lematizada / canónica */
  lema: string;
  /** Categoría gramatical (Part-of-Speech Tagging en formato Universal POS) */
  pos: string;
}

/**
 * Representa un arco de dependencia gramatical entre dos palabras (Universal Dependencies).
 */
export interface Dependencia {
  /** Palabra núcleo o regente */
  gobernador: string;
  /** Palabra modificadora o subordinada */
  dependiente: string;
  /** Tipo de relación gramatical (ej. nsubj, obj, root, cc, mark) */
  relacion: string;
}

/**
 * Estructura de respuesta del análisis sintáctico y semántico devuelta por el servidor.
 */
export interface ResultadoAnalisis {
  /** Oración original analizada */
  oracion: string;
  /** Lista de tokens léxicos */
  tokens: Token[];
  /** Grafo de dependencias sintácticas */
  dependencias: Dependencia[];
  /** Notación en paréntesis del árbol de constituyentes o dependencias */
  arbol_sintactico: string;
  /** Clasificación gramatical (Simple, Compuesta Coordinada, Compuesta Subordinada) */
  tipo: string;
  /** Nube o nexo semántico (ej. Copulativa, Causal, Condicional) */
  relacion_semantica: string;
  /** Núcleo del sujeto identificado */
  sujeto: string;
  /** Verbo principal / raíz de la oración */
  verbo_principal: string;
  /** Objeto directo o complemento directo identificado */
  objeto_directo: string;
}

/**
 * Servicio inyectable que gestiona las peticiones HTTP al endpoint de análisis sintáctico.
 */
@Injectable({ providedIn: 'root' })
export class AnalizadorService {
  /** URL base de la API REST de Flask */
  private readonly apiUrl = 'http://localhost:5000/api/analizar';

  constructor(private http: HttpClient) {}

  /**
   * Envía una oración al backend para realizar el análisis sintáctico.
   * 
   * @param oracion Cadena de texto de la oración a analizar.
   * @param motor Motor de NLP a utilizar ('stanza' o 'spacy'). Por defecto 'stanza'.
   * @returns Observable con la respuesta del resultado del análisis (`ResultadoAnalisis`).
   */
  analizar(oracion: string, motor: string = 'stanza'): Observable<ResultadoAnalisis> {
    return this.http.post<ResultadoAnalisis>(this.apiUrl, { oracion, motor });
  }
}


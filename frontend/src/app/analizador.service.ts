import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Token {
  palabra: string;
  lema: string;
  pos: string;
}

export interface Dependencia {
  gobernador: string;
  dependiente: string;
  relacion: string;
}

export interface ResultadoAnalisis {
  oracion: string;
  tokens: Token[];
  dependencias: Dependencia[];
  arbol_sintactico: string;
  tipo: string;
  relacion_semantica: string;
  sujeto: string;
  verbo_principal: string;
  objeto_directo: string;
}

@Injectable({ providedIn: 'root' })
export class AnalizadorService {
  private readonly apiUrl = 'http://localhost:5000/api/analizar';

  constructor(private http: HttpClient) {}

  analizar(oracion: string, motor: string = 'stanza'): Observable<ResultadoAnalisis> {
    return this.http.post<ResultadoAnalisis>(this.apiUrl, { oracion, motor });
  }
}

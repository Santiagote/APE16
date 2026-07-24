"""
Script de evaluación y benchmark comparativo de rendimiento entre motores NLP:
spaCy (es_core_news_sm) vs. Stanford Stanza (español).

Mide y compara:
1. Tiempo de inicialización / carga del modelo en memoria.
2. Tiempo total y promedio de procesamiento sobre un conjunto de oraciones de prueba.
3. Consumo de memoria RAM (pico en MB) usando la librería estándar `tracemalloc`.
4. Diferencias estructurales en las salidas (POS tags y Árboles Sintácticos/Constituyentes).
"""

import os
import sys
import time
import tracemalloc

# Ajustar el sys.path para permitir la importación de los módulos locales del backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from servicios.clasificador_oraciones import ClasificadorOraciones
from nlp.fachada_spacy import FachadaSpacy
from nlp.fachada_stanza import FachadaStanza


def medir_memoria_y_tiempo_init(cls_fachada):
    """
    Mide el tiempo de ejecución y el pico de memoria consumida durante la inicialización de una fachada NLP.

    :param cls_fachada: Clase de la fachada a instanciar (FachadaSpacy o FachadaStanza).
    :return: Tupla (instancia_creada, tiempo_en_segundos, memoria_pico_en_MB).
    """
    tracemalloc.start()
    t0 = time.perf_counter()
    instancia = cls_fachada()
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return instancia, (t1 - t0), peak / (1024 * 1024)


def medir_procesamiento(instancia, oraciones):
    """
    Mide el tiempo y consumo de memoria RAM durante el procesamiento sintáctico de un lote de oraciones.

    :param instancia: Objeto fachada previamente instanciado.
    :param oraciones: Lista de cadenas de texto con las oraciones de prueba.
    :return: Tupla (lista_resultados, tiempo_total, tiempo_promedio, memoria_pico_MB).
    """
    tracemalloc.start()
    t0 = time.perf_counter()
    resultados = []
    for o in oraciones:
        res = instancia.analizar(o)
        resultados.append(res)
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tiempo_total = t1 - t0
    tiempo_promedio = tiempo_total / len(oraciones)
    return resultados, tiempo_total, tiempo_promedio, peak / (1024 * 1024)


def main():
    """Función principal que ejecuta el benchmark completo y muestra el reporte tabulado."""
    oraciones_prueba = [
        "El estudiante lee un libro en la biblioteca.",
        "Juan estudia medicina y María cursa derecho.",
        "Iremos al parque si el clima mejora mañana.",
        "El perro persigue al gato pero no logra alcanzarlo.",
        "El profesor explicó la lección porque los alumnos tenían dudas."
    ]

    print("========================================================================")
    print("      BENCHMARK COMPARATIVO: SPACY vs STANFORD (STANZA) EN APE16        ")
    print("========================================================================\n")

    # 1. Medir Inicialización de spaCy
    print("[1/2] Inicializando FachadaSpacy (es_core_news_sm)...")
    spacy_fachada, t_init_spacy, mem_init_spacy = medir_memoria_y_tiempo_init(FachadaSpacy)
    print(f"      - Tiempo de inicialización: {t_init_spacy:.4f} s")
    print(f"      - Memoria pico en init: {mem_init_spacy:.2f} MB\n")

    # 2. Medir Inicialización de Stanza
    print("[2/2] Inicializando FachadaStanza (es - tokenize,pos,lemma,depparse,constituency)...")
    stanza_fachada, t_init_stanza, mem_init_stanza = medir_memoria_y_tiempo_init(FachadaStanza)
    print(f"      - Tiempo de inicialización: {t_init_stanza:.4f} s")
    print(f"      - Memoria pico en init: {mem_init_stanza:.2f} MB\n")

    # 3. Medir Procesamiento en Lote
    print("--- Midiendo tiempo y memoria de procesamiento de oraciones ---")
    res_spacy, t_proc_spacy, t_avg_spacy, mem_proc_spacy = medir_procesamiento(spacy_fachada, oraciones_prueba)
    res_stanza, t_proc_stanza, t_avg_stanza, mem_proc_stanza = medir_procesamiento(stanza_fachada, oraciones_prueba)

    # 4. Imprimir Tabla Resumen de Métricas
    print(f"\nRESULTADOS DE RENDIMIENTO Y RECURSOS:")
    print(f"+-----------------------------------+--------------------+--------------------+")
    print(f"| Métrica                           | spaCy              | Stanza (Stanford)  |")
    print(f"+-----------------------------------+--------------------+--------------------+")
    print(f"| Tiempo Init Modelo                | {t_init_spacy:16.4f} s | {t_init_stanza:16.4f} s |")
    print(f"| Tiempo Total 5 Oraciones          | {t_proc_spacy:16.4f} s | {t_proc_stanza:16.4f} s |")
    print(f"| Tiempo Promedio / Oración         | {t_avg_spacy:16.4f} s | {t_avg_stanza:16.4f} s |")
    print(f"| Memoria RAM en Init (pico)        | {mem_init_spacy:14.2f} MB | {mem_init_stanza:14.2f} MB |")
    print(f"| Memoria RAM en Procesar (pico)    | {mem_proc_spacy:14.2f} MB | {mem_proc_stanza:14.2f} MB |")
    print(f"+-----------------------------------+--------------------+--------------------+\n")

    # 5. Comparar Detalles de Salida Sintáctica
    print("=" * 80)
    print("COMPARACIÓN DETALLADA DE SALIDAS (EJEMPLO CON ORACIÓN #1)")
    print("=" * 80)
    print(f"Oración: \"{oraciones_prueba[0]}\"\n")

    print("[SPA-CY] Tokens & POS:")
    for t in res_spacy[0].tokens[:5]:
        print(f"  Word: {t.palabra:<12} Lemma: {t.lema:<12} POS: {t.pos}")
    print("\n[STANZA] Tokens & POS:")
    for t in res_stanza[0].tokens[:5]:
        print(f"  Word: {t.palabra:<12} Lemma: {t.lema:<12} POS: {t.pos}")

    print("\n[SPA-CY] Árbol Sintáctico Genético (Basado en jerarquía de dependencias):")
    print(f"  {res_spacy[0].arbol_sintactico}")

    print("\n[STANZA] Árbol Sintáctico Nativo (Constituency Tree / SBAR, NP, VP):")
    print(f"  {res_stanza[0].arbol_sintactico}\n")


if __name__ == "__main__":
    main()


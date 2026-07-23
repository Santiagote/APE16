FEIRNNR - Carrera de
Computación
• Analizar árboles sintácticos y dependencias generadas por
CoreNLP.
• Clasificar automáticamente oraciones compuestas según sus
conectores y relaciones semánticas..
3. Materiales y reactivos:
• PC con acceso a Internet.
• Documentación del estándar de tokens definida para el problema
elegido.
• Diapositivas semana 15 y 16
4. Equipos y herramientas
Software
o Python 3.10+, VS Code, librerías re, threading, Java.
Hardware
o Procesador multinúcleo, 8 GB RAM.
5. Procedimiento / Metodología
Actividad 1
Instalar Stanford CoreNLP y configurarlo para español.
Actividad 2
Analizar las siguientes oraciones.
María estudia porque mañana tiene un examen.
Pedro llegó y Ana salió.
Aunque llueve iremos al parque.
Si estudias aprobarás.
Juan cocina mientras Ana limpia.
Mostrar:
Token
POS
Dependencias
Árbol sintáctico

FEIRNNR - Carrera de
Computación
Actividad 3
Analizar las siguientes oraciones simples.
Pedro compró un automóvil.
Ana cocina la cena.
Luis juega fútbol.
Responder:
¿Quién es el sujeto?
¿Cuál es el verbo principal?
¿Cuál es el objeto directo?
Actividad 4
Implementar reglas para identificar conectores.
Coordinadas
Conector Tipo
y Copulativa
e Copulativa
ni Copulativa
o Disyuntiva
u Disyuntiva
pero Adversativa
sin embargo Adversativa
Subordinadas
Conector Tipo
porque Causal
ya que Causal
puesto que Causal
si Condicional
aunque Concesiva

FEIRNNR - Carrera de
Computación
Conector Tipo
mientras Temporal
cuando Temporal
para que Final
por lo tanto Consecutiva
Actividad 5
Clasificar automáticamente las oraciones.
Ejemplo:
Pedro llegó y Ana salió.
Resultado esperado:
Tipo:
Compuesta Coordinada
Relación:
Copulativa
Actividad 6
Comparar los resultados obtenidos con los generados por spaCy en la
práctica anterior.
Completar la siguiente tabla:
Aspecto spaCy Stanford CoreNLP
Tiempo de ejecución
Precisión POS
Árbol sintáctico
Dependencias
Facilidad de uso
Consumo de memoria
Nota: se debe enviar las oraciones en un front-end, caso contrario no se
hará valida la practica

                                                                                      FEIRNNR - Carrera de
Computación

6. Resultados esperados:
El estudiante deberá obtener:
•  Análisis léxico.
•  Árbol sintáctico.
•  Dependencias.
•  Clasificación semántica de las oraciones.
•  Comparación entre ambas herramientas.
7. Preguntas de Control:
¿Qué diferencias encontró entre spaCy y Stanford CoreNLP?
¿Cuál herramienta genera árboles sintácticos más detallados?
¿Qué ventajas ofrece Stanford CoreNLP para el análisis lingüístico?
¿Qué limitaciones presenta el enfoque basado en reglas para el análisis
semántico?
¿Qué mejoras implementaría para aumentar la precisión del clasificador??

8. Evaluación
1.
| Criterio        |     | Excelente  | Bueno    | Bajo      |
| --------------- | --- | ---------- | -------- | --------- |
| Funcionamiento  |     | Funciona   | Parcial  | No        |
| (back-end,      |     | completo   | (2)      | funciona  |
| front-end)      | se  | (4)        |          | (0)       |
evaluara
| criterios  | de  |     |     |     |
| ---------- | --- | --- | --- | --- |
Verificacion
| Documento         | de    | Funciona  | Parcial  | No        |
| ----------------- | ----- | --------- | -------- | --------- |
| practica (Enlace  |       | completo  | (2)      | funciona  |
| a                 | git,  | (3)       |          | (0)       |
metodología
| usada  por  | el  |     |     |     |
| ----------- | --- | --- | --- | --- |
alumno,
resultados,
| preguntas  | de  |     |     |     |
| ---------- | --- | --- | --- | --- |
control,
bibliografía,
conclusiones,
| video  | de  |     |     |     |
| ------ | --- | --- | --- | --- |
explicación)
| Defensa   | de  | Todos  los   | Parcial  | No      |
| --------- | --- | ------------ | -------- | ------- |
| practica  |     | puntos  (3)  | (1)      | valido  |
(0)

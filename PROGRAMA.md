# Programa propuesto · Analista Lab

**Público:** personas hispanohablantes que empiezan desde cero. **Resultado deseado:** obtener, preparar, analizar y comunicar datos con criterio, construir un portafolio y tener una base para especializaciones.

La versión 0.1 incluye dos microlecciones y una práctica por módulo. Esta propuesta describe cómo ampliarla hasta un programa más profundo. Un objetivo inicial de **160–240 horas** de trabajo distribuido en aproximadamente **24–36 semanas**, según experiencia y ritmo, es una estimación de diseño del programa ampliado; no una duración medida de la versión actual ni una promesa de dominio o empleo.

## Ruta y prerrequisitos

| Nº | Módulo | Contenido a desarrollar | Prerrequisito | Evidencia de aprendizaje |
| --- | --- | --- | --- | --- |
| 1 | Pensar como analista | Preguntas de negocio, métricas, granularidad, tipos de datos, sesgos, ética y privacidad | Ninguno | Brief y diccionario |
| 2 | Excel / Google Sheets | Tablas, fórmulas, búsquedas, tablas dinámicas y controles | 1 | Resumen conciliado |
| 3 | Estadística básica | Media, mediana, cuantiles, dispersión, distribuciones, probabilidades y porcentajes | 1 y aritmética básica | Explicar centro y variabilidad |
| 4 | SQL básico | SELECT, filtros, NULL, fechas, agregación, GROUP BY y HAVING | 1–3 | Consultas verificadas |
| 5 | SQL intermedio/avanzado | JOINs, cardinalidad, subconsultas, CASE, CTEs, ventanas, planes e índices | 4 | Acumulados y conciliación |
| 6 | Python | Variables, estructuras, funciones, errores, entornos, Jupyter, NumPy y pandas | 1–3 | Notebook reproducible |
| 7 | Limpieza / wrangling | Perfilado, faltantes, duplicados, tipos, merge, reshape, fechas, validaciones y datos de APIs | 5–6 | Pipeline y registro de cambios |
| 8 | EDA / visualización | Distribuciones, grupos, correlaciones, gráficos, matplotlib/seaborn y accesibilidad | 3, 6–7 | Hallazgo con límites |
| 9 | Estadística intermedia | Muestreo, estimación, intervalos, pruebas t/chi-cuadrado, potencia, A/B y múltiples pruebas | 3 y 8 | Informe de comparación |
| 10 | Power BI / comunicación | Power Query, modelo estrella, DAX, contexto de filtros, dashboards y presentación | 2, 5, 7–9 | Informe con medidas verificadas |
| 11 | Estadística avanzada | Álgebra de apoyo, regresión lineal/logística, diagnósticos, ANOVA, bootstrap, pruebas robustas y series temporales | 6–9 | Modelo interpretado y validado |
| 12 | Machine learning | Baselines, split, CV, pipelines, clasificación/regresión, métricas, tuning, calibración y sesgos | 6–9 y 11 | Comparación sin fuga de información |
| 13 | Data mining | Clustering, PCA, cargas y escalado, reglas de asociación y anomalías | 6–9 y 12 | Patrones estables e interpretables |
| 14 | Portafolio / trabajo reproducible | Git/GitHub, README, dependencias, controles de calidad, automatización, entrevistas y uso responsable de IA | Trabajo progresivo desde 6 | Proyectos que otra persona pueda ejecutar |

Los módulos 1–10 forman la ruta de análisis. Los módulos 11–13 introducen especializaciones que conviene estudiar después. El portafolio y los hábitos de reproducibilidad se construyen a lo largo del programa.

## Formato de una lección ampliada

1. Objetivo concreto: «Puedo identificar si un JOIN duplicó ventas».
2. Explicación en español, con vocabulario técnico inglés al lado cuando resulte útil.
3. Ejemplo resuelto sobre un caso consistente.
4. Video opcional breve o tramo seleccionado de un curso con autor y enlace original.
5. Ejercicio guiado con pistas progresivas.
6. Ejercicio independiente con datos o condiciones diferentes.
7. Quiz con explicación y variaciones de preguntas.
8. Entregable o reflexión que demuestre comprensión.

Una distribución orientativa sería 60 % de práctica/proyectos, 20 % teoría, 10 % videos y 10 % repaso/quiz. Debe ajustarse según los resultados de alumnos, no presentarse como una regla demostrada.

## Evaluación y proyectos

El quiz de 3 preguntas actual es formativo. Para ampliar la evaluación, construir un banco con varias preguntas por objetivo, variar números, revisar respuestas libres y pedir que el alumno explique y depure un resultado incorrecto. La finalización en el sitio no equivale a una evaluación profesional ni una certificación.

1. **Análisis comercial:** archivo original y limpio, consultas SQL, gráfico y recomendación. Empezar con el caso pequeño, después repetir con un dataset abierto más amplio.
2. **Dashboard:** KPIs, dimensiones, filtros, documentación y diseño de experimento. Revisar medidas bajo distintos filtros.
3. **Modelo:** baseline, pipeline, comparación dentro de entrenamiento, evaluación final reservada, límites y README reproducible.

Conservar rúbricas con criterios de corrección, reproducibilidad, interpretación y comunicación. Añadir revisión entre compañeros o docente cuando exista una comunidad.

## Qué más añadiría

- **Alfabetización de datos y lógica de negocio:** denominadores, cohortes, embudos, ingresos frente a beneficio, preguntas causales frente a descriptivas.
- **Matemáticas de apoyo:** porcentajes, unidades, álgebra, matrices y logaritmos según se necesiten, con una ruta de refuerzo.
- **Obtención de datos:** CSV/JSON, APIs, documentación de origen, licencias y privacidad.
- **Control de calidad:** claves, rangos, coherencia entre herramientas, registros y trazabilidad.
- **Automatización:** scripts parametrizados, lectura repetible de archivos, logs y manejo de errores.
- **Comunicación:** resúmenes ejecutivos, presentaciones, gráficas accesibles y recomendaciones medibles.
- **Práctica laboral:** retos SQL, depuración, interpretación de informes e instrucciones para proyectos de portafolio.
- **Comunidad y mantenimiento:** reporte de errores, preguntas frecuentes y revisión periódica de enlaces y contenidos.

## Evolución técnica

La edición inicial usa HTML/CSS/JavaScript estáticos, navegación con hash y localStorage. Permite lecciones, quizzes, gráficos, descargas y videos sin backend. Para SQL dentro de la página se puede evaluar SQLite/WebAssembly; Python en navegador con Pyodide exige gestionar descarga, memoria y compatibilidad. Actualmente ambos se practican en notebooks.

Si se necesitan cuentas, progreso compartido, administración docente o certificados verificables, hará falta un servicio externo de identidad y datos además de GitHub Pages. Añadirlo cuando exista una necesidad concreta.

# Analista Lab

Una primera versión de un curso de análisis de datos en español, compatible con **GitHub Pages**. Nombre provisional; se puede adaptar al proyecto.

Incluye 14 módulos, 28 microlecciones, 14 prácticas con pistas y soluciones, 42 preguntas con explicación, 3 proyectos con rúbricas y 3 notebooks ejecutables. Es una base introductoria del programa; los módulos avanzados necesitan más profundidad y ejercicios para formar una especialización completa.

## Usar el sitio

Abre `index.html` con Chrome, Edge o Firefox. Es autónomo: HTML, CSS, JavaScript, contenidos, datos y notebooks están dentro del archivo. No necesita instalación ni un servidor para las funciones principales. Los videos y enlaces externos necesitan conexión a internet.

- **Ruta:** busca módulos y filtra por etapa.
- **Módulo:** teoría → práctica → mini quiz → recursos.
- **Progreso:** marca las dos lecturas y supera el quiz con al menos 2/3. El sitio conserva la mejor nota.
- **Laboratorio:** cambia números, agrega un valor extremo y compara agrupamientos comerciales.
- **Prácticas SQL/Python:** descarga un notebook y ábrelo en Colab (Archivo → Subir notebook) o Jupyter. El sitio no ejecuta estos lenguajes directamente.
- **Proyectos:** descarga briefs y usa rúbricas de autoevaluación.
- **Mi progreso:** exporta/importa un JSON con lecturas, notas, quizzes y rúbricas. Solo se guarda en el navegador actual; no hay autenticación ni sincronización.

## Publicar en GitHub Pages

Repositorio propuesto: `analista-lab`. Para una cuenta GitHub Free, utiliza un repositorio público.

1. Crea el repositorio y añade al menos `index.html`. Para conservar el código editable y materiales, sube todos los archivos de este proyecto.
2. En **Settings → Pages → Build and deployment → Source**, selecciona **Deploy from a branch**.
3. Selecciona la rama `main` y carpeta **/(root)**; guarda.
4. Espera la publicación y usa la URL que muestre GitHub. En un repositorio llamado `analista-lab` de la cuenta `luksoto`, la dirección prevista es `https://luksoto.github.io/analista-lab/` (no supone que ya esté publicada).

El sitio usa rutas con `#` y no requiere reglas de redirección para abrir módulos directamente. No incluye secretos ni datos reales.

Guía oficial: <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>

## Editar contenido o diseño

| Archivo | Propósito |
| --- | --- |
| `course.js` | Módulos, lecciones, prácticas, quizzes, recursos y proyectos |
| `core.js` | Estadística, evaluación, validación de progreso y exportaciones |
| `app.js` | Navegación, vistas e interacción |
| `styles.css` | Diseño y adaptación a móviles |
| `shell.html` | Estructura y metadatos |
| `build.py` | Genera `index.html`, notebooks, CSV y base SQLite |
| `PROGRAMA.md` | Ruta ampliada propuesta y mejoras educativas |
| `FUENTES.md` | Autoría y procedencia de recursos externos |

Después de editar, ejecuta `python build.py` (requiere Python 3 y Node.js). Esto regenera el archivo publicable y los datos descargables. No necesitas ejecutar este comando para usar la versión incluida.

## Verificación

```bash
python build.py
node --test tests/core.test.js
node tests/smoke.js
python tests/verify.py
```

La verificación Python requiere numpy, pandas, matplotlib y scikit-learn. Las pruebas ejecutan los tres notebooks y comprueban consultas SQLite y totales. Las pruebas de interfaz renderizan plantillas y ejercitan manejadores con un DOM simulado; **no equivalen a QA visual en navegador**.

## Datos

Mercado Andino es ficticio. El CSV limpio tiene 12 ventas y 6 clientes. Ingresos: 2440 UM; coste: 1660 UM; margen: 780 UM. El margen no incluye gastos operativos.

El archivo raw contiene 13 filas por una copia exacta de una operación, espacios/formato en ciudades y un coste ausente. Después de quitar la copia hay 12 ventas y cobertura de costes de 11/12. El margen de operaciones con costes conocidos es 745 UM; el margen total completo no se conoce sin recuperar el coste ausente. No se rellena silenciosamente con cero.

Los 600 casos del notebook de modelos son sintéticos e independientes. Se usan para practicar split, validación cruzada, pipelines, clasificación, PCA y clustering.

## Próximas mejoras

Ampliar lecciones y ejercicios, añadir datasets abiertos con licencia, más preguntas por objetivo, accesibilidad y QA visual, revisión de proyectos y, si se necesita, cuentas y sincronización mediante un servicio externo. GitHub Pages por sí solo aloja archivos estáticos.

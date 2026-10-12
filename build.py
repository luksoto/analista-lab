"""Genera un sitio autónomo para GitHub Pages y sus materiales descargables."""
from pathlib import Path
import csv
import io
import json
import sqlite3
import subprocess

ROOT = Path(__file__).resolve().parent


def js_value(expression):
    result = subprocess.run(['node', '-e', f'process.stdout.write(JSON.stringify({expression}))'], cwd=ROOT, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def cell(kind, text):
    data = {'cell_type': kind, 'metadata': {}, 'source': text.splitlines(keepends=True)}
    if kind == 'code':
        data.update(execution_count=None, outputs=[])
    return data


def notebook(cells):
    return {'nbformat': 4, 'nbformat_minor': 5, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python', 'version': '3.12'}, 'colab': {'provenance': []}}, 'cells': [dict(c, id=f'cell-{i:03}') for i, c in enumerate(cells)]}


def main():
    course = js_value("require('./course.js')")
    sales = course['sales']
    raw = js_value("require('./core.js').rawSales(require('./course.js').sales)")
    sql = js_value("require('./core.js').sqlSetup(require('./course.js').sales)")
    data = ROOT / 'data'
    data.mkdir(exist_ok=True)
    for name, rows in [('ventas.csv', sales), ('ventas_raw.csv', raw)]:
        with (data / name).open('w', encoding='utf-8-sig', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(sales[0]))
            writer.writeheader()
            writer.writerows(rows)
    (data / 'mercado_andino.sql').write_text(sql, encoding='utf-8')
    dbpath = data / 'mercado_andino.sqlite'
    dbpath.unlink(missing_ok=True)
    with sqlite3.connect(dbpath) as conn:
        conn.executescript(sql)

    sql_nb = notebook([
        cell('markdown', '# Analista Lab · SQL con SQLite\n\n**Datos sintéticos, no personas reales.** Abre en Colab con Archivo → Subir notebook, o en Jupyter. Ejecuta las celdas desde arriba. Python crea una base SQLite en memoria; las consultas son SQL real. No requiere descargar datos externos.\n\nObjetivos: filtrar, agrupar, unir y calcular acumulados. Dialecto: SQLite. Las funciones de fecha y LIMIT pueden diferir en otros motores.\n'),
        cell('code', 'import sqlite3\nimport pandas as pd\n\nconn = sqlite3.connect(":memory:")\nsetup_sql = ' + repr(sql) + '\nconn.executescript(setup_sql)\nprint("SQLite", sqlite3.sqlite_version)\nprint(pd.read_sql_query("SELECT * FROM ventas LIMIT 5", conn))\n'),
        cell('markdown', '## Comprueba la base\n\nHay 12 ventas y 6 clientes distintos. Ingresos: 2440 UM; costes: 1660 UM; margen: 780 UM. Estos totales pertenecen al archivo **limpio**, con todos los costes conocidos.\n'),
        cell('code', 'assert conn.execute("SELECT COUNT(*) FROM ventas").fetchone()[0] == 12\nassert conn.execute("SELECT SUM(importe) FROM ventas").fetchone()[0] == 2440\nassert conn.execute("SELECT SUM(importe-coste) FROM ventas").fetchone()[0] == 780\nprint("Base preparada y totales comprobados.")\n'),
        cell('markdown', '## Reto 1 · Ingresos por ciudad\n\nEdita la consulta para devolver ciudad e ingresos, ordenados de mayor a menor. Después cambia el filtro para mostrar solo operaciones de Tecnología con importe >= 250.\n'),
        cell('code', '# Reemplaza esta consulta con tu solución.\nconsulta = "SELECT * FROM ventas LIMIT 5;"\nresultado = pd.read_sql_query(consulta, conn)\nprint(resultado.to_string(index=False))\n'),
        cell('markdown', '## Reto 2 · JOIN sin duplicar\n\nUne ventas con clientes. Comprueba que siguen existiendo 12 filas y que la suma de importes sigue siendo 2440. La tabla clientes contiene una fila por cliente_id. Explica qué ocurriría si esa clave estuviera duplicada.\n'),
        cell('code', '# Escribe aquí tu JOIN y tus comprobaciones.\n# pd.read_sql_query(consulta_join, conn)\n'),
        cell('markdown', '## Reto 3 · CTE y ventana\n\nConstruye una CTE de ingresos mensuales. Añade SUM(ingresos) OVER para el acumulado. Enero, febrero y marzo tienen 750, 760 y 930 UM; los acumulados deben ser 750, 1510 y 2440. Usa un marco ROWS explícito.\n'),
        cell('code', '# Escribe y ejecuta tu consulta mensual.\n'),
        cell('markdown', '## Revisión, después de intentarlo\n\n- Ingresos por ciudad: Mendoza 960, Neuquén 750, Córdoba 730.\n- Un JOIN con claves múltiples puede multiplicar ventas: comprueba cardinalidad y totales.\n- La CTE puede agrupar con substr(fecha,1,7); la ventana ordena por mes y acumula desde UNBOUNDED PRECEDING hasta CURRENT ROW.\n\nEntrega la consulta, resultado y explicación de cada comprobación. Resolver el notebook requiere editar las celdas de reto; ejecutar únicamente la preparación no resuelve los ejercicios.\n\nReferencia: https://www.sqlite.org/lang_select.html\n')
    ])
    python_nb = notebook([
        cell('markdown', '# Analista Lab · Python, limpieza y EDA\n\nDataset sintético integrado. Ejecuta desde arriba en Colab o Jupyter. Hay una tabla limpia de referencia y una versión raw con errores intencionales. Necesitas pandas y matplotlib; vienen habitualmente en Colab. En local: `pip install pandas matplotlib`.\n'),
        cell('code', 'import json\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\nventas = json.loads(' + repr(json.dumps(sales, ensure_ascii=False)) + ')\nraw_rows = json.loads(' + repr(json.dumps(raw, ensure_ascii=False)) + ')\nlimpio = pd.DataFrame(ventas)\nraw = pd.DataFrame(raw_rows)\nprint(raw.info())\nprint(raw.head())\n'),
        cell('markdown', '## Reto 1 · Auditoría antes de modificar\n\nCuenta filas, venta_id únicos, costes ausentes y ciudades distintas. ¿El duplicado es una copia exacta o tiene información contradictoria? Usa `duplicated`, `isna` y `nunique`.\n'),
        cell('code', '# Añade aquí tu auditoría.\nprint("Filas raw:", len(raw))\nprint("Ventas distintas:", raw["venta_id"].nunique())\n'),
        cell('markdown', '## Demostración · Limpieza reproducible\n\nLa venta repetida es una copia exacta. No habría que eliminar una clave repetida con valores contradictorios sin investigar. El coste ausente **sigue siendo desconocido**: no se rellena con cero ni con el original limpio.\n'),
        cell('code', 'df = raw.copy()\nrepetidas = df[df["venta_id"].duplicated(keep=False)]\nconflictos = repetidas.groupby("venta_id").nunique(dropna=False).gt(1).any(axis=1)\nassert not conflictos.any(), "Investigar ventas repetidas con valores contradictorios"\ndf["ciudad"] = df["ciudad"].str.strip().str.title()\ndf["coste"] = pd.to_numeric(df["coste"], errors="coerce")\ndf = df.drop_duplicates(subset=["venta_id"]).copy()\ndf["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d")\ndf["mes"] = df["fecha"].dt.to_period("M").astype(str)\ndf["margen"] = df["importe"] - df["coste"]\nprint("Filas limpias:", len(df))\nprint("Costes conocidos:", df["coste"].notna().sum(), "/", len(df))\nprint("Ingresos totales:", df["importe"].sum())\nprint("Margen de operaciones con coste conocido:", df.loc[df["coste"].notna(), "margen"].sum())\nprint("No es el margen total completo: falta recuperar un coste.")\n'),
        cell('markdown', '## Reto 2 · Reproduce un KPI\n\nCalcula ingresos, margen y clientes distintos usando **limpio**. Deben coincidir con SQL y Excel. Luego explica por qué no puedes calcular el margen total completo usando solo raw/df.\n'),
        cell('code', '# Escribe tus cálculos. Referencia: 2440 UM, 780 UM, 6 clientes.\n'),
        cell('markdown', '## Demostración · Un gráfico comprobable\n\nLa limpieza no altera los ingresos. Compara categorías, ciudades y meses; evita atribuir causas a estas 12 ventas.\n'),
        cell('code', 'resumen = df.groupby("ciudad")["importe"].sum().sort_values()\nax = resumen.plot.barh(color="#b64d24", figsize=(7, 3))\nax.set_xlabel("Ingresos (UM)")\nax.set_title("Ingresos por ciudad · Caso sintético")\nplt.tight_layout()\nplt.show()\n'),
        cell('markdown', '## Reto 3 · Explica un hallazgo\n\nAgrupa por categoría, identifica su número de ventas y su ingreso medio. Escribe hallazgo, límite y siguiente pregunta. Entrega también un registro de cambios (13 → 12 filas, ciudades normalizadas y coste sin recuperar).\n'),
        cell('code', '# Añade una agregación con groupby y describe el hallazgo en una celda Markdown.\n'),
        cell('markdown', '## Comprobaciones de la demostración\n\nEstas comprobaciones verifican la preparación del ejemplo. No evalúan automáticamente las respuestas libres de los retos.\n'),
        cell('code', 'assert len(df) == 12\nassert df["ciudad"].nunique() == 3\nassert df["coste"].isna().sum() == 1\nassert df["importe"].sum() == 2440\nassert df.loc[df["coste"].notna(), "margen"].sum() == 745\nassert limpio["importe"].sum() == 2440\nassert (limpio["importe"] - limpio["coste"]).sum() == 780\nprint("Preparación comprobada. Revisa tus respuestas con el módulo.")\n'),
        cell('markdown', 'Referencias: https://pandas.pydata.org/docs/getting_started/intro_tutorials/ y https://docs.python.org/es/3/tutorial/\n')
    ])
    models_nb = notebook([
        cell('markdown', '# Analista Lab · Modelos y validación\n\n600 observaciones sintéticas independientes. No representan clientes reales. Objetivo: practicar clasificación, referencia y selección sin fuga de información. No sirve para recomendar decisiones reales. Dependencias: numpy, pandas, scikit-learn; normalmente disponibles en Colab. En local: `pip install numpy pandas scikit-learn`.\n\nSeleccionaremos C mediante validación cruzada dentro de entrenamiento. La prueba se consulta al final para evaluar el modelo elegido y la referencia.\n'),
        cell('code', 'import numpy as np\nimport pandas as pd\nfrom sklearn.datasets import make_classification\nfrom sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.dummy import DummyClassifier\nfrom sklearn.metrics import balanced_accuracy_score, precision_score, recall_score, confusion_matrix\n\nX_array, y_array = make_classification(n_samples=600, n_features=6, n_informative=4, n_redundant=1, weights=[0.8, 0.2], random_state=42)\nX = pd.DataFrame(X_array, columns=[f"feature_{i}" for i in range(6)])\ny = pd.Series(y_array, name="clase")\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\nassert set(X_train.index).isdisjoint(set(X_test.index))\nprint("Entrenamiento:", len(X_train), "Prueba reservada:", len(X_test))\n'),
        cell('markdown', '## Validación dentro de entrenamiento\n\nCada fold ajusta imputación y escalado únicamente sobre sus filas de entrenamiento porque están dentro del pipeline. La selección compara balanced accuracy; revisa después si esa métrica coincide con el coste de los errores del problema.\n'),
        cell('code', 'cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\nresultados = []\nfor valor_c in [0.1, 1.0, 10.0]:\n    candidato = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(C=valor_c, max_iter=2000, random_state=42))\n    scores = cross_val_score(candidato, X_train, y_train, cv=cv, scoring="balanced_accuracy")\n    resultados.append({"C": valor_c, "cv_media": float(scores.mean()), "cv_sd": float(scores.std(ddof=1))})\ncomparacion = pd.DataFrame(resultados).sort_values("cv_media", ascending=False)\nmejor_c = float(comparacion.iloc[0]["C"])\nprint(comparacion.to_string(index=False))\nprint("C seleccionado sin consultar prueba:", mejor_c)\n'),
        cell('markdown', '## Cierra las decisiones antes de evaluar\n\nNo cambies C, las variables ni el umbral usando los resultados de la siguiente celda. Si haces nuevas decisiones después, necesitarás otra prueba independiente para una evaluación final honesta.\n'),
        cell('code', 'modelo = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(C=mejor_c, max_iter=2000, random_state=42))\nreferencia = DummyClassifier(strategy="most_frequent")\nmodelo.fit(X_train, y_train)\nreferencia.fit(X_train, y_train)\n\nevaluacion = []\nfor nombre, estimador in [("Referencia", referencia), ("Logística", modelo)]:\n    pred = estimador.predict(X_test)\n    evaluacion.append({"modelo": nombre, "balanced_accuracy": balanced_accuracy_score(y_test, pred), "precision": precision_score(y_test, pred, zero_division=0), "recall": recall_score(y_test, pred, zero_division=0)})\nprint(pd.DataFrame(evaluacion).to_string(index=False))\nprint("Matriz logística (filas=reales, columnas=predichas):")\nprint(confusion_matrix(y_test, modelo.predict(X_test), labels=[0, 1]))\n'),
        cell('markdown', '## Reto · Defiende el informe\n\nSi el modelo no supera la referencia en prueba, no lo presentes como una mejora. Informa el resultado y diseña un nuevo ciclo de evaluación con otra prueba independiente antes de hacer ajustes.\n\n1. Explica por qué el split aleatorio estratificado es razonable para estos datos sintéticos independientes, pero puede fallar con datos temporales o repetidos por cliente.\n2. Compara referencia y modelo. Describe qué errores importa minimizar.\n3. Propón una mejora y cómo evaluarla sin reutilizar la prueba para seleccionar.\n4. Explica por qué un resultado sintético no demuestra desempeño en una empresa real.\n'),
        cell('code', '# Añade comprobaciones o análisis exploratorio de entrenamiento.\n# No utilices X_test/y_test para elegir nuevas variables o parámetros.\n'),
        cell('markdown', '## Extensión · PCA y clustering exploratorio\n\nEstos son ejemplos sobre entrenamiento. PCA no usa y; la varianza explicada no es accuracy. Estandarizamos porque las distancias y la varianza dependen de la escala. No se presentan estos grupos como segmentos de negocio validados.\n'),
        cell('code', 'from sklearn.decomposition import PCA\nfrom sklearn.cluster import KMeans\n\npca_pipeline = make_pipeline(StandardScaler(), PCA(n_components=0.80, svd_solver="full"))\ncomponentes = pca_pipeline.fit_transform(X_train)\nprint("Componentes para al menos 80 % de varianza:", componentes.shape[1])\nprint("Varianza acumulada:", pca_pipeline[-1].explained_variance_ratio_.sum())\ncluster_pipeline = make_pipeline(StandardScaler(), KMeans(n_clusters=3, n_init=10, random_state=42))\nclusters = cluster_pipeline.fit_predict(X_train)\nprint("Tamaños de grupos exploratorios:", np.bincount(clusters))\n'),
        cell('markdown', 'Referencia oficial para evitar fuga de información: https://scikit-learn.org/stable/common_pitfalls.html\n\nReferencia de PCA: https://scikit-learn.org/stable/modules/decomposition.html#pca\n')
    ])
    notebooks = {'sql': sql_nb, 'python': python_nb, 'models': models_nb}
    names = {'sql': '01_sql.ipynb', 'python': '02_python_limpieza_eda.ipynb', 'models': '03_modelos.ipynb'}
    (ROOT / 'notebooks').mkdir(exist_ok=True)
    for key, nb in notebooks.items():
        (ROOT / 'notebooks' / names[key]).write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding='utf-8')
    (ROOT / 'notebooks.js').write_text('const NOTEBOOKS = ' + json.dumps(notebooks, ensure_ascii=False) + ';\n', encoding='utf-8')
    html = (ROOT / 'shell.html').read_text(encoding='utf-8')
    for token, filename in [('STYLES', 'styles.css'), ('COURSE', 'course.js'), ('CORE', 'core.js'), ('NOTEBOOKS', 'notebooks.js'), ('APP', 'app.js')]:
        text = (ROOT / filename).read_text(encoding='utf-8')
        if token != 'STYLES':
            text = text.replace('</script', '<\\/script')
        html = html.replace('/* INLINE_' + token + ' */', text)
    (ROOT / 'index.html').write_text(html, encoding='utf-8')
    (ROOT / '.nojekyll').touch()
    print(f'Sitio autónomo generado: index.html ({len(html.encode())} bytes); 3 notebooks y datasets.')


if __name__ == '__main__':
    main()

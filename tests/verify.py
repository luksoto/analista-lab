"""Comprueba HTML, consultas de ejemplo y ejecuta notebooks en Python real."""
from pathlib import Path
import json
import sqlite3
import os

os.environ['MPLBACKEND'] = 'Agg'
os.environ['OMP_NUM_THREADS'] = '2'
ROOT = Path(__file__).resolve().parents[1]
from html.parser import HTMLParser


class Tags(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.items = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.items.append((tag, dict(attrs)))

    def select(self, tag):
        return [attrs for name, attrs in self.items if name == tag]

    def ids(self):
        return [attrs['id'] for _, attrs in self.items if 'id' in attrs]

html = (ROOT / 'index.html').read_text(encoding='utf-8')
soup = Tags(html)
assert soup.select('html')[0]['lang'] == 'es'
assert len(soup.select('script')) == 4
assert 'INLINE_' not in html
assert not any('src' in s for s in soup.select('script'))
ids = soup.ids()
assert len(ids) == len(set(ids))

rendered = json.loads((ROOT / 'tests/render-output.json').read_text())
module_ids = [key.removeprefix('module-') for key in rendered if key.startswith('module-')]
for page, source in rendered.items():
    fragment = Tags(source)
    ids = fragment.ids()
    assert len(ids) == len(set(ids)), page
    for anchor in fragment.select('a'):
        href = anchor['href']
        if href.startswith('#modulo/'):
            assert href.split('/')[-1] in module_ids, (page, href)
        if anchor.get('target') == '_blank':
            assert 'noopener' in anchor.get('rel', '').split(), (page, href)
    for image in fragment.select('iframe'):
        assert image.get('title')

conn = sqlite3.connect(':memory:')
conn.executescript((ROOT / 'data/mercado_andino.sql').read_text())
assert conn.execute('SELECT ciudad,SUM(importe) ingresos FROM ventas GROUP BY ciudad ORDER BY ingresos DESC').fetchall() == [('Mendoza', 960), ('Neuquén', 750), ('Córdoba', 730)]
query = '''WITH mensual AS (SELECT substr(fecha,1,7) mes,SUM(importe) ingresos FROM ventas GROUP BY substr(fecha,1,7)) SELECT mes,ingresos,SUM(ingresos) OVER (ORDER BY mes ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM mensual ORDER BY mes'''
assert conn.execute(query).fetchall() == [('2026-01', 750, 750), ('2026-02', 760, 1510), ('2026-03', 930, 2440)]
assert conn.execute('SELECT COUNT(*),SUM(v.importe) FROM ventas v LEFT JOIN clientes c ON v.cliente_id=c.cliente_id').fetchone() == (12, 2440)

for path in sorted((ROOT / 'notebooks').glob('*.ipynb')):
    nb = json.loads(path.read_text(encoding='utf-8'))
    assert nb['nbformat'] == 4 and nb['nbformat_minor'] == 5
    assert nb['metadata']['kernelspec']['name'] == 'python3'
    assert len({cell['id'] for cell in nb['cells']}) == len(nb['cells'])
    scope = {'__name__': '__main__'}
    for index, cell in enumerate(nb['cells']):
        assert cell['cell_type'] in ('markdown', 'code')
        assert isinstance(cell['source'], list)
        if cell['cell_type'] == 'code':
            assert cell['outputs'] == [] and cell['execution_count'] is None
            exec(compile(''.join(cell['source']), str(path) + f':cell{index}', 'exec'), scope)
    if path.name.startswith('03'):
        assert len(scope['X_train']) == 480 and len(scope['X_test']) == 120
        assert set(scope['X_train'].index).isdisjoint(scope['X_test'].index)
        import numpy as np
        assert np.allclose(scope['modelo'].named_steps['standardscaler'].mean_, scope['X_train'].mean().to_numpy())
    print('Notebook ejecutado:', path.name)
print('HTML, rutas, consultas SQL y tres notebooks verificados. No incluye QA visual en navegador.')

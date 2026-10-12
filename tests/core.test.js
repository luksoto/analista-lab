const test=require('node:test');
const assert=require('node:assert/strict');
const C=require('../core.js');
const course=require('../course.js');

test('La ruta tiene contenido completo y referencias válidas',()=>{
  assert.equal(course.modules.length,14);
  assert.equal(new Set(course.modules.map(m=>m.id)).size,14);
  assert.equal(course.modules.flatMap(m=>m.lessons).length,28);
  assert.equal(course.modules.flatMap(m=>m.quiz).length,42);
  assert.equal(course.projects.length,3);
  for(const m of course.modules){
    assert.equal(m.lessons.length,2);assert.equal(m.quiz.length,3);
    assert.ok(course.phases.some(p=>p.id===m.phase));
    for(const l of m.lessons){assert.ok(l.title&&l.body&&l.example&&l.takeaway);}
    assert.ok(m.practice.prompt&&m.practice.hint&&m.practice.solution&&m.practice.steps.length);
    for(const q of m.quiz){assert.equal(q.options.length,3);assert.ok(q.answer>=0&&q.answer<3);assert.ok(q.why);}
    for(const id of m.resources)assert.ok(course.resources.some(r=>r.id===id));
  }
});
test('Los valores extremos cambian media y mediana según el ejemplo',()=>{
  let s=C.stats([10,12,12,14,16]);assert.equal(s.mean,12.8);assert.equal(s.median,12);assert.equal(s.range,6);
  s=C.stats([10,12,12,14,16,150]);assert.ok(Math.abs(s.mean-35.6666666667)<1e-8);assert.equal(s.median,13);
});
test('Desviación muestral, conjuntos pares y números negativos',()=>{
  assert.equal(C.stats([2,4,8,10]).median,6);
  assert.equal(C.stats([-4,-2,0]).mean,-2);
  assert.equal(C.stats([1,2,3],true).variance,1);
  assert.equal(C.stats([5],true).std,null);
  assert.equal(C.stats([5]).std,0);
});
test('El laboratorio rechaza entradas no numéricas y tamaños excesivos',()=>{
  assert.deepEqual(C.parseNumbers('1.5 -2; 3,4'),[1.5,-2,3,4]);
  for(const text of ['', '1 hola', '1 Infinity','2e100','<script>','1 0x22'])assert.throws(()=>C.parseNumbers(text));
  assert.throws(()=>C.parseNumbers(Array(101).fill('1').join(' ')));
});
test('El dataset y todos los agrupamientos concilian',()=>{
  assert.equal(course.sales.length,12);
  assert.equal(new Set(course.sales.map(r=>r.cliente_id)).size,6);
  assert.equal(course.sales.reduce((s,r)=>s+r.importe,0),2440);
  assert.equal(course.sales.reduce((s,r)=>s+r.importe-r.coste,0),780);
  assert.deepEqual(C.groupSales(course.sales,'ciudad'),[{name:'Mendoza',value:960},{name:'Neuquén',value:750},{name:'Córdoba',value:730}]);
  assert.deepEqual(C.groupSales(course.sales,'mes').map(r=>r.value),[750,760,930]);
  for(const g of ['ciudad','mes','categoria','canal'])assert.equal(C.groupSales(course.sales,g).reduce((s,r)=>s+r.value,0),2440);
});
test('La versión raw conserva el problema de coste desconocido',()=>{
  const raw=C.rawSales(course.sales);assert.equal(raw.length,13);assert.equal(new Set(raw.map(r=>r.venta_id)).size,12);assert.equal(raw.filter(r=>r.coste===null).length,1);
  assert.equal(course.sales[2].coste,45);assert.notEqual(raw[0].ciudad,course.sales[0].ciudad);
});
test('El quiz exige respuestas válidas y no aprueba formularios incompletos',()=>{
  const m=course.modules[0];assert.throws(()=>C.gradeQuiz(m,[0,null,2]));assert.throws(()=>C.gradeQuiz(m,[0,1,8]));assert.throws(()=>C.gradeQuiz(m,[1]));
  for(const module of course.modules)assert.equal(C.gradeQuiz(module,module.quiz.map(q=>q.answer)),3);
});
test('Repetir un quiz conserva la mejor nota y cuenta intentos',()=>{
  const p=C.emptyProgress(),m=course.modules[0];
  C.recordQuiz(m,p,m.quiz.map(q=>q.answer));C.recordQuiz(m,p,m.quiz.map(q=>(q.answer+1)%3));
  assert.deepEqual(p.quizzes[m.id],{best:3,attempts:2});
});
test('Completar un módulo requiere lecturas y un quiz suficiente',()=>{
  const p=C.emptyProgress(),m=course.modules[0];p.lessons[m.id+':0']=true;p.lessons[m.id+':1']=true;
  assert.equal(C.moduleComplete(m,p),false);p.quizzes[m.id]={best:1,attempts:1};assert.equal(C.moduleComplete(m,p),false);p.quizzes[m.id].best=2;assert.equal(C.moduleComplete(m,p),true);delete p.lessons[m.id+':0'];assert.equal(C.moduleComplete(m,p),false);
});
test('Importar filtra claves ajenas, puntuaciones falsas y notas demasiado largas',()=>{
  const p=C.emptyProgress();p.lessons['fundamentos:0']=true;p.lessons['falso:0']=true;p.quizzes['fundamentos']={best:99,attempts:1};p.notes.fundamentos='x'.repeat(12000);p.lastModule='falso';
  const clean=C.validateProgress(p,course);assert.equal(clean.lessons['fundamentos:0'],true);assert.equal(clean.lessons['falso:0'],undefined);assert.equal(clean.quizzes.fundamentos,undefined);assert.equal(clean.notes.fundamentos.length,10000);assert.equal(clean.lastModule,'fundamentos');assert.throws(()=>C.validateProgress({schema:2},course));
});
test('Exportar e importar conserva el progreso legítimo',()=>{
  const p=C.emptyProgress();p.notes.python='Mi explicación';p.lessons['python:1']=true;p.quizzes.python={best:2,attempts:3};p.projects.comercial=[true,false,true];p.lastModule='python';
  const saved=C.validateProgress(JSON.parse(JSON.stringify(p)),course);assert.equal(saved.notes.python,'Mi explicación');assert.equal(saved.lessons['python:1'],true);assert.deepEqual(saved.quizzes.python,{best:2,attempts:3});assert.equal(saved.projects.comercial[2],true);assert.equal(saved.lastModule,'python');
});
test('Búsquedas sin acentos y contenido seguro al mostrar notas',()=>{
  assert.equal(C.normalize('Estadística y CÓRDOBA'),'estadistica y cordoba');
  assert.equal(C.escape('<img src=x onerror="alert(1)">'),'&lt;img src=x onerror=&quot;alert(1)&quot;&gt;');
});

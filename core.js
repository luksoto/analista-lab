'use strict';
const LabCore = (() => {
  const normalize = s => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const escape = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function parseNumbers(text) {
    const parts = String(text).trim().split(/[\s,;]+/).filter(Boolean);
    if (!parts.length) throw new Error('Introduce al menos un número.');
    if (parts.length > 100) throw new Error('Usa como máximo 100 números.');
    const nums = parts.map(s => /^[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[-+]?\d+)?$/i.test(s) ? Number(s) : NaN);
    if (nums.some(n => !Number.isFinite(n) || Math.abs(n)>1e9)) throw new Error('Revisa los valores. Separa números con espacios; usa punto para los decimales y magnitudes de hasta 1 000 000 000.');
    return nums;
  }
  function stats(values, sample=false) {
    if (!values.length) throw new Error('No hay observaciones.');
    const sorted=[...values].sort((a,b)=>a-b), n=values.length;
    const mean=values.reduce((sum,v)=>sum+v,0)/n;
    const mid=Math.floor(n/2), median=n%2 ? sorted[mid] : (sorted[mid-1]+sorted[mid])/2;
    const variance=sample && n<2 ? null : values.reduce((s,v)=>s+(v-mean)**2,0)/(sample?n-1:n);
    return {n,mean,median,min:sorted[0],max:sorted[n-1],range:sorted[n-1]-sorted[0],variance,std:variance===null?null:Math.sqrt(variance)};
  }
  function groupSales(sales,group) {
    const result=new Map();
    for(const row of sales){const key=group==='mes'?row.fecha.slice(0,7):row[group];result.set(key,(result.get(key)||0)+row.importe);}
    const entries=Array.from(result,([name,value])=>({name,value}));
    return group==='mes'?entries.sort((a,b)=>a.name.localeCompare(b.name)):entries.sort((a,b)=>b.value-a.value);
  }
  function gradeQuiz(module, answers) {
    if (!Array.isArray(answers) || answers.length!==module.quiz.length || answers.some((a,i)=>!Number.isInteger(a)||a<0||a>=module.quiz[i].options.length)) throw new Error('Responde las tres preguntas antes de revisar.');
    return module.quiz.filter((q,i)=>q.answer===answers[i]).length;
  }
  function emptyProgress(){return {schema:1,lessons:{},quizzes:{},projects:{},notes:{},lastModule:'fundamentos'};}
  function validateProgress(value,course) {
    if (!value || typeof value!=='object' || Array.isArray(value) || value.schema!==1) throw new Error('Este archivo no tiene el formato de progreso de Analista Lab.');
    const clean=emptyProgress();
    for(const mod of course.modules){
      for(let i=0;i<mod.lessons.length;i++){const id=mod.id+':'+i;if(value.lessons?.[id]===true) clean.lessons[id]=true;}
      const q=value.quizzes?.[mod.id];
      if(q && Number.isInteger(q.best) && q.best>=0 && q.best<=mod.quiz.length && Number.isInteger(q.attempts) && q.attempts>=0) clean.quizzes[mod.id]={best:q.best,attempts:Math.min(q.attempts,100000)};
      if(typeof value.notes?.[mod.id]==='string') clean.notes[mod.id]=value.notes[mod.id].slice(0,10000);
    }
    for(const p of course.projects){clean.projects[p.id]=[];for(let i=0;i<p.criteria.length;i++){if(value.projects?.[p.id]?.[i]===true) clean.projects[p.id][i]=true;}}
    if(course.modules.some(m=>m.id===value.lastModule)) clean.lastModule=value.lastModule;
    return clean;
  }
  function moduleComplete(mod,progress){return mod.lessons.every((_,i)=>progress.lessons[mod.id+':'+i]) && (progress.quizzes[mod.id]?.best||0)>=2;}
  function recordQuiz(mod,progress,answers){const score=gradeQuiz(mod,answers),previous=progress.quizzes[mod.id];progress.quizzes[mod.id]={best:Math.max(score,previous?.best||0),attempts:(previous?.attempts||0)+1};return score;}
  function csv(sales){const cols=['venta_id','fecha','cliente_id','ciudad','categoria','canal','importe','coste'];const quote=x=>'"'+String(x??'').replace(/"/g,'""')+'"';return cols.join(',')+'\n'+sales.map(row=>cols.map(c=>quote(row[c])).join(',')).join('\n')+'\n';}
  function rawSales(sales){const rows=sales.map(r=>({...r}));rows[0].ciudad=' neuquén ';rows[4].ciudad=' CÓRDOBA ';rows[2].coste=null;rows.push({...rows[11]});return rows;}
  function sqlSetup(sales){const cols=['venta_id','fecha','cliente_id','ciudad','categoria','canal','importe','coste'];const quote=v=>typeof v==='number'?String(v):v===null?'NULL':"'"+String(v).replace(/'/g,"''")+"'";return 'DROP TABLE IF EXISTS ventas;\nCREATE TABLE ventas (venta_id INTEGER PRIMARY KEY, fecha TEXT, cliente_id INTEGER, ciudad TEXT, categoria TEXT, canal TEXT, importe REAL, coste REAL);\nINSERT INTO ventas VALUES\n'+sales.map(r=>'('+cols.map(c=>quote(r[c])).join(',')+')').join(',\n')+';\nCREATE TABLE clientes (cliente_id INTEGER PRIMARY KEY, segmento TEXT);\nINSERT INTO clientes VALUES (1,\'Frecuente\'),(2,\'Frecuente\'),(3,\'Frecuente\'),(4,\'Ocasional\'),(5,\'Ocasional\'),(6,\'Ocasional\');\n';}
  return {normalize,escape,parseNumbers,stats,groupSales,gradeQuiz,emptyProgress,validateProgress,moduleComplete,recordQuiz,csv,rawSales,sqlSetup};
})();
if(typeof module!=='undefined') module.exports=LabCore;

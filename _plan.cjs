
require('./rhythm.js');const R=globalThis.Rhythm||require('./rhythm.js');const P=require('./posts.json');const by=Object.fromEntries(P.map((p,i)=>[p.id,i]));
const START=["p03", "p52", "p02", "p47", "p06", "p05", "p50", "p41", "p49"], PARK=new Set(["p13", "p31", "p45"]);
const rest=P.map((_,i)=>i).filter(i=>!START.includes(P[i].id)&&!PARK.has(P[i].id));
const order=[...START.map(id=>by[id]),...rest];const locked=new Set(START.map(id=>by[id]));
let best=null;for(const seed of [3,7,11,19,23,31]){const r=R.optimize(order,P,R.DEFAULTS,{seed,locked,iters:80000});if(!best||r.cost<best.cost)best=r;}
const ev=R.evaluate(best.order,P,R.DEFAULTS,true);
console.log(JSON.stringify({order:best.order.map(i=>P[i].id),cost:best.cost,issues:ev.issues.length}));

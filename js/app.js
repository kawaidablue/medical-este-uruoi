const mb=document.getElementById('menuBtn'),nv=document.getElementById('navOverlay'),nc=document.getElementById('navClose');
const openNav=()=>{nv.classList.add('open');document.body.style.overflow='hidden';};
const closeNav=()=>{nv.classList.remove('open');document.body.style.overflow='';};
mb.addEventListener('click',openNav);
if(nc)nc.addEventListener('click',closeNav);
nv.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeNav));
const els=[...document.querySelectorAll('.reveal')];
function shw(el){el.classList.add('in');el.__shown=1;}
function rev(){
  const vh=window.innerHeight||document.documentElement.clientHeight;
  for(const el of els){ if(el.__shown)continue; const r=el.getBoundingClientRect(); if(r.top<vh*0.9&&r.bottom>-40)shw(el); }
}
window.addEventListener('scroll',rev,{passive:true});
window.addEventListener('resize',rev);
rev(); setTimeout(rev,200);
setTimeout(()=>{for(const el of els)if(!el.__shown)shw(el);},2600);

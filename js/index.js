(function(){
  var track=document.getElementById('track'); if(!track) return;
  var GAP=24;
  var originals=Array.prototype.slice.call(track.children);
  var LEN=originals.length;
  var pre=originals.map(function(n){return n.cloneNode(true);});
  var post=originals.map(function(n){return n.cloneNode(true);});
  pre.reverse().forEach(function(n){track.insertBefore(n, track.firstChild);});
  post.forEach(function(n){track.appendChild(n);});
  var cards=Array.prototype.slice.call(track.children);
  var idx=LEN, cardW=0, busy=false;
  function visible(){var w=track.parentElement.clientWidth; return w>=1000?4 : w>=640?2 : 1;}
  function size(){
    var vp=track.parentElement.clientWidth; var V=visible();
    cardW=(vp-GAP*(V-1))/V;
    cards.forEach(function(c){c.style.flex='0 0 '+cardW+'px';c.style.width=cardW+'px';});
    place(false);
  }
  function place(anim){
    track.style.transition=anim?'transform .6s cubic-bezier(.4,0,.2,1)':'none';
    track.style.transform='translateX('+(-(idx*(cardW+GAP)))+'px)';
  }
  function go(d){ if(busy)return; busy=true; idx+=d; place(true); }
  track.addEventListener('transitionend',function(){
    if(idx>=LEN*2){ idx-=LEN; place(false); }
    if(idx<LEN){ idx+=LEN; place(false); }
    busy=false;
  });
  window.uslide=function(d){ go(d); restart(); };
  var timer; function restart(){ clearInterval(timer); timer=setInterval(function(){go(1);},4000); }
  var rt; window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(size,150);});
  size(); restart();
})();

/* ===== スクロールフェードイン ===== */
(function(){
  var SEL='.hero-copy,.shead,.slider,.treat-row,.news-row,.news-more,.srow,.pickup .pimg,.pickup .pbody,.cgrid,.greet-head,.greet-body,.greet-sign,.covid-panel,.info-card,.map,.timetable,.rs-card';
  var els=Array.prototype.slice.call(document.querySelectorAll(SEL));
  if(!els.length) return;
  // セクション単位で上から順にスタッガー（全セクション統一のリズム）
  els.forEach(function(el){
    var sec=el.closest('section')||document.body;
    if(sec.__rvi==null) sec.__rvi=0;
    var i=sec.__rvi++;
    if(i>0) el.style.transitionDelay=Math.min(i*0.08,0.45)+'s';
  });
  function show(el){ el.classList.add('rv-in'); el.__shown=1; }
  // スクロール判定で確実に表示（ビューポートに入った要素を表示）
  function reveal(){
    var vh=window.innerHeight||document.documentElement.clientHeight;
    for(var k=0;k<els.length;k++){
      var el=els[k];
      if(el.__shown) continue;
      var r=el.getBoundingClientRect();
      if(r.top<vh*0.9 && r.bottom>-40) show(el);
    }
  }
  window.addEventListener('scroll',reveal,{passive:true});
  window.addEventListener('resize',reveal);
  reveal();
  setTimeout(reveal,200);
  // 安全策：万一スクロール判定が及ばなくても一定時間後に必ず全表示
  setTimeout(function(){ for(var k=0;k<els.length;k++){ if(!els[k].__shown) show(els[k]); } },2600);
})();

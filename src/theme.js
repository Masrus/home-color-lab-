(function(){
  var root=document.documentElement,hue=document.getElementById('hue'),sheet=document.getElementById('sheet'),phone=document.getElementById('phone');
  var bri=document.getElementById('bri'),CH=255,CL=22,mode='dark';
  function briL(v){return 6+v*0.86;}
  function setCustom(){CH=+hue.value;CL=briL(+bri.value);root.style.setProperty('--ch',CH);root.style.setProperty('--cl',CL.toFixed(1));document.querySelector('.briw').classList.toggle('lt',+bri.value>=50);applyTheme();}
  function rnd(a,b){return a+Math.random()*(b-a);}
  function reroll(full){var st=root.style;
    st.setProperty('--td',full?'.9s':'6s');
    st.setProperty('--ax',rnd(0,45).toFixed(0)+'%');st.setProperty('--ay',rnd(0,35).toFixed(0)+'%');
    st.setProperty('--bx',rnd(55,100).toFixed(0)+'%');st.setProperty('--by',rnd(25,65).toFixed(0)+'%');
    st.setProperty('--cx',rnd(0,100).toFixed(0)+'%');st.setProperty('--cy',rnd(75,100).toFixed(0)+'%');
    if(full){st.setProperty('--ao',rnd(-70,70).toFixed(0));st.setProperty('--bo',rnd(-70,70).toFixed(0));st.setProperty('--co',rnd(-70,70).toFixed(0));}}
  var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  setInterval(function(){if(mode==='custom'&&!document.hidden&&!rm)reroll(false);},6000);
  reroll(true);
  hue.addEventListener('input',setCustom);bri.addEventListener('input',setCustom);
  document.getElementById('next').addEventListener('click',function(){sheet.classList.add('min');});
  document.getElementById('grab').addEventListener('click',function(){sheet.classList.toggle('min');});
  var mq=window.matchMedia?window.matchMedia('(prefers-color-scheme: light)'):null;
  function applyTheme(){
    var c=mode==='custom',l=c?+bri.value>=50:(mode==='light'||(mode==='system'&&mq&&mq.matches));
    var nt=l?'light':'dark',ot=root.getAttribute('data-th');
    if(ot&&ot!==nt){root.classList.add('flip');clearTimeout(applyTheme.t);applyTheme.t=setTimeout(function(){root.classList.remove('flip');},520);}
    root.setAttribute('data-th',nt);
    if(c)root.setAttribute('data-c','1');else root.removeAttribute('data-c');
    sheet.dataset.m=mode;
  }
  if(mq&&mq.addEventListener)mq.addEventListener('change',applyTheme);
  document.querySelectorAll('.thm').forEach(function(b){b.addEventListener('click',function(){
    if(b.dataset.t==='custom')reroll(true);mode=b.dataset.t;document.querySelectorAll('.thm').forEach(function(x){x.classList.toggle('on',x===b);});applyTheme();});});
  var scr=document.querySelector('.scroll');
  scr.addEventListener('scroll',function(){root.style.setProperty('--sc',Math.min(1,scr.scrollTop/120).toFixed(3));},{passive:true});
  var DEF=getComputedStyle(root).getPropertyValue('--fontfamily/general')||'';
  var FN=[['Inter','"Inter"'],['Figtree','"Figtree"'],['Roboto Flex','"Roboto Flex"'],['PT Sans','"PT Sans"'],['SF Pro',null]];
  var fnt=document.getElementById('fnt'),fname=document.getElementById('fname');
  function setFont(i){
    fnt.value=i;var f=FN[i];fname.textContent=f[0];
    root.style.setProperty('--fontfamily/general',f[1]?f[1]+',-apple-system,system-ui,sans-serif':'');
  }
  fnt.addEventListener('input',function(){setFont(+fnt.value);});
  setFont(4);
  var lg=document.getElementById('logo');if(lg)lg.addEventListener('click',function(){sheet.classList.remove('min');});
  function fit(){var w=window.innerWidth-32;phone.style.zoom=w<393?(w/393):1;}
  window.addEventListener('resize',fit);fit();
  setCustom();
})();

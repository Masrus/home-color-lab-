(function(){
  var root=document.documentElement,hue=document.getElementById('hue'),sheet=document.getElementById('sheet'),phone=document.getElementById('phone');
  var bri=document.getElementById('bri'),CH=255,CL=22,mode='dark';
  function briL(v){return 6+v*0.86;}
  function setCustom(){CH=+hue.value;CL=briL(+bri.value);root.style.setProperty('--ch',CH);root.style.setProperty('--cl',CL.toFixed(1));applyTheme();}
  hue.addEventListener('input',setCustom);bri.addEventListener('input',setCustom);
  document.getElementById('next').addEventListener('click',function(){sheet.classList.add('min');});
  document.getElementById('grab').addEventListener('click',function(){sheet.classList.toggle('min');});
  var mq=window.matchMedia?window.matchMedia('(prefers-color-scheme: light)'):null;
  function applyTheme(){
    var c=mode==='custom',l=c?CL>=55:(mode==='light'||(mode==='system'&&mq&&mq.matches));
    root.setAttribute('data-th',l?'light':'dark');
    if(c)root.setAttribute('data-c','1');else root.removeAttribute('data-c');
    sheet.dataset.m=mode;
  }
  if(mq&&mq.addEventListener)mq.addEventListener('change',applyTheme);
  document.querySelectorAll('.thm').forEach(function(b){b.addEventListener('click',function(){
    mode=b.dataset.t;document.querySelectorAll('.thm').forEach(function(x){x.classList.toggle('on',x===b);});applyTheme();});});
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

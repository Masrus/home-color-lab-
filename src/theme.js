(function(){
  var root=document.documentElement,hue=document.getElementById('hue'),sheet=document.getElementById('sheet'),phone=document.getElementById('phone');
  var S=0;
  function setColor(h,s){
    S=s; root.style.setProperty('--thumb',s===0?'#5c5c60':''); root.style.setProperty('--h',h); root.style.setProperty('--s',s);
    hue.value=s===0?0:Math.round(h)+10;
  }
  hue.addEventListener('input',function(){var v=+hue.value;if(v<=8){setColor(+root.style.getPropertyValue('--h')||255,0);}else{setColor(v-10,70);}});
  document.getElementById('next').addEventListener('click',function(){sheet.classList.add('min');});
  document.getElementById('grab').addEventListener('click',function(){sheet.classList.toggle('min');});
  var mq=window.matchMedia?window.matchMedia('(prefers-color-scheme: light)'):null,mode='dark';
  function applyTheme(){var l=mode==='light'||(mode==='system'&&mq&&mq.matches);root.setAttribute('data-th',l?'light':'dark');}
  if(mq&&mq.addEventListener)mq.addEventListener('change',applyTheme);
  document.querySelectorAll('.thm').forEach(function(b){b.addEventListener('click',function(){
    mode=b.dataset.t;document.querySelectorAll('.thm').forEach(function(x){x.classList.toggle('on',x===b);});applyTheme();});});
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
  applyTheme();setColor(255,0);
})();

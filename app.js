// app.js - App wiring (events, progress, saved advisories)
(function(){
  window.__marketCsvCache = null;
  window.fetchMarketCsvCached = async function(url){
    if(window.__marketCsvCache) return window.__marketCsvCache;
    const res = await fetch(url, { cache: 'force-cache' });
    const text = await res.text();
    window.__marketCsvCache = text;
    return text;
  };

  let progressTimer = null, progressAuto = null, progressCurrent = 0;
  window.startProgress = function(){
    const bar = document.getElementById('appProgress');
    const pb = document.getElementById('appProgressBar');
    if(!bar || !pb) return;
    bar.style.display = 'block'; pb.style.width = '0%'; progressCurrent = 0;
    const recTxt = document.getElementById('recProgressText');
    if(recTxt){ recTxt.style.display = 'inline'; recTxt.textContent = '0%'; }
    clearInterval(progressAuto);
    progressAuto = setInterval(()=>{
      if(progressCurrent >= 90){ clearInterval(progressAuto); return; }
      window.setProgress(progressCurrent + 1);
    }, 120);
  };
  window.setProgress = function(pct){
    const pb = document.getElementById('appProgressBar');
    progressCurrent = Math.max(0, Math.min(100, pct));
    if(pb){ pb.style.width = progressCurrent + '%'; pb.setAttribute('aria-valuenow', String(progressCurrent)); }
    const recTxt = document.getElementById('recProgressText');
    if(recTxt){ recTxt.textContent = Math.round(progressCurrent) + '%'; }
  };
  window.completeProgress = function(){
    const bar = document.getElementById('appProgress'); if(!bar) return;
    clearTimeout(progressTimer); clearInterval(progressAuto);
    window.setProgress(100);
    progressTimer = setTimeout(()=>{ bar.style.display = 'none'; }, 800);
  };
})();


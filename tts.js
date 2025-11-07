// tts.js - Text-to-Speech helpers (global)
(function(){
  if(!('speechSynthesis' in window)) return;
  let voices = [];
  function loadVoices(){ try{ voices = speechSynthesis.getVoices() || []; }catch(e){ voices = []; } }
  loadVoices();
  window.speechSynthesis.onvoiceschanged = loadVoices;

  function pickVoiceForLang(lang){
    const langMap = { en:'en', hi:'hi', pa:'pa', kn:'kn', te:'te' };
    const prefix = langMap[lang] || 'en';
    let v = voices.find(v=> (v.lang||'').toLowerCase().startsWith(prefix+'-'));
    if(v) return v;
    v = voices.find(v=> (v.lang||'').toLowerCase().startsWith(prefix));
    if(v) return v;
    v = voices.find(v=> (v.lang||'').toLowerCase().startsWith('en-in')) || voices.find(v=> (v.lang||'').toLowerCase().startsWith('en'));
    return v || null;
  }

  window.speakText = function speakText(text, lang){
    try{
      const clean = (text||'').toString().trim();
      if(!clean) return;
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(clean);
      const map = {en:'en-IN', hi:'hi-IN', pa:'pa-IN', kn:'kn-IN', te:'te-IN'};
      utter.lang = map[lang] || 'en-IN';
      const v = pickVoiceForLang(lang);
      if(v) utter.voice = v;
      utter.rate = 0.95;
      speechSynthesis.speak(utter);
    }catch(e){}
  };
})();


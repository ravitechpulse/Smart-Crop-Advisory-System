// voice-nav.js - Tab-wise voice navigation and page reading
(function(){
  let currentTab = 0;
  let isVoiceMode = false;
  
  const sections = [
    { id: 'hero', title: 'hero_title', desc: 'hero_sub' },
    { id: 'features', title: 'features_title', desc: 'feat_soil_sub' },
    { id: 'demo', title: 'demo_title', desc: 'results_intro' },
    { id: 'market', title: 'market_title', desc: 'market_placeholder' },
    { id: 'weather', title: 'weather_title', desc: 'weather_placeholder' },
    { id: 'seasonality', title: 'seasonality_title', desc: 'season_kharif_items' },
    { id: 'cases', title: 'cases_title', desc: 'case1_desc' },
    { id: 'help', title: 'help_title', desc: 'help_ivr_text' }
  ];

  window.startVoiceNavigation = function(){
    isVoiceMode = true;
    currentTab = 0;
    speakCurrentSection();
  };

  window.nextVoiceSection = function(){
    if(!isVoiceMode) return;
    currentTab = (currentTab + 1) % sections.length;
    speakCurrentSection();
  };

  window.prevVoiceSection = function(){
    if(!isVoiceMode) return;
    currentTab = currentTab === 0 ? sections.length - 1 : currentTab - 1;
    speakCurrentSection();
  };

  function speakCurrentSection(){
    const section = sections[currentTab];
    const lang = document.getElementById('langSelect')?.value || 'en';
    
    // Scroll to section
    const element = document.getElementById(section.id);
    if(element) element.scrollIntoView({ behavior: 'smooth' });
    
    // Speak section content with proper language support
    const title = window.i18n?.[lang]?.[section.title] || section.title;
    const description = window.i18n?.[lang]?.[section.desc] || section.desc;
    
    // Add navigation instructions in the selected language
    const navInstructions = {
      en: 'Press next or previous to navigate.',
      hi: 'अगले या पिछले पर दबाकर नेविगेट करें।',
      pa: 'ਅਗਲੇ ਜਾਂ ਪਿਛਲੇ 'ਤੇ ਦਬਾ ਕੇ ਨੈਵੀਗੇਟ ਕਰੋ।',
      kn: 'ಮುಂದೆ ಅಥವಾ ಹಿಂದೆ ಒತ್ತಿ ನ್ಯಾವಿಗೇಟ್ ಮಾಡಿ।',
      te: 'తదుపరి లేదా మునుపటి నొక్కి నావిగేట్ చేయండి।'
    };
    
    const navText = navInstructions[lang] || navInstructions.en;
    const text = `${title}. ${description}. ${navText}`;
    
    if(window.speakText) window.speakText(text, lang);
  }

  window.readFullPage = function(){
    const lang = document.getElementById('langSelect')?.value || 'en';
    const sections = ['hero', 'features', 'demo', 'market', 'weather', 'seasonality', 'cases', 'help'];
    let fullText = '';
    
    sections.forEach(sectionId => {
      const element = document.getElementById(sectionId);
      if(element) {
        const title = element.querySelector('h1, h2, h3, h4, h5, h6')?.textContent || '';
        const content = element.textContent || '';
        fullText += title + '. ' + content.substring(0, 100) + '. ';
      }
    });
    
    if(window.speakText) window.speakText(fullText, lang);
  };
})();

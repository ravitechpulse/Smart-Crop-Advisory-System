// api-integration.js - Connect frontend to Flask backend
(function(){
  const API_BASE_URL = 'http://127.0.0.1:5000/api';

  async function callBackendAPI(endpoint, method = 'GET', data = null) {
    try {
      const options = { method, headers: { 'Content-Type': 'application/json' } };
      if (data && method !== 'GET') options.body = JSON.stringify(data);
      const res = await fetch(`${API_BASE_URL}${endpoint}`, options);
      if (!res.ok) throw new Error(`API ${endpoint} failed: ${res.status}`);
      return await res.json();
    } catch (e) {
      console.warn('Backend call failed:', e.message);
      return null;
    }
  }

  // Try backend for recommendation; return null if not available
  window.recommendViaBackend = async function(district, taluk, n, p, k, phVal, lastCrop){
    const payload = {
      district: (district||'').toLowerCase(),
      nitrogen: Number(n)||0,
      phosphorus: Number(p)||0,
      potassium: Number(k)||0,
      ph: Number(phVal)||7.0,
      last_crop: lastCrop||''
    };
    const data = await callBackendAPI('/recommend', 'POST', payload);
    if(!data || !data.crop) return null;
    return {
      crop: data.crop,
      soilType: data.soil_type,
      needN: data.fertilizer_gap?.nitrogen_gap ?? 0,
      needP: data.fertilizer_gap?.phosphorus_gap ?? 0,
      needK: data.fertilizer_gap?.potassium_gap ?? 0,
      pestTip: 'Monitor for common pests; use neem-based spray if early signs appear.',
      reason: data.reasoning || `AI recommendation (${Math.round((data.confidence||0)*100)}% conf.)`,
      district
    };
  };

  // Weather render helper - updates both weather boxes
  window.loadWeatherFromBackend = async function(district){
    const data = await callBackendAPI(`/weather?district=${encodeURIComponent(district)}`);
    const mainBox = document.getElementById('weatherBoxMain');
    const demoBox = document.getElementById('weatherBox');
    
    if(data && (data.temperature!==undefined)){
      const weatherHtml = `
        <div class="weather-info">
          <h6>Current Weather in ${data.district || district}</h6>
          <div class="row g-2">
            <div class="col-6">
              <strong>Temperature:</strong> ${Number(data.temperature).toFixed(1)}°C
            </div>
            <div class="col-6">
              <strong>Humidity:</strong> ${data.humidity}%
            </div>
            <div class="col-6">
              <strong>Conditions:</strong> ${data.description}
            </div>
            <div class="col-6">
              <strong>Wind:</strong> ${data.wind_speed} m/s
            </div>
          </div>
        </div>
      `;
      
      if(mainBox) mainBox.innerHTML = weatherHtml;
      if(demoBox) demoBox.innerHTML = weatherHtml;
    } else {
      const fallbackText = `Weather data unavailable for ${district}. Please try again later.`;
      if(mainBox) mainBox.innerHTML = fallbackText;
      if(demoBox) demoBox.innerHTML = fallbackText;
    }
  };

  // Market render helper (10 rows) - updates both market tables
  window.loadMarketFromBackend = async function(district){
    const data = await callBackendAPI(district ? `/market-prices?district=${encodeURIComponent(district)}` : '/market-prices');
    const mainTable = document.getElementById('marketTableMain');
    const demoTable = document.getElementById('marketTable');
    
    if(data && Array.isArray(data.prices)){
      let html = '<table class="table table-sm"><thead><tr><th>Date</th><th>Mandi</th><th>Commodity</th><th>Price (₹/qtl)</th></tr></thead><tbody>';
      data.prices.slice(0,10).forEach(row=>{
        html += `<tr><td>${row.date||''}</td><td>${row.mandi||row.mandi_name||''}</td><td>${row.commodity||''}</td><td>₹ ${row.price||''}</td></tr>`;
      });
      html += '</tbody></table>';
      
      if(mainTable) mainTable.innerHTML = html;
      if(demoTable) demoTable.innerHTML = html;
    } else {
      const fallbackText = `Market data unavailable${district ? ' for ' + district : ''}. Please try again later.`;
      if(mainTable) mainTable.innerHTML = fallbackText;
      if(demoTable) demoTable.innerHTML = fallbackText;
    }
  };
})();



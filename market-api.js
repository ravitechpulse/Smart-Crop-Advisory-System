// market-api.js - Live market data integration
(function(){
  const marketData = [
    { commodity: 'Wheat', price: '2450', mandi: 'Patiala', date: '2025-01-15' },
    { commodity: 'Rice (Basmati)', price: '3200', mandi: 'Amritsar', date: '2025-01-15' },
    { commodity: 'Maize', price: '1950', mandi: 'Ludhiana', date: '2025-01-15' },
    { commodity: 'Cotton', price: '6800', mandi: 'Bathinda', date: '2025-01-15' },
    { commodity: 'Mustard', price: '5800', mandi: 'Sangrur', date: '2025-01-15' },
    { commodity: 'Gram', price: '5200', mandi: 'Moga', date: '2025-01-15' },
    { commodity: 'Potato', price: '1800', mandi: 'Jalandhar', date: '2025-01-15' },
    { commodity: 'Bajra', price: '2200', mandi: 'Fazilka', date: '2025-01-15' },
    { commodity: 'Sugarcane', price: '340', mandi: 'Hoshiarpur', date: '2025-01-15' },
    { commodity: 'Vegetables', price: '2800', mandi: 'Kapurthala', date: '2025-01-15' }
  ];

  window.loadLiveMarketData = function(){
    const table = document.getElementById('marketTable');
    const mainTable = document.getElementById('marketTableMain');
    
    let html = '<table class="table table-sm"><thead><tr><th>Date</th><th>Mandi</th><th>Commodity</th><th>Price (₹/quintal)</th></tr></thead><tbody>';
    
    marketData.forEach(item => {
      html += `<tr><td>${item.date}</td><td>${item.mandi}</td><td>${item.commodity}</td><td>₹ ${item.price}</td></tr>`;
    });
    
    html += '</tbody></table>';
    
    if(table) table.innerHTML = html;
    if(mainTable) mainTable.innerHTML = html;
  };

  // Auto-refresh every 30 minutes
  setInterval(loadLiveMarketData, 30 * 60 * 1000);
})();

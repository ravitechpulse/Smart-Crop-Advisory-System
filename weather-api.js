// weather-api.js - Weather alerts and phone notifications
(function(){
  window.collectPhoneForAlerts = function(){
    const phone = prompt('Enter your phone number for weather alerts (with country code, e.g. 919812345678):');
    if(!phone) return;
    
    try{
      localStorage.setItem('farmer_phone', phone);
      alert('Phone number saved! You will receive weather alerts via SMS.');
    }catch(e){
      alert('Could not save phone number. Please try again.');
    }
  };

  window.sendWeatherAlert = function(district, message){
    const phone = localStorage.getItem('farmer_phone');
    if(!phone) return;
    
    // In real implementation, this would call a backend API
    const alertMessage = `Weather Alert for ${district}: ${message}`;
    console.log('SMS Alert:', phone, alertMessage);
    
    // For demo, show WhatsApp link
    const waMessage = encodeURIComponent(alertMessage);
    window.open(`https://wa.me/${phone}?text=${waMessage}`, '_blank');
  };

  window.getWeatherAlerts = function(district){
    const alerts = [
      'Rain expected in next 2 hours. Cover your crops.',
      'High temperature alert. Increase irrigation.',
      'Wind speed high. Secure your farm equipment.',
      'Frost warning tonight. Protect tender crops.',
      'Humidity high. Watch for fungal diseases.'
    ];
    
    const randomAlert = alerts[Math.floor(Math.random() * alerts.length)];
    sendWeatherAlert(district, randomAlert);
  };
})();

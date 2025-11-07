# weather_api.py - Weather API integration and alert system
import requests
import logging
from datetime import datetime, timedelta
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or "demo_key"  # Replace with actual OpenWeather API key
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, district, state="Punjab", country="IN"):
        """Get current weather for a district"""
        try:
            # For demo purposes, return mock data
            if self.api_key == "demo_key":
                return self.get_mock_weather(district)
            
            # Real API call (when API key is available)
            url = f"{self.base_url}/weather"
            params = {
                'q': f"{district},{state},{country}",
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'district': district,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return self.get_mock_weather(district)
    
    def get_mock_weather(self, district):
        """Return mock weather data for demo"""
        import random
        
        # District-specific weather patterns
        district_weather = {
            'patiala': {'temp': 28, 'humidity': 65, 'rainfall': 0},
            'ludhiana': {'temp': 29, 'humidity': 60, 'rainfall': 0},
            'amritsar': {'temp': 27, 'humidity': 70, 'rainfall': 0},
            'jalandhar': {'temp': 28, 'humidity': 68, 'rainfall': 0},
            'fazilka': {'temp': 32, 'humidity': 45, 'rainfall': 0},
            'bathinda': {'temp': 31, 'humidity': 50, 'rainfall': 0}
        }
        
        base_weather = district_weather.get(district.lower(), {'temp': 28, 'humidity': 60, 'rainfall': 0})
        
        return {
            'temperature': base_weather['temp'] + random.uniform(-3, 3),
            'humidity': base_weather['humidity'] + random.randint(-10, 10),
            'pressure': 1013 + random.randint(-20, 20),
            'description': random.choice(['clear sky', 'few clouds', 'scattered clouds', 'overcast clouds']),
            'wind_speed': random.uniform(2, 8),
            'rainfall': base_weather['rainfall'] + random.uniform(0, 5),
            'district': district.title(),
            'timestamp': datetime.now().isoformat(),
            'source': 'mock_data'
        }
    
    def get_weather_alerts(self, district):
        """Generate weather alerts based on current conditions"""
        try:
            weather_data = self.get_current_weather(district)
            alerts = []
            
            # Temperature alerts
            if weather_data['temperature'] > 35:
                alerts.append({
                    'type': 'heat_wave',
                    'severity': 'high',
                    'message': f'High temperature alert: {weather_data["temperature"]:.1f}°C. Increase irrigation frequency.',
                    'recommendation': 'Water crops early morning or late evening to prevent heat stress.'
                })
            elif weather_data['temperature'] < 5:
                alerts.append({
                    'type': 'frost',
                    'severity': 'high',
                    'message': f'Frost warning: {weather_data["temperature"]:.1f}°C. Protect tender crops.',
                    'recommendation': 'Cover crops with protective sheets or use irrigation to prevent frost damage.'
                })
            
            # Humidity alerts
            if weather_data['humidity'] > 80:
                alerts.append({
                    'type': 'high_humidity',
                    'severity': 'medium',
                    'message': f'High humidity: {weather_data["humidity"]}%. Watch for fungal diseases.',
                    'recommendation': 'Apply preventive fungicide and ensure proper ventilation.'
                })
            elif weather_data['humidity'] < 30:
                alerts.append({
                    'type': 'low_humidity',
                    'severity': 'medium',
                    'message': f'Low humidity: {weather_data["humidity"]}%. Increase irrigation.',
                    'recommendation': 'Water crops more frequently to maintain soil moisture.'
                })
            
            # Wind alerts
            if weather_data['wind_speed'] > 15:
                alerts.append({
                    'type': 'strong_wind',
                    'severity': 'medium',
                    'message': f'Strong winds: {weather_data["wind_speed"]:.1f} m/s. Secure farm equipment.',
                    'recommendation': 'Tie down loose equipment and check for wind damage.'
                })
            
            # Rainfall alerts
            if weather_data.get('rainfall', 0) > 10:
                alerts.append({
                    'type': 'heavy_rain',
                    'severity': 'high',
                    'message': f'Heavy rainfall: {weather_data["rainfall"]:.1f}mm. Check drainage.',
                    'recommendation': 'Ensure proper drainage and cover harvested crops.'
                })
            
            return {
                'district': district,
                'alerts': alerts,
                'weather_data': weather_data,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating weather alerts: {str(e)}")
            return {
                'district': district,
                'alerts': [],
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_forecast(self, district, days=7):
        """Get weather forecast for next few days"""
        try:
            # For demo, return mock forecast
            forecast = []
            base_temp = 28
            
            for i in range(days):
                date = datetime.now() + timedelta(days=i)
                temp = base_temp + (i * 0.5) + (-1 if i % 2 == 0 else 1)
                
                forecast.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'temperature_max': temp + 3,
                    'temperature_min': temp - 3,
                    'humidity': 60 + (i * 2),
                    'rainfall': 0 if i % 3 != 0 else random.uniform(5, 15),
                    'description': 'clear sky' if i % 2 == 0 else 'few clouds'
                })
            
            return {
                'district': district,
                'forecast': forecast,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting forecast: {str(e)}")
            return None

# Global weather API instance
weather_api = WeatherAPI()

def get_weather_for_district(district):
    """Public interface for weather data"""
    return weather_api.get_current_weather(district)

def get_alerts_for_district(district):
    """Public interface for weather alerts"""
    return weather_api.get_weather_alerts(district)

def get_forecast_for_district(district, days=7):
    """Public interface for weather forecast"""
    return weather_api.get_forecast(district, days)

# test_api.py - API tests for SmartCrop Advisory System
import unittest
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestSmartCropAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_crop_recommendation(self):
        """Test crop recommendation endpoint"""
        payload = {
            'district': 'patiala',
            'nitrogen': 25,
            'phosphorus': 18,
            'potassium': 220,
            'ph': 7.2,
            'last_crop': 'wheat'
        }
        
        response = self.app.post('/api/recommend', 
                               data=json.dumps(payload),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('crop', data)
        self.assertIn('confidence', data)
        self.assertIn('soil_type', data)
    
    def test_crop_recommendation_missing_field(self):
        """Test crop recommendation with missing field"""
        payload = {
            'district': 'patiala',
            'nitrogen': 25,
            'phosphorus': 18,
            'potassium': 220
            # Missing 'ph' field
        }
        
        response = self.app.post('/api/recommend',
                               data=json.dumps(payload),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_market_prices(self):
        """Test market prices endpoint"""
        response = self.app.get('/api/market-prices')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('prices', data)
        self.assertIn('count', data)
    
    def test_market_prices_with_district(self):
        """Test market prices with district filter"""
        response = self.app.get('/api/market-prices?district=patiala')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('prices', data)
    
    def test_weather_data(self):
        """Test weather data endpoint"""
        response = self.app.get('/api/weather?district=patiala')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('temperature', data)
        self.assertIn('humidity', data)
    
    def test_weather_alerts(self):
        """Test weather alerts endpoint"""
        response = self.app.get('/api/weather-alerts?district=patiala')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('district', data)
        self.assertIn('alerts', data)
    
    def test_register_farmer(self):
        """Test farmer registration"""
        payload = {
            'phone': '919876543210',
            'name': 'Test Farmer',
            'district': 'patiala',
            'taluk': 'samana'
        }
        
        response = self.app.post('/api/register-farmer',
                               data=json.dumps(payload),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('farmer_id', data)
    
    def test_register_farmer_missing_phone(self):
        """Test farmer registration without phone"""
        payload = {
            'name': 'Test Farmer',
            'district': 'patiala'
            # Missing phone
        }
        
        response = self.app.post('/api/register-farmer',
                               data=json.dumps(payload),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_send_alert(self):
        """Test sending alert"""
        payload = {
            'phone': '919876543210',
            'district': 'patiala',
            'type': 'weather'
        }
        
        response = self.app.post('/api/send-alert',
                               data=json.dumps(payload),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
    
    def test_get_districts(self):
        """Test getting districts list"""
        response = self.app.get('/api/districts')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('districts', data)
        self.assertIn('count', data)
    
    def test_get_soil_data(self):
        """Test getting soil data for district"""
        response = self.app.get('/api/soil-data/patiala')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('district', data)
        self.assertIn('soil_data', data)
    
    def test_get_soil_data_invalid_district(self):
        """Test getting soil data for invalid district"""
        response = self.app.get('/api/soil-data/invalid')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()

# endpoints.py - API endpoints for SmartCrop Advisory System
from flask import Blueprint, request, jsonify
import logging
from datetime import datetime
import sqlite3
import pandas as pd

from models.predict import get_crop_recommendation, get_fertilizer_recommendation
from utils.weather_api import get_weather_for_district, get_alerts_for_district
from utils.sms_api import send_weather_alert_to_farmer, send_crop_alert_to_farmer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/recommend', methods=['POST'])
def recommend_crop():
    """Get crop recommendation based on soil data"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['district', 'nitrogen', 'phosphorus', 'potassium', 'ph']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract data
        district = data['district']
        nitrogen = float(data['nitrogen'])
        phosphorus = float(data['phosphorus'])
        potassium = float(data['potassium'])
        ph = float(data['ph'])
        last_crop = data.get('last_crop', '')
        
        # Get soil type for district
        soil_df = pd.read_csv('datasets/soil_data.csv')
        district_info = soil_df[soil_df['district'].str.lower() == district.lower()]
        
        if district_info.empty:
            return jsonify({'error': 'District not found in database'}), 400
        
        soil_type = district_info.iloc[0]['soil_type']
        
        # Get crop recommendation
        crop_prediction = get_crop_recommendation(
            nitrogen, phosphorus, potassium, ph, district, soil_type, last_crop
        )
        
        # Get fertilizer recommendation
        fertilizer_rec = get_fertilizer_recommendation(
            nitrogen, phosphorus, potassium, crop_prediction['crop']
        )
        
        # Prepare response
        recommendation = {
            'crop': crop_prediction['crop'],
            'confidence': crop_prediction['confidence'],
            'method': crop_prediction['method'],
            'soil_type': soil_type,
            'fertilizer_gap': fertilizer_rec,
            'district': district.title(),
            'timestamp': datetime.now().isoformat(),
            'reasoning': crop_prediction.get('reasoning', '')
        }
        
        # Save recommendation to database
        save_recommendation_to_db(data, recommendation)
        
        return jsonify(recommendation)
        
    except Exception as e:
        logger.error(f"Error in crop recommendation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/market-prices', methods=['GET'])
def get_market_prices():
    """Get current market prices"""
    try:
        district = request.args.get('district')
        
        # Load market data
        prices_df = pd.read_csv('datasets/market_prices.csv')
        
        # Filter by district if specified
        if district:
            prices_df = prices_df[prices_df['district'].str.lower() == district.lower()]
        
        # Get latest prices (today's data)
        today = datetime.now().strftime('%Y-%m-%d')
        latest_prices = prices_df[prices_df['date'] == today]
        
        if latest_prices.empty:
            # Return latest available data
            latest_prices = prices_df.sort_values('date', ascending=False).head(10)
        
        prices = latest_prices.to_dict('records')
        
        return jsonify({
            'prices': prices,
            'count': len(prices),
            'date': today,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching market prices: {str(e)}")
        return jsonify({'error': 'Failed to fetch market prices'}), 500

@api_bp.route('/weather', methods=['GET'])
def get_weather():
    """Get weather data for a district"""
    try:
        district = request.args.get('district')
        if not district:
            return jsonify({'error': 'District parameter required'}), 400
        
        # Get current weather
        weather_data = get_weather_for_district(district)
        
        return jsonify(weather_data)
        
    except Exception as e:
        logger.error(f"Error fetching weather: {str(e)}")
        return jsonify({'error': 'Failed to fetch weather data'}), 500

@api_bp.route('/weather-alerts', methods=['GET'])
def get_weather_alerts():
    """Get weather alerts for a district"""
    try:
        district = request.args.get('district')
        if not district:
            return jsonify({'error': 'District parameter required'}), 400
        
        # Get weather alerts
        alerts_data = get_alerts_for_district(district)
        
        return jsonify(alerts_data)
        
    except Exception as e:
        logger.error(f"Error fetching weather alerts: {str(e)}")
        return jsonify({'error': 'Failed to fetch weather alerts'}), 500

@api_bp.route('/register-farmer', methods=['POST'])
def register_farmer():
    """Register a new farmer"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'phone' not in data:
            return jsonify({'error': 'Phone number required'}), 400
        
        phone = data['phone']
        district = data.get('district', '')
        taluk = data.get('taluk', '')
        name = data.get('name', '')
        
        # Save to database
        conn = sqlite3.connect('datasets/smartcrop.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO farmers (phone, name, district, taluk)
                VALUES (?, ?, ?, ?)
            ''', (phone, name, district, taluk))
            
            farmer_id = cursor.lastrowid
            conn.commit()
            
            return jsonify({
                'status': 'success',
                'farmer_id': farmer_id,
                'message': 'Farmer registered successfully',
                'timestamp': datetime.now().isoformat()
            })
            
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Phone number already registered'}), 400
        finally:
            conn.close()
        
    except Exception as e:
        logger.error(f"Error registering farmer: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@api_bp.route('/send-alert', methods=['POST'])
def send_alert():
    """Send weather or crop alert to farmer"""
    try:
        data = request.get_json()
        
        phone = data.get('phone')
        district = data.get('district')
        alert_type = data.get('type', 'weather')  # 'weather' or 'crop'
        
        if not phone or not district:
            return jsonify({'error': 'Phone and district required'}), 400
        
        if alert_type == 'weather':
            # Get weather alerts and send
            alerts_data = get_alerts_for_district(district)
            result = send_weather_alert_to_farmer(phone, district, alerts_data)
            
        elif alert_type == 'crop':
            # Get crop recommendation and send
            # This would typically use saved recommendation data
            crop_data = {
                'crop': 'Wheat',
                'confidence': 0.85,
                'fertilizer_gap': {
                    'nitrogen_gap': 20,
                    'phosphorus_gap': 10,
                    'potassium_gap': 15
                }
            }
            result = send_crop_alert_to_farmer(phone, district, crop_data)
            
        else:
            return jsonify({'error': 'Invalid alert type'}), 400
        
        return jsonify({
            'status': 'success',
            'alert_type': alert_type,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error sending alert: {str(e)}")
        return jsonify({'error': 'Failed to send alert'}), 500

@api_bp.route('/districts', methods=['GET'])
def get_districts():
    """Get list of all Punjab districts"""
    try:
        # Load district data
        districts_df = pd.read_csv('datasets/soil_data.csv')
        districts = districts_df[['district', 'region', 'soil_type']].to_dict('records')
        
        return jsonify({
            'districts': districts,
            'count': len(districts),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching districts: {str(e)}")
        return jsonify({'error': 'Failed to fetch districts'}), 500

@api_bp.route('/soil-data/<district>', methods=['GET'])
def get_soil_data(district):
    """Get soil data for a specific district"""
    try:
        soil_df = pd.read_csv('datasets/soil_data.csv')
        district_data = soil_df[soil_df['district'].str.lower() == district.lower()]
        
        if district_data.empty:
            return jsonify({'error': 'District not found'}), 404
        
        soil_info = district_data.iloc[0].to_dict()
        
        return jsonify({
            'district': district.title(),
            'soil_data': soil_info,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching soil data: {str(e)}")
        return jsonify({'error': 'Failed to fetch soil data'}), 500

def save_recommendation_to_db(request_data, recommendation):
    """Save recommendation to database"""
    try:
        conn = sqlite3.connect('datasets/smartcrop.db')
        cursor = conn.cursor()
        
        # Get farmer ID if phone provided
        farmer_id = None
        if 'phone' in request_data:
            cursor.execute('SELECT id FROM farmers WHERE phone = ?', (request_data['phone'],))
            farmer = cursor.fetchone()
            if farmer:
                farmer_id = farmer[0]
        
        # Save recommendation
        cursor.execute('''
            INSERT INTO recommendations (
                farmer_id, district, soil_type, nitrogen, phosphorus, potassium, ph,
                last_crop, recommended_crop, confidence_score, method
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            farmer_id,
            request_data['district'],
            recommendation['soil_type'],
            request_data['nitrogen'],
            request_data['phosphorus'],
            request_data['potassium'],
            request_data['ph'],
            request_data.get('last_crop', ''),
            recommendation['crop'],
            recommendation['confidence'],
            recommendation['method']
        ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error saving recommendation: {str(e)}")

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SmartCrop Advisory API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

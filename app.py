# app.py - Main Flask application for SmartCrop Advisory System
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import sqlite3
import os
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE = 'datasets/smartcrop.db'

def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Farmers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE,
            district TEXT,
            taluk TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Recommendations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            district TEXT,
            soil_type TEXT,
            crop_recommended TEXT,
            fertilizer_gap TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES farmers (id)
        )
    ''')
    
    # Weather alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            district TEXT,
            alert_message TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES farmers (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    """Get crop recommendation based on soil data"""
    try:
        data = request.json
        district = data.get('district', '').lower()
        n = float(data.get('nitrogen', 0))
        p = float(data.get('phosphorus', 0))
        k = float(data.get('potassium', 0))
        ph = float(data.get('ph', 7.0))
        # Accept both lastCrop and last_crop from clients
        last_crop = data.get('lastCrop') or data.get('last_crop') or ''
        
        # Load district soil data
        soil_data = pd.read_csv('datasets/soil_data.csv')
        district_info = soil_data[soil_data['district'].str.lower() == district]
        
        if district_info.empty:
            return jsonify({'error': 'District not found'}), 400
        
        soil_type = district_info.iloc[0]['soil_type']
        
        # Simple rule-based recommendation (can be replaced with ML model)
        if soil_type == 'sandy':
            crop = 'Pearl Millet (Bajra)'
        elif soil_type == 'loamy':
            crop = 'Rice'
        else:
            crop = 'Maize'
        
        # Calculate fertilizer gaps
        target_n, target_p, target_k = 40, 30, 30
        need_n = max(0, target_n - n)
        need_p = max(0, target_p - p)
        need_k = max(0, target_k - k)
        
        recommendation = {
            'crop': crop,
            'soil_type': soil_type,
            'fertilizer_gap': {
                'nitrogen': need_n,
                'phosphorus': need_p,
                'potassium': need_k
            },
            'reason': f'Based on {soil_type} soil type and regional data for {district.title()}',
            'pest_tip': 'Monitor for common pests; use neem-based spray if early signs appear.',
            'confidence': 0.82,
            'method': 'rule_based'
        }
        
        return jsonify(recommendation)
        
    except Exception as e:
        logger.error(f"Error in recommendation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/market-prices', methods=['GET'])
def get_market_prices():
    """Get current market prices"""
    try:
        prices_df = pd.read_csv('datasets/market_prices.csv')
        # Optional district filter
        district = request.args.get('district')
        if district:
            prices_df = prices_df[prices_df['district'].str.lower() == district.lower()]
        prices = prices_df.to_dict('records')
        # Return wrapped object for easier frontend handling
        return jsonify({ 'prices': prices, 'count': len(prices) })
    except Exception as e:
        logger.error(f"Error fetching market prices: {str(e)}")
        return jsonify({'error': 'Failed to fetch market prices'}), 500

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Return simple mock weather for a district (demo)"""
    try:
        district = request.args.get('district', 'patiala')
        # Simple mock values; in production integrate OpenWeather or IMD
        base = {
            'patiala': (28.5, 65, 1012, 'clear sky', 3.2),
            'ludhiana': (29.0, 60, 1010, 'few clouds', 4.1),
            'amritsar': (27.2, 70, 1013, 'scattered clouds', 3.0)
        }
        t, h, p, desc, wind = base.get(district.lower(), (28.0, 62, 1011, 'clear sky', 3.5))
        return jsonify({
            'temperature': t,
            'humidity': h,
            'pressure': p,
            'description': desc,
            'wind_speed': wind,
            'district': district
        })
    except Exception as e:
        logger.error(f"Error fetching weather: {str(e)}")
        return jsonify({'error': 'Failed to fetch weather data'}), 500

@app.route('/api/weather-alert', methods=['POST'])
def send_weather_alert():
    """Send weather alert to farmer"""
    try:
        data = request.json
        phone = data.get('phone')
        district = data.get('district')
        message = data.get('message')
        
        if not phone or not district:
            return jsonify({'error': 'Phone and district required'}), 400
        
        # Save to database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Get or create farmer
        cursor.execute('SELECT id FROM farmers WHERE phone = ?', (phone,))
        farmer = cursor.fetchone()
        
        if not farmer:
            cursor.execute('INSERT INTO farmers (phone, district) VALUES (?, ?)', (phone, district))
            farmer_id = cursor.lastrowid
        else:
            farmer_id = farmer[0]
        
        # Save alert
        cursor.execute('''
            INSERT INTO weather_alerts (farmer_id, district, alert_message)
            VALUES (?, ?, ?)
        ''', (farmer_id, district, message))
        
        conn.commit()
        conn.close()
        
        # In production, integrate with SMS/WhatsApp API here
        logger.info(f"Weather alert sent to {phone}: {message}")
        
        return jsonify({'status': 'success', 'message': 'Alert sent successfully'})
        
    except Exception as e:
        logger.error(f"Error sending weather alert: {str(e)}")
        return jsonify({'error': 'Failed to send alert'}), 500

@app.route('/api/register-farmer', methods=['POST'])
def register_farmer():
    """Register a new farmer"""
    try:
        data = request.json
        phone = data.get('phone')
        district = data.get('district')
        taluk = data.get('taluk')
        
        if not phone:
            return jsonify({'error': 'Phone number required'}), 400
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO farmers (phone, district, taluk)
                VALUES (?, ?, ?)
            ''', (phone, district, taluk))
            conn.commit()
            farmer_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Phone number already registered'}), 400
        finally:
            conn.close()
        
        return jsonify({'status': 'success', 'farmer_id': farmer_id})
        
    except Exception as e:
        logger.error(f"Error registering farmer: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Initialize database
    os.makedirs('datasets', exist_ok=True)
    init_db()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)

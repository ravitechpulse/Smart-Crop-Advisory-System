# config.py - Configuration settings for SmartCrop Advisory System
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smartcrop-secret-key-2025'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///datasets/smartcrop.db'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # API Keys
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    WHATSAPP_TOKEN = os.environ.get('WHATSAPP_TOKEN')
    
    # Model paths
    MODEL_PATH = 'models/crop_recommendation_model.pkl'
    SCALER_PATH = 'models/feature_scaler.pkl'
    
    # Data paths
    SOIL_DATA_PATH = 'datasets/soil_data.csv'
    MARKET_DATA_PATH = 'datasets/market_prices.csv'
    TRAINING_DATA_PATH = 'datasets/training_data.csv'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

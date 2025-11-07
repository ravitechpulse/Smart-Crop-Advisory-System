# predict.py - Model prediction interface for crop recommendation
import pandas as pd
import numpy as np
import joblib
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CropPredictor:
    def __init__(self, model_path='models/crop_recommendation_model.pkl', 
                 scaler_path='models/feature_scaler.pkl',
                 encoder_path='models/label_encoder.pkl'):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.encoder_path = encoder_path
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.load_models()
    
    def load_models(self):
        """Load trained models"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logger.info("Model loaded successfully")
            else:
                logger.warning("Model file not found. Using fallback prediction.")
            
            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
                logger.info("Scaler loaded successfully")
            
            if os.path.exists(self.encoder_path):
                self.label_encoder = joblib.load(self.encoder_path)
                logger.info("Label encoder loaded successfully")
                
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
    
    def get_district_features(self, district):
        """Get district-specific features"""
        district_data = {
            'patiala': {'rainfall': 650, 'temperature': 28},
            'ludhiana': {'rainfall': 600, 'temperature': 29},
            'amritsar': {'rainfall': 700, 'temperature': 27},
            'jalandhar': {'rainfall': 650, 'temperature': 28},
            'fazilka': {'rainfall': 400, 'temperature': 32},
            'bathinda': {'rainfall': 450, 'temperature': 31},
            'moga': {'rainfall': 600, 'temperature': 29},
            'sangrur': {'rainfall': 550, 'temperature': 30},
            'firozpur': {'rainfall': 400, 'temperature': 32},
            'hoshiarpur': {'rainfall': 800, 'temperature': 26}
        }
        
        return district_data.get(district.lower(), {'rainfall': 600, 'temperature': 28})
    
    def predict_crop(self, nitrogen, phosphorus, potassium, ph, district, soil_type, last_crop=None):
        """Predict best crop for given conditions"""
        try:
            # Get district features
            district_features = self.get_district_features(district)
            
            # Prepare features
            features = [
                float(nitrogen),
                float(phosphorus),
                float(potassium),
                float(ph),
                district_features['rainfall'],
                district_features['temperature']
            ]
            
            # Encode district and soil type if encoders available
            if self.label_encoder and self.scaler and self.model:
                try:
                    district_encoded = self.label_encoder.transform([district])[0]
                    soil_type_encoded = self.label_encoder.transform([soil_type])[0]
                    features.extend([district_encoded, soil_type_encoded])
                    
                    # Scale features
                    features_scaled = self.scaler.transform([features])
                    
                    # Make prediction
                    crop_prediction = self.model.predict(features_scaled)[0]
                    probabilities = self.model.predict_proba(features_scaled)[0]
                    confidence = max(probabilities)
                    
                    return {
                        'crop': crop_prediction,
                        'confidence': confidence,
                        'method': 'ml_model',
                        'probabilities': dict(zip(self.model.classes_, probabilities))
                    }
                except Exception as e:
                    logger.warning(f"ML prediction failed, using fallback: {str(e)}")
            
            # Fallback rule-based prediction
            return self.fallback_prediction(nitrogen, phosphorus, potassium, ph, district, soil_type, last_crop)
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return self.fallback_prediction(nitrogen, phosphorus, potassium, ph, district, soil_type, last_crop)
    
    def fallback_prediction(self, nitrogen, phosphorus, potassium, ph, district, soil_type, last_crop=None):
        """Fallback rule-based prediction"""
        try:
            # Simple rule-based logic
            if soil_type.lower() in ['sandy', 'sandy loam']:
                crop = 'Pearl Millet (Bajra)'
            elif soil_type.lower() in ['loamy', 'loam to clay loam']:
                crop = 'Rice'
            elif soil_type.lower() == 'alluvial':
                if float(ph) > 7.5:
                    crop = 'Wheat'
                else:
                    crop = 'Maize'
            else:
                crop = 'Maize'
            
            # Adjust based on last crop (crop rotation)
            if last_crop and 'wheat' in last_crop.lower():
                crop = 'Rice' if crop == 'Wheat' else 'Maize'
            
            return {
                'crop': crop,
                'confidence': 0.75,  # Lower confidence for rule-based
                'method': 'rule_based',
                'reasoning': f'Based on {soil_type} soil type and regional patterns'
            }
            
        except Exception as e:
            logger.error(f"Error in fallback prediction: {str(e)}")
            return {
                'crop': 'Maize',
                'confidence': 0.5,
                'method': 'default',
                'reasoning': 'Default recommendation due to prediction error'
            }
    
    def get_fertilizer_recommendation(self, nitrogen, phosphorus, potassium, crop):
        """Get fertilizer recommendations based on soil test and crop"""
        try:
            # Target NPK values for different crops (kg/ha)
            crop_requirements = {
                'wheat': {'N': 120, 'P': 60, 'K': 60},
                'rice': {'N': 100, 'P': 50, 'K': 50},
                'maize': {'N': 150, 'P': 75, 'K': 75},
                'cotton': {'N': 80, 'P': 40, 'K': 40},
                'bajra': {'N': 60, 'P': 30, 'K': 30},
                'mustard': {'N': 80, 'P': 40, 'K': 40},
                'gram': {'N': 20, 'P': 60, 'K': 20}
            }
            
            # Get requirements for the crop (case-insensitive)
            crop_lower = crop.lower()
            requirements = crop_requirements.get(crop_lower, {'N': 100, 'P': 50, 'K': 50})
            
            # Calculate gaps
            n_gap = max(0, requirements['N'] - float(nitrogen))
            p_gap = max(0, requirements['P'] - float(phosphorus))
            k_gap = max(0, requirements['K'] - float(potassium))
            
            return {
                'nitrogen_gap': n_gap,
                'phosphorus_gap': p_gap,
                'potassium_gap': k_gap,
                'total_fertilizer': n_gap + p_gap + k_gap,
                'recommendations': {
                    'urea': round(n_gap / 46 * 100, 1) if n_gap > 0 else 0,  # Urea is 46% N
                    'dap': round(p_gap / 18 * 100, 1) if p_gap > 0 else 0,   # DAP is 18% P
                    'mop': round(k_gap / 60 * 100, 1) if k_gap > 0 else 0    # MOP is 60% K
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating fertilizer: {str(e)}")
            return {
                'nitrogen_gap': 0,
                'phosphorus_gap': 0,
                'potassium_gap': 0,
                'total_fertilizer': 0,
                'recommendations': {}
            }

# Global predictor instance
predictor = CropPredictor()

def get_crop_recommendation(nitrogen, phosphorus, potassium, ph, district, soil_type, last_crop=None):
    """Public interface for crop recommendation"""
    return predictor.predict_crop(nitrogen, phosphorus, potassium, ph, district, soil_type, last_crop)

def get_fertilizer_recommendation(nitrogen, phosphorus, potassium, crop):
    """Public interface for fertilizer recommendation"""
    return predictor.get_fertilizer_recommendation(nitrogen, phosphorus, potassium, crop)

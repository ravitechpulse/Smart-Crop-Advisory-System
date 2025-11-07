# train_model.py - Machine Learning model training for crop recommendation
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CropRecommendationModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_columns = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'rainfall', 'temperature']
        
    def load_data(self, data_path):
        """Load training data from CSV"""
        try:
            self.data = pd.read_csv(data_path)
            logger.info(f"Loaded {len(self.data)} training samples")
            return True
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def preprocess_data(self):
        """Preprocess the training data"""
        try:
            # Handle missing values
            self.data = self.data.fillna(self.data.mean())
            
            # Encode categorical variables
            self.data['district_encoded'] = self.label_encoder.fit_transform(self.data['district'])
            self.data['soil_type_encoded'] = LabelEncoder().fit_transform(self.data['soil_type'])
            
            # Prepare features and target
            feature_cols = self.feature_columns + ['district_encoded', 'soil_type_encoded']
            self.X = self.data[feature_cols]
            self.y = self.data['crop']
            
            logger.info(f"Preprocessed data shape: {self.X.shape}")
            return True
        except Exception as e:
            logger.error(f"Error preprocessing data: {str(e)}")
            return False
    
    def train(self):
        """Train the model"""
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                self.X, self.y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            
            logger.info(f"Model accuracy: {accuracy:.3f}")
            logger.info("Classification Report:")
            logger.info(classification_report(y_test, y_pred))
            
            return True
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return False
    
    def save_model(self, model_path, scaler_path):
        """Save trained model and scaler"""
        try:
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)
            joblib.dump(self.label_encoder, 'models/label_encoder.pkl')
            logger.info("Model saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False
    
    def predict(self, features):
        """Make prediction on new data"""
        try:
            # Ensure features are in correct format
            if len(features) != len(self.feature_columns) + 2:  # +2 for district and soil_type
                raise ValueError("Invalid number of features")
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]
            
            return {
                'crop': prediction,
                'confidence': max(probabilities),
                'probabilities': dict(zip(self.model.classes_, probabilities))
            }
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            return None

def train_crop_model():
    """Main function to train the crop recommendation model"""
    model = CropRecommendationModel()
    
    # Load data
    if not model.load_data('../datasets/training_data.csv'):
        return False
    
    # Preprocess data
    if not model.preprocess_data():
        return False
    
    # Train model
    if not model.train():
        return False
    
    # Save model
    if not model.save_model('crop_recommendation_model.pkl', 'feature_scaler.pkl'):
        return False
    
    logger.info("Model training completed successfully!")
    return True

if __name__ == "__main__":
    train_crop_model()

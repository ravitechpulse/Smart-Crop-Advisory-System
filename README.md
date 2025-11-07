# SmartCrop Advisory System - Backend

A comprehensive backend system for providing AI-powered crop recommendations to small and marginal farmers in Punjab, India.

## 🚀 Features

- **Machine Learning Models**: Crop recommendation using Random Forest classifier
- **Weather Integration**: Real-time weather data and alerts
- **SMS/WhatsApp Notifications**: Automated alerts to farmers
- **Database Management**: SQLite database with comprehensive schema
- **RESTful API**: Complete API endpoints for frontend integration
- **Regional Data**: Punjab-specific soil, weather, and market data

## 📁 Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── models/
│   ├── train_model.py   # ML model training
│   └── predict.py       # Model prediction interface
├── api/
│   └── endpoints.py     # API route definitions
├── database/
│   ├── schema.sql       # Database schema
│   └── init_db.py      # Database initialization
├── utils/
│   ├── weather_api.py   # Weather API integration
│   └── sms_api.py      # SMS/WhatsApp notifications
└── datasets/
    ├── soil_data.csv           # Punjab soil data
    ├── market_prices.csv       # Market price data
    ├── training_data.csv       # ML training data
    └── smartcrop.db           # SQLite database
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-crop-advisory/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python database/init_db.py
   ```

5. **Train ML model (optional)**
   ```bash
   python models/train_model.py
   ```

## 🚀 Running the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## 📊 API Endpoints

### Core Endpoints

- `POST /api/recommend` - Get crop recommendation
- `GET /api/market-prices` - Get market prices
- `GET /api/weather` - Get weather data
- `GET /api/weather-alerts` - Get weather alerts
- `POST /api/register-farmer` - Register new farmer
- `POST /api/send-alert` - Send SMS/WhatsApp alert

### Data Endpoints

- `GET /api/districts` - Get all Punjab districts
- `GET /api/soil-data/<district>` - Get soil data for district
- `GET /api/health` - Health check

## 🤖 Machine Learning

### Training Data
- **File**: `datasets/training_data.csv`
- **Features**: Nitrogen, Phosphorus, Potassium, pH, Rainfall, Temperature, District, Soil Type
- **Target**: Crop recommendation
- **Model**: Random Forest Classifier

### Prediction Features
- Soil nutrient levels (NPK)
- Soil pH
- Regional weather data
- District-specific soil types
- Crop rotation history

## 🌦️ Weather Integration

### Current Features
- Real-time weather data (mock for demo)
- Weather alerts (temperature, humidity, wind, rainfall)
- District-specific weather patterns
- Automated alert notifications

### API Integration
- OpenWeatherMap API (configurable)
- Fallback to mock data for demo

## 📱 Notification System

### SMS Integration
- Twilio API integration
- Mock SMS for demo purposes
- Formatted weather and crop alerts

### WhatsApp Integration
- WhatsApp Business API
- Rich message formatting
- Automated delivery tracking

## 🗄️ Database Schema

### Tables
- **farmers**: Farmer registration and contact info
- **recommendations**: Crop recommendations history
- **weather_alerts**: Weather alert logs
- **market_prices**: Market price data
- **soil_reports**: Soil test reports
- **crop_yields**: Yield tracking
- **api_logs**: API usage logs
- **feedback**: Farmer feedback

## 🔧 Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///datasets/smartcrop.db
OPENWEATHER_API_KEY=your-api-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
WHATSAPP_TOKEN=your-whatsapp-token
```

### Config Classes
- **DevelopmentConfig**: Debug mode enabled
- **ProductionConfig**: Production settings
- **TestingConfig**: Test database and settings

## 📈 Performance Features

- **Caching**: In-memory caching for market data
- **Database Indexing**: Optimized queries with indexes
- **Async Processing**: Non-blocking API calls
- **Error Handling**: Comprehensive error logging
- **Rate Limiting**: API rate limiting (configurable)

## 🔒 Security Features

- **Input Validation**: Comprehensive data validation
- **SQL Injection Prevention**: Parameterized queries
- **CORS Configuration**: Cross-origin resource sharing
- **API Authentication**: Token-based authentication (configurable)

## 📊 Monitoring & Logging

- **Structured Logging**: JSON-formatted logs
- **API Metrics**: Request/response tracking
- **Error Tracking**: Comprehensive error logging
- **Performance Monitoring**: Response time tracking

## 🧪 Testing

### Unit Tests
```bash
python -m pytest tests/
```

### API Testing
```bash
# Test crop recommendation
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"district":"patiala","nitrogen":25,"phosphorus":18,"potassium":220,"ph":7.2}'
```

## 🚀 Deployment

### Production Deployment
1. Set production environment variables
2. Use production database (PostgreSQL recommended)
3. Enable HTTPS with SSL certificates
4. Configure reverse proxy (Nginx)
5. Set up monitoring and logging

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

**Annadata's Legacy**
- **Team Lead**: Ravi Kumar S J
- **Team Members**: Shalom Raj, Renuka Prasad

## 📞 Support

For support and questions:
- Email: rjayaram@gitam.in
- Toll-free: 1800-XXX-XXXX

---

**Built with ❤️ for Indian Farmers**

-- schema.sql - Database schema for SmartCrop Advisory System

-- Farmers table
CREATE TABLE IF NOT EXISTS farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT UNIQUE NOT NULL,
    name TEXT,
    district TEXT NOT NULL,
    taluk TEXT,
    village TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recommendations table
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER NOT NULL,
    district TEXT NOT NULL,
    taluk TEXT,
    soil_type TEXT,
    nitrogen REAL,
    phosphorus REAL,
    potassium REAL,
    ph REAL,
    last_crop TEXT,
    recommended_crop TEXT NOT NULL,
    fertilizer_recommendation TEXT,
    confidence_score REAL,
    method TEXT, -- 'ml_model', 'rule_based', 'default'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers (id)
);

-- Weather alerts table
CREATE TABLE IF NOT EXISTS weather_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    district TEXT NOT NULL,
    alert_type TEXT NOT NULL, -- 'rain', 'drought', 'pest', 'disease'
    alert_message TEXT NOT NULL,
    severity TEXT, -- 'low', 'medium', 'high', 'critical'
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_status TEXT DEFAULT 'pending', -- 'pending', 'sent', 'failed'
    FOREIGN KEY (farmer_id) REFERENCES farmers (id)
);

-- Market prices table
CREATE TABLE IF NOT EXISTS market_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mandi_name TEXT NOT NULL,
    commodity TEXT NOT NULL,
    price REAL NOT NULL,
    unit TEXT DEFAULT 'quintal',
    district TEXT NOT NULL,
    date DATE NOT NULL,
    source TEXT, -- 'agmarknet', 'manual', 'api'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Soil test reports table
CREATE TABLE IF NOT EXISTS soil_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    district TEXT NOT NULL,
    taluk TEXT,
    nitrogen REAL,
    phosphorus REAL,
    potassium REAL,
    ph REAL,
    organic_carbon REAL,
    soil_type TEXT,
    test_date DATE,
    lab_name TEXT,
    report_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers (id)
);

-- Crop yield records table
CREATE TABLE IF NOT EXISTS crop_yields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    season TEXT NOT NULL, -- 'kharif', 'rabi', 'zaid'
    year INTEGER NOT NULL,
    crop TEXT NOT NULL,
    area REAL NOT NULL, -- in acres
    yield_amount REAL, -- in quintals
    yield_per_acre REAL,
    district TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers (id)
);

-- API usage logs table
CREATE TABLE IF NOT EXISTS api_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT NOT NULL,
    method TEXT NOT NULL,
    farmer_id INTEGER,
    request_data TEXT,
    response_status INTEGER,
    response_time REAL, -- in milliseconds
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers (id)
);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    recommendation_id INTEGER,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback_text TEXT,
    is_helpful BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers (id),
    FOREIGN KEY (recommendation_id) REFERENCES recommendations (id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_farmers_phone ON farmers (phone);
CREATE INDEX IF NOT EXISTS idx_farmers_district ON farmers (district);
CREATE INDEX IF NOT EXISTS idx_recommendations_farmer ON recommendations (farmer_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_district ON recommendations (district);
CREATE INDEX IF NOT EXISTS idx_weather_alerts_farmer ON weather_alerts (farmer_id);
CREATE INDEX IF NOT EXISTS idx_weather_alerts_district ON weather_alerts (district);
CREATE INDEX IF NOT EXISTS idx_market_prices_commodity ON market_prices (commodity);
CREATE INDEX IF NOT EXISTS idx_market_prices_date ON market_prices (date);
CREATE INDEX IF NOT EXISTS idx_soil_reports_farmer ON soil_reports (farmer_id);
CREATE INDEX IF NOT EXISTS idx_crop_yields_farmer ON crop_yields (farmer_id);
CREATE INDEX IF NOT EXISTS idx_crop_yields_season_year ON crop_yields (season, year);
CREATE INDEX IF NOT EXISTS idx_api_logs_endpoint ON api_logs (endpoint);
CREATE INDEX IF NOT EXISTS idx_api_logs_created_at ON api_logs (created_at);

-- Insert sample data
INSERT OR IGNORE INTO farmers (phone, name, district, taluk, village) VALUES
('919876543210', 'Ravi Kumar', 'Patiala', 'Samana', 'Samana'),
('919876543211', 'Shalom Raj', 'Ludhiana', 'Ludhiana', 'Ludhiana'),
('919876543212', 'Renuka Prasad', 'Amritsar', 'Amritsar', 'Amritsar');

INSERT OR IGNORE INTO market_prices (mandi_name, commodity, price, unit, district, date, source) VALUES
('Patiala Mandi', 'Wheat', 2450, 'quintal', 'Patiala', '2025-01-15', 'manual'),
('Amritsar Mandi', 'Rice (Basmati)', 3200, 'quintal', 'Amritsar', '2025-01-15', 'manual'),
('Ludhiana Mandi', 'Maize', 1950, 'quintal', 'Ludhiana', '2025-01-15', 'manual'),
('Bathinda Mandi', 'Cotton', 6800, 'quintal', 'Bathinda', '2025-01-15', 'manual'),
('Sangrur Mandi', 'Mustard', 5800, 'quintal', 'Sangrur', '2025-01-15', 'manual');

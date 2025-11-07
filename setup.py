# setup.py - Setup script for SmartCrop Advisory System
import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a command and log the result"""
    try:
        logger.info(f"Running: {description}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'datasets',
        'models',
        'logs',
        'tests',
        'uploads'
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"✅ Created directory: {directory}")
        except Exception as e:
            logger.error(f"❌ Failed to create directory {directory}: {str(e)}")

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def initialize_database():
    """Initialize the database"""
    return run_command("python database/init_db.py", "Initializing database")

def train_model():
    """Train the ML model"""
    return run_command("python models/train_model.py", "Training ML model")

def setup_environment():
    """Set up environment file"""
    env_file = '.env'
    env_example = 'env_example.txt'
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        try:
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            logger.info("✅ Created .env file from example")
        except Exception as e:
            logger.error(f"❌ Failed to create .env file: {str(e)}")

def main():
    """Main setup function"""
    logger.info("🚀 Setting up SmartCrop Advisory System...")
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        logger.error("❌ Setup failed at dependency installation")
        return False
    
    # Initialize database
    if not initialize_database():
        logger.error("❌ Setup failed at database initialization")
        return False
    
    # Train model
    if not train_model():
        logger.warning("⚠️ Model training failed, but continuing...")
    
    # Setup environment
    setup_environment()
    
    logger.info("🎉 Setup completed successfully!")
    logger.info("📝 Next steps:")
    logger.info("   1. Update .env file with your API keys")
    logger.info("   2. Run: python app.py")
    logger.info("   3. Visit: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# init_db.py - Database initialization script
import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the SQLite database with schema and sample data"""
    try:
        # Create datasets directory if it doesn't exist
        os.makedirs('datasets', exist_ok=True)
        
        # Connect to database
        db_path = 'datasets/smartcrop.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Read and execute schema
        with open('database/schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Execute schema (split by semicolon for multiple statements)
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        for statement in statements:
            cursor.execute(statement)
        
        conn.commit()
        logger.info("Database initialized successfully")
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        logger.info(f"Created tables: {[table[0] for table in tables]}")
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False

def reset_database():
    """Reset the database (drop all tables and recreate)"""
    try:
        db_path = 'datasets/smartcrop.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            logger.info("Existing database removed")
        
        return init_database()
        
    except Exception as e:
        logger.error(f"Error resetting database: {str(e)}")
        return False

if __name__ == "__main__":
    print("Initializing SmartCrop Advisory System Database...")
    if init_database():
        print("✅ Database initialization completed successfully!")
    else:
        print("❌ Database initialization failed!")

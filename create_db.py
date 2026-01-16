"""
Script to create MySQL database for the Event Booking Platform
Run this before running migrations
"""
import mysql.connector
from mysql.connector import Error
import sys

# Database configuration - Update these if needed
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'newpassword',  # Change this to your MySQL password
    'database': 'eventbooking_db'
}

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Database '{DB_CONFIG['database']}' created successfully!")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Error creating database: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL server is running")
        print("2. Check your MySQL username and password")
        print("3. Update the password in this script if needed")
        return False

if __name__ == "__main__":
    print("Creating MySQL database...")
    print(f"Host: {DB_CONFIG['host']}")
    print(f"User: {DB_CONFIG['user']}")
    print(f"Database: {DB_CONFIG['database']}\n")
    
    # Update password if provided as argument
    if len(sys.argv) > 1:
        DB_CONFIG['password'] = sys.argv[1]
        print(f"Using password from command line argument\n")
    
    if create_database():
        print("\n✅ Database created! You can now run:")
        print("   python manage.py makemigrations")
        print("   python manage.py migrate")
    else:
        print("\n❌ Failed to create database. Please check the error above.")


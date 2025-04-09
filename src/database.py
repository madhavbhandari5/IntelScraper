# database.py
import mysql.connector
from config import DB_CONFIG

def create_database():
    # Connect to MySQL without specifying a database
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cursor = conn.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS UNData")

    # Switch to the newly created database
    cursor.execute("USE UNData")

    # Create the Animals table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Animals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_or_area VARCHAR(255),
            year INT,
            commodity VARCHAR(255),
            flow VARCHAR(255),
            trade_usd DECIMAL(15, 2),
            weight_kg DECIMAL(15, 2),
            quantity_name VARCHAR(255),
            quantity DECIMAL(15, 2)
        )
    """)

    # Create the Meats table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Meats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_or_area VARCHAR(255),
            year INT,
            commodity VARCHAR(255),
            flow VARCHAR(255),
            trade_usd DECIMAL(15, 2),
            weight_kg DECIMAL(15, 2),
            quantity_name VARCHAR(255),
            quantity DECIMAL(15, 2)
        )
    """)

    # Create the Fishes table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Fishes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_or_area VARCHAR(255),
            year INT,
            commodity VARCHAR(255),
            flow VARCHAR(255),
            trade_usd DECIMAL(15, 2),
            weight_kg DECIMAL(15, 2),
            quantity_name VARCHAR(255),
            quantity DECIMAL(15, 2)
        )
    """)

    # Create the Dairies table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Dairies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_or_area VARCHAR(255),
            year INT,
            commodity VARCHAR(255),
            flow VARCHAR(255),
            trade_usd DECIMAL(15, 2),
            weight_kg DECIMAL(15, 2),
            quantity_name VARCHAR(255),
            quantity DECIMAL(15, 2)
        )
    """)

    # Create the AnimalOriginated table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AnimalOriginated (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_or_area VARCHAR(255),
            year INT,
            commodity VARCHAR(255),
            flow VARCHAR(255),
            trade_usd DECIMAL(15, 2),
            weight_kg DECIMAL(15, 2),
            quantity_name VARCHAR(255),
            quantity DECIMAL(15, 2)
        )
    """)

    # Create the Trees table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Trees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_or_area VARCHAR(255),
            year INT,
            commodity VARCHAR(255),
            flow VARCHAR(255),
            trade_usd DECIMAL(15, 2),
            weight_kg DECIMAL(15, 2),
            quantity_name VARCHAR(255),
            quantity DECIMAL(15, 2)
        )
    """)

    # Commit and close the connection
    conn.commit()
    conn.close()

def insert_data(table_name, data_list):
    # Connect to MySQL with the database specified
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Use the UNData database
    cursor.execute("USE UNData")

    # Insert data into the specified table
    insert_query = f"""
        INSERT INTO {table_name} (country_or_area, year, commodity, flow, trade_usd, weight_kg, quantity_name, quantity)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, data_list)

    # Commit and close the connection
    conn.commit()
    conn.close()
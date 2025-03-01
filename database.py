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

    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS InfantDeaths (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country VARCHAR(255),
            year INT,
            deaths INT
        )
    """)

    # Commit and close the connection
    conn.commit()
    conn.close()

def insert_data(data_list):
    # Connect to MySQL with the database specified
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Use the UNData database
    cursor.execute("USE UNData")

    # Insert data into the table
    insert_query = "INSERT INTO InfantDeaths (country, year, deaths) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, data_list)

    # Commit and close the connection
    conn.commit()
    conn.close()

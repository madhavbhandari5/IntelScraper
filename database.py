import mysql.connector
from config import DB_CONFIG

def create_database():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS UNData")
    cursor.execute("USE UNData")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS InfantDeaths (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country VARCHAR(255),
            year INT,
            deaths INT
        )
    """)
    conn.commit()
    conn.close()

def insert_data(data_list):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("USE UNData")
    insert_query = "INSERT INTO InfantDeaths (country, year, deaths) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, data_list)
    conn.commit()
    conn.close()

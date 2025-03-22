# main.py
from database import create_database, insert_data
from scraper import scrape_all_tables

def main():
    # Create the database and tables
    create_database()
    
    # Scrape data for all tables
    print("Starting scraping process...")
    data = scrape_all_tables()
    
    # Insert data into the Animals table
    print("Inserting data into the Animals table...")
    insert_data("Animals", data["Animals"])
    print(f"Inserted {len(data['Animals'])} records into the Animals table.")
    
    # Insert data into the Meats table
    print("Inserting data into the Meats table...")
    insert_data("Meats", data["Meats"])
    print(f"Inserted {len(data['Meats'])} records into the Meats table.")
    
    # Insert data into the Fishes table
    print("Inserting data into the Fishes table...")
    insert_data("Fishes", data["Fishes"])
    print(f"Inserted {len(data['Fishes'])} records into the Fishes table.")
    
    print("Data insertion complete.")

if __name__ == "__main__":
    main()
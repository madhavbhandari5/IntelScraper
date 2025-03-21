# main.py
from database import create_database, insert_data
from scraper import scrape_all_pages

def main():
    # Create the database and table
    create_database()
    
    # Scrape all pages
    print("Starting scraping process...")
    data = scrape_all_pages()
    print(f"Scraped {len(data)} records.")
    
    # Insert data into the database
    print("Inserting data into the database...")
    insert_data(data)
    print("Data insertion complete.")

if __name__ == "__main__":
    main()
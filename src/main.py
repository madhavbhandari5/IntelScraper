from database import create_database
from scraper import scrape_all_pages

if __name__ == "__main__":
    create_database()
    scrape_all_pages()

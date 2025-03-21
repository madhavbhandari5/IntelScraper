import requests
from bs4 import BeautifulSoup
import mysql.connector
from database import insert_data
from config import BASE_URL, TOTAL_PAGES

def scrape_page(page_number):
    url = f"{BASE_URL}&p={page_number}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_number}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    data_list = []
    
    table = soup.find("table", {"class": "tblData"})
    if not table:
        print(f"No data table found on page {page_number}")
        return []
    
    rows = table.find_all("tr")[1:]  # Skip header row
    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 3:
            country = columns[0].text.strip()
            year = columns[1].text.strip()
            deaths = columns[2].text.strip()
            data_list.append((country, year, deaths))
    
    return data_list

def scrape_all_pages():
    for page in range(1, TOTAL_PAGES + 1):
        print(f"Scraping page {page}...")
        data = scrape_page(page)
        if data:
            insert_data(data)
    print("Scraping completed!")

if __name__ == "__main__":
    scrape_all_pages()

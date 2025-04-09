# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_page(driver):
    data = []
    table = driver.find_element(By.CLASS_NAME, 'DataContainer')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    
    for row in rows[1:]:  # Skip header row
        cols = row.find_elements(By.TAG_NAME, 'td')
        try:
            country_or_area = cols[0].text.strip()
            
            # Handle empty or missing values for year
            year = cols[1].text.strip().replace(',', '')
            year = int(year) if year else 0  # Default to 0 if empty
            
            commodity = cols[2].text.strip()
            flow = cols[3].text.strip()
            
            # Handle empty or missing values for trade_usd
            trade_usd = cols[4].text.strip().replace(',', '')
            trade_usd = float(trade_usd) if trade_usd else 0.0
            
            # Handle empty or missing values for weight_kg
            weight_kg = cols[5].text.strip().replace(',', '')
            weight_kg = float(weight_kg) if weight_kg else 0.0
            
            quantity_name = cols[6].text.strip()
            
            # Handle empty or missing values for quantity
            quantity = cols[7].text.strip().replace(',', '')
            quantity = float(quantity) if quantity else 0.0
            
            data.append((country_or_area, year, commodity, flow, trade_usd, weight_kg, quantity_name, quantity))
        except Exception as e:
            print(f"Error processing row: {e}")
            continue  # Skip this row and continue with the next one
    
    return data

def scrape_table(driver, url, max_pages=20):
    driver.get(url)
    all_data = []
    try:
        for page in range(1, max_pages + 1):
            # Wait for the table to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'DataContainer'))
            )
            
            # Scrape the current page
            current_page = driver.find_element(By.ID, 'spanPageIndexB').text
            print(f"Scraping page {current_page} of {url}")
            page_data = scrape_page(driver)
            all_data.extend(page_data)
            
            # Check if there is a next page
            next_button = driver.find_element(By.ID, 'linkNextB')
            if 'disabled' in next_button.get_attribute('class'):
                print("No more pages available. Stopping scraping.")
                break  # Exit if there is no next page
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
            # Re-locate the table after navigating to the next page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'DataContainer'))
            )
    except Exception as e:
        print(f"Error during scraping: {e}")
    
    return all_data

def scrape_all_tables():
    # Initialize the WebDriver using the Service class
    service = Service(executable_path='/usr/bin/chromedriver')  # Use Service class
    driver = webdriver.Chrome(service=service)  # Pass the service object
    
    # Scrape the Animals table
    animals_url = "https://data.un.org/Data.aspx?d=ComTrade&f=_l1Code%3a2"
    animals_data = scrape_table(driver, animals_url, max_pages=20)
    
    # Scrape the Meats table
    meats_url = "https://data.un.org/Data.aspx?d=ComTrade&f=_l1Code%3a3"
    meats_data = scrape_table(driver, meats_url, max_pages=20)
    
    # Scrape the Fishes table
    fishes_url = "https://data.un.org/Data.aspx?d=ComTrade&f=_l1Code%3a4"
    fishes_data = scrape_table(driver, fishes_url, max_pages=20)

    # Scrape the Dairies table
    dairies_url = "https://data.un.org/Data.aspx?d=ComTrade&f=_l1Code%3a5"
    dairies_data = scrape_table(driver, dairies_url, max_pages=20)
    
    # Scrape the Meats table
    animaloriginated_url = "https://data.un.org/Data.aspx?d=ComTrade&f=_l1Code%3a6"
    animaloriginated_data = scrape_table(driver, animaloriginated_url, max_pages=20)
    
    # Scrape the Trees table
    trees_url = "https://data.un.org/Data.aspx?d=ComTrade&f=_l1Code%3a7"
    trees_data = scrape_table(driver, trees_url, max_pages=20)
    
    driver.quit()
    
    return {
        "Animals": animals_data,
        "Meats": meats_data,
        "Fishes": fishes_data,
        "Dairies": dairies_data,
        "AnimalOriginated": animaloriginated_data,
        "Trees": trees_data
    }
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
            year = int(cols[1].text.strip())
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

def scrape_all_pages():
    # Initialize the WebDriver using the Service class
    service = Service(executable_path='/usr/bin/chromedriver')  # Use Service class
    driver = webdriver.Chrome(service=service)  # Pass the service object
    driver.get("https://data.un.org/Data.aspx?d=ComTrade&f=_l1Code%3a2")
    
    all_data = []
    try:
        while True:
            # Wait for the table to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'DataContainer'))
            )
            
            # Scrape the current page
            current_page = driver.find_element(By.ID, 'spanPageIndexB').text
            print(f"Scraping page {current_page}")
            page_data = scrape_page(driver)
            all_data.extend(page_data)
            
            # Check if there is a next page
            next_button = driver.find_element(By.ID, 'linkNextB')
            if 'disabled' in next_button.get_attribute('class'):
                break  # Exit if there is no next page
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
    finally:
        driver.quit()
    
    return all_data
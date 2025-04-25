# Project Name: IntelScraper

# Project Title: Custom Web Scraper with Data Visualization: Insights from the Web

## YouTube Link: 
[https://www.youtube.com/watch?v=005RQ6pRFIY&ab_channel=MadhavBhandari]

## Project Setup
## Clone the Repository
Clone this repository to your local machine:

`git clone https://github.com/madhavbhandari5/IntelScraper.git`

`cd IntelScraper`

## Create and Activate Virtual Environment
`cd src`

`python -m venv venv`

`source venv/bin/activate  # On Windows use: venv\Scripts\activate`

`pip install -r requirements.txt`


## Install Dependencies (Optional)
`pip install streamlit mysql-connector-python pandas plotly selenium pycountry`

## Run the Scraper App
`python main.py`

## Run the Streamlit App
`streamlit run dashboard.py`

## Project Description
IntelScraper is a Python-based web scraping tool designed to extract, process, and visualize data from [UN Data](https://data.un.org/). This project automates data retrieval from the website, transforming raw information into meaningful insights through visualization.

## Purpose
The primary objective of IntelScraper is to facilitate automated data extraction from UN Data and present it in an interactive and user-friendly format. This enables researchers, analysts, and businesses to analyze global datasets more efficiently.

## Value
- **Researchers & Analysts:** Provides structured access to global datasets.
- **Policy Makers & Businesses:** Enables data-driven decision-making based on official international data.
- **Students & Educators:** A practical example of web scraping and data visualization.
By automating data collection and analysis, this project reduces manual effort and enhances accuracy.

## Technologies Used
- **Web Scraping:** BeautifulSoup, Selenium, requests
- **Data Processing:** pandas
- **Visualization:** matplotlib, seaborn, Plotly
- **Dashboard:** Streamlit
- **Storage:** MySQL, CSV

This project delivers an efficient and automated approach to working with large-scale global data from the UN Data platform.



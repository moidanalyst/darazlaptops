## Import neccessary modules

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set display options
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Auto-adjust width to display all columns
pd.set_option('display.precision', 2)  # Set precision for floating-point numbers

# Function for scraping data from a page

def fetch_page_data(url):
    browser.get(url)
    name_search = browser.find_elements(By.CLASS_NAME, "title-wrapper--IaQ0m")
    price_search = browser.find_elements(By.CLASS_NAME, "currency--GVKjl")
    
    # # Iterate over the elements and print names and prices
    items_list = []
    prices_list = []

    # get names of laptops
    for items, prices in zip(name_search, price_search):
    
        item = items.text.strip()
        price = prices.text.strip()

        items_list.append(item)
        prices_list.append(price)

    # Insert both lists into a Data Frame and clean and transform the data
    df = pd.DataFrame({"Laptop" : items_list, "Price" : prices_list})
    df["Price"] = df["Price"].astype("string").str.replace('Rs. ', '').str.replace(',', '').astype(int, errors = 'ignore')
    return df

# Open the browser and go to Daraz

# open the browser
browser = webdriver.Chrome()
browser.maximize_window()

# load the webpage
page_url = 'https://www.daraz.pk/laptops/?page='

# create an empty list to store data frames returned
dfs = []

#loop over all pages and get the data
for pages in range(20):
    print("Scraping page ", pages + 1, "....")
    df = fetch_page_data(page_url + str(pages + 1))
    dfs.append(df)

# Concatenate the list of DataFrames into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Put the combined data frame into an excel file
combined_df.to_excel(r"C:\Downloads\Daraz Laptops Data\Data.xlsx")

# Close the browser
browser.quit()

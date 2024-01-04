import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
options.set_capability('browser_version', 'latest')
options.set_capability('os', 'Windows')
options.set_capability('os_version', '10')
options.set_capability('resolution', '1024x768')
options.set_capability('name', 'OLX Scraping Test')

username = 'muhammadarasy_XjL2rC'
access_key = '9yDUvfNRsz9v152bHotT'

driver = webdriver.Remote(
    command_executor=f'https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub',
    options=options
)

url = "https://www.olx.co.id/jakarta-dki_g2000007/mobil-bekas_c198"
driver.get(url)

wait = WebDriverWait(driver, 30)

# Wait for the first listing to be present to make sure the page has loaded
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li._3V_Ww")))

try:
    while True:
        # Try to find and click the 'load more' button
        try:
            load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-aut-id='btnLoadMore']")))
            driver.execute_script("arguments[0].click();", load_more_button)
            print("Clicked 'Load More'")
            # Wait for the new items to load
            time.sleep(5)
        except TimeoutException:
            # If no more 'Load More' button, exit the loop
            print("No more 'Load More' button found, finished loading all items.")
            break

    # After loading all items, now start scraping
    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = soup.findAll('li', class_="_3V_Ww")
    products = []

    for item in items:
        product_name = item.find("div", class_="_2Gr10").text if item.find("div", class_="_2Gr10") else 'N/A'
        price = item.find("span", {"data-aut-id": "itemPrice"}).text if item.find("span", {"data-aut-id": "itemPrice"}) else 'N/A'
        year_mileage = item.find("div", class_="_21gnE").text if item.find("div", class_="_21gnE") else 'N/A'
        location = item.find("div", class_="_3VRSm").text if item.find("div", class_="_3VRSm") else 'N/A'
        products.append((product_name, price, year_mileage, location))

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Save to CSV file
    csv_file = "OLX_Used_Car_Dataset.csv"  # Ensure this is the correct path in your environment
    df = pd.DataFrame(products, columns=["product_name", "price", "year_mileage", "location"])
    df.to_csv(csv_file, index=False)
    print(f"Data Saved Successfully to {csv_file}")
    driver.quit()
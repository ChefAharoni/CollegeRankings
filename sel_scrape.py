from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_page(page_source):
    """Scrape the required data from a single page's HTML source."""
    soup = BeautifulSoup(page_source, "html.parser")
    us_universities = soup.find_all("tr", {"data-v-ae1ab4a8": True})
    data = []

    # Find all elements with the class 'inputWrapper'
    input_wrappers = driver.find_elements(By.CLASS_NAME, "inputWrapper")

    # Select the correct filter button based on its index
    # Adjust the index as necessary to select the correct filter button
    filter_button = input_wrappers[2]
    filter_button.click()
    time.sleep(2)  # Wait for the dropdown to open

    # Now target the specific <li> element containing 'United States'
    us_option_xpath = "//li[contains(text(), 'United States')]"
    us_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, us_option_xpath))
    )
    us_option.click()
    time.sleep(2)  # Wait for the filter to apply

    for uni in us_universities:
        if "us.png" in str(uni):
            ranking_div = uni.find("div", class_="ranking")
            ranking = ranking_div.get_text(strip=True) if ranking_div else None

            name_span = uni.find("span", class_="univ-name")
            name = name_span.get_text(strip=True) if name_span else None

            # logo_img = uni.find("img", class_="univ-logo")
            # logo = logo_img["src"] if logo_img and "src" in logo_img.attrs else None

            if ranking and name:
                data.append({"Ranking": ranking, "Name": name})

    return data


# Start a Selenium WebDriver session
driver = webdriver.Chrome()

# URL of the page to scrape
URL = "https://www.shanghairanking.com/rankings/gras/2023/RS0210"

driver.get(URL)
time.sleep(5)  # Wait for the page to fully load

all_data = []

# Assuming a maximum of 10 pages for simplicity, adjust as needed
for i in range(10):
    # Scrape the current page
    page_data = scrape_page(driver.page_source)
    all_data.extend(page_data)

    # Click the 'Next' button to go to the next page
    try:
        next_button = driver.find_element(By.CLASS_NAME, "ant-pagination-next")
        next_button.click()
        time.sleep(5)  # Wait for the next page to load
    except Exception as e:
        print("No more pages or an error occurred:", e)
        break


# Close the browser session
driver.quit()

# Convert the data to a DataFrame and save to CSV
df = pd.DataFrame(all_data)
csv_file_path = "data/us_universities_rankings_all_pages.csv"
df.to_csv(csv_file_path, index=False)

print(f"Data scraped and saved to {csv_file_path}")

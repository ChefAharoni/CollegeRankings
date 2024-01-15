from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_driver():
    """Initialize the Selenium WebDriver."""
    driver = webdriver.Chrome()
    return driver


def select_us_filter(driver):
    """Select the United States filter."""
    input_wrappers = driver.find_elements(By.CLASS_NAME, "inputWrapper")
    filter_button = input_wrappers[2]
    filter_button.click()
    time.sleep(2)  # Wait for the dropdown to open

    us_option_xpath = "//li[contains(text(), 'United States')]"
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, us_option_xpath))
    ).click()
    time.sleep(2)  # Wait for the filter to apply


def scrape_page(driver):
    """Scrape the required data from a single page."""
    soup = BeautifulSoup(driver.page_source, "html.parser")
    us_universities = soup.find_all("tr", {"data-v-ae1ab4a8": True})
    data = []

    for uni in us_universities:
        if "us.png" in str(uni):
            ranking_div = uni.find("div", class_="ranking")
            ranking = ranking_div.get_text(strip=True) if ranking_div else None
            name_span = uni.find("span", class_="univ-name")
            name = name_span.get_text(strip=True) if name_span else None
            if ranking and name:
                data.append({"Ranking": ranking, "Name": name})

    return data


def navigate_to_next_page(driver):
    """Navigate to the next page if possible."""
    try:
        next_button = driver.find_element(By.CLASS_NAME, "ant-pagination-next")
        if "ant-pagination-disabled" in next_button.get_attribute("class"):
            print("No more pages to navigate.")
            return False
        next_button.click()
        time.sleep(5)  # Wait for the next page to load
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False


def main(url):
    """Main function to orchestrate the scraping process."""
    driver = init_driver()
    driver.get(url)
    time.sleep(5)  # Wait for the page to fully load

    select_us_filter(driver)  # Select the United States filter

    all_data = []
    while True:
        all_data.extend(scrape_page(driver))
        if not navigate_to_next_page(driver):
            break

    driver.quit()

    # Save the scraped data to CSV
    df = pd.DataFrame(all_data)
    csv_file_path = "data/us_universities_rankings_all_pages.csv"
    df.to_csv(csv_file_path, index=False)
    print(f"Data scraped and saved to {csv_file_path}")


if __name__ == "__main__":
    url = "https://www.shanghairanking.com/rankings/gras/2023/RS0210"
    main(url)

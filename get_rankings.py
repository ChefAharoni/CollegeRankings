from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_driver():
    """
    Initialize the Selenium WebDriver.

    Returns:
        driver (WebDriver): The initialized Selenium WebDriver.
    """
    driver = webdriver.Chrome()
    return driver


def select_us_filter(driver: webdriver, country="United States") -> None:
    """
    Select the United States filter.

    Args:
        driver (WebDriver): The Selenium WebDriver.

    Returns:
        None
    """
    input_wrappers = driver.find_elements(By.CLASS_NAME, "inputWrapper")
    filter_button = input_wrappers[2]
    filter_button.click()
    time.sleep(2)  # Wait for the dropdown to open
    country_option_xpath = f"//li[contains(text(), '{country}')]"
    # us_option_xpath = "//li[contains(text(), 'United States')]"
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, country_option_xpath))
    ).click()
    time.sleep(2)  # Wait for the filter to apply


def scrape_page(driver: webdriver) -> list[str, str]:
    """
    Scrape the required data from a single page.

    Args:
        driver (WebDriver): The Selenium WebDriver.

    Returns:
        data (list): A list of dictionaries containing the scraped data.
    """
    soup = BeautifulSoup(driver.page_source, "html.parser")
    us_universities = soup.find_all("tr", {"data-v-ae1ab4a8": True})
    data = []

    for uni in us_universities:
        ranking_div = uni.find("div", class_="ranking")
        ranking = ranking_div.get_text(strip=True) if ranking_div else None
        name_span = uni.find("span", class_="univ-name")
        name = name_span.get_text(strip=True) if name_span else None
        if ranking and name:
            data.append({"Ranking": ranking, "Name": name})

    return data


def navigate_to_next_page(driver: webdriver) -> bool:
    """
    Navigate to the next page if possible.

    Args:
        driver (WebDriver): The Selenium WebDriver.

    Returns:
        bool: True if successfully navigated to the next page, False otherwise.
    """
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


def get_country_code(country: str):
    """
    Returns the country code for a given country name.

    Parameters:
        country (str): The name of the country.

    Returns:
        str: The country code.
    """
    words = country.split()
    if len(words) == 1:
        return words[0].title()
    else:
        return "".join([w[0] for w in words]).upper()


def main(url: str, country="United States") -> None:
    """
    Main function to orchestrate the scraping process.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        None
    """
    driver = init_driver()  # Initialize the Selenium WebDriver
    driver.get(url)  # Navigate to the URL
    time.sleep(5)  # Wait for the page to fully load

    select_us_filter(driver, country)  # Select the United States filter

    all_data = []
    while True:
        all_data.extend(scrape_page(driver))
        if not navigate_to_next_page(driver):
            break

    driver.quit()

    # Save the scraped data to CSV
    df = pd.DataFrame(all_data)
    country_code = get_country_code(country)
    csv_file_path = f"data/{country_code}_universities_rankings_all_pages.csv"
    df.to_csv(csv_file_path, index=False)
    print(f"Data scraped and saved to {csv_file_path}")


if __name__ == "__main__":
    url = "https://www.shanghairanking.com/rankings/gras/2023/RS0210"
    countries = ["United States", "United Kingdom", "Canada", "Israel"]
    # country = "United States"
    # country = "United Kingdom"
    # country = "Israel"
    for country in countries:
        main(url, country)

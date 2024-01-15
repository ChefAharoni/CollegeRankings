from selenium import webdriver
import selenium

driver = webdriver.Chrome()
driver.get('https://www.shanghairanking.com/rankings/gras/2023/RS0210')
driver.implicitly_wait(5)


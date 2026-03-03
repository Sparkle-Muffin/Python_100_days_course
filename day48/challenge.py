from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=firefox_options)
driver.get("https://secure-retreat-92358.herokuapp.com/")

name = driver.find_element(By.NAME, value="fName")
name.send_keys("Imie")
surname = driver.find_element(By.NAME, value="lName")
surname.send_keys("Nazwisko")
email = driver.find_element(By.NAME, value="email")
email.send_keys("mojemail@gmail.com")

button = driver.find_element(By.XPATH, value="/html/body/form/button")
button.click()

driver.quit()

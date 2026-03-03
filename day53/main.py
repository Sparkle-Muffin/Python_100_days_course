import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=firefox_options)
wait = WebDriverWait(driver, 10)


zillow_website = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(zillow_website)
data = response.text
soup = BeautifulSoup(data, "html.parser")
addresses = soup.select("li address")
prices = soup.select("li span.PropertyCardWrapper__StyledPriceLine")
links = soup.select("li a.StyledPropertyCardDataArea-anchor")


driver.get("https://forms.gle/t1RCFd9nMncSf7nh7")

for i in range(len(addresses)):
    address_input = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//span[normalize-space()=\"What's the address of the property?\"]"
            "/ancestor::div[@jscontroller='sWGJ4b']//input[@type='text']"
        ))
    )
    price_input = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//span[normalize-space()=\"What's the price per month?\"]"
            "/ancestor::div[@jscontroller='sWGJ4b']//input[@type='text']"
        ))
    )
    link_input = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//span[normalize-space()=\"What's the link to the property?\"]"
            "/ancestor::div[@jscontroller='sWGJ4b']//input[@type='text']"
        ))
    )
    send_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Prześlij']"))
        )

    address_input.send_keys(addresses[i].text)
    price_input.send_keys(prices[i].text)
    link_input.send_keys(links[i]["href"])
    send_button.click()

    next_answer_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='Prześlij kolejną odpowiedź']"))
        )
    next_answer_button.click()


driver.quit()

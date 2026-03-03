from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime as dt

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=firefox_options)

# driver.get("https://appbrewery.github.io/instant_pot/")
# price_dollar = driver.find_element(By.CLASS_NAME, value="a-price-whole")
# price_cents = driver.find_element(By.CLASS_NAME, value="a-price-fraction")
# print(f"The price is {price_dollar.text}.{price_cents.text}.")

driver.get("https://www.python.org/")

# search_bar = driver.find_element(By.NAME, value="q")
# print(search_bar.get_attribute("placeholder"))
# button = driver.find_element(By.ID, value="submit")
# print(button.size)
# documentation_link = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
# print(documentation_link.text)
# bug_link = driver.find_element(By.XPATH, value="/html/body/div/footer/div[2]/div/ul/li[3]/a")
# print(bug_link.text)

dates = driver.find_elements(By.CSS_SELECTOR, value=".event-widget ul li time")
events_dates = []
for d in dates:
    date = dt.datetime.fromisoformat(d.get_attribute("datetime")).strftime("%Y-%m-%d")
    events_dates.append(date)
print(events_dates)

events = driver.find_elements(By.CSS_SELECTOR, value=".event-widget ul li a")
events_names = []
for e in events:
    event = e.text
    events_names.append(event)
print(events_names)

events_dict = {}
for i, e_d in enumerate(events_dates):
    events_dict[i] = {
        "time": e_d,
        "name":events_names[i]
        }
print(events_dict)

driver.quit()

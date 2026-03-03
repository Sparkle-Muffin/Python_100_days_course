from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
from time import time


BUYING_INTERVAL = 10   # in seconds
GAME_LENGTH = 5 * 60  # in seconds


# Check what can be bought
stop_event = threading.Event()
def check_element_periodically(buildings, interval):
    while not stop_event.is_set():
        highest_price = 0
        highest_price_building = None
        for b in buildings:
            if b.get_attribute("class") == "product unlocked enabled":
                price = int(b.find_element(By.CLASS_NAME, "price").text)
                if price > highest_price:
                    highest_price = price
                    highest_price_building = b
        if highest_price_building != None:
            highest_price_building.click()

        stop_event.wait(interval)


# 0) Init
firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=firefox_options)
driver.get("https://ozh.github.io/cookieclicker/")
wait = WebDriverWait(driver, 15)


# 1) Click the language button
language_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="langSelect-EN"]'))
)
language_button.click()


# 2) Wait for the cookie button to be clickable
cookie_button = wait.until(
    EC.element_to_be_clickable((By.ID, 'bigCookie'))
)


# 3) Create buildings list
buildings = []
for n in range(20):
    building = wait.until(
        EC.presence_of_element_located((By.ID, f"product{n}"))
    )
    buildings.append(building)


# 4) Create a thread that will be called every BUYING_INTERVAL
thread = threading.Thread(
    target=check_element_periodically,
    args=(buildings, BUYING_INTERVAL),
    daemon=True
)
thread.start()


# 5) Get div holding the number of cookies
total_cookies = wait.until(
        EC.presence_of_element_located((By.ID, "cookies"))
    )


# 6) Click cookies in a loop
start_time = time()
while True:
    cookie_button.click()
    if time() - start_time > GAME_LENGTH:
        print(f"You collected {total_cookies.text}")
        break

driver.quit()

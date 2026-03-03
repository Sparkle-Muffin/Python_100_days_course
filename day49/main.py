from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from date_converter import DateConverter
import time


# 0) Init
BASE_DIR = Path(__file__).parent
user_data_dir = BASE_DIR / "firefox_profile"
os.makedirs(user_data_dir, exist_ok=True)
ACCOUNT_NAME = "piesktoryjezdzilkoleja"
ACCOUNT_EMAIL = "piesktoryjezdzilkoleja@gmail.com"  # The email you registered with
ACCOUNT_PASSWORD = "BardzoTrudneHaslo888!"      # The password you used during registration
CLASS_DATES = [
    {
        "day": "Tuesday",
        "time": "6:00 PM"
    },
    {
        "day": "Thursday",
        "time": "6:00 PM"
    }
]
ADVANCE = {
    "days": 3,
    "hours": 0,
    "minutes": 0
}

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("-profile")
firefox_options.add_argument(f"{user_data_dir}")
driver = webdriver.Firefox(options=firefox_options)
driver.get("https://appbrewery.github.io/gym/")
wait = WebDriverWait(driver, 2)


def retry(func, retries, description):
    for i in range(retries):
        print(f"Trying to run {description} function for the {i+1} time.")
        try:
            return func()
        except:
            print("fail")
            if i == retries - 1:
                raise
            time.sleep(1)

    
# 1) Log in
def login():
    log_in_button = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "Navigation_button__uyKX2"))
    )
    log_in_button.click()

    email_input = wait.until(
        EC.presence_of_element_located((By.ID, "email-input"))
    )
    email_input.clear()
    email_input.send_keys(f"{ACCOUNT_EMAIL}")

    password_input = wait.until(
        EC.presence_of_element_located((By.ID, "password-input"))
    )
    password_input.clear()
    password_input.send_keys(f"{ACCOUNT_PASSWORD}")

    submit_button = wait.until(
        EC.presence_of_element_located((By.ID, "submit-button"))
    )
    submit_button.click()

    wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))


# 2) Book the class
def book_class():
    classes_booked = 0
    waitlists_joined = 0
    already_booked_waitlisted = 0

    for date in CLASS_DATES:
        date_converter = DateConverter(date["day"], date["time"])
        tag_date = date_converter.convert_to_tag_format()
        human_readable_date = date_converter.convert_to_human_readable_format()

        class_divs = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"div[id$='{tag_date}']"))
            )
        for div in class_divs:
            activity_class_name = div.find_element(By.CSS_SELECTOR, value="h3").text
            activity_class_button = div.find_element(By.CSS_SELECTOR, value="button")
            activity_class_status = activity_class_button.text

            if activity_class_status == "Book Class":
                activity_class_button.click()
                classes_booked += 1
                print(f"✓ Booked: {activity_class_name} on {human_readable_date}")

            elif activity_class_status == "Join Waitlist":
                activity_class_button.click()
                waitlists_joined += 1
                print(f"✓ Joined waitlist: {activity_class_name} on {human_readable_date}")

            elif activity_class_status == "Booked":
                already_booked_waitlisted += 1
                print(f"✓ Already booked: {activity_class_name} on {human_readable_date}")

            elif activity_class_status == "Waitlisted":
                already_booked_waitlisted += 1
                print(f"✓ Already on waitlist: {activity_class_name} on {human_readable_date}")

    print("--- BOOKING SUMMARY ---")
    print(f"Classes booked: {classes_booked}")
    print(f"Waitlists joined: {waitlists_joined}")
    print(f"Already booked/waitlisted: {already_booked_waitlisted}")
    print(f"Total classes processed: {classes_booked + waitlists_joined + already_booked_waitlisted}")


retry(func=login, retries=10, description="login")
retry(func=book_class, retries=10, description="book_class")


# driver.quit()

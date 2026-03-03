import os
import smtplib
import random
import datetime as dt
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
birthdays_path = BASE_DIR / "birthdays.csv"
letter_templates_dir = BASE_DIR / "letter_templates"
my_email = os.getenv("MY_EMAIL")
app_password = os.getenv("APP_PASSWORD")
recipient_email = os.getenv("RECIPIENT_EMAIL")
birthday_date = dt.datetime(year=2026, month=1, day=1)

def send_email(title, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=app_password)
        connection.sendmail(from_addr=my_email, 
                            to_addrs=recipient_email, 
                            msg=f"Subject:{title}\n\n{body}")
        connection.close()

def check_if_today_is_birthday(birthday_date):
    today_date = dt.datetime.now()
    if birthday_date.year == today_date.year and birthday_date.month == today_date.month and birthday_date.day == today_date.day:
        return True
    else:
        return False

def fill_letter_template(name, template_path):
    with open(template_path) as file:
        content = file.read()
        content = content.replace("[NAME]", name)
    return content

def send_wishes(people):
    today_date = dt.datetime.now()
    letter_templates_dir_list = os.listdir(letter_templates_dir)
    for person in people: 
        if person["month"] == today_date.month and person["day"] == today_date.day:
            letter_template_path = random.choice(letter_templates_dir_list)
            letter_template_path = letter_templates_dir / letter_template_path
            filled_letter = fill_letter_template(person["name"], letter_template_path)
            send_email(title="Happy birthday!", body=filled_letter)

people_df = pd.read_csv(birthdays_path)
people = people_df.to_dict(orient="records")
people_with_birthday = send_wishes(people)

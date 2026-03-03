import requests
from bs4 import BeautifulSoup
import smtplib
import os


my_email = os.getenv("MY_EMAIL")
app_password = os.getenv("APP_PASSWORD")
recipient_email = os.getenv("RECIPIENT_EMAIL")
ORIGINAL_PRICE = float(100.99)
WEBSITE_URL = "https://appbrewery.github.io/instant_pot/"


def get_current_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0"
    }
    response = requests.get(
        WEBSITE_URL,
        headers=headers,
        timeout=10
    )    
    website = response.text

    soup = BeautifulSoup(website, "html.parser")

    price_decimal = soup.select_one("span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span[aria-hidden='true'] span.a-price-whole").get_text()
    price_fraction = soup.select_one("span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span[aria-hidden='true'] span.a-price-fraction").get_text()

    price = float(price_decimal + price_fraction)
    return price


def send_email(title, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=app_password)
        connection.sendmail(from_addr=my_email, 
                            to_addrs=recipient_email, 
                            msg=f"Subject:{title}\n\n{body}")
        connection.close()


current_price = get_current_price()
if current_price < ORIGINAL_PRICE:
    title = "Lower price alert!"
    body = f"It looks like the price of the product you want to buy dropped from {ORIGINAL_PRICE} to {current_price}! Check out: {WEBSITE_URL}."
    send_email(title, body)

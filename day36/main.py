import os
import requests
import datetime as dt
from twilio.rest import Client
import json
from pathlib import Path


BASE_DIR = Path(__file__).parent
company_stock_path = BASE_DIR / "company_stock.json"
company_news_path = BASE_DIR / "company_news.json"
alphavantage_api = "https://www.alphavantage.co/query"
newsapi_api = "https://newsapi.org/v2/everything"
COMPANY_SYMBOL = "TSLA"
COMPANY_NAME = "tesla"
NUMBER_OF_ARTICLES = 3


def get_company_stock_data():
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": COMPANY_SYMBOL,
        "apikey": os.getenv("ALPHAVANTAGE_API_KEY")
    }
    response = requests.get(alphavantage_api, params=parameters)
    response.raise_for_status()
    stock_data = response.json()

    with open(company_stock_path, mode="w") as file:
        json.dump(stock_data, file, indent=4)

    days = stock_data["Time Series (Daily)"]
    for i, day in enumerate(days):
        if i == 0:
            new_close_value = days[day]["4. close"]
        elif i == 1:
            old_close_value = days[day]["4. close"]
        else:
            break

    return float(new_close_value), float(old_close_value)
 

def get_news_about_company():
    today = dt.datetime.now()
    delta = dt.timedelta(days=1)
    yesterday = (today-delta).strftime("%Y-%m-%d")
    two_days_ago = (today-2*delta).strftime("%Y-%m-%d")

    parameters = {
        "q": COMPANY_NAME,
        "from": two_days_ago,
        "to": yesterday,
        "sortBy": "popularity",
        "apiKey": os.getenv("NEWSAPI_API_KEY")
    }
    response = requests.get(newsapi_api, params=parameters)
    response.raise_for_status()
    news_data = response.json()

    with open(company_news_path, mode="w") as file:
        json.dump(news_data, file, indent=4)

    articles = []
    for i, art in enumerate(news_data["articles"]):
        article = {
            "Headline": art["title"],
            "Brief": art["description"]
        }
        articles.append(article)

        if i == NUMBER_OF_ARTICLES - 1:
            break

    return articles


def send_whatsapp_notification(price_change, article):
    account_sid = os.getenv("ACf6a8b90a70a0ad11eda437baad7bbca4")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    if price_change > 0:
        change_symbol = "📈"
    elif price_change < 0:
        change_symbol = "📉"
    else:
        change_symbol = ""

    message = client.messages.create(
        from_=f'whatsapp:{os.getenv("TWILIO_PHONE_NUMBER")}',
        body=f"{COMPANY_SYMBOL} {change_symbol}{abs(price_change)}%\nHeadline: {article["Headline"]}\nBrief: {article["Brief"]}",
        to=f'whatsapp:{os.getenv("MY_PHONE_NUMBER")}'
    )

    print(message.sid)


new_close_value, old_close_value = get_company_stock_data()
share_price_change_perc = round((new_close_value - old_close_value) / old_close_value * 100, 0)
print(share_price_change_perc)

articles = get_news_about_company()
print(articles)

for article in articles:
    send_whatsapp_notification(share_price_change_perc, article)

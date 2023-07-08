import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")

NUM_TOP_ARTICLES = 3

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY
}


    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
new_list = [float(value['4. close']) for (key, value) in data.items()]

yesterday_close = new_list[0]
day_before_yesterday_close = new_list[1]

difference = abs(yesterday_close-day_before_yesterday_close)
difference_percent = (difference/yesterday_close) * 100

if difference_percent > 5:
    if yesterday_close < day_before_yesterday_close:
        direction = "🔻"
    else:
        direction = "🔺"

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    top_articles = news_data["articles"][:NUM_TOP_ARTICLES]

    for article in top_articles:
        # proxy_client = TwilioHttpClient()
        # proxy_client.session.proxies = {'https': os.environ['https_proxy']}

        message_text = f"{STOCK_NAME}: {direction} {difference_percent}% \nHeadline: {article['title']}\nBrief: {article['description']}"

        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
          from_=os.environ.get("FROM_TWILIO_NUM"),
          to=os.environ.get("TO_TWILIO_NUM"),
          body=message_text
        )
        print(message.sid)
        print(message.status)



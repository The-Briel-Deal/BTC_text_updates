# ----- IMPORTING MODULES ----- #
import os
import requests
import twilio.rest
import json
import btc_price
import datetime
# ----- DEFINING VARIABLES ----- #
ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
ACCOUNT_AUTH = os.environ.get('ACCOUNT_AUTH')
MY_PHONE = os.environ.get('MY_PHONE')
TWILIO_PHONE = os.environ.get('PHONE_NUMBER')
NEWS_KEY = os.environ.get('NEWS_KEY')
YESTERDAY_DATE = str((datetime.date.today() - datetime.timedelta(days=1)))
# ----- DEFINING FUNCTIONS ----- #


# ----- MAIN LOGIC ----- #
BTC_yesterday = requests.get('https://www.alphavantage.co/query',
                             params={'function': 'DIGITAL_CURRENCY_DAILY',
                                     'symbol': 'BTC',
                                     'market': 'USD',
                                     'apikey': os.environ.get('ALPHA_KEY')})
BTC_YESTERDAY_PRICE = (BTC_yesterday.json()["Time Series (Digital Currency Daily)"][YESTERDAY_DATE]['1a. open (USD)'])
BTC_YESTERDAY_PRICE_FLOAT = round(float(BTC_YESTERDAY_PRICE), 2)
print(BTC_YESTERDAY_PRICE_FLOAT)

# if BTC_yesterday <
# ----- FINDING NEWS ON BTC ----- #
btc_news = requests.get('https://newsapi.org/v2/top-headlines',
                        params={'apiKey': NEWS_KEY,
                                'q': 'Bitcoin',
                                'pageSize': '5'})
btc_news_dict = btc_news.json()['articles']
with open('dog.json', mode='w') as file:
    json.dump(BTC_yesterday.json(), file, indent=4)
# ----- FINDING CURRENT PRICE ----- #
BTC = btc_price.BtcPrice()
current_price = BTC.current_price()
if BTC_YESTERDAY_PRICE_FLOAT > current_price:
    increased_or_decreased = "did not increase"

else:
    increased_or_decreased = "did increase"
percentage_iod = round(((current_price / BTC_YESTERDAY_PRICE_FLOAT) * 100), 1)

# ----- SENDING MESSAGE ----- #
client = twilio.rest.Client(ACCOUNT_SID, ACCOUNT_AUTH)
message = client.messages.create(body=f'The current price ${current_price}'
                                      f'\n\nThe price {increased_or_decreased} by {percentage_iod}% since yesterday'
                                      f'\n\nHere are some news stories on the current price'
                                      f'\n\n{btc_news_dict[0]["title"]}\n{btc_news_dict[0]["url"]}'
                                      f'\n\n{btc_news_dict[1]["title"]}\n{btc_news_dict[1]["url"]}',
                                 from_=TWILIO_PHONE,
                                 to=MY_PHONE)

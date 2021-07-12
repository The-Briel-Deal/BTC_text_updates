import requests
import os
ALPHA_KEY = os.environ.get('ALPHA_KEY')


class BtcPrice:
    def __init__(self):
        self.BTC = requests.get('https://www.alphavantage.co/query',
                           params={'function': 'CURRENCY_EXCHANGE_RATE',
                                   'from_currency': 'BTC',
                                   'to_currency': 'USD',
                                   'apikey': ALPHA_KEY})

    def current_price(self):
        btc_dict = self.BTC.json()['Realtime Currency Exchange Rate']
        current_btc_price = btc_dict["5. Exchange Rate"]
        btc_price_rounded = round(float(current_btc_price), 2)
        return btc_price_rounded

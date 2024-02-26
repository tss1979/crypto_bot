from config import URL, API_KEY
from utils import keys
import requests
import json


class ConversionException(Exception):
    pass


class ExchConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str ):
        if quote == base:
            raise ConversionException(f'Невозможно паревести одинаковые валюты: {base}')
        quote_ticker, base_ticker = keys.get(quote.lower()), keys.get(base.lower())
        if quote_ticker is None:
            raise ConversionException(f'Не удалось обработать валюту: { quote }')
        if base_ticker is None:
            raise ConversionException(f'Не удалось обработать валюту: { base }')
        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать { amount }')
        query = URL + f'to={ base_ticker }&from={ quote_ticker }&amount={ amount }&apikey={ API_KEY }'
        r = requests.get(query)
        total_base = json.loads(r.content).get('result')
        return total_base
    
import requests
from dataclasses import dataclass
import json
import os
from datetime import datetime

# class Price:
#     def __init__(self, value: int, currency: str):
#         self.value = value
#         self.currency = currency

# EXCHANGE_RATES = {
#     "chf": {
#         "chf": 1,
#         "usd": 0.9,
#         "uah": 0.02,
#     },
#     "usd": {
#         "chf": 1.1,
#         "uah": 0.3,
#     },
#     "uah": {
#         "chf": 3,
#         "usd": 38,
#     },
# }

ALPHAVANTAGE_API_KEY = "SAL0OR37YA2EZC2O"
MIDDLE_CURRENCY = "CHF"
LOG = "logs.json"


@dataclass
class Price:
    value: float
    currency: str



class Exenge_service(Price):
    
    def __add__(first: Price, other: "Price"):
        if first.currency == other.currency:
            return Price(
                value=(first.value + other.value), currency=first.currency
            )

        left_in_middle: float = convert(
            value=first.value,
            currency_from=first.currency,
            currency_to=MIDDLE_CURRENCY,
        )
        right_in_middle: float = convert(
            value=other.value,
            currency_from=other.currency,
            currency_to=MIDDLE_CURRENCY,
        )

        total_in_middle: float = left_in_middle + right_in_middle
        total_in_left_currency: float = convert(
            value=total_in_middle,
            currency_from=MIDDLE_CURRENCY,
            currency_to=first.currency,
        )
        
        return Exenge_service(value=total_in_left_currency, currency=first.currency)
    
def add_log(file_path, currency_from, currency_to, rate):
    timestamp = datetime.now().isoformat()

        # Создание нового объекта для записи
    new_entry = {
            "currency_from": currency_from,
            "currency_to": currency_to,
            "rate": rate,
            "timestamp": timestamp,
                 }

    try:
         # Попытка чтения существующего файла
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Добавление новой записи в массив 'results'
            data['results'].append(new_entry)

        # Перезапись файла с обновленными данными
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

            print(f"Новая запись добавлена в лог: {new_entry}")

    except FileNotFoundError:
        # Если файл не существует, создаем новый
        with open(file_path, 'w') as file:
            data = {'results': [new_entry]}
            json.dump(data, file, indent=2)

        print(f"Файл лога создан, новая запись добавлена: {new_entry}")
    except Exception as e:
        print(f"Произошла ошибка при добавлении записи в лог: {e}")

def convert(value: float, currency_from: str, currency_to: str) -> float:
    response: requests.Response = requests.get(
        f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_from}&to_currency={currency_to}&apikey={ALPHAVANTAGE_API_KEY}"
    )
    result: dict = response.json()
    # Response example
    # {
    #     "Realtime Currency Exchange Rate": {
    #         "1. From_Currency Code": "UAH",
    #         "2. From_Currency Name": "Ukrainian Hryvnia",
    #         "3. To_Currency Code": "USD",
    #         "4. To_Currency Name": "United States Dollar",
    #         "5. Exchange Rate": "0.02648000",
    #         "6. Last Refreshed": "2024-02-12 19:04:02",
    #         "7. Time Zone": "UTC",
    #         "8. Bid Price": "0.02647900",
    #         "9. Ask Price": "0.02648000"
    #     }
    # }
    print(result)
    coefficient: float = float(
        result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    )
    add_log(LOG, currency_from, currency_to, coefficient)

    return value * coefficient


flight = Exenge_service(value=200, currency="USD")
hotel = Exenge_service(value=1000, currency="UAH")

total: Exenge_service = flight + hotel
print(total)
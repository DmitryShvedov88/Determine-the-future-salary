import requests


params = {
    "text": "программист",
    "date_from": "2023-10-15"
     }
response = requests.get('https://api.hh.ru/vacancies/',  params=params)
print(response.raise_for_status())
print(response.status_code)
print(response.text)

languages = {}

import requests

languages = ["Python", "Java", "Javascript"]
languages_vatations = {}

for language in languages:
    params = {
        "text": language,
        "date_from": "2023-10-15"
        }
    response = requests.get('https://api.hh.ru/vacancies/',  params=params)
    response.raise_for_status()
    print(response.status_code)
    language_info = response.json()
    count = language_info["found"]
    languages_vatations[language] = count
print(languages_vatations)

import requests
# находим колличество вакансий на определенном языке
# languages = ["Python", "Java", "Javascript", "C", "C#", "F#", "Ruby", "Go", "Golang"]
# languages_vacations = {}

# for language in languages:
#     params = {
#         "text": language,
#         "date_from": "2023-10-15"
#         }
#     response = requests.get('https://api.hh.ru/vacancies/',  params=params)
#     response.raise_for_status()
#     language_info = response.json()
#     count = language_info["found"]
#     languages_vacations[language] = count
# print(languages_vacations)
# выводим зарплату из вакансий
language = "Python"
params = {
    "text": language,
    "date_from": "2023-10-15"  
    }
response = requests.get('https://api.hh.ru/vacancies/',  params=params)
response.raise_for_status()
language_info = response.json()
vacations = language_info["items"]
for vacation in vacations:
    print(vacation["salary"])

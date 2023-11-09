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
def predict_rub_salary(salary):
    if salary == None:
        print("None")
    else:
        if str(salary["currency"]) == "RUR":
            if salary["from"] == None:
                mid = int(salary["to"])*0.8
                print(mid)
            elif salary["to"] == None:
                mid = int(salary["from"])*1.2
                print(mid)       
            else:
                mid = (int(salary["from"]) + int(salary["to"]))/2
                print(mid)
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
    salary = vacation["salary"]
    predict_rub_salary(salary)

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
# def predict_rub_salary(salary):
#     if salary == None:
#         print("None")
#     else:
#         if str(salary["currency"]) == "RUR":
#             if salary["from"] == None:
#                 mid = int(salary["to"])*0.8
#                 print(mid)
#             elif salary["to"] == None:
#                 mid = int(salary["from"])*1.2
#                 print(mid)       
#             else:
#                 mid = (int(salary["from"]) + int(salary["to"]))/2
#                 print(mid)
# language = "Python"
# params = {
#     "text": language,
#     "date_from": "2023-10-15"  
#     }
# response = requests.get('https://api.hh.ru/vacancies/',  params=params)
# response.raise_for_status()
# language_info = response.json()
# vacations = language_info["items"]
# for vacation in vacations:
#     salary = vacation["salary"]
#     predict_rub_salary(salary)
#
# находим количество вакансий по языка, среднюю запрлату и кол вакансий из которых считали среднюю 


def predict_rub_salary(salary):
    if str(salary["currency"]) == "RUR":
        if salary["from"] == None:
            midlle = int(salary["to"])*0.8
        elif salary["to"] == None:
            midlle = int(salary["from"])*1.2
        else:
            midlle = (int(salary["from"]) + int(salary["to"]))/2
        return midlle 


languages = ["Python", "Java", "Javascript", "C", "C#", "F#", "Ruby", "Go", "Golang"]
languages_vacations = {}

for language in languages:
    page = 0
    pages_number = 1
    while page < 2:
        params = {
            "text": language,
            }
        response = requests.get('https://api.hh.ru/vacancies/',  params=params)
        response.raise_for_status()
        language_info = response.json() 
        pages_number = language_info['pages']
        page += 1
        print(page)
        count = language_info["found"]
        languages_vacations[language] = {"vacancies_found": count}
        vacations = language_info["items"]
        mid_summ = 0
        vacancies_processed = 0
        for vacation in vacations:
            salary = vacation["salary"]
            if salary:
                mid = predict_rub_salary(salary)
                if mid:
                    mid_summ += mid
                    vacancies_processed += 1
        languages_vacations[language]["vacancies_processed"] = vacancies_processed
        average_salary = mid_summ/vacancies_processed
        languages_vacations[language]["average_salary"] = average_salary
    print(languages_vacations)

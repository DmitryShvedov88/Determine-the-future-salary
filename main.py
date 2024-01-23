import requests
import os
from dotenv import load_dotenv, find_dotenv
#находим колличество вакансий на определенном языке
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
# response = requests.get('https://api.hh.ru/vacancies/',  params=params)
# response.raise_for_status()
# language_info = response.json()
# vacations = language_info["items"]
# for vacation in vacations:
#     salary = vacation["salary"]
#     predict_rub_salary(salary)
#
# находим количество вакансий по языка, среднюю запрлату и кол вакансий из которых считали среднюю 


def predict_rub_salary(salary_from, salary_to):
        if salary_from == None:
            midlle = int(salary_to)*0.8
        elif salary_to == None:
            midlle = int(salary_from)*1.2
        else:
            midlle = (int(salary_from) + int(salary_to))/2
        if midlle == 0:
            return None
        return midlle


# languages = ["Python", "Java", "Javascript", "C", "C#", "F#", "Ruby", "Go", "Golang"]
# languages_vacations = {}

# for language in languages:
#     page = 0
#     pages_number = 1
#     while page < 2:
#         params = {
#             "text": language,
#             }
#         response = requests.get('https://api.hh.ru/vacancies/',  params=params)
#         response.raise_for_status()
#         language_info = response.json()
#         pages_number = language_info['pages']
#         page += 1
#         count = language_info["found"]
#         languages_vacations[language] = {"vacancies_found": count}
#         vacations = language_info["items"]
#         mid_summ = 0
#         vacancies_processed = 0
#         for vacation in vacations:
#             salary = vacation["salary"]
#             if str(salary["currency"]) == "RUR":
#                 salary_from, salary_to = salary["from"], salary["to"]
#                 mid = predict_rub_salary(salary_from, salary_to)
#                 if mid:
#                     mid_summ += mid
#                     vacancies_processed += 1
#         languages_vacations[language]["vacancies_processed"] = vacancies_processed
#         average_salary = mid_summ/vacancies_processed
#         languages_vacations[language]["average_salary"] = average_salary
# for language in languages_vacations.items():
#     print(language[0], language[1])

#def predict_salary(salary_from, salary_to):
# common prediction logic

#выводим зщарплату по вакансии в НН
#def predict_rub_salary_hh(vacancy):
# return number or None

#Запрос к сайту СуперДжоб
load_dotenv(find_dotenv())


def predict_rub_salary_sj(vacation, mid_summ, vacancies_processed):
    print("id:", vacation["id"])
    payment_from, payment_to = vacation["payment_from"], vacation["payment_to"]
    print(payment_from, payment_to)
    mid = predict_rub_salary(payment_from, payment_to)
    if mid:
        mid_summ += mid
        vacancies_processed += 1
        print("mid_summ_2:", mid_summ, "vacancies_processed_2:", vacancies_processed)




languages = ["Python", "Си", "SQL"]
#["Python", "Java", "Javascript", "C", "C#", "F#", "Ruby", "Go", "Golang", "SQL"]
languages_vacations = {}

for language in languages:
    vacation_number = 0
    vacations_number = 1
    headers = {"X-Api-App-Id": os.getenv("superjob_key")}
    params = {"keyword": f"{language}", "town": "Москва"}
    response = requests.get('https://api.superjob.ru/2.0/vacancies/',  headers=headers, params=params)
    response.raise_for_status()
    vacations_info = response.json()
    count = vacations_info["total"]
    vacations = vacations_info["objects"]
    count = vacations_info["total"]
    print(language)
    languages_vacations[language] = {"vacancies_found": count}
    mid_summ = 0
    vacancies_processed = 0
    for vacation in vacations: 
        vacation_number += 1
        predict_rub_salary_sj(vacation, mid_summ, vacancies_processed)
    # languages_vacations[language]["vacancies_processed"] = vacancies_processed
    # average_salary = mid_summ/vacancies_processed
    # languages_vacations[language]["average_salary"] = average_salary

for language in languages_vacations.items():
    print(language[0], language[1])

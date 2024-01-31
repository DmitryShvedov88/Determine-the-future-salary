import requests
import os
from dotenv import load_dotenv, find_dotenv
from terminaltables import AsciiTable
load_dotenv(find_dotenv())


languages = ["Python", "Си", "SQL"]
languages_vacations = {}


def made_table(title, languages_vacations):
    data = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for language in languages_vacations.items():
        language_data = []
        language_data.append(language[0])
        for key, value in language[1].items():
            language_data.append(value)
        data.append(language_data)
    table = AsciiTable(data, title)
    print(table.table)


# находим количество вакансий по языка, среднюю зарплату и кол вакансий из которых считали среднюю
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


# Запрос к сайту НН
def take_hh_vacations():
    for language in languages:
        page = 0
        while page < 2:
            params = {
                "text": language,
                }
            response = requests.get('https://api.hh.ru/vacancies/',  params=params)
            response.raise_for_status()
            language_info = response.json()
            page += 1
            count = language_info["found"]
            languages_vacations[language] = {"vacancies_found": count}
            vacations = language_info["items"]
            mid_summ = 0
            vacancies_processed = 0
            for vacation in vacations:
                salary = vacation["salary"]
                if salary:
                    if str(salary["currency"]) == "RUR":
                        salary_from, salary_to = salary["from"], salary["to"]
                        mid = predict_rub_salary(salary_from, salary_to)
                        if mid:
                            mid_summ += mid
                            vacancies_processed += 1
            languages_vacations[language]["vacancies_processed"] = vacancies_processed
            average_salary = int((mid_summ/vacancies_processed)//1)
            languages_vacations[language]["average_salary"] = average_salary
    title = "HeadHunter Moscow"
    made_table(title, languages_vacations)

# Запрос к сайту СуперДжоб

def take_sj_vacations():
    for language in languages:
        vacation_number = 0
        headers = {"X-Api-App-Id": os.getenv("SUPERJOB_KEY")}
        params = {"keyword": f"{language}", "town": "Москва"}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',  headers=headers, params=params)
        response.raise_for_status()
        vacations_info = response.json()
        count = vacations_info["total"]
        vacations = vacations_info["objects"]
        count = vacations_info["total"]
        languages_vacations[language] = {"vacancies_found": count}
        mid_summ = 0
        vacancies_processed = 0
        for vacation in vacations:
            vacation_number += 1
            payment_from, payment_to = vacation["payment_from"], vacation["payment_to"]
            mid = predict_rub_salary(payment_from, payment_to)
            if mid:
                mid_summ += mid
                vacancies_processed += 1
        languages_vacations[language]["vacancies_processed"] = vacancies_processed
        average_salary = int((mid_summ/vacancies_processed)//1)
        languages_vacations[language]["average_salary"] = average_salary
    title = "SuperJob Moscow"
    made_table(title, languages_vacations)


if __name__ == "__main__":
    take_hh_vacations()
    take_sj_vacations()

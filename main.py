import requests
import os
import time
from dotenv import load_dotenv, find_dotenv
from terminaltables import AsciiTable


LANGUAGES = [
    "Python",
    "Си",
    "SQL"
    ]


def fill_table(vacation_table, title, languages_vacations):
    for language in languages_vacations:
        vacation_table.append(
            [
                language,
                languages_vacations[language]["vacancies_found"],
                languages_vacations[language]["vacancies_processed"],
                languages_vacations[language]["average_salary"]
            ]
        )
    vacation_table = AsciiTable(vacation_table, title)
    return vacation_table


def made_table():
    """Make a table and display it on the screen"""
    table = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]
    return table


def predict_rub_salary(salary_from, salary_to):
    """Find the number of vacancies by language,
    the average salary and the number of vacancies
    of which we considered the average"""

    if salary_to and not salary_from:
        midlle = int(salary_to)*0.8
    elif salary_from and not salary_to:
        midlle = int(salary_from)*1.2
    else:
        midlle = (int(salary_from) + int(salary_to))/2
    if midlle == 0:
        return None
    return midlle


def take_hh_vacations():
    """Request to the hh.ru website"""

    languages_vacations = {}
    for language in LANGUAGES:
        pages_number = 1
        days = 1
        page = 0
        while page < pages_number:
            params = {
                "text": language,
                "period": days,
                }
            try:
                response = requests.get('https://api.hh.ru/vacancies/',  params=params)
                response.raise_for_status()
                page_payload = response.json()
                pages_number = page_payload["pages"]
                page += 1
                count = page_payload["found"]
                vacations = page_payload["items"]
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
                                time.sleep(0.1)
            except requests.exceptions.HTTPError:
                time.sleep(1)
            if vacancies_processed == 0:
                average_salary = 0
            else:
                average_salary = int((mid_summ/vacancies_processed)//1)
            languages_vacations[language] = {
                "vacancies_found": count,
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
                }
    title = "HeadHunter Moscow"
    table = made_table()
    vacation_table = fill_table(table, title, languages_vacations)
    print(vacation_table.table)


def take_sj_vacations(headers):
    """Request to the Superjob website"""

    languages_vacations = {}
    for language in LANGUAGES:
        vacation_counter = 0
        params = {"keyword": f"{language}", "town": "Москва"}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',  headers=headers, params=params)
        response.raise_for_status()
        page_payload = response.json()
        count = page_payload["total"]
        vacations = page_payload["objects"]
        count = page_payload["total"]
        mid_summ = 0
        vacancies_processed = 0
        for vacation in vacations:
            vacation_counter += 1
            payment_from, payment_to = vacation["payment_from"], vacation["payment_to"]
            mid = predict_rub_salary(payment_from, payment_to)
            if mid:
                mid_summ += mid
                vacancies_processed += 1
        if vacancies_processed == 0:
            average_salary = 0
        else:
            average_salary = int((mid_summ/vacancies_processed)//1)
        languages_vacations[language] = {
                "vacancies_found": count,
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
                }
    title = "SuperJob Moscow"
    table = made_table()
    vacation_table = fill_table(table, title, languages_vacations)
    print(vacation_table.table)

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    headers = {"X-Api-App-Id": os.getenv("SUPERJOB_KEY")}
    take_hh_vacations()
    take_sj_vacations(headers)

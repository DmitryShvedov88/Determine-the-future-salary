import os
import time
import requests
from dotenv import load_dotenv, find_dotenv
from terminaltables import AsciiTable


LANGUAGES = [
    "Python",
    "Си",
    "SQL"
]


def made_table(title, languages_vacancies):
    """Make a table and display it on the screen"""
    table = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]
    for language in languages_vacancies:
        table.append(
            [
                language,
                languages_vacancies[language]["vacancies_found"],
                languages_vacancies[language]["vacancies_processed"],
                languages_vacancies[language]["average_salary"]
            ]
        )
    vacancy_table = AsciiTable(table, title)
    return vacancy_table


def predict_salary(salary_from, salary_to):
    """Find the number of vacancies by language,
    the average salary and the number of vacancies
    of which we considered the average"""

    if salary_to and not salary_from:
        midlle = int(salary_to) * 0.8
    elif salary_from and not salary_to:
        midlle = int(salary_from) * 1.2
    else:
        midlle = (int(salary_from) + int(salary_to)) / 2
    if midlle == 0:
        return None
    return midlle


def predict_rub_salary(salary):
    if not salary:
        return None
    if str(salary["currency"]) != "RUR":
        return None
    if str(salary["currency"]) == "RUR":
        midlle = predict_salary(salary["from"], salary["to"])
        return midlle


def take_hh_vacancies():
    """Request to the hh.ru website"""

    languages_vacancies = {}
    for language in LANGUAGES:
        pages_number = 1
        days = 5
        page = 0
        while page < pages_number:
            params = {
                "text": language,
                "period": days,
            }
            try:
                response = requests.get(
                    'https://api.hh.ru/vacancies/',
                    params=params,
                    timeout=5
                )
                response.raise_for_status()
                page_payload = response.json()
            except requests.exceptions.HTTPError:
                time.sleep(1)
            pages_number = page_payload["pages"]
            page += 1
            count = page_payload["found"]
            vacancies = page_payload["items"]
            mid_summ = 0
            vacancies_processed = 0
            for vacation in vacancies:
                salary = vacation["salary"]
                mid = predict_rub_salary(salary)
                if mid:
                    mid_summ += mid
                    vacancies_processed += 1
                time.sleep(0.1)
            if not vacancies_processed:
                average_salary = 0
            else:
                average_salary = int((mid_summ / vacancies_processed) // 1)
            languages_vacancies[language] = {
                "vacancies_found": count,
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
            }
    return languages_vacancies


def take_sj_vacancies(headers):
    """Request to the Superjob website"""
    languages_vacancies = {}
    vacancies_on_page = 25
    for language in LANGUAGES:
        pages_number = 1
        page = 0
        while page < pages_number:
            vacancy_counter = 0
            params = {
                "keyword": f"{language}",
                "town": "Москва",
                "count": vacancies_on_page
            }
            response = requests.get(
                'https://api.superjob.ru/2.0/vacancies/',
                headers=headers,
                params=params,
                timeout=5
            )
            response.raise_for_status()
            page_payload = response.json()
            vacancies = page_payload["objects"]
            count = page_payload["total"]
            mid_summ = 0
            vacancies_processed = 0
            pages_number = page_payload["total"] // vacancies_on_page
            page += 1
            for vacancy in vacancies:
                vacancy_counter += 1
                payment_from = vacancy["payment_from"]
                payment_to = vacancy["payment_to"]
                mid = predict_salary(payment_from, payment_to)
                if mid:
                    mid_summ += mid
                    vacancies_processed += 1
            if not vacancies_processed:
                average_salary = 0
            else:
                average_salary = int((mid_summ / vacancies_processed) // 1)
            languages_vacancies[language] = {
                "vacancies_found": count,
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
            }
    return languages_vacancies


def print_hh_vacancies():
    languages_vacancies = take_hh_vacancies()
    title = "HeadHunter Moscow"
    vacancy_table = made_table(title, languages_vacancies)
    print(vacancy_table.table)


def print_sj_vacancies(headers):
    languages_vacancies = take_sj_vacancies(headers)
    title = "SuperJob Moscow"
    vacancy_table = made_table(title, languages_vacancies)
    print(vacancy_table.table)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    headers = {"X-Api-App-Id": os.getenv("SUPERJOB_KEY")}
    print_hh_vacancies()
    print_sj_vacancies(headers)

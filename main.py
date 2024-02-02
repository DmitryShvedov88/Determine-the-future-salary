import requests
import os
from dotenv import load_dotenv, find_dotenv
from terminaltables import AsciiTable


LANGUAGES = [
    "Python",
    "Си",
    "SQL"
    ]
languages_vacations = {}


def made_table(title, languages_vacations):
    """Make a table and display it on the screen"""
    table_header = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]
    for language in languages_vacations.items():
        table_rows = []
        table_rows.append(language[0])
        for key, value in language[1].items():
            table_rows.append(value)
        table_header.append(table_rows)
    table = AsciiTable(table_header, title)
    print(table.table)


def predict_rub_salary(salary_from, salary_to):
    """Find the number of vacancies by language,
    the average salary and the number of vacancies
    of which we considered the average"""

    if salary_from == None:
        midlle = int(salary_to)*0.8
    elif salary_to == None:
        midlle = int(salary_from)*1.2
    else:
        midlle = (int(salary_from) + int(salary_to))/2
    if midlle == 0:
        return None
    return midlle


def take_hh_vacations():
    """Request to the hh.ru website"""

    for language in LANGUAGES:
        page = 0
        while page < 2:
            params = {
                "text": language,
                }
            response = requests.get('https://api.hh.ru/vacancies/',  params=params)
            response.raise_for_status()
            page_payload = response.json()
            page += 1
            count = page_payload["found"]
            languages_vacations[language] = {"vacancies_found": count}
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
            languages_vacations[language]["vacancies_processed"] = vacancies_processed
            average_salary = int((mid_summ/vacancies_processed)//1)
            languages_vacations[language]["average_salary"] = average_salary
    title = "HeadHunter Moscow"
    made_table(title, languages_vacations)


def take_sj_vacations():
    """Request to the Superjob website"""

    for language in LANGUAGES:
        vacation_counter = 0
        headers = {"X-Api-App-Id": os.getenv("SUPERJOB_KEY")}
        params = {"keyword": f"{language}", "town": "Москва"}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',  headers=headers, params=params)
        response.raise_for_status()
        page_payload = response.json()
        count = page_payload["total"]
        vacations = page_payload["objects"]
        count = page_payload["total"]
        languages_vacations[language] = {"vacancies_found": count}
        mid_summ = 0
        vacancies_processed = 0
        for vacation in vacations:
            vacation_counter += 1
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
    load_dotenv(find_dotenv())
    take_hh_vacations()
    take_sj_vacations()

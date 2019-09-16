import requests
from itertools import count


def unload_vacancies_hh(language):
    all_pages = []
    url = 'https://api.hh.ru/vacancies/'
    for page in count():
        params = {
            'text' : f'(программист OR разработчик) AND {language}',
            'area' : '1',
            'page' : page,
            'per_page' : '100',
            'period' : '30',
            'only_with_salary' : 'true'
        }
        response = requests.get(url, params=params)
        vacancy_page = response.json()
        all_pages += vacancy_page['items']
        if page >= vacancy_page['pages']:
            all_pages.append(vacancy_page['found'])
            break
    found = response.json()['found']
    return [all_pages, found]


def get_salary_RUR_hh(vacancies):
    salary = 0
    non_RUR = 0
    for payment in vacancies:
        try:
            if payment['salary']['currency'] == 'RUR':
                if payment['salary']['to'] and payment['salary']['from']:
                    salary += (payment['salary']['to'] + payment['salary']['from'])/2
                elif not payment['salary']['to']:
                    salary += payment['salary']['from'] * 1.2
                elif not payment['salary']['from']:
                    salary += payment['salary']['to'] * 0.8 
            if not payment['salary']['currency'] == 'RUR':
                non_RUR += 1
        except TypeError:
            pass
    return [salary, non_RUR]


def get_hh_base():
    payment_list = ['C++', 'Python', 'Java', 'Ruby', 'C', 'C#', 'JavaScript', 'PHP', 'Typescript', 'Objective-C', 'Scala', 'Swift', 'Go']
    language_base = {}
    for language in payment_list:
        vacancies = unload_vacancies_hh(language)
        salary_and_processed = get_salary_RUR_hh(vacancies[0])
        try:
            processed = vacancies[1] - salary_and_processed[1]
        except ZeroDivisionError:
            processed = vacancies[1]
        language_base.update(
            {language : {
                'vacancies_found' :  vacancies[1],
                'vacancies_processed' : processed,
                'vacancies_salary' : int(salary_and_processed[0] / processed)
                }
            }
        )
        print(f'{language} is done')
    return language_base


if __name__ == "__main__":
    get_hh_base()
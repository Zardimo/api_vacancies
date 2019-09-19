import requests
from itertools import count


def job_unloading_hh(language):
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


def summ_salary(salary_to, salary_from):
    if salary_to and salary_from:
        salary = (salary_to + salary_from)/2
    elif not salary_to:
        salary = salary_from * 1.2
    elif not salary_from:
        salary = salary_to * 0.8
    return salary



def get_salary(vacancies, site):
    salary = 0
    rur = 0
    for vacancy in vacancies:
        if site == 'hh':
            try:
                if vacancy['salary']['currency'] == 'RUR':
                    rur += 1
                    salary += summ_salary(
                        vacancy['salary']['to'], vacancy['salary']['from'])
            except TypeError:
                pass
        else:
            if vacancy['currency'] == 'rub': 
                rur += 1
                salary += summ_salary(
                    vacancy['payment_to'], vacancy['payment_from'])
    return [salary, rur]


def main(site):
    languages = ['C++', 'Python', 'Java', 'Ruby', 'C', 'C#', 'JavaScript',
        'PHP', 'Typescript', 'Objective-C', 'Scala', 'Swift', 'Go']
    data_on_languages_for_table_sj = {}
    for language in languages:
        vacancies, found_vacancies = job_unloading_hh(language)
        salary, processed = get_salary(vacancies, site)
        data_on_languages_for_table_sj.update(
            {language : {
                'vacancies_found' :  found_vacancies,
                'vacancies_processed' : processed,
                'vacancies_salary' : int(salary / processed)
                }
            }
        )
        print(f'{language} is done')
    return data_on_languages_for_table_sj


if __name__ == "__main__":
    main('hh')
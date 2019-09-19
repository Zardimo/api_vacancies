import requests
import os
from api_vacancies_hh import get_salary


def job_unloading_sj(language):
    key_sj = os.getenv('SECRET_TOKEN_SJ')
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id' : key_sj
    }
    params = {
        'page' : '0',
        'count' : '100',
        'keyword' : f'Программист {language}',
        'town' : '4',
        'no_agreement' : '1'
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def main(site):
    languages = ['C++', 'Python', 'Java', 'Ruby', 'C', 'C#', 'JavaScript',
        'PHP', 'Typescript', 'Objective-C', 'Scala', 'Swift', 'Go']
    data_on_languages_for_table_sj = {}
    for language in languages:
        vacancies_base = job_unloading_sj(language)
        if vacancies_base['total'] > 0:
            salary_vacancies, processed = get_salary(
                vacancies_base['objects'], site)
            salary = int(salary_vacancies / processed)
        else:
            processed = salary = 0
        data_on_languages_for_table_sj.update(
        {language : {
            'vacancies_found' : vacancies_base['total'],
            'vacancies_processed' : processed,
            'vacancies_salary' : salary
            }
        })
    return data_on_languages_for_table_sj


if __name__ == '__main__':
    main()
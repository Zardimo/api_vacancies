import requests
import os


def unload_vacancies_sj(language):
    key_sj = os.getenv('TOKEN')
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


def get_salary_RUB_sj(vacancies):
    salary = 0
    non_rub = 0
    for payment in vacancies:
        if payment['paymentrency'] == 'rub': 
            if payment['payment_from'] and payment['payment_to']:
                salary += payment['payment_from'] + payment['payment_to'] / 2
            if not payment['payment_to']:
                salary += payment['payment_from'] * 1.2
            if not payment['payment_from']:
                salary += payment['payment_to'] * 0.8
        else:
            non_rub += 1
    return [salary, non_rub]


def get_sj_base():
    language_list = ['C++', 'Python', 'Java', 'Ruby', 'C', 'C#', 'JavaScript', 'PHP', 'Typescript', 'Objective-C', 'Scala', 'Swift', 'Go']
    language_base = {}
    for language in language_list:
        vacancies_base = unload_vacancies_sj(language)
        if vacancies_base['total'] > 0:
            try:
                processed = vacancies_base['total'] - get_salary_RUB_sj(vacancies_base['objects'])[1]
            except ZeroDivisionError:
                processed = vacancies_base['total']
            salary = int(get_salary_RUB_sj(vacancies_base['objects'])[0] / processed)
        else:
            processed = salary = 0
        language_base.update(
        {language : {
            'vacancies_found' : vacancies_base['total'],
            'vacancies_processed' : processed,
            'vacancies_salary' : salary
            }
        })
    return language_base


if __name__ == '__main__':
    get_sj_base()
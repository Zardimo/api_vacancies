import requests
import os


def vacancies_sj(language):
    secret_key = os.getenv('SECRET_KEY')
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id' : secret_key
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
    for cur in vacancies:
        if cur['currency'] == 'rub': 
            if cur['payment_from'] and cur['payment_to']:
                salary += cur['payment_from'] + cur['payment_to'] / 2
            if not cur['payment_to']:
                salary += cur['payment_from'] * 1.2
            if not cur['payment_from']:
                salary += cur['payment_to'] * 0.8
        else:
            non_rub += 1
    return [salary, non_rub]


def sj_data():
    lang_list = ['C++', 'Python', 'Java', 'Ruby', 'C', 'C#', 'JavaScript', 'PHP', 'Typescript', 'Objective-C', 'Scala', 'Swift', 'Go']
    lang_stat = {}
    for vac in lang_list:
        vacancies_lib = vacancies_sj(vac)
        if vacancies_lib['total'] > 0:
            try:
                vacancies_proc = vacancies_lib['total'] - get_salary_RUB_sj(vacancies_lib['objects'])[1]
            except ZeroDivisionError:
                vacancies_proc = vacancies_lib['total']
            vacancies_sal = int(get_salary_RUB_sj(vacancies_lib['objects'])[0] / vacancies_proc)
        else:
            vacancies_proc = vacancies_sal = 0
        lang_stat.update(
        {vac : {
            'vacancies_found' : vacancies_lib['total'],
            'vacancies_processed' : vacancies_proc,
            'vacancies_salary' : vacancies_sal
            }
        })
    return lang_stat


if __name__ == '__main__':
    sj_data()
import requests
from itertools import count


def found_vacancies(language):
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
        page_vac = response.json()
        all_pages += page_vac['items']
        if page >= page_vac['pages']:
            all_pages.append(page_vac['found'])
            break
    found = response.json()['found']
    return [all_pages, found]


def get_salary_RUR_hh(vacancies):
    salary = 0
    non_RUR = 0
    for lang in vacancies:
        try:
            if lang['salary']['currency'] == 'RUR':
                if lang['salary']['to'] and lang['salary']['from']:
                    salary += (lang['salary']['to'] + lang['salary']['from'])/2
                elif not lang['salary']['to']:
                    salary += lang['salary']['from'] * 1.2
                elif not lang['salary']['from']:
                    salary += lang['salary']['to'] * 0.8 
            if not lang['salary']['currency'] == 'RUR':
                non_RUR += 1
        except TypeError:
            pass
    return [salary, non_RUR]


def hh_data():
    lang_list = ['C++', 'Python', 'Java', 'Ruby', 'C', 'C#', 'JavaScript', 'PHP', 'Typescript', 'Objective-C', 'Scala', 'Swift', 'Go']
    lang_stat = {}
    for language in lang_list:
        vacancies = found_vacancies(language)
        salary_and_processed = get_salary_RUR_hh(vacancies[0])
        try:
            vac_proc = vacancies[1] - salary_and_processed[1]
        except ZeroDivisionError:
            vac_proc = vac_found
        lang_stat.update(
            {language : {
                'vacancies_found' :  vacancies[1],
                'vacancies_processed' : vac_proc,
                'vacancies_salary' : int(salary_and_processed[0] / vac_proc)
                }
            }
        )
        print(f'{language} is done')
    return lang_stat


if __name__ == "__main__":
    hh_data()
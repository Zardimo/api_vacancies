from terminaltables import AsciiTable, DoubleTable, SingleTable
from api_vacancies_hh import get_hh_base
from api_vacancies_sj import get_sj_base
import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description='This program takes information about the vacancies of related programming languages ​​from sites (HeadHunter and SuperJob) and displays it in a table. \n Type "-sj" or "-hh" to choise'
        )
    parser.add_argument('-hh', '--HeadHunter', action='store_true')
    parser.add_argument('-sj', '--SuperJob', action='store_true')
    return parser


def main(table_data, title):
    table_instance = SingleTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)


def prepare_data_for_the_table(data):
    table_data = ()
    table_data += ('Язык Программирования', 'Ваканский найдено', 'Вакансий обработано', 'Средняя зарплата'),
    for lang_data in data:
        table_data += (lang_data, data[lang_data]['vacancies_found'], data[lang_data]['vacancies_processed'], data[lang_data]['vacancies_salary']),
    return table_data


if __name__ == '__main__':
    parser = create_parser()
    args_namespace = parser.parse_args()
    if args_namespace.HeadHunter:
        main(prepare_data_for_the_table(get_hh_base('hh')), 'HeadHunter Moscow')
    elif args_namespace.SuperJob:
        main(prepare_data_for_the_table(get_sj_base('sj')), 'SuperJob Moscow')
    else:
        print('Select job search site(-sj, -hh)')
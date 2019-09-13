from terminaltables import AsciiTable, DoubleTable, SingleTable
from api_vacancies_hh import hh_data
from api_vacancies_sj import sj_data
import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description='This program takes information about the vacancies of related programming languages ​​from sites (HeadHunter and SuperJob) and displays it in a table. \n Type "-sj" or "-hh" to choise'
        )
    parser.add_argument('-hh', '--HeadHunter', action='store_true')
    parser.add_argument('-sj', '--SuperJob', action='store_true')
    return parser


def main(TABLE_DATA, title):
    table_instance = SingleTable(TABLE_DATA, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)


def creating_table_data(data):
    TABLE_DATA = ()
    TABLE_DATA += ('Язык Программирования', 'Ваканский найдено', 'Вакансий обработано', 'Средняя зарплата'),
    for lang_data in data:
        TABLE_DATA += (lang_data, data[lang_data]['vacancies_found'], data[lang_data]['vacancies_processed'], data[lang_data]['vacancies_salary']),
    return TABLE_DATA


if __name__ == '__main__':
    parser = create_parser()
    args_namespace = parser.parse_args()
    if args_namespace.HeadHunter:
        main(creating_table_data(hh_data()), 'HeadHunter Moscow')
    elif args_namespace.SuperJob:
        main(creating_table_data(sj_data()), 'SuperJob Moscow')
    else:
        print('Select job search site(-sj, -hh)')
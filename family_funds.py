import datetime
import json
import uuid
from constants import COMMANDS


def get_default_data():
    user_dict = {
	    'expenses' : [],
	    'categories' : ['разное'],
	    'is_app_configured' : False,
        'utc_offset' : 3,
    }
    return user_dict


def save_user_data(data_dict, user_id):
    with open(f'{user_id}.json', 'w') as json_handler:
        json.dump(data_dict, json_handler)


def load_user_data(user_id):
    try:
        with open(f'{user_id}.json', 'r', encoding='utf-8') as json_handler:
            data_dict = json.load(json_handler)
    except OSError:
        data_dict = get_default_data()
    return data_dict


def get_command_descriptions():
    commands_message = ''
    for command in COMMANDS.values():
        commands_message += f'{command}\n'
    return commands_message


def check_expense_string(user_string):
    user_string = user_string.split()
    feedback = 'ok'
    if len(user_string) == 1:
        return f'Вы забыли указать сумму. Примеры правильного ввода:\n"/add 100 мороженка" или "/add 500"'
    try:
        if int(user_string[1]) <= 0:
            feedback = f'Вы указали некорректную сумму. Сумма расхода должна быть больше нуля'
    except ValueError:
        feedback = f'Задана некорректная сумма. Примеры правильного ввода:\n"/add 100 мороженка" или "/add 500"'
    return feedback


def make_expense(user_string):
    sum = user_string.split()[1]
    if len(user_string.split()) == 2:
        description = None
    else:
        description = user_string[(len(sum) + 6):]
    expense = {
        'id' : str(uuid.uuid4()),
        'when' : datetime.datetime.utcnow().strftime('%d.%m.%y, %H:%M'),
        'sum' : sum,
        'category' : 'разное',
        'description' : description,
    }
    return expense


def add_expense(expenses_list, new_expense):
    if expenses_list is None:
        expenses_list = []
    expenses_list.append(new_expense)
    feedback = f"Новая расходная операция на сумму {new_expense['sum']} рублей.\n"
    if new_expense['description'] is not None:
        feedback += f"Комментарий: {new_expense['description']}"
    feedback += f'\n Пожалуйста, выберите категорию расхода:'
    return expenses_list, feedback


def add_category(categories_list, user_string):
    new_category = user_string[8:].lower().strip()
    if categories_list is None:
        categories_list = get_default_data()['categories']
    categories_list.append(new_category)
    feedback = f'Добавлена категория {new_category.capitalize()}'
    return categories_list, feedback


def add_categories(categories_list, user_string):
    feedback = 'Добавлены следующие категории: '
    for category in user_string.split(','):
        if category[0] == '/':
            category = category[9:]
        category = category.lower().strip()
        categories_list.append(category)
        feedback += f'{category.capitalize()}, '
    return categories_list, feedback[:-2]


def show_categories(categories_list):
    if categories_list is None:
        categories_list = get_default_data()['categories']
    report = 'Вам доступны следующие категории расходов:'
    for category in sorted(categories_list):
        report += f'\n • {category.capitalize()}'
    return report


def format_expenses_report(expenses_list, user_id):
    report = ''
    utc_offset = datetime.timedelta(hours=load_user_data(user_id)['utc_offset'])
    for expense in expenses_list:
        when = datetime.datetime.strptime(expense['when'], '%d.%m.%y, %H:%M')
        report += f"• ({(when + utc_offset).strftime('%d.%m.%y, %H:%M')}) ({expense['category'].capitalize()}):  -{expense['sum']} руб. "
        if expense['description'] is not None:
            report += f"\n{expense['description']}"
        report += '\n'
    if report == '':
        report = 'Расходов не найдено. Везет же!'
    else:
        report = 'Cписок ваших расходов:\n' + report
    return report


def find_expense_num_by_id(expenses_list, target_id):
    expense_num = next((num for num, expense in enumerate(expenses_list) if expense['id'] == target_id), None)
    return expense_num
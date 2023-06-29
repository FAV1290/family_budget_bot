import datetime
import uuid
from constants import MISCELLANEOUS_CATEGORY
from data_handlers import filter_user_data, load_data, save_data, find_index_by_id


def check_expense_string(user_input):
    user_input, feedback = user_input.split(), 'ok'
    if len(user_input) == 1:
        return f'Вы забыли указать сумму. Примеры правильного ввода:\n"/add 100 мороженка" или "/add 500"'
    try:
        if int(user_input[1]) <= 0:
            feedback = f'Вы указали некорректную сумму. Сумма расхода должна быть больше нуля'
    except ValueError:
        feedback = f'Задана некорректная сумма. Примеры правильного ввода:\n"/add 100 мороженка" или "/add 500"'
    return feedback


def make_expense(user_id, user_input):
    user_categories = filter_user_data(load_data(), user_id)['categories']
    sum = user_input.split()[1]
    if len(user_input.split()) == 2:
        description = None
    else:
        description = user_input.partition(' ')[2][(len(sum) + 1):]
    if description is not None and description.lower().strip() in user_categories:
        category, description = description.lower().strip(), None
    else:
        category = MISCELLANEOUS_CATEGORY
    expense = {
        'user_id' : user_id,
        'expense_id' : uuid.uuid4(),
        'created_at' : datetime.datetime.utcnow(),
        'sum' : sum,
        'category' : category,
        'description' : description,
    }
    return expense


def get_new_expense_feedback(new_expense):
    feedback = f"Новая расходная операция на сумму {new_expense['sum']} рублей\n"
    if new_expense['description'] is not None:
        feedback += f"Комментарий: {new_expense['description']}\n"
    if new_expense['category'] != MISCELLANEOUS_CATEGORY:
        feedback += f"Расход добавлен в категорию {new_expense['category'].title()}"
    return feedback


def save_new_expense(new_expense):
    data_dict = load_data()
    data_dict['expenses'].append(new_expense)
    save_data(data_dict)


def add_expense(user_id, user_input):
    feedback = check_expense_string(user_input)
    if feedback != 'ok':
        return None, feedback
    new_expense = make_expense(user_id, user_input)
    feedback = get_new_expense_feedback(new_expense)
    save_new_expense(new_expense)
    return new_expense, feedback


def update_expense(updated_expense):
    data_dict = load_data()
    target_index = find_index_by_id(data_dict['expenses'], 'expense_id', updated_expense['expense_id'])
    if target_index is None:
        data_dict['expenses'].append(updated_expense)
    else:
        data_dict['expenses'][target_index] = updated_expense
    save_data(data_dict)


def format_expenses_report(user_id):
    user_data = filter_user_data(load_data(), user_id)
    expenses_list = user_data['expenses']
    report = None
    utc_offset = datetime.timedelta(hours=user_data['settings']['utc_offset'])
    for expense in expenses_list:
        created_at = expense['created_at']
        report = str(report or '') + f"• ({(created_at + utc_offset).strftime('%d.%m.%y, %H:%M')}) ({expense['category'].capitalize()}):  -{expense['sum']} руб. "
        if expense['description'] is not None:
            report += f"\n{expense['description']}"
        report += '\n'
    if report is None:
        report = 'Расходов не найдено. Везет же!'
    else:
        report = 'Cписок ваших расходов:\n' + report
    return report

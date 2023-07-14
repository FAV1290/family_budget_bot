import datetime
import uuid
from constants import MISCELLANEOUS_CATEGORY
from database_handlers import (
save_new_expense, get_user_categories, get_user_expenses, get_user_utc_offset
)


def check_expense_input(user_input):
    user_input, feedback = user_input.split(), 'ok'
    if len(user_input) == 1:
        feedback = ''.join(
            [
                'Вы забыли указать сумму. Примеры правильного ввода:',
                '\n"/add 100 мороженка" или "/add 500"',
            ]
        )
        return feedback 
    try:
        if int(user_input[1]) <= 0:
            feedback = 'Вы указали некорректную сумму. Сумма расхода должна быть больше нуля'
    except ValueError:
        feedback = ''.join(
            [
                'Задана некорректная сумма. Примеры правильного ввода:',
                '\n"/add 100 мороженка" или "/add 500"',
            ]
        )
    return feedback


def make_expense(user_id, user_input):
    user_categories = get_user_categories(user_id)
    amount = user_input.split()[1]
    if len(user_input.split()) == 2:
        description = None
    else:
        description = user_input.partition(' ')[2][(len(amount) + 1):]
    if description is not None and description.lower().strip() in user_categories:
        category, description = description.lower().strip(), None
    else:
        category = MISCELLANEOUS_CATEGORY
    expense = {
        'user_id' : user_id,
        'expense_id' : uuid.uuid4(),
        'created_at' : datetime.datetime.utcnow(),
        'amount' : amount,
        'category' : category,
        'description' : description,
    }
    return expense


def get_new_expense_feedback(new_expense):
    feedback = f"Новая расходная операция на сумму {new_expense['amount']} рублей\n"
    if new_expense['description'] is not None:
        feedback += f"Комментарий: {new_expense['description']}\n"
    if new_expense['category'] != MISCELLANEOUS_CATEGORY:
        feedback += f"Расход добавлен в категорию {new_expense['category'].title()}"
    return feedback


def add_expense(user_id, user_input):
    feedback = check_expense_input(user_input)
    if feedback != 'ok':
        return None, feedback
    new_expense = make_expense(user_id, user_input)
    feedback = get_new_expense_feedback(new_expense)
    save_new_expense(new_expense)
    return new_expense, feedback


def make_expenses_report(user_id):
    expenses_list = get_user_expenses(user_id)
    report = ''
    utc_offset = datetime.timedelta(hours=get_user_utc_offset(user_id))
    for expense in expenses_list:
        formatted_created_at = (expense['created_at'] + utc_offset).strftime('%d.%m.%y, %H:%M')
        formatted_category = expense['category'].capitalize()
        report += f"• ({formatted_created_at}) ({formatted_category}): -{expense['amount']} руб."
        if expense['description'] is not None:
            report += f" ({expense['description'].capitalize()})"
        report += '\n'
    if report == '':
        report = 'Расходов не найдено. Везет же!'
    else:
        report = 'Cписок ваших расходов:\n' + report
    return report

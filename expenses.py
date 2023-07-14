import datetime
import uuid
from constants import MISCELLANEOUS_CATEGORY_NAME
from database_handlers import save_new_expense, get_user_expenses, get_user_settings


def check_expense_input(user_input):
    feedback = 'ok'
    try:
        if int(user_input) <= 0:
            feedback = 'Сумма расхода должна быть больше нуля.'
    except ValueError:
        feedback = ''.join(
            [
                'Задана некорректная сумма. Примеры правильного ввода:',
                '\n"/add 100 мороженка" или "/add 500".',
            ]
        )
    return feedback


def make_expense_dict(user_id, user_input):
    amount = int(user_input)
    expense = {
        'user_id' : user_id,
        'expense_id' : uuid.uuid4(),
        'created_at' : datetime.datetime.utcnow(),
        'amount' : amount,
        'category' : MISCELLANEOUS_CATEGORY_NAME,
        'description' : None,
    }
    return expense


def add_expense(user_id, user_input):
    feedback = check_expense_input(user_input)
    if feedback != 'ok':
        return None, feedback
    new_expense = make_expense_dict(user_id, user_input)
    save_new_expense(new_expense)
    return new_expense, feedback


def make_expenses_report(user_id):
    expenses_list = get_user_expenses(user_id)
    report = ''
    utc_offset = datetime.timedelta(hours=get_user_settings(user_id)['utc_offset'])
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

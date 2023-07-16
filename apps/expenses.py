import datetime
import uuid
from constants import MISCELLANEOUS_CATEGORY_NAME
from db.database_models import Expense
from db.expenses import save_new_expense, get_user_expenses
from db.settings import get_user_settings
from apps.incomes import get_incomes_sum


def check_expense_amount(user_input):
    feedback = 'ok'
    try:
        if int(user_input) <= 0:
            feedback = 'Значение должно быть больше нуля.'
    except ValueError:
        feedback = 'Введено некорректное значение.'
    return feedback


def make_expense_object(target_user_id, user_input):
    expense_amount = int(user_input)
    expense_object = Expense(
        user_id = target_user_id,
        expense_id = uuid.uuid4(),
        created_at = datetime.datetime.utcnow(),
        amount = expense_amount,
        category = MISCELLANEOUS_CATEGORY_NAME,
        description = None,
    )
    return expense_object


def add_expense(user_id, user_input):
    feedback = check_expense_amount(user_input)
    if feedback != 'ok':
        return None, feedback
    new_expense = make_expense_object(user_id, user_input)
    save_new_expense(new_expense)
    return new_expense, feedback


def make_expenses_report(user_id):
    expenses_list = get_user_expenses(user_id)
    incomes_sum = get_incomes_sum(user_id)
    expenses_sum = 0
    report = ''
    utc_offset = datetime.timedelta(hours=get_user_settings(user_id).utc_offset)
    for expense in expenses_list:
        expenses_sum += expense.amount
        formatted_created_at = (expense.created_at + utc_offset).strftime('%d.%m.%y, %H:%M')
        formatted_category = expense.category.capitalize()
        report += f'• ({formatted_created_at}) ({formatted_category}): -{expense.amount} руб.'
        if expense.description is not None:
            report += f" ({expense.description.capitalize()})"
        report += '\n'
    if report == '':
        report = 'Расходов не найдено. Везет же!'
    else:
        report_phrases = [
                'Cписок ваших расходов:\n',
                report,
                f'\nВсего потрачено: {expenses_sum}',
                f' из {incomes_sum} (остаток: {incomes_sum - expenses_sum})',
        ]
        if incomes_sum == 0:
            report_phrases.pop(3)
        report = ''.join(report_phrases)
    return report


def get_expenses_sum(user_id):
    expenses_list = get_user_expenses(user_id)
    expenses_sum = 0
    for expense_object in expenses_list:
        expenses_sum += expense_object.amount
    return expenses_sum
    
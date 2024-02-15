import uuid
import datetime
from db.database_models import Income
from db.incomes import save_new_income, get_user_incomes
from db.settings import get_user_settings


def check_positive_amount(user_input):
    feedback = 'ok'
    try:
        if int(user_input) <= 0:
            feedback = 'Значение должно быть больше нуля.'
    except ValueError:
        feedback = 'Введено некорректное значение.'
    return feedback


def make_income_object(target_user_id, income_amount):
    new_income = Income(
        user_id = target_user_id,
        income_id = uuid.uuid4(),
        amount = income_amount,
        description = None,
        created_at = datetime.datetime.utcnow(),
    )
    return new_income


def add_income(user_id, user_input):
    feedback = check_positive_amount(user_input)
    if feedback != 'ok':
        return None, feedback
    new_income = make_income_object(user_id, user_input)
    save_new_income(new_income)
    return new_income, feedback


def get_current_incomes(user_id):
    incomes_list = get_user_incomes(user_id)
    user_utc_offset = get_user_settings(user_id).utc_offset
    user_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=user_utc_offset)
    current_period = datetime.datetime.strftime(user_datetime, '%m-%Y')
    current_incomes = [income for income in incomes_list if datetime.datetime.strftime(
        income.created_at, '%m-%Y') == current_period]
    return current_incomes


def get_incomes_sum(user_id):
    user_incomes = get_current_incomes(user_id)
    incomes_sum = sum([income.amount for income in user_incomes])
    return incomes_sum


def make_incomes_report(user_id):
    incomes_list = get_current_incomes(user_id)
    utc_offset = datetime.timedelta(hours=get_user_settings(user_id).utc_offset)
    incomes_sum = get_incomes_sum(user_id)
    report = f'Общий бюджет текущего периода: {incomes_sum} руб.\n'
    if incomes_list not in (None, []):
        report += 'Он формируется из следующих приходов:\n'
    for income in incomes_list:
        formatted_created_at = (income.created_at + utc_offset).strftime('%d.%m.%y, %H:%M')   
        report += f'• ({formatted_created_at}): +{income.amount} руб.'
        if income.description is not None:
            report += f' ({income.description.capitalize()})'
        report += '\n'
    return report

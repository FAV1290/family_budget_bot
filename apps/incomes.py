import uuid
from db.database_models import Income
from db.incomes import save_new_income, get_user_incomes


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
    )
    return new_income


def add_income(user_id, user_input):
    feedback = check_positive_amount(user_input)
    if feedback != 'ok':
        return None, feedback
    new_income = make_income_object(user_id, user_input)
    save_new_income(new_income)
    return new_income, feedback


def get_incomes_sum(user_id):
    user_incomes = get_user_incomes(user_id)
    incomes_sum = sum([income.amount for income in user_incomes])
    return incomes_sum

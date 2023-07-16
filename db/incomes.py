from db.database_init import db_session
from db.database_models import Income


def save_new_income(income_object):
    db_session.add(income_object)
    db_session.commit()


def change_income_description(target_income_id, new_description):
    target_income_object = Income.query.filter(Income.income_id == target_income_id).first()
    target_income_object.description = new_description
    db_session.commit()


def get_user_incomes(target_user_id):
    user_incomes_object = Income.query.filter(Income.user_id == target_user_id)
    user_incomes = [income_object for income_object in user_incomes_object]
    return user_incomes
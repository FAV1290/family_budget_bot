from db.database_init import db_session
from db.database_models import Expense


def save_new_expense(expense_object):
    db_session.add(expense_object)
    db_session.commit()


def change_expense_category(target_id, new_category):
    target_expense_object = Expense.query.filter(Expense.expense_id == target_id).first()
    target_expense_object.category = new_category
    db_session.commit()


def change_expense_description(target_id, new_description):
    target_expense_object = Expense.query.filter(Expense.expense_id == target_id).first()
    target_expense_object.description = new_description
    db_session.commit()


def get_user_expenses(target_user_id):
    user_expenses_object = Expense.query.filter(
        Expense.user_id == target_user_id).order_by(Expense.created_at)
    user_expenses = [expense_object for expense_object in user_expenses_object]
    return user_expenses


def get_expense_by_id(target_expense_id):
    expense_object = Expense.query.filter(Expense.expense_id == target_expense_id).first()
    return expense_object

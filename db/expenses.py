from db.database_init import db_session
from db.database_models import Expense
from apps.converters import convert_expense_dict_to_object, convert_expense_object_to_dict


def save_new_expense(expense):
    new_expense_object = convert_expense_dict_to_object(expense)
    db_session.add(new_expense_object)
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
    user_expenses = []
    user_expenses_object = Expense.query.filter(
        Expense.user_id == target_user_id).order_by(Expense.created_at)
    for expense_object in user_expenses_object:
        new_expense = convert_expense_object_to_dict(expense_object)
        user_expenses.append(new_expense)
    return user_expenses


def get_expense_by_id(target_expense_id):
    expense_object = Expense.query.filter(Expense.expense_id == target_expense_id).first()
    target_expense = convert_expense_object_to_dict(expense_object)
    return target_expense

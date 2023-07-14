from database_init import db_session
from constants import DEFAULT_CATEGORIES
from database_models import Expense, Categories, Settings


def convert_expense_dict_to_object(expense):
    expense_object = Expense(
        user_id = expense['user_id'],
        expense_id = expense['expense_id'],
        created_at = expense['created_at'],
        amount = expense['amount'],
        category = expense['category'],
        description = expense['description'],
    )
    return expense_object


def save_new_expense(expense):
    new_expense_object = convert_expense_dict_to_object(expense)
    db_session.add(new_expense_object)
    db_session.commit()


def change_expense_category(target_id, new_category):
    target_expense_object = Expense.query.filter(Expense.expense_id == target_id).first()
    target_expense_object.category = new_category
    db_session.commit()


def update_categories(target_id, categories_list):
    categories_object = Categories.query.filter(Categories.user_id == target_id).first()
    if categories_object is None:
        new_categories_object = Categories(
            user_id = target_id,
            user_categories = categories_list,
        )
        db_session.add(new_categories_object)
    else:
        categories_object.user_categories = categories_list
    db_session.commit()


def get_user_categories(target_id):
    user_categories_object = Categories.query.filter(Categories.user_id == target_id).first()
    if user_categories_object is None or user_categories_object.user_categories in (None, []):
        return DEFAULT_CATEGORIES
    return user_categories_object.user_categories


def get_user_expenses(target_user_id):
    user_expenses = []
    user_expenses_object = Expense.query.filter(
        Expense.user_id == target_user_id).order_by(Expense.created_at)
    for expense_object in user_expenses_object:
        new_expense = {
            'user_id' : expense_object.user_id,
            'expense_id' : expense_object.expense_id,
            'created_at' : expense_object.created_at,
            'amount' : expense_object.amount,
            'category' : expense_object.category,
            'description' : expense_object.description,
        }
        user_expenses.append(new_expense)
    return user_expenses


def get_expense_by_id(target_expense_id):
    expense_object = Expense.query.filter(Expense.expense_id == target_expense_id).first()
    target_expense = {
        'user_id' : expense_object.user_id,
        'expense_id' : expense_object.expense_id,
        'created_at' : expense_object.created_at,
        'amount' : expense_object.amount,
        'category' : expense_object.category,
        'description' : expense_object.description,
    }
    return target_expense


def update_utc_offset(target_id, new_utc_offset):
    settings_object = Settings.query.filter(Settings.user_id == target_id).first()
    if settings_object is None:
        new_settings_object = Settings(
            user_id = target_id,
            is_app_configured = False,
            utc_offset = new_utc_offset
        )
        db_session.add(new_settings_object)
    else:
        settings_object.utc_offset = new_utc_offset
    db_session.commit()


def update_config_status(target_id, new_status):
    settings_object = Settings.query.filter(Settings.user_id == target_id).first()
    if settings_object is None:
        new_settings_object = Settings(
            user_id = target_id,
            is_app_configured = new_status,
            utc_offset = 0
        )
        db_session.add(new_settings_object)
    else:
        settings_object.is_app_configured = new_status
    db_session.commit()



def get_user_utc_offset(target_id):
    settings_object = Settings.query.filter(Settings.user_id == target_id).first()
    if settings_object is None or settings_object.utc_offset is None:
        return 0
    return settings_object.utc_offset


def get_user_config_status(target_id):
    settings_object = Settings.query.filter(Settings.user_id == target_id).first()
    if settings_object is None or settings_object.is_app_configured is None:
        return False
    return settings_object.is_app_configured

    
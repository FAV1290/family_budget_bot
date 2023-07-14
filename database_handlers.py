import uuid
from database_init import db_session
from constants import DEFAULT_CATEGORIES_NAMES
from database_models import Expense, Category, Settings


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


def convert_expense_object_to_dict(expense_object):
    expense_dict = {
        'user_id' : expense_object.user_id,
        'expense_id' : expense_object.expense_id,
        'created_at' : expense_object.created_at,
        'amount' : expense_object.amount,
        'category' : expense_object.category,
        'description' : expense_object.description,
    }
    return expense_dict   

    
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


def convert_category_dict_to_object(category):
    category_object = Category(
        user_id = category['user_id'],
        category_id = category['category_id'],
        name = category['name'],
        limit = category['limit'],
    )
    return category_object


def convert_category_object_to_dict(category_object):
        category_dict = {
            'user_id' : category_object.user_id,
            'category_id' : category_object.category_id,
            'name' : category_object.name,
            'limit' : category_object.limit,
        }
        return category_dict


def clear_user_categories(target_user_id):
    user_categories_object = Category.query.filter(Category.user_id == target_user_id)
    for item in user_categories_object:
        db_session.delete(item)
    db_session.commit()


def save_new_category(category):
    new_category_object = convert_category_dict_to_object(category)
    db_session.add(new_category_object)
    db_session.commit()


def set_default_categories(target_user_id):
    for category_name in DEFAULT_CATEGORIES_NAMES:
        new_category = {
            'user_id' : target_user_id,
            'category_id' : uuid.uuid4(),
            'name' : category_name,
            'limit' : None,
        }
        save_new_category(new_category)


def get_user_categories(target_id):
    user_categories_object = Category.query.filter(Category.user_id == target_id)
    user_categories = []
    if user_categories_object.first() is None:
        set_default_categories(target_id)
        return get_user_categories(target_id)
    for category_object in user_categories_object:
        user_category = convert_category_object_to_dict(category_object)
        user_categories.append(user_category)
    return user_categories


def change_category_limit(target_id, new_limit):
    target_category_object = Category.query.filter(Category.category_id == target_id).first()
    target_category_object.limit = new_limit
    db_session.commit()


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


def convert_settings_object_to_dict(settings_object):
    settings_dict = {
        'user_id' : settings_object.user_id,
        'is_app_configured' : settings_object.is_app_configured,
        'utc_offset' : settings_object.utc_offset,
    }
    return settings_dict   


def get_user_settings(target_id):
    settings_object = Settings.query.filter(Settings.user_id == target_id).first()
    if settings_object is None:
        settings_object = Settings(
            user_id = target_id,
            is_app_configured = False,
            utc_offset = 0
        )
    return convert_settings_object_to_dict(settings_object)
    
import uuid
from constants import DEFAULT_CATEGORIES_NAMES
from db.database_init import db_session
from db.database_models import Expense, Category


def clear_user_categories(target_user_id):
    user_categories_object = Category.query.filter(Category.user_id == target_user_id)
    for item in user_categories_object:
        db_session.delete(item)
    db_session.commit()


def save_new_category(category_object):
    db_session.add(category_object)
    db_session.commit()


def set_default_categories(target_user_id):
    for category_name in DEFAULT_CATEGORIES_NAMES:
        new_category_object = Category(
            user_id = target_user_id,
            category_id = uuid.uuid4(),
            name = category_name,
            limit = None,
        )
        save_new_category(new_category_object)


def get_user_categories(target_user_id):
    categories_object = Category.query.filter(
        Category.user_id == target_user_id).order_by(Category.name)
    if categories_object.first() is None:
        set_default_categories(target_user_id)
        return get_user_categories(target_user_id)
    user_categories_list = [category for category in categories_object]
    return user_categories_list


def change_category_limit(category_id, new_limit):
    target_category = Category.query.filter(Category.category_id == category_id).first()
    target_category.limit = new_limit
    db_session.commit()


def get_expenses_sum_by_category(target_id, category_name):
    target_expenses_object = Expense.query.filter(Expense.user_id == target_id)
    expenses_sum = 0
    for expense_object in target_expenses_object:
        if expense_object.category == category_name:
            expenses_sum += expense_object.amount
    return expenses_sum

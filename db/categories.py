import uuid
from constants import DEFAULT_CATEGORIES_NAMES
from db.database_init import db_session
from db.database_models import Expense, Category
from apps.converters import convert_category_dict_to_object, convert_category_object_to_dict


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


def get_expenses_sum_by_category(target_id, category_name): #А оптимально ли? И точно ли в этом модуле этой функции место?
    target_expenses_object = Expense.query.filter(Expense.user_id == target_id)
    expenses_sum = 0
    for expense_object in target_expenses_object:
        if expense_object.category == category_name:
            expenses_sum += expense_object.amount
    return expenses_sum

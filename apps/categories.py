import uuid
from db.database_models import Category
from db.categories import get_user_categories, save_new_category, get_expenses_sum_by_category


def get_user_categories_names(user_id):
    return [category.name for category in get_user_categories(user_id)]


def check_category_name(user_id, user_input):
    category, feedback = user_input.lower().strip(), 'ok'
    categories_list = get_user_categories_names(user_id)
    if category in categories_list:
        feedback = f'Категория {category.capitalize()} уже существует'
    elif category == '' or len(category) > 50:
        feedback = 'Не удалось добавить категорию. Возможно, вы ввели некорректные данные?'
    return feedback


def check_category_limit(user_input):
    feedback = 'ok'
    try:
        if int(user_input) < 0:
            feedback = 'Лимит не может быть отрицательным.'
    except ValueError:
        feedback = 'Введено некорректное значение.'
    return feedback


def make_category_object(target_user_id, user_input):
    category_object = Category(
        user_id = target_user_id,
        category_id = uuid.uuid4(),
        name = user_input,
        limit = None,
    )
    return category_object


def add_category(user_id, user_input):
    feedback = check_category_name(user_id, user_input)
    if feedback != 'ok':
        return feedback
    new_category = make_category_object(user_id, user_input)
    feedback = f'Категория {new_category.name.capitalize()} успешно добавлена'
    save_new_category(new_category)
    return feedback


def make_categories_report(user_id):
    categories_list = get_user_categories(user_id)
    report = 'Вам доступны следующие категории расходов:'
    for category in sorted(categories_list, key = lambda category:category.name):
        report += f'\n • {category.name.capitalize()}'
        if category.limit is not None:
            report += f' (Лимит: {category.limit} руб., '
            expenses_sum = get_expenses_sum_by_category(user_id, category.name)
            balance = category.limit - expenses_sum
            report += f'остаток: {balance} руб.)'
    return report

from db.database_models import Category, Expense


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


def convert_settings_object_to_dict(settings_object):
    settings_dict = {
        'user_id' : settings_object.user_id,
        'is_app_configured' : settings_object.is_app_configured,
        'utc_offset' : settings_object.utc_offset,
    }
    return settings_dict

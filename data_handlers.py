import datetime, uuid, json
from constants import FILEPATH, DEFAULT_DATA_DICT, DEFAULT_CATEGORIES


def save_data(data_dict):
    for record in data_dict['expenses']:
        record['expense_id'] = str(record['expense_id'])
        record['created_at'] = record['created_at'].strftime('%d.%m.%y, %H:%M')
    with open(FILEPATH, 'w') as json_handler:
        json.dump(data_dict, json_handler)


def load_data():
    try:
        with open(FILEPATH, 'r', encoding='utf-8') as json_handler:
            data_dict = json.load(json_handler)
    except OSError:
        data_dict = DEFAULT_DATA_DICT
    for record in data_dict['expenses']:
        record['expense_id'] = uuid.UUID(record['expense_id'])
        record['created_at'] = datetime.datetime.strptime(record['created_at'], '%d.%m.%y, %H:%M')
    return data_dict


def find_parameters_by_id(parameters_list, user_id):
    for record in parameters_list:
        if record['user_id'] == user_id:
            return record


def filter_user_data(data_dict, user_id):
    user_data = {}
    categories = find_parameters_by_id(data_dict['categories'], user_id)
    if categories is None:
        user_data['categories'] = DEFAULT_CATEGORIES
    else:
        user_data['categories'] = categories['user_categories']
    user_data['expenses'] = [expense for expense in data_dict['expenses'] if expense['user_id'] == user_id]
    user_data['settings'] = find_parameters_by_id(data_dict['settings'], user_id)
    if user_data['settings'] is None:
        user_data['settings'] = {
            'user_id' : user_id,
            'is_app_configured' : False,
            'utc_offset' : 0
        }   
    return user_data


def get_expense_by_id(expense_id):
    expenses_list = load_data()['expenses']
    return [expense for expense in expenses_list if expense['expense_id'] == uuid.UUID(expense_id)][0]


def find_index_by_id(list_of_dicts, dict_key, target_id):
    target_index = next((index for index, record in enumerate(list_of_dicts) if record[dict_key] == target_id), None)
    return target_index

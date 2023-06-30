from constants import DEFAULT_CATEGORIES
from data_handlers import save_data, load_data, filter_user_data, find_index_by_id


def update_categories(user_id, categories_list):
    data_dict = load_data()
    target_index = find_index_by_id(data_dict['categories'], 'user_id', user_id)
    if target_index is None:
        data_dict['categories'].append({'user_id' : user_id, 'user_categories' : categories_list})
    else:
        data_dict['categories'][target_index]['user_categories'] = categories_list
    save_data(data_dict)


def add_category(user_id, user_input):
    feedback = None
    categories_list = filter_user_data(load_data(), user_id)['categories']
    if categories_list is None or categories_list == []:
        categories_list = DEFAULT_CATEGORIES
    for category in map(str.strip, user_input.partition(' ')[2].lower().split(',')):
        if category in categories_list:
            feedback = str(feedback or '') + f'• Категория {category.capitalize()} уже существует\n'
        elif category == '' or len(category) > 50:
            continue
        else:
            feedback = str(feedback or '') +  f'• Категория {category.capitalize()} добавлена\n'
            categories_list.append(category)
    update_categories(user_id, categories_list)
    if feedback is None:
        feedback = 'Не удалось добавить ни одной категории.\nВозможно, вы ввели некорректные данные?'
    return feedback


def show_categories(user_id):
    categories_list = filter_user_data(load_data(), user_id)['categories']
    if categories_list is None or categories_list == []:
        categories_list = DEFAULT_CATEGORIES
    report = 'Вам доступны следующие категории расходов:'
    for category in sorted(categories_list):
        report += f'\n • {category.capitalize()}'
    return report

from database_handlers import update_categories, get_user_categories


def check_categories_input(user_id, user_input):
    feedback = ''
    categories_list = get_user_categories(user_id)
    for category in map(str.strip, user_input.partition(' ')[2].lower().split(',')):
        if category in categories_list:
            feedback = feedback + f'• Категория {category.capitalize()} уже существует\n'
        elif category == '' or len(category) > 50:
            continue
        else:
            feedback = feedback +  f'• Категория {category.capitalize()} добавлена\n'
            categories_list.append(category)
    if feedback == '':
        feedback = ''.join(
            [
                'Не удалось добавить ни одной категории.',
                '\nВозможно, вы ввели некорректные данные?',
            ]
        )
    return categories_list, feedback


def add_category(user_id, user_input):
    categories_list, feedback = check_categories_input(user_id, user_input)
    update_categories(user_id, categories_list)
    return feedback


def make_categories_report(user_id):
    categories_list = get_user_categories(user_id)
    report = 'Вам доступны следующие категории расходов:'
    for category in sorted(categories_list):
        report += f'\n • {category.capitalize()}'
    return report

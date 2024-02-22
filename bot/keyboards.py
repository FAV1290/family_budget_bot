from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from db.models import Category


def create_user_categories_keyboard(
    user_categories: list[Category],
    line_size: int = 2,
) -> InlineKeyboardMarkup:
    keyboard, keyboard_line = [], []
    for index, category in enumerate(user_categories):
        button = InlineKeyboardButton(category.name.capitalize(), callback_data=str(category.id))
        keyboard_line.append(button)
        if index % line_size == line_size - 1:
            keyboard.append(keyboard_line)
            keyboard_line = []
    keyboard.append(keyboard_line)
    keyboard.append([InlineKeyboardButton('Без категории', callback_data='None')])
    return InlineKeyboardMarkup(keyboard)


def create_yes_or_no_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('Да', callback_data='yes'),
        InlineKeyboardButton('Нет', callback_data='no'),
    ]])

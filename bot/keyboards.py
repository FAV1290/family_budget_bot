from datetime import datetime, timedelta

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from db.models import Category
from bot.conversations.enums import UTCRegion


def create_user_categories_keyboard(
    user_categories: list[Category],
    line_size: int = 2,
    add_none_button: bool = True,
) -> InlineKeyboardMarkup:
    keyboard, keyboard_line = [], []
    for index, category in enumerate(user_categories):
        button = InlineKeyboardButton(category.name.capitalize(), callback_data=str(category.id))
        keyboard_line.append(button)
        if index % line_size == line_size - 1:
            keyboard.append(keyboard_line)
            keyboard_line = []
    keyboard.append(keyboard_line)
    if add_none_button:
        keyboard.append([InlineKeyboardButton('Без категории', callback_data='None')])
    return InlineKeyboardMarkup(keyboard)


def create_yes_or_no_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('Да', callback_data='yes'),
        InlineKeyboardButton('Нет', callback_data='no'),
    ]])


def create_utc_regions_keyboard() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(
        region.value.capitalize(), callback_data=region.value) for region in UTCRegion]
    return InlineKeyboardMarkup([buttons[index:index + 2] for index in range(0, len(buttons), 2)])


def create_utc_offsets_keyboard(offsets: list[int]) -> InlineKeyboardMarkup:
    buttons = []
    for offset in offsets:
        label = (datetime.utcnow() + timedelta(hours=offset)).strftime('%d-%m-%Y %H:%M')
        button = InlineKeyboardButton(label, callback_data=str(offset))
        buttons.append(button)
    return InlineKeyboardMarkup([buttons[index:index + 3] for index in range(0, len(buttons), 3)])

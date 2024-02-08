from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from constants import REGIONS, UTC_OFFSETS_DIVISION
from apps.categories import get_user_categories_names


def make_categories_buttons(user_id):
    categories = get_user_categories_names(user_id)
    button_list = []
    for category in categories:
        button = InlineKeyboardButton(category.title(), callback_data=category)
        button_list.append(button)
    reply_markup = InlineKeyboardMarkup(
        [button_list[index:index + 3] for index in range(0, len(button_list), 3)])
    return reply_markup


def make_regions_buttons():
    button_list = [InlineKeyboardButton(
        key.title().replace('И', 'и'), callback_data = value) for key, value in REGIONS]
    reply_markup = InlineKeyboardMarkup(
        [button_list[index:index + 2] for index in range(0, len(button_list), 2)])
    return reply_markup


def make_utc_buttons(region):
    button_list = []
    for offset in UTC_OFFSETS_DIVISION[region]:
        if offset > 0:
            title = '+' + str(offset)
        else:
            title = str(offset)
        button = InlineKeyboardButton(title, callback_data = offset)
        button_list.append(button)
    reply_markup = InlineKeyboardMarkup(
        [button_list[index:index + 3] for index in range(0, len(button_list), 3)])
    return reply_markup


def make_true_false_question_buttons():
    button_list = [InlineKeyboardButton(
        key, callback_data = value) for key, value in [('Да', 'yes'), ('Нет', 'no')]]
    reply_markup = InlineKeyboardMarkup([button_list])
    return reply_markup

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters)
from constants import MISCELLANEOUS_CATEGORY_NAME, COMMANDS
from expenses import add_expense
from categories import get_user_categories_names
from database_handlers import (
    get_expense_by_id, change_expense_category, change_expense_description)


AMOUNT, CATEGORY, DESCRIPTION_CHOICE, DESCRIPTION_CHANGE = range(4)


def start_naming_stage(update, context):
    update.message.reply_text('Пожалуйста, введите сумму расхода:', quote=False)
    return AMOUNT


def make_categories_buttons(user_id, new_expense):
    categories = get_user_categories_names(user_id)
    button_list = []
    for category in categories:
        data_string = str(new_expense['expense_id']) + category
        button = InlineKeyboardButton(category.title(), callback_data = data_string)
        button_list.append(button)
    reply_markup = InlineKeyboardMarkup(
        [button_list[index:index + 3] for index in range(0, len(button_list), 3)]
    )
    return reply_markup


def start_amount_stage(update, context):
    expense, feedback = add_expense(update.message.chat.id, update.message.text)
    if expense is None:
        feedback += ' Попробуйте еще раз.'
        update.message.reply_text(feedback, quote=False)
        return AMOUNT
    else:
        reply_markup = make_categories_buttons(update.message.chat.id, expense)
        feedback = 'Теперь выберите желаемую категорию:'
        update.message.reply_text(feedback, quote=False, reply_markup=reply_markup)
        return CATEGORY


def make_comment_buttons(expense_id):
    yes_tuple = ('Да', str(expense_id) + 'yes')
    no_tuple = ('Нет', str(expense_id) + 'no')
    button_list = [
        InlineKeyboardButton(key, callback_data = value) for key, value in [yes_tuple, no_tuple]]
    reply_markup = InlineKeyboardMarkup([button_list])
    return reply_markup


def start_category_stage(update, context):
    target_id = update.callback_query.data[:36]
    target_category = update.callback_query.data[36:]
    target_expense = get_expense_by_id(target_id)
    update.callback_query.answer()
    change_expense_category(target_id, target_category)
    feedback = ''.join(
        [
            f'Новая расходная операция на сумму {target_expense["amount"]} рублей.',
            f'\nРасход добавлен в категорию {target_category.title()}. ',
            'Желаете добавить к нему комментарий?'
        ]
    )
    comment_markup = make_comment_buttons(target_id)
    update.callback_query.edit_message_text(text=feedback, reply_markup = comment_markup)
    return DESCRIPTION_CHOICE


def start_description_choice(update, context):
    user_answer = update.callback_query.data[36:]
    update.callback_query.answer()
    if user_answer == 'no':
        update.callback_query.edit_message_text(
            'Хорошо, расход добавлен без комментария. Чтобы добавить еще один, введите /add')
        return ConversationHandler.END
    else:
        update.callback_query.edit_message_text('Хорошо, введите текст комментария:')
        target_id = update.callback_query.data[:36]
        context.chat_data['expense_id'] = target_id
        return DESCRIPTION_CHANGE
    

def start_description_stage(update, context):
    target_id = context.chat_data.pop('expense_id')
    new_description = update.message.text
    change_expense_description(target_id, new_description)
    bot_answer = ''.join(
        [
           'Комментарий (а вместе с ним и расход) успешно добавлен.',
           'Чтобы добавить еще один расход, введите /add' 
        ]
    )
    update.message.reply_text(bot_answer, quote=False)
    return ConversationHandler.END


def start_cancel_stage(update, context):
    bot_message = [
        'Похоже, вам приглянулась другая команда.',
        'Сейчас я выйду из режима добавления расхода, чтобы ее можно было использовать.',
        'Если вы не успели выбрать категорию расхода,'
        f'он будет сохранен в категории "{MISCELLANEOUS_CATEGORY_NAME.title()}"',
    ]
    update.message.reply_text(' '.join(bot_message), quote=False)
    return ConversationHandler.END


def add_expense_handler():
    add_expense_handler = ConversationHandler(
        entry_points=[CommandHandler('add', start_naming_stage)], 
        states={
            AMOUNT: [MessageHandler(Filters.text & ~Filters.command, start_amount_stage)],
            CATEGORY: [CallbackQueryHandler(start_category_stage)],
            DESCRIPTION_CHOICE: [CallbackQueryHandler(start_description_choice)],
            DESCRIPTION_CHANGE: [MessageHandler(
                Filters.text & ~Filters.command, start_description_stage
            )],
        },
        fallbacks=[CommandHandler(COMMANDS.keys(), start_cancel_stage)],
        per_user=False,
    )
    return add_expense_handler

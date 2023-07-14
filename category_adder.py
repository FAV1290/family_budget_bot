from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters)
from constants import COMMANDS
from categories import check_category_input, make_category_dict
from database_handlers import save_new_category, change_category_limit
from expenses import check_expense_input


NAME, LIMIT_CHOICE, LIMIT_SET = range(3)


def start_greetings_stage(update, context):
    update.message.reply_text('Пожалуйста, введите имя категории:', quote=False)
    return NAME


def make_limit_choice_buttons(category_id):
    yes_tuple = ('Да', str(category_id) + 'yes')
    no_tuple = ('Нет', str(category_id) + 'no')
    button_list = [
        InlineKeyboardButton(key, callback_data = value) for key, value in [yes_tuple, no_tuple]]
    reply_markup = InlineKeyboardMarkup([button_list])
    return reply_markup


def start_naming_stage(update, context):
    feedback = check_category_input(update.message.chat.id, update.message.text)
    if feedback == 'ok':
        new_category = make_category_dict(update.message.chat.id, update.message.text)
        limit_markup = make_limit_choice_buttons(new_category['category_id'])
        feedback = ''.join(
            [
                f'Категория {new_category["name"].capitalize()} успешно добавлена.',
                'Хотите установить для нее лимит расходов?',
            ]
        )
        save_new_category(new_category)
        update.message.reply_text(feedback, quote=False, reply_markup = limit_markup)
        return LIMIT_CHOICE
    else:
        feedback += '\n Чтобы попробовать снова, повторите команду /new_category.'
        update.message.reply_text(feedback, quote=False)
        return ConversationHandler.END
    

def start_limit_choice_stage(update, context):
    user_answer = update.callback_query.data[36:]
    update.callback_query.answer()
    if user_answer == 'no':
        update.callback_query.edit_message_text(
            'Ясно, эта категория будет без лимита. Чтобы добавить еще одну, введите /new_category')
        return ConversationHandler.END
    else:
        update.callback_query.edit_message_text('Хорошо, введите целочисленный лимит расхода:')
        target_id = update.callback_query.data[:36]
        context.chat_data['category_id'] = target_id
        return LIMIT_SET
    

def start_limit_set_stage(update, context):
    target_id = context.chat_data.pop('category_id')
    feedback = check_expense_input(update.message.text)
    if feedback == 'ok':
        new_limit = update.message.text
        change_category_limit(target_id, new_limit)
        update.message.reply_text(f'Лимит успешно установлен.', quote=False)
        return ConversationHandler.END
    else:
        feedback += '\nПопробуйте еще раз.'
        update.message.reply_text(feedback, quote=False)
        return LIMIT_SET
    

def start_cancel_stage(update, context):
    bot_message = [
        'Похоже, вам приглянулась другая команда.',
        'Сейчас я выйду из режима добавления категории, чтобы ее можно было использовать.',
    ]
    update.message.reply_text(' '.join(bot_message), quote=False)
    return ConversationHandler.END


def add_category_handler():
    add_category_handler = ConversationHandler(
        entry_points=[CommandHandler('new_category', start_greetings_stage)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, start_naming_stage)],
            LIMIT_CHOICE: [CallbackQueryHandler(start_limit_choice_stage)],
            LIMIT_SET: [MessageHandler(Filters.text & ~Filters.command, start_limit_set_stage)],
        },
        fallbacks=[CommandHandler(COMMANDS.keys(), start_cancel_stage)],
        per_user=False,
    )
    return add_category_handler

from telegram.ext import (
    CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters)
from constants import COMMANDS
from db.categories import save_new_category, change_category_limit
from apps.categories import check_category_name, make_category_object, check_category_limit
from bot.keyboards import make_true_false_question_buttons


NAME, LIMIT_CHOICE, LIMIT_SET = range(3)


def start_greetings_stage(update, context):
    update.message.reply_text('Пожалуйста, введите имя категории:', quote=False)
    return NAME
    

def start_naming_stage(update, context):    #А почему не add_category? Та функция вроде делает примерно то же самое
    user_input = update.message.text.lower().strip()
    feedback = check_category_name(update.message.chat.id, user_input)
    if feedback == 'ok':
        new_category = make_category_object(update.message.chat.id, user_input)
        limit_markup = make_true_false_question_buttons()
        feedback = ''.join(
            [
                f'Категория {new_category.name.capitalize()} успешно добавлена.',
                'Хотите установить для нее лимит расходов?',
            ]
        )
        save_new_category(new_category)
        context.chat_data['category_id'] = new_category.category_id
        update.message.reply_text(feedback, quote=False, reply_markup = limit_markup)
        return LIMIT_CHOICE
    else:
        feedback += '\n Чтобы попробовать снова, повторите команду /new_category.'
        update.message.reply_text(feedback, quote=False)
        return ConversationHandler.END
    

def start_limit_choice_stage(update, context):
    user_answer = update.callback_query.data
    update.callback_query.answer()
    if user_answer == 'no':
        update.callback_query.edit_message_text(
            'Ясно, эта категория будет без лимита. Чтобы добавить еще одну, введите /new_category')
        return ConversationHandler.END
    else:
        update.callback_query.edit_message_text('Хорошо, введите целочисленный лимит расхода:')
        return LIMIT_SET
    

def start_limit_set_stage(update, context):
    target_id = context.chat_data['category_id']
    feedback = check_category_limit(update.message.text)
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

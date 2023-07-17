from telegram.ext import (
    CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters)
from constants import COMMANDS
from db.categories import change_category_limit
from apps.categories import get_user_category_by_name, check_category_limit
from bot.keyboards import make_categories_buttons


CATEGORY_CHOOSE, LIMIT_SET = range(2)


def start_greetings_stage(update, context):
    bot_message = 'Выберите категорию, лимит которой желаете изменить:'
    categories_markup = make_categories_buttons(update.message.chat.id)
    update.message.reply_text(bot_message, quote=False, reply_markup=categories_markup)
    return CATEGORY_CHOOSE


def start_category_choose_stage(update, context):
    target_user_id = update.callback_query.message.chat.id
    target_category_name = update.callback_query.data    #Как тут дела с регистром? Проверить
    update.callback_query.answer()
    target_category = get_user_category_by_name(target_user_id, target_category_name)
    context.chat_data['category_id'] = target_category.category_id
    update.callback_query.edit_message_text(
        f'Укажите новый лимит категории {target_category.name}:')
    return LIMIT_SET


def start_imit_set_stage(update, context):  #А может взять функцию из add_category_dialog?
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


def start_cancel_stage(update, context):    #А не сделать ли общий кэнселлер на все диалоги?
    bot_message = [
        'Похоже, вам приглянулась другая команда.',
        'Чтобы вы могли вызвать ее, выполнение текущего действия будет прервано'
    ]
    update.message.reply_text(' '.join(bot_message), quote=False)
    return ConversationHandler.END


def change_category_limit_handler():
    change_category_limit_handler = ConversationHandler(
        entry_points=[CommandHandler('category_limit', start_greetings_stage)], 
        states={
            CATEGORY_CHOOSE: [CallbackQueryHandler(start_category_choose_stage)],
            LIMIT_SET: [MessageHandler(Filters.text & ~Filters.command, start_imit_set_stage)],
        },
        fallbacks=[CommandHandler(COMMANDS.keys(), start_cancel_stage)],
        per_user=False,
    )
    return change_category_limit_handler

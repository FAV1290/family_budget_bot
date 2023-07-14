import datetime
from telegram.ext import (
    CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters)
from constants import COMMANDS
from db.settings import update_utc_offset, get_user_settings, update_config_status
from apps.categories import add_category 
from bot.keyboards import make_true_false_question_buttons, make_regions_buttons, make_utc_buttons


NOT_FIRST_LAUNCH, REGION, UTC_OFFSET, CATEGORIES = range(4)
   

def start_greetings_stage(update, context):
    config_status = get_user_settings(update.message.chat.id).is_app_configured
    if config_status:
        bot_answer = ' '.join([
            'Привет! Если не ошибаюсь, мы с вами уже зафиксировали первоначальные настройки.',
            'Уверены, что хотите повторить процесс?',
        ])
        reinit_buttons = make_true_false_question_buttons()
        update.message.reply_text(bot_answer, quote=False, reply_markup = reinit_buttons)
        return NOT_FIRST_LAUNCH     
    else:
        bot_answer = [
            'Привет! Я помогаю вести семейный бюджет!',
            'Начнем знакомство с настроек',
        ]
        update.message.reply_text(' '.join(bot_answer), quote=False)
        region_question = 'Сперва выберите регион, в котором находитесь:'
        regions_buttons = make_regions_buttons()
        update.message.reply_text(region_question, quote=False, reply_markup = regions_buttons)
        return REGION


def start_reinit_stage(update, context):
    user_answer = update.callback_query.data
    if user_answer == 'yes':
        update_config_status(update.callback_query.message.chat.id, False)
        region_question = 'Да будет так. Сперва выберите регион, в котором находитесь:'
        regions_buttons = make_regions_buttons()
        update.callback_query.edit_message_text(region_question, reply_markup = regions_buttons())
        return REGION
    else:
        update.callback_query.edit_message_text('Тогда отбой. До скорых встреч!')
        return ConversationHandler.END


def start_region_stage(update, context):
    region = update.callback_query.data
    update.callback_query.answer()
    utc_question = ''.join(
        [
            'Теперь укажите отклонение времени от UTC в вашем регионе ',
            '(Например, московское время - UTC+3):'
        ])
    update.callback_query.edit_message_text(utc_question, reply_markup = make_utc_buttons(region))
    return UTC_OFFSET


def start_utc_offset_stage(update, context):
    offset = int(update.callback_query.data)
    update.callback_query.answer()
    estimated_date = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=offset)).strftime('%d.%m.%y, %H:%M')
    bot_answer = [
        f'Принято! Согласно этим данным, сейчас у вас {estimated_date}.',
        '\nТеперь давайте добавим какую-нибудь категорию расходов.'
        '\nВведите ее название или /cancel,',
        'чтобы отложить это действие',
        '(Позднее вы сможете добавлять категории с помощью команды /new_category).',
    ]
    update.callback_query.edit_message_text(' '.join(bot_answer))
    update_utc_offset(update.callback_query.message.chat.id, offset)
    return CATEGORIES


def make_bot_farewell_speach(categories_skipped = False):
    bot_answer = [
        'Вас понял, пока что никаких новых категорий.',
        'А начальная настройка, тем временем, завершена.',
        'Приятного вам использования и вкратце о командах:',
        '\n• /categories - посмотреть категории расходов',
        '\n• /new_category - добавить категорию расходов',
        '\n• /add - добавить расход',        
        '\n• /help - посмотреть все доступные команды', 
    ]
    if not categories_skipped:
        bot_answer.pop(0)
    return ' '.join(bot_answer)


def skip_categories_stage(update, context):
    bot_answer = make_bot_farewell_speach(categories_skipped=True)
    update.message.reply_text(bot_answer, quote=False)
    update_config_status(update.message.chat.id, True)
    return ConversationHandler.END


def start_categories_stage(update, context):
    categories_report = add_category(update.message.chat.id, update.message.text)
    update.message.reply_text(categories_report, quote=False)
    bot_answer = make_bot_farewell_speach()
    update.message.reply_text(bot_answer, quote=False)
    update_config_status(update.message.chat.id, True)
    return ConversationHandler.END


def start_cancel_stage(update, context):
    bot_message = [
        'Похоже, вам приглянулась другая команда. Сейчас я выйду из режима настроек,',
        'чтобы ее можно было использовать.',
        'Если же захотите вернуться к настройкам, введите "/start"',
    ]
    update.message.reply_text(' '.join(bot_message), quote=False)
    return ConversationHandler.END


def start_handler():
    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_greetings_stage)],
        states={
            NOT_FIRST_LAUNCH: [CallbackQueryHandler(start_reinit_stage)],
            REGION: [CallbackQueryHandler(start_region_stage)],
            UTC_OFFSET: [CallbackQueryHandler(start_utc_offset_stage)],
            CATEGORIES: [
                CommandHandler('cancel', skip_categories_stage),
                MessageHandler(Filters.text & ~Filters.command, start_categories_stage)
            ],
        },
        fallbacks=[CommandHandler(COMMANDS.keys(), start_cancel_stage)],
        per_user=False,
    )
    return start_handler

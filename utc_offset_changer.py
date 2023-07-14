import datetime
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from first_launch import make_regions_buttons, make_utc_buttons
from database_handlers import update_utc_offset
from constants import COMMANDS


REGION, UTC_OFFSET = range(2)


def start_greetings_stage(update, context):
        region_question = 'Выберите регион, в котором находитесь:'
        regions_buttons = make_regions_buttons()
        update.message.reply_text(region_question, quote=False, reply_markup = regions_buttons)
        return REGION


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
    bot_answer = f'Готово! Согласно этим данным, сейчас у вас {estimated_date}.'
    update.callback_query.edit_message_text(bot_answer)
    update_utc_offset(update.callback_query.message.chat.id, offset)
    return ConversationHandler.END


def start_cancel_stage(update, context):
    bot_message = [
        'Похоже, вам приглянулась другая команда.',
        'Сейчас я выйду из режима смены часового пояса, чтобы ее можно было использовать.',
    ]
    update.message.reply_text(' '.join(bot_message), quote=False)
    return ConversationHandler.END


def add_utc_offset_handler():
    utc_offset_handler = ConversationHandler(
    entry_points=[CommandHandler('utc_offset', start_greetings_stage)],
    states={
        REGION: [CallbackQueryHandler(start_region_stage)],
        UTC_OFFSET: [CallbackQueryHandler(start_utc_offset_stage)],
    },
    fallbacks=[CommandHandler(COMMANDS.keys(), start_cancel_stage)],
    per_user=False,
    )
    return utc_offset_handler
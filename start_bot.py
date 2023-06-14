import logging
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import API_TOKEN  # Плохо, заменить на переменную окружения
from family_funds import get_command_descriptions, check_outlay_string, make_outlay, add_outlay, format_outlays_report


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def start_handler(update, context): # Тут будут начальные настройки. Или не будут? Продумать механизм, который не позволит одной командой обнулить свои данные
    update.message.reply_text('Привет! Я помогаю вести семейный бюджет! Вот список доступных команд:', quote=False)
    update.message.reply_text(get_command_descriptions(), quote=False)


def help_handler(update, context):
    update.message.reply_text('Вам доступны следующие команды:', quote=False)
    update.message.reply_text(get_command_descriptions(), quote=False)


def outlay_add_handler(update, context):
    outlays = context.chat_data.get('outlays')
    feedback = check_outlay_string(update.message.text)
    if feedback == 'ok':
        new_outlay = make_outlay(update.message.text)
        context.chat_data['outlays'], feedback = add_outlay(outlays, new_outlay)
    update.message.reply_text(feedback, quote=False)


def show_outlays_handler(update, context):
    outlays_report = format_outlays_report(context.chat_data['outlays'])
    update.message.reply_text('Cписок ваших расходов:', quote=False)
    update.message.reply_text(outlays_report, quote=False)


def main():
    ffbot = Updater(API_TOKEN, use_context=True)
    dp = ffbot.dispatcher
    dp.add_handler(CommandHandler('start', start_handler))
    dp.add_handler(CommandHandler('help', help_handler))    
    dp.add_handler(CommandHandler('add', outlay_add_handler))
    dp.add_handler(CommandHandler('outlays', show_outlays_handler))
    logging.info(f'\n\n\n{datetime.datetime.now()}: Bot has started')
    ffbot.start_polling()
    ffbot.idle()


if __name__ == "__main__":
    main()

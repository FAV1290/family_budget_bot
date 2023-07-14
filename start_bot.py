import logging
import datetime
from telegram.ext import Updater, CommandHandler
from constants import API_TOKEN, COMMANDS
from apps.categories import make_categories_report
from apps.expenses import make_expenses_report
from bot.first_launch_dialog import start_handler
from bot.add_expense_dialog import add_expense_handler
from bot.add_category_dialog import add_category_handler
from bot.utc_offset_dialog import add_utc_offset_handler


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def get_command_descriptions():
    commands_message = ''
    for command in COMMANDS.values():
        commands_message += f'{command}\n'
    return commands_message


def help_handler(update, context):
    update.message.reply_text('Вам доступны следующие команды:', quote=False)
    update.message.reply_text(get_command_descriptions(), quote=False)


def show_expenses_handler(update, context):
    expenses_report = make_expenses_report(update.message.chat.id)
    update.message.reply_text(expenses_report, quote=False)


def show_categories_handler(update, context):
    categories_report = make_categories_report(update.message.chat.id)
    update.message.reply_text(categories_report, quote=False)


def main():
    ffbot = Updater(API_TOKEN, use_context=True)
    dp = ffbot.dispatcher
    dp.add_handler(start_handler()) #s
    dp.add_handler(add_expense_handler()) #a
    dp.add_handler(add_category_handler()) #n
    dp.add_handler(add_utc_offset_handler()) #u
    dp.add_handler(CommandHandler('help', help_handler)) #h    
    dp.add_handler(CommandHandler('categories', show_categories_handler)) #c
    dp.add_handler(CommandHandler('expenses', show_expenses_handler)) #e
    logging.info(f'\n\n\n{datetime.datetime.now()}: Bot has started')
    ffbot.start_polling()
    ffbot.idle()


if __name__ == "__main__":
    main()

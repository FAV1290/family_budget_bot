import logging
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from constants import API_TOKEN, COMMANDS
from data_handlers import load_data, filter_user_data, get_expense_by_id
from categories import show_categories, add_category
from expenses import format_expenses_report, add_expense, update_expense


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def get_command_descriptions():
    commands_message = ''
    for command in COMMANDS.values():
        commands_message += f'{command}\n'
    return commands_message


def start_handler(update, context): 
    update.message.reply_text('Привет! Я помогаю вести семейный бюджет! Вот список доступных команд:', quote=False)
    update.message.reply_text(get_command_descriptions(), quote=False)


def help_handler(update, context):
    update.message.reply_text('Вам доступны следующие команды:', quote=False)
    update.message.reply_text(get_command_descriptions(), quote=False)


def make_categories_buttons(user_id, new_expense):
    categories = filter_user_data(load_data(), user_id)['categories']
    button_list = []
    for category in categories:
        button = InlineKeyboardButton(category.title(), callback_data = str(new_expense['expense_id']) + category)
        button_list.append(button)
    reply_markup = InlineKeyboardMarkup([button_list[index:index + 3] for index in range(0, len(button_list), 3)])
    return reply_markup


def expense_add_handler(update, context):
    expense, feedback = add_expense(update.message.chat.id, update.message.text)
    if expense is None or expense['category'] != 'разное':
        reply_markup = None
    else:
        reply_markup = make_categories_buttons(update.message.chat.id, expense)
        feedback += f'\nПожалуйста, выберите категорию расхода:'
    update.message.reply_text(feedback, quote=False, reply_markup=reply_markup)


def set_expense_category(update, context):
    target_id = update.callback_query.data[:36]
    target_category = update.callback_query.data[36:]
    target_expense = get_expense_by_id(target_id)
    update.callback_query.answer('Отличный выбор!')
    target_expense['category'] = target_category
    update_expense(target_expense)
    feedback = f"Новая расходная операция на сумму {target_expense['sum']} рублей"
    feedback += f"\nРасход добавлен в категорию {target_category.title()}"
    update.callback_query.edit_message_text(text=feedback)


def add_category_handler(update, context):
    categories_report = add_category(update.message.chat.id, update.message.text)
    update.message.reply_text(categories_report, quote=False)


def show_expenses_handler(update, context):
    expenses_report = format_expenses_report(update.message.chat.id)
    update.message.reply_text(expenses_report, quote=False)


def show_categories_handler(update, context):
    categories_report = show_categories(update.message.chat.id)
    update.message.reply_text(categories_report, quote=False)


def main():
    ffbot = Updater(API_TOKEN, use_context=True)
    dp = ffbot.dispatcher
    dp.add_handler(CommandHandler('start', start_handler))
    dp.add_handler(CommandHandler('help', help_handler))    
    dp.add_handler(CommandHandler('add', expense_add_handler))
    dp.add_handler(CallbackQueryHandler(set_expense_category))
    dp.add_handler(CommandHandler('add_category', add_category_handler))
    dp.add_handler(CommandHandler('categories', show_categories_handler))  
    dp.add_handler(CommandHandler('expenses', show_expenses_handler))
    logging.info(f'\n\n\n{datetime.datetime.now()}: Bot has started')
    ffbot.start_polling()
    ffbot.idle()


if __name__ == "__main__":
    main()

import logging
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from settings import API_TOKEN
from family_funds import get_command_descriptions, check_expense_string
from family_funds import add_category, add_categories, show_categories
from family_funds import make_expense, add_expense, format_expenses_report, find_expense_num_by_id
from family_funds import save_user_data, load_user_data


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def start_handler(update, context):
    update.message.reply_text('Привет! Я помогаю вести семейный бюджет! Вот список доступных команд:', quote=False)
    update.message.reply_text(get_command_descriptions(), quote=False)


def help_handler(update, context):
    update.message.reply_text('Вам доступны следующие команды:', quote=False)
    update.message.reply_text(get_command_descriptions(), quote=False)


def make_categories_buttons(categories, new_expense):
    button_list = []
    for category in categories:
        button = InlineKeyboardButton(category.title(), callback_data = new_expense['id'] + category)
        button_list.append(button)
    reply_markup = InlineKeyboardMarkup([button_list[i:i + 3] for i in range(0, len(button_list), 3)])
    return reply_markup


def expense_add_handler(update, context):
    context.chat_data.update(load_user_data(update.message.chat.id))
    expenses = context.chat_data.get('expenses')
    feedback = check_expense_string(update.message.text)
    if feedback == 'ok':
        new_expense = make_expense(update.message.text)
        context.chat_data['expenses'], feedback = add_expense(expenses, new_expense)
        reply_markup = make_categories_buttons(context.chat_data['categories'], new_expense)
        save_user_data(context.chat_data, update.message.chat.id)
        update.message.reply_text(feedback, quote=False, reply_markup=reply_markup)
    else:    
        update.message.reply_text(feedback, quote=False)


def set_expense_category(update, context):
    target_id = update.callback_query.data[:36]
    target_category = update.callback_query.data[36:]
    context.chat_data.update(load_user_data(update.callback_query.message.chat.id))
    update.callback_query.answer('Отличный выбор!')
    expense_num = find_expense_num_by_id(context.chat_data['expenses'], target_id)
    context.chat_data['expenses'][expense_num]['category'] = target_category
    save_user_data(context.chat_data, update.callback_query.message.chat.id)
    update.callback_query.edit_message_text(text=f"Расход добавлен в категорию {target_category.title()}")


def add_category_handler(update, context):
    context.chat_data.update(load_user_data(update.message.chat.id))
    categories = context.chat_data.get('categories')
    context.chat_data['categories'], feedback = add_category(categories, update.message.text)
    save_user_data(context.chat_data, update.message.chat.id)
    update.message.reply_text(feedback, quote=False)


def add_categories_handler(update, context):
    context.chat_data.update(load_user_data(update.message.chat.id))
    categories = context.chat_data.get('categories')
    context.chat_data['categories'], feedback = add_categories(categories, update.message.text)
    save_user_data(context.chat_data, update.message.chat.id)
    update.message.reply_text(feedback, quote=False)


def show_expenses_handler(update, context):
    context.chat_data.update(load_user_data(update.message.chat.id))
    expenses_report = format_expenses_report(context.chat_data['expenses'], update.message.chat.id)
    update.message.reply_text(expenses_report, quote=False)


def show_categories_handler(update, context):
    context.chat_data.update(load_user_data(update.message.chat.id))
    categories_report = show_categories(context.chat_data.get('categories'))
    update.message.reply_text(categories_report, quote=False)


def main():
    ffbot = Updater(API_TOKEN, use_context=True)
    dp = ffbot.dispatcher
    dp.add_handler(CommandHandler('start', start_handler))
    dp.add_handler(CommandHandler('help', help_handler))    
    dp.add_handler(CommandHandler('add', expense_add_handler))
    dp.add_handler(CallbackQueryHandler(set_expense_category))
    dp.add_handler(CommandHandler('add_cat', add_category_handler))
    dp.add_handler(CommandHandler('add_cats', add_categories_handler))
    dp.add_handler(CommandHandler('my_cats', show_categories_handler))  
    dp.add_handler(CommandHandler('expenses', show_expenses_handler))
    logging.info(f'\n\n\n{datetime.datetime.now()}: Bot has started')
    ffbot.start_polling()
    ffbot.idle()


if __name__ == "__main__":
    main()

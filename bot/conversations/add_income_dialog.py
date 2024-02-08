from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from constants import COMMANDS
from apps.incomes import add_income
from db.incomes import change_income_description
from bot.keyboards import make_true_false_question_buttons


AMOUNT, COMMENT_QUESTION, COMMENT_SET = range(3)


def start_greetings_stage(update, context):
    update.message.reply_text('Пожалуйста, введите сумму прихода:', quote=False)
    return AMOUNT


def start_amount_stage(update, context):
    new_income, feedback = add_income(update.message.chat.id, update.message.text)
    if feedback == 'ok':
        feedback = 'Приход успешно добавлен. Дополнить его описанием?'
        description_question_markup = make_true_false_question_buttons()    #А может сделать дату этой клавы булевой?
        context.chat_data['income_id'] = new_income.income_id
        update.message.reply_text(feedback, quote=False, reply_markup=description_question_markup)
        return COMMENT_QUESTION
    feedback += '\nЧтобы попробовать снова, повторно введите /boost_income'
    update.message.reply_text(feedback, quote=False)
    return ConversationHandler.END


def start_comment_question_stage(update, context):
    user_answer = update.callback_query.data
    update.callback_query.answer()
    if user_answer == 'no':
        update.callback_query.edit_message_text('Приход успешно добавлен')
        return ConversationHandler.END
    update.callback_query.edit_message_text('Хорошо. Введите описание для нового прихода:')
    return COMMENT_SET


def start_comment_set_stage(update, context):
    income_id = context.chat_data['income_id']
    change_income_description(income_id, update.message.text)
    update.message.reply_text('Описание успешно добавлено')
    return ConversationHandler.END


def start_cancel_stage(update, context):
    bot_message = [
        'Похоже, вам приглянулась другая команда.',
        'Сейчас я выйду из режима добавления прихода, чтобы ее можно было использовать.',
    ]
    update.message.reply_text(' '.join(bot_message), quote=False)
    return ConversationHandler.END


def add_income_handler():
    add_income_handler = ConversationHandler(
        entry_points=[CommandHandler('boost_income', start_greetings_stage)],
        states={
            AMOUNT: [MessageHandler(Filters.text & ~Filters.command, start_amount_stage)],
            COMMENT_QUESTION: [CallbackQueryHandler(start_comment_question_stage)],
            COMMENT_SET: [MessageHandler(Filters.text & ~Filters.command, start_comment_set_stage)],
        },
        fallbacks=[CommandHandler(COMMANDS.keys(), start_cancel_stage)],
        per_user=False,
    )
    return add_income_handler

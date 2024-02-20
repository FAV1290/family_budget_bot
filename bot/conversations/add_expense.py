from telegram import Update
from telegram.ext import ContextTypes, filters, ConversationHandler, CommandHandler, MessageHandler

from bot.conversations.enums import AddExpenseConversationState


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Введите сумму расхода или /cancel для отмены:')
    return AddExpenseConversationState.AMOUNT


async def process_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    raw_amount = update.message.text
    await update.message.reply_text(f'Вы ввели следующую сумму: {raw_amount}')   
    return ConversationHandler.END


async def toggle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Галя, у нас отмена!') 
    return ConversationHandler.END


add_expense_handler = ConversationHandler(
    entry_points=[CommandHandler('add', start_conversation)],
    states={
        AddExpenseConversationState.AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_amount)],
    },
    fallbacks=[CommandHandler('cancel', toggle_cancel)],
    )

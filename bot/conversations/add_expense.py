import re
import uuid
import typing

from telegram import Update
from telegram.ext import (
    ContextTypes, filters, ConversationHandler,
    CommandHandler, MessageHandler, CallbackQueryHandler,
)

from db.models import Profile, Expense
from bot.conversations.enums import AddExpenseState
from utils.validators import is_amount_str_valid
from bot.keyboards import create_user_categories_keyboard, create_yes_or_no_keyboard


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message
    await update.message.reply_text('Введите сумму расхода (целое число) или /cancel для отмены:')
    return AddExpenseState.AMOUNT


async def process_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message and update.effective_chat
    assert context.chat_data is not None
    amount_str = re.sub(r'\.|,|\s', '', update.message.text or '')
    if is_amount_str_valid(amount_str):
        context.chat_data.update({'new_expense': {'amount': int(amount_str)}})
        current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        await update.message.reply_text(
            'В какую категорию добавить расход?',
            reply_markup=create_user_categories_keyboard(current_profile.categories),
        )
        return AddExpenseState.CATEGORY
    await update.message.reply_text('Некорректная сумма! Попробуйте еще раз:')
    return AddExpenseState.AMOUNT


async def process_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.callback_query and context.chat_data
    query = update.callback_query
    target_category_id = uuid.UUID(query.data) if query.data != 'None' else None
    context.chat_data['new_expense']['category_id'] = target_category_id
    await query.answer()
    await query.edit_message_text(
        'Принято. Добавить комментарий к расходу?',
        reply_markup=create_yes_or_no_keyboard(),
    )
    return AddExpenseState.DESCRIPTION_CHOICE


async def process_description_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.callback_query and update.effective_chat and context.chat_data
    query = update.callback_query
    await query.answer()
    if query.data == 'yes':
        await query.edit_message_text('Введите текст комментария:')
        return AddExpenseState.DESCRIPTION_SET
    Expense.create(profile_id=update.effective_chat.id, **context.chat_data['new_expense'])
    await query.edit_message_text('Расход успешно добавлен!')
    return ConversationHandler.END


async def process_description_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message and update.effective_chat and context.chat_data
    context.chat_data['new_expense']['description'] = update.message.text
    Expense.create(profile_id=update.effective_chat.id, **context.chat_data['new_expense'])
    await update.message.reply_text('Расход успешно добавлен!')
    return ConversationHandler.END


async def toggle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message
    await update.message.reply_text('Галя, у нас отмена!')
    return ConversationHandler.END


def get_expense_add_handler_params() -> dict[str, typing.Any]:
    return {
        'entry_points': [CommandHandler('add', start_conversation)],
        'states': {
            AddExpenseState.AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_amount),
            ],
            AddExpenseState.CATEGORY: [CallbackQueryHandler(process_category)],
            AddExpenseState.DESCRIPTION_CHOICE: [CallbackQueryHandler(process_description_choice)],
            AddExpenseState.DESCRIPTION_SET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_description_set),
            ],
        },
        'fallbacks': [CommandHandler('cancel', toggle_cancel)],
    }

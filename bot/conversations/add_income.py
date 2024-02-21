import typing

from telegram import Update
from telegram.ext import (
    ContextTypes, filters, ConversationHandler,
    CommandHandler, MessageHandler, CallbackQueryHandler,
)

from db.models import Profile, Income
from utils.validators import is_amount_str_valid
from bot.conversations.enums import AddIncomeState
from bot.keyboards import create_yes_or_no_keyboard


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message
    await update.message.reply_text('Введите сумму прихода (целое число) или /cancel для отмены:')
    return AddIncomeState.AMOUNT


async def process_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message and update.message.text and context.chat_data is not None
    amount_str = update.message.text.replace(' ', '').replace(',', '').replace('.', '')
    if is_amount_str_valid(amount_str):
        context.chat_data.update({'new_income': {'amount': int(amount_str)}})
        await update.message.reply_text(
            'Добавить к приходу комментарий?',
            reply_markup=create_yes_or_no_keyboard(),
        )
        return AddIncomeState.DESCRIPTION_CHOICE
    await update.message.reply_text('Некорректная сумма! Попробуйте еще раз:')
    return AddIncomeState.AMOUNT


async def process_description_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.callback_query and update.effective_chat and context.chat_data
    query = update.callback_query
    await query.answer()
    if query.data == 'yes':
        await query.edit_message_text('Введите текст комментария:')
        return AddIncomeState.DESCRIPTION_SET
    current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
    Income.create(profile_id=current_profile.id, **context.chat_data['new_income'])
    await query.edit_message_text('Приход успешно добавлен!')
    return ConversationHandler.END


async def process_description_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message and update.effective_chat and context.chat_data
    context.chat_data['new_income']['description'] = update.message.text
    current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
    Income.create(profile_id=current_profile.id, **context.chat_data['new_income'])
    await update.message.reply_text('Приход успешно добавлен!')
    return ConversationHandler.END


async def toggle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message
    await update.message.reply_text('Галя, у нас отмена!')
    return ConversationHandler.END


def get_income_add_handler_params() -> dict[str, typing.Any]:
    return {
        'entry_points': [CommandHandler('boost_income', start_conversation)],
        'states': {
            AddIncomeState.AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_amount),
            ],
            AddIncomeState.DESCRIPTION_CHOICE: [CallbackQueryHandler(process_description_choice)],
            AddIncomeState.DESCRIPTION_SET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_description_set),
            ],
        },
        'fallbacks': [CommandHandler('cancel', toggle_cancel)],
    }

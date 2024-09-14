import re
import uuid
import typing

from telegram import Update
from telegram.ext import (
    ContextTypes, filters, ConversationHandler,
    CommandHandler, CallbackQueryHandler, MessageHandler,
)

from db.models import Profile, Category
from utils.validators import is_amount_str_valid
from bot.keyboards import create_user_categories_keyboard
from bot.conversations.enums import UpdateCategoryLimitState


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message and update.effective_chat
    profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
    await update.message.reply_text(
        "Выберите категорию, для которой нужно установить лимит, или введите /cancel для отмены:",
        reply_markup=create_user_categories_keyboard(profile.categories, add_none_button=False),
    )
    return UpdateCategoryLimitState.CATEGORY


async def process_category_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.callback_query and context.chat_data is not None
    query = update.callback_query
    target_category_id = uuid.UUID(query.data) if query.data != "None" else None
    context.chat_data.update({"new_category_limit": {"category_id": target_category_id}})
    await query.answer()
    await query.edit_message_text(
        "Теперь напишите целое число:\n"
        "• Чтобы задать лимит, не добавляйте к нему никаких символов.\n"
        "• Чтобы увеличить текущий лимит на введенное число — поставьте перед ним «+».\n"
        "• Чтобы уменьшить — поставьте перед введенным числом «-»."
    )
    return UpdateCategoryLimitState.LIMIT


async def process_category_limit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message and context.chat_data is not None
    operation_marker_str = update.message.text[0] if update.message.text else ""
    limit_str = re.sub(r"\.|,|\+|-|\s", "", update.message.text or "")
    if is_amount_str_valid(limit_str):
        target_category_id = context.chat_data["new_category_limit"]["category_id"]
        target_category = Category.fetch_by_id(target_category_id)
        if not target_category:
            await update.message.reply_text("Категория не найдена. Изменение лимита отменено.")
            return UpdateCategoryLimitState.LIMIT
        if operation_marker_str == "+":
            new_limit = int(limit_str) + (target_category.limit or 0)
        elif operation_marker_str == "-":
            difference = (target_category.limit or 0) - int(limit_str)
            new_limit = difference if difference > 0 else 0
        else:
            new_limit = int(limit_str)
        target_category.update_limit(new_limit)
        await update.message.reply_text("Лимит успешно установлен!")
        return ConversationHandler.END
    await update.message.reply_text("Некорректный лимит! Попробуйте еще раз:")
    return UpdateCategoryLimitState.LIMIT


async def toggle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message
    await update.message.reply_text("Галя, у нас отмена!")
    return ConversationHandler.END


def get_update_category_limit_handler_params() -> dict[str, typing.Any]:
    return {
        "entry_points": [CommandHandler("limit_category", start_conversation)],
        "states": {
            UpdateCategoryLimitState.CATEGORY: [CallbackQueryHandler(process_category_choice)],
            UpdateCategoryLimitState.LIMIT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_category_limit),
            ],
        },
        "fallbacks": [CommandHandler("cancel", toggle_cancel)],
    }

import re
import typing

from telegram import Update
from telegram.ext import (
    ContextTypes, filters, ConversationHandler,
    CommandHandler, MessageHandler, CallbackQueryHandler,
)

from db.models import Profile, Category
from bot.conversations.enums import AddCategoryState
from bot.keyboards import create_yes_or_no_keyboard
from utils.validators import is_category_name_valid, is_amount_str_valid


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message
    await update.message.reply_text("Введите название категории или /cancel для отмены:")
    return AddCategoryState.NAME


async def process_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message and update.effective_chat
    assert context.chat_data is not None
    name_str = update.message.text or ""
    current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
    profile_categories_names = [category.name for category in current_profile.categories]
    if is_category_name_valid(name_str, profile_categories_names):
        context.chat_data.update({"new_category": {"name": name_str}})
        await update.message.reply_text(
            "Записал. Хотите задать лимит этой категории?",
            reply_markup=create_yes_or_no_keyboard(),
        )
        return AddCategoryState.LIMIT_CHOICE
    await update.message.reply_text("Некорректное название! Попробуйте еще раз:")
    return AddCategoryState.NAME


async def process_limit_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.callback_query and update.effective_chat and context.chat_data
    query = update.callback_query
    await query.answer()
    if query.data == "yes":
        await query.edit_message_text("Введите лимит:")
        return AddCategoryState.LIMIT_SET
    Category.create(profile_id=update.effective_chat.id, **context.chat_data["new_category"])
    await query.edit_message_text("Категория успешно добавлена!")
    return ConversationHandler.END


async def process_limit_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message and update.effective_chat
    assert context.chat_data is not None
    limit_str = re.sub(r"\.|,|\s", "", update.message.text or "")
    if is_amount_str_valid(limit_str):
        context.chat_data["new_category"]["limit"] = int(limit_str)
        Category.create(profile_id=update.effective_chat.id, **context.chat_data["new_category"])
        await update.message.reply_text("Категория успешно добавлена!")
        return ConversationHandler.END
    await update.message.reply_text("Некорректный лимит! Попробуйте еще раз:")
    return AddCategoryState.LIMIT_SET


async def toggle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message
    await update.message.reply_text("Галя, у нас отмена!")
    return ConversationHandler.END


def get_category_add_handler_params() -> dict[str, typing.Any]:
    return {
        "entry_points": [CommandHandler("new_category", start_conversation)],
        "states": {
            AddCategoryState.NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_name),
            ],
            AddCategoryState.LIMIT_CHOICE: [CallbackQueryHandler(process_limit_choice)],
            AddCategoryState.LIMIT_SET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_limit_set),
            ],
        },
        "fallbacks": [CommandHandler("cancel", toggle_cancel)],
    }

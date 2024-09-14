import typing
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler

from db.models import Profile
from bot.conversations.enums import UTCRegion
from bot.conversations.enums import UpdateUTCOffsetState
from bot.keyboards import create_utc_regions_keyboard, create_utc_offsets_keyboard


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message
    await update.message.reply_text(
        "Выберите регион, в котором находитесь, или введите /cancel для отмены:",
        reply_markup=create_utc_regions_keyboard(),
    )
    return UpdateUTCOffsetState.REGION


async def process_region_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.callback_query
    query = update.callback_query
    chosen_region = query.data
    await query.answer()
    await query.edit_message_text(
        "Теперь выберите ваши текущие дату и время:",
        reply_markup=create_utc_offsets_keyboard(UTCRegion(chosen_region).get_offsets()),
    )
    return UpdateUTCOffsetState.UTC_OFFSET


async def process_utc_offset_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.callback_query and update.effective_chat
    current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
    query = update.callback_query
    new_utc_offset = int(query.data) if query.data else 0
    await query.answer()
    current_profile.set_utc_offset(new_utc_offset)
    now = (datetime.utcnow() + timedelta(hours=new_utc_offset)).strftime("%d-%m-%Y %H:%M")
    await query.edit_message_text(f"Часовой пояс успешно установлен! Текущие дата и время: {now}")
    return ConversationHandler.END


async def toggle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message
    await update.message.reply_text("Галя, у нас отмена!")
    return ConversationHandler.END


def get_update_utc_offset_handler_params() -> dict[str, typing.Any]:
    return {
        "entry_points": [CommandHandler("utc_offset", start_conversation)],
        "states": {
            UpdateUTCOffsetState.REGION: [CallbackQueryHandler(process_region_choice)],
            UpdateUTCOffsetState.UTC_OFFSET: [CallbackQueryHandler(process_utc_offset_choice)],
        },
        "fallbacks": [CommandHandler("cancel", toggle_cancel)],
    }

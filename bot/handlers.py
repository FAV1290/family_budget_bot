from telegram import Update
from telegram.ext import ContextTypes

from db.models import Category, Profile
from constants import START_MESSAGE, COMMANDS


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.effective_message:
        Profile.fetch_by_id_or_create(update.effective_message.chat_id)
        await update.message.reply_text(START_MESSAGE)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        text_lines = [f'• /{command} — {description}' for command, description in COMMANDS.items()]
        await update.message.reply_text('Вам доступны следующие команды:')
        await update.message.reply_text('\n'.join(text_lines))


async def category_add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message and update.message.text:
        current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        new_category_name = update.message.text.split(maxsplit=1)[1]
        Category.create(profile_id=current_profile.id, name=new_category_name)
        print(current_profile.categories)

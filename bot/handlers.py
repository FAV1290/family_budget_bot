from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ContextTypes

from constants import START_MESSAGE, COMMANDS
from db.models import Category, Profile, Income, Expense


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.effective_message:
        Profile.fetch_by_id_or_create(update.effective_message.chat_id)
        await update.message.reply_text(START_MESSAGE)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        text_lines = [f'• /{command} — {description}' for command, description in COMMANDS.items()]
        await update.message.reply_text('Вам доступны следующие команды:')
        await update.message.reply_text('\n'.join(text_lines))


# Add validators and transform to ConversationHandler
async def category_add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message and update.message.text:
        current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        new_category_name = update.message.text.split(maxsplit=1)[1]
        Category.create(profile_id=current_profile.id, name=new_category_name)


# Add validators and transform to ConversationHandler
async def income_add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message and update.message.text:
        current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        new_income_amount, new_income_description = update.message.text.split(maxsplit=2)[1:]
        Income.create(
            profile_id=current_profile.id,
            amount=new_income_amount,
            description=new_income_description,
        )


# Add validators and transform to ConversationHandler
async def expense_add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message and update.message.text:
        current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        new_expense_amount, new_expense_description = update.message.text.split(maxsplit=2)[1:]
        Expense.create(
            profile_id=current_profile.id,
            amount=new_expense_amount,
            description=new_expense_description,
        )


# Add validators and transform to ConversationHandler
async def utc_offset_set_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message and update.message.text:
        current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        new_utc_offset = int(update.message.text.split(maxsplit=1)[1])
        current_profile.set_utc_offset(new_utc_offset)
        now = (datetime.utcnow() + timedelta(hours=new_utc_offset)).strftime('%d-%m-%Y %H:%M:%S')
        await update.message.reply_text(
            f'Часовой пояс успешно изменен. Ваши текущие дата и время: {now}')


async def rm_last_expense_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message:
        current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        if current_profile.expenses:
            target_expense = current_profile.expenses[-1]
            target_expense_str = str(target_expense)
            target_expense.delete()
            print(target_expense.amount)
            await update.message.reply_text('Удален расход со следующими параметрами:')
            await update.message.reply_text(target_expense_str)
        else:
            await update.message.reply_text('Расходы не найдены \U0001F937')

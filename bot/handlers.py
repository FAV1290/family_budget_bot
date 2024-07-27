from telegram import Update
from telegram.ext import ContextTypes

from utils.reports import (
    compose_current_incomes_report,
    compose_current_expenses_report,
    compose_user_categories_report,
)
from constants import START_MESSAGE, COMMANDS
from db.models import Profile, Income, Expense


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.effective_message:
        Profile.fetch_by_id_or_create(update.effective_message.chat_id)
        await update.message.reply_text(START_MESSAGE)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        text_lines = [f"• /{command} — {description}" for command, description in COMMANDS.items()]
        await update.message.reply_text("Вам доступны следующие команды:")
        await update.message.reply_text("\n".join(text_lines))


async def rm_last_expense_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message:
        current_profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        if current_profile.expenses:
            target_expense = current_profile.expenses[-1]
            target_expense_str = str(target_expense)
            target_expense.delete()
            await update.message.reply_text("Удален расход со следующими параметрами:")
            await update.message.reply_text(target_expense_str)
        else:
            await update.message.reply_text("Расходы не найдены \U0001F937")


async def incomes_report_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message:
        profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        incomes = Income.fetch_current_period_objects(profile.id, profile.utc_offset)
        await update.message.reply_text(compose_current_incomes_report(incomes, profile.utc_offset))


async def expenses_report_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message:
        profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        incomes = Income.fetch_current_period_objects(profile.id, profile.utc_offset)
        expenses = Expense.fetch_current_period_objects(profile.id, profile.utc_offset)
        await update.message.reply_text(
            compose_current_expenses_report(expenses, incomes, profile.utc_offset))


async def categories_report_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.message:
        profile = Profile.fetch_by_id_or_create(update.effective_chat.id)
        incomes = Income.fetch_current_period_objects(profile.id, profile.utc_offset)
        expenses = Expense.fetch_current_period_objects(profile.id, profile.utc_offset)
        await update.message.reply_text(
            compose_user_categories_report(incomes, expenses, profile.categories))

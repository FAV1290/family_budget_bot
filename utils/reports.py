from typing import Sequence
from datetime import timedelta

from db.models import Income


def compose_current_incomes_report(current_incomes: Sequence[Income], utc_offset: int = 0) -> str:
    incomes_sum = sum([income.amount for income in current_incomes])
    report = f'Общий бюджет текущего периода: {incomes_sum} руб.\n'
    report += 'Он формируется из следующих приходов:' if current_incomes else ''
    for income in current_incomes:
        created_at_str = (income.created_at + timedelta(utc_offset)).strftime('%d.%m.%y, %H:%M')
        report += f'\n• ({created_at_str}): +{income.amount} руб.'
        report += f' ({income.description.capitalize()})' if income.description else ''
    return report

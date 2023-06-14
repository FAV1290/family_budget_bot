import datetime
from constants import COMMANDS


def get_command_descriptions():
    commands_message = ''
    for command in COMMANDS.values():
        commands_message += f"{command}\n"
    return commands_message


def check_outlay_string(user_string):
    user_string = user_string.split()
    feedback = 'ok'
    if len(user_string) == 1:
        return f'Вы забыли указать сумму. Примеры правильного ввода:\n"/sum 100 мороженка" или "/sum 500".'
    try:
        if int(user_string[1]) <= 0:
            feedback = f'Сумма расхода должна быть больше нуля.'
    except ValueError:
        feedback = f'Задана некорректная сумма. Примеры правильного ввода:\n"/sum 100 мороженка" или "/sum 500".'
    return feedback


def make_outlay(user_string):
    sum = user_string.split()[1]
    if len(user_string.split()) == 2:
        description = None
    else:
        description = user_string[(len(sum) + 6):]
    outlay = {
        'id' : '',  # Продумать и добавить генерацию id позднее
        'when' : datetime.datetime.now(),   # В дальнейшем заменить на UTC
        'sum' : sum,
        'category' : '',    # Когда я освою InlineKeyboardMarkup, здесь появятся категории
        'description' : description,
    }
    return outlay


def add_outlay(outlays_list, new_outlay):
    if outlays_list is None:
        outlays_list = []
    outlays_list.append(new_outlay)
    feedback = f"Новая расходная операция:\n"
    feedback += f"Сумма: {new_outlay['sum']} руб."
    if new_outlay['description'] is not None:
        feedback += f"\nКомментарий: {new_outlay['description']}"
    return outlays_list, feedback


def format_outlays_report(outlays_list):
    report = ''
    for outlay in outlays_list:
        report += f"• ({outlay['when'].strftime('%d.%m.%y, %H:%M')}): -{outlay['sum']} руб."
        if outlay['description'] is not None:
            report += f" ({outlay['description']})"
        report += '\n'
    return report

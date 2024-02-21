from enum import IntEnum


class AddExpenseState(IntEnum):
    START = 0
    AMOUNT = 1
    CATEGORY = 2
    DESCRIPTION_CHOICE = 3
    DESCRIPTION_SET = 4

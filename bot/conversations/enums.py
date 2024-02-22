from enum import IntEnum


class AddExpenseState(IntEnum):
    AMOUNT = 1
    CATEGORY = 2
    DESCRIPTION_CHOICE = 3
    DESCRIPTION_SET = 4


class AddIncomeState(IntEnum):
    AMOUNT = 1
    DESCRIPTION_CHOICE = 2
    DESCRIPTION_SET = 3


class AddCategoryState(IntEnum):
    NAME = 1
    LIMIT_CHOICE = 2
    LIMIT_SET = 3

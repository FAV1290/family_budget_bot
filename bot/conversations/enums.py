from enum import IntEnum


class AddExpenseConversationState(IntEnum):
    START = 0
    AMOUNT = 1
    DESCRIPTION = 2
    CATEGORY = 3
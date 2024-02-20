def is_expense_amount_valid(raw_amount: str) -> bool:
    return all([
        raw_amount.isdigit(),
        raw_amount[0] != '0',
        int(raw_amount) > 0,
    ])
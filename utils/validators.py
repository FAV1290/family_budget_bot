def is_expense_amount_valid(raw_amount_str: str) -> bool:
    amount_str = raw_amount_str.replace(' ', '').replace(',', '').replace('.', '')
    if not amount_str:
        return False
    validity_conditions = [amount_str.isdigit(), amount_str[0] != '0']
    return all(validity_conditions)

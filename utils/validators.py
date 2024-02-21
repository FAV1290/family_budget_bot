def is_amount_str_valid(amount_str: str) -> bool:
    if not amount_str:
        return False
    validity_conditions = [amount_str.isdigit(), amount_str[0] != '0']
    return all(validity_conditions)

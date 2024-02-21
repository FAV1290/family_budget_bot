import pytest

from utils.validators import is_amount_str_valid


@pytest.mark.parametrize(
    'raw_amount',
    [
        pytest.param('', id='blank string'),
        pytest.param(' ', id='lonely space symbol'),
        pytest.param('-', id='lonely minus symbol'),
        pytest.param('b', id='lonely non-digit symbol'),
        pytest.param('0', id='lonely zero digit'),
        pytest.param('      ', id='spaces sequence'),
        pytest.param('00000000000', id='zeroes sequence'),
        pytest.param('012', id='leading by zero digit sequence'),
        pytest.param('0ABCDEFG', id='leading by zero non-digit sequence'),
        pytest.param('ABCDEFG', id='non-digit sequence'),
        pytest.param('-100', id='negative amount'),
        pytest.param('+100', id='positive amount with plus symbol'),
        pytest.param('\u0001', id='non-digit unicode symbol with digit code'),
        pytest.param('123 456', id='digit sequence with space'),
        pytest.param('234 567 890', id='digit sequence with spaces'),
        pytest.param(' 123', id='digit sequence with leading space'),
        pytest.param('123 ', id='digit sequence with trailing space'),
        pytest.param('123.456.789', id='digit sequence with dot delimiters'),
        pytest.param('123,456,789', id='digit sequence with comma delimiters'),
    ],
)
def test__is_amount_str_valid__false_cases(raw_amount: str) -> None:
    assert not is_amount_str_valid(raw_amount)


@pytest.mark.parametrize(
    'raw_amount',
    [
        pytest.param('\u0031', id='digit unicode symbol with digit code'),
        pytest.param('1', id='lonely non-zero digit'),
        pytest.param('12345', id='valid input without zeroes'),
        pytest.param('10000', id='valid input with zeroes'),
    ],
)
def test__is_amount_str_valid__true_cases(raw_amount: str) -> None:
    assert is_amount_str_valid(raw_amount)

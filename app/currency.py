from flask import current_app
from decimal import Decimal, ROUND_HALF_UP
from .const import DEFAULT_CURRENCY


def round_accurate(num, decimal):
    str_deci = 1
    for _ in range(decimal):
        str_deci = str_deci / 10
    str_deci = str(str_deci)
    result = Decimal(str(num)).quantize(
        Decimal(str_deci), rounding=ROUND_HALF_UP)
    result = float(result)
    return result


def parameter_check(params, currency_data):

    source = params.get('source', default='', type=str).upper()
    target = params.get('target', default='', type=str).upper()
    amount = params.get('amount', type=str)
    if amount == None:
        raise Exception("amount is missing.")
    amount = float(amount.replace('$', '').replace(',', ''))
    if amount < 0:
        raise Exception('amount needs to be greater or equal than 0')
    if source in currency_data['currencies'] and target in currency_data['currencies'][source]:
        return source, target, amount
    raise Exception('source or target not exists')


def get_currency_data():
    if current_app.config['IS_DEFAULT_CURRENCY_DATA']:
        return DEFAULT_CURRENCY
    # TODO: add different sources to get the currency data


def convert(params):
    currency_data = get_currency_data()
    parameters = parameter_check(params, currency_data)
    source, target, amount = parameters
    currency = currency_data['currencies'][source][target]
    converted = round_accurate(amount * currency, 2)
    # TODO: check range of input amount correspond to currency
    return {'msg': 'success',
            'amount': '${:,}'.format(converted)
            }

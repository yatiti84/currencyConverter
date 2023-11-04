from flask import current_app


def parameter_check(params, currency_data):

    source = params.get('source', default="", type=str)
    target = params.get('target', default="", type=str)
    amount = params.get('amount', default="0", type=str)
    amount = int(amount.replace('$', '').replace(',', ''))
    if source in currency_data['currencies'] and target in currency_data['currencies'][source]:
        return source, target, amount
    return False


def get_currency_data():
    if current_app.config['CURRENCY_MODE'] is False:
        return current_app.config['DEFAULT_CURRENCY']
    # can add more sources to get the currency data


def convert(params):
    currency_data = get_currency_data()
    parameters = parameter_check(params, currency_data)
    if parameters:
        source, target, amount = parameters
        currency = currency_data['currencies'][source][target]
        converted = round(amount * currency, 2)
        return {"msg": "success",
                "amount": "${:,}".format(converted)
                }

    else:
        return {"msg": "fail",
                "amount": "$0"
                }


# if __name__ == '__main__':
    # parameter = {
    #     'source':'USD',
    #     'target': 'JPY',
    #     amount: '$1,525'
    # }
    # convert(parameter)

from decimal import Decimal


def create_options_ticker(ticker, strike, expiration_year, expiration_month, expiration_day, contract_type):
    ticker = str(ticker).upper()
    strike = str(strike)
    expiration_year = str(expiration_year).zfill(2)
    expiration_month = str(expiration_month).zfill(2)
    expiration_day = str(expiration_day).zfill(2)
    contract_type = 'C' if contract_type else 'P'

    strike_d = Decimal(strike)
    num_dec = strike_d.as_tuple().exponent
    length_strike = len(strike.replace('.', ''))

    if num_dec == 0:
        strike_string_for_insertion = f'{strike.replace(".", "").zfill(8)}'
    elif num_dec == -1:
        strike_string_for_insertion = f'{strike.replace(".", "").zfill(6)}00'
    elif num_dec == -2:
        strike_string_for_insertion = f'{strike.replace(".", "").zfill(4)}0000'
    else:
        raise ValueError("Invalid strike format")

    expiry = f'{expiration_year}{expiration_month}{expiration_day}'
    options_ticker = f'O:{ticker}{expiry}{contract_type}{strike_string_for_insertion}'

    return options_ticker

# Example optionsTicker = 'O:AAPL230915C00170000'


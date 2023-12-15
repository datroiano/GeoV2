from time_functions import from_unix_time, to_unix_time


class SingleOptionStrategy:
    def __init__(self, cleaned_data):
        self.cleaned_data = {data['unix_time']: data for data in cleaned_data}

    def get_price_at_time(self, target_time, pricing):
        if target_time in self.cleaned_data:
            if pricing == 0:
                return self.cleaned_data[target_time]['low']
            elif pricing == 1:
                return round((self.cleaned_data[target_time]['low'] + self.cleaned_data[target_time]['high']) / 2,
                             ndigits=2)
            elif pricing == 2:
                return self.cleaned_data[target_time]['high']
        else:
            closest_time = min(filter(lambda t: t > target_time, self.cleaned_data))
            return self.get_price_at_time(closest_time, pricing)

    def calculate_profit_timed_entry(self, entry_time, exit_time, size=1, pricing=1):
        entry_time = int(to_unix_time(entry_time))
        exit_time = int(to_unix_time(exit_time))

        entry_price = self.get_price_at_time(entry_time, pricing)
        exit_price = self.get_price_at_time(exit_time, pricing)

        entry_value = int(size) * entry_price
        exit_value = int(size) * exit_price
        profit_loss_dollars = round(exit_value - entry_value, ndigits=2)

        if entry_value != 0:
            profit_loss_percent = round(profit_loss_dollars / entry_value, ndigits=2)
        else:
            profit_loss_percent = 0

        trade_array = {
            "trade_data": {
                "entry_price": entry_price,
                "entry_time": from_unix_time(entry_time),
                "exit_price": exit_price,
                "exit_time": from_unix_time(exit_time),
                "entry_value": entry_value,
                "exit_value": exit_value,
                "profit_loss_dollars": profit_loss_dollars,
                "profit_loss_percent": profit_loss_percent,
                "size": size,
                "pricing": pricing
            }
        }

        return trade_array

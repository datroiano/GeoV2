from time_functions import from_unix_time, to_unix_time
import options_contract as oc


class TwoOptionStrategy:
    def __init__(self, cleaned_data_op_1, cleaned_data_op_2):
        self.op_1_data = cleaned_data_op_1
        self.op_2_data = cleaned_data_op_2

    @staticmethod
    def filter_data(data, window_start, window_end):
        window_start = int(to_unix_time(window_start))
        window_end = int(to_unix_time(window_end))
        return [value for value in data.values() if window_start <= value['unix_time'] <= window_end]

    @staticmethod
    def combine_data(data_1, data_2, pricing):
        if pricing == 0:
            return [(item1['unix_time'], item1['low'] + item2['low'], item1['volume'] + item2['volume'])
                    for item1 in data_1 for item2 in data_2 if item1['unix_time'] == item2['unix_time']]
        elif pricing == 1:
            return [(item1['unix_time'], ((item1['low'] + item1['high']) / 2) + ((item2['low'] + item2['high']) / 2),
                     item1['volume'] + item2['volume'])
                    for item1 in data_1 for item2 in data_2 if item1['unix_time'] == item2['unix_time']]
        elif pricing == 2:
            return [(item1['unix_time'], item1['high'] + item2['high'], item1['volume'] + item2['volume'])
                    for item1 in data_1 for item2 in data_2 if item1['unix_time'] == item2['unix_time']]
        else:
            return None  # Pricing selection is not 0, 1, or 2

    def long_strangle_simulation(self, entry_window_start, entry_window_end, exit_window_start, exit_window_end,
                                 size=1, pricing=1):
        entry_data_1 = self.filter_data(self.op_1_data, entry_window_start, entry_window_end)
        exit_data_1 = self.filter_data(self.op_1_data, exit_window_start, exit_window_end)
        entry_data_2 = self.filter_data(self.op_2_data, entry_window_start, entry_window_end)
        exit_data_2 = self.filter_data(self.op_2_data, exit_window_start, exit_window_end)

        combined_entry_data = self.combine_data(entry_data_1, entry_data_2, pricing)
        combined_exit_data = self.combine_data(exit_data_1, exit_data_2, pricing)

        if combined_entry_data is None or combined_exit_data is None:
            return None

        simulation_data = []
        for item1 in combined_entry_data:
            for item2 in combined_exit_data:
                if item1[0] < item2[0]:
                    entry_time = from_unix_time(item1[0])
                    exit_time = from_unix_time(item2[0])
                    entry_strategy_value = round(item1[1] * size, ndigits=2)
                    entry_trading_volume = round(item1[2], ndigits=2)
                    exit_strategy_value = round(item2[1] * size, ndigits=2)
                    exit_trading_volume = round(item2[2], ndigits=2)
                    profit_loss_dollars = round((item2[1] - item1[1]) * size, ndigits=2)
                    profit_loss_percent = round(((item2[1] - item1[1]) * size / item1[1]), ndigits=4)

                    simulation_data.append({
                        'entry_time': entry_time,
                        'exit_time': exit_time,
                        'entry_strategy_value': entry_strategy_value,
                        'entry_trading_volume': entry_trading_volume,
                        'exit_strategy_value': exit_strategy_value,
                        'exit_trading_volume': exit_trading_volume,
                        'profit_loss_dollars': profit_loss_dollars,
                        'profit_loss_percent': profit_loss_percent
                    })

        return simulation_data



ticker = 'CRM'
trade_date = '2023-11-29'
expirations = '2023-12-01'
strike1 = 250
strike2 = strike1


contract1 = oc.OptionsContract(ticker, strike1, expirations, is_call=True)
contract1data = oc.OptionsContractsPriceData(options_contract=contract1,
                                             from_date=trade_date, to_date=trade_date,
                                             window_start_time='09:30:00', window_end_time='16:30:00',
                                             timespan='minute')

contract2 = oc.OptionsContract(ticker, strike2, expirations, is_call=False)
contract2data = oc.OptionsContractsPriceData(options_contract=contract1,
                                             from_date=trade_date, to_date=trade_date,
                                             window_start_time='09:30:00', window_end_time='16:30:00',
                                             timespan='minute')

simulation = TwoOptionStrategy(contract1data.pull_options_price_data(), contract2data.pull_options_price_data())
long_straddle_example = simulation.long_strangle_simulation(entry_window_start=f'{trade_date} 09:30:00',
                                                            entry_window_end=f'{trade_date} 11:30:00',
                                                            exit_window_start=f'{trade_date} 14:30:00',
                                                            exit_window_end=f'{trade_date} 16:00:00')

print(contract1data.pull_options_price_data())
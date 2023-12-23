from strangle_simulation_inputs_from_earnings import TestCompanies
import options_contract as oc
from two_contract_strategy import TwoOptionStrategy
from strategy_meta_analysis import MetaAnalysis
import statistics


def companies_bulk_simulation(corrected_strikes, entry_start, entry_end, exit_start, exit_end, pricing=1):
    master_out = []
    j = 0  # Actually used iteration counter (non-error)
    for i, item in enumerate(corrected_strikes, start=1):
        ticker = item.get('symbol')
        strike1 = item.get('target_strike')
        strike2 = item.get('target_strike')
        expirations = item.get('target_expiration_date')
        trade_date = item.get('trade_date')

        contract1 = oc.OptionsContract(ticker, strike1, expirations, is_call=True)
        contract1data = oc.OptionsContractsPriceData(options_contract=contract1,
                                                     from_date=trade_date, to_date=trade_date,
                                                     window_start_time='09:30:00', window_end_time='16:30:00',
                                                     timespan='minute')

        contract2 = oc.OptionsContract(ticker, strike2, expirations, is_call=False)
        contract2data = oc.OptionsContractsPriceData(options_contract=contract2,
                                                     from_date=trade_date, to_date=trade_date,
                                                     window_start_time='09:30:00', window_end_time='16:30:00',
                                                     timespan='minute')

        simulation = TwoOptionStrategy(contract1data.pull_options_price_data(),
                                       contract2data.pull_options_price_data())
        long_straddle = simulation.long_strangle_simulation(entry_window_start=f'{trade_date} {entry_start}',
                                                            entry_window_end=f'{trade_date} {entry_end}',
                                                            exit_window_start=f'{trade_date} {exit_start}',
                                                            exit_window_end=f'{trade_date} {exit_end}',
                                                            pricing=pricing)

        j += 1

        meta_data = MetaAnalysis(long_straddle)
        profit_loss_percent_table = meta_data.profit_loss_percent_table()
        avg_return = statistics.mean(profit_loss_percent_table) if profit_loss_percent_table else 0
        variance = statistics.variance(profit_loss_percent_table) if profit_loss_percent_table else 0
        std_dev = statistics.stdev(profit_loss_percent_table) if profit_loss_percent_table else 0

        new_entry = {
            'ticker': ticker,
            # Include other necessary fields here from earnings pulls information
            f'sim-company-{j}': {'average_return_percent': round(avg_return, ndigits=4),
                                 'return_variance': round(variance, ndigits=4),
                                 'return_standard_deviation': round(std_dev, ndigits=4),
                                 'raw_simulation_data': long_straddle}
        }

        if long_straddle:
            master_out.append(new_entry)
        else:
            master_out.append({'skipped_company': ticker,
                               f'sim-company-{j}': "NONE"
                               })

    return master_out


sim = TestCompanies(min_revenue=10_000_000_000, from_date="2023-12-01", to_date="2023-12-22",
                    report_hour="", data_limit=60, skipped_tickers=[], max_companies=5)

x = companies_bulk_simulation(sim.correct_strikes, entry_start='09:30:00', entry_end='11:00:00',
                              exit_start="14:00:00", exit_end="15:59:00")


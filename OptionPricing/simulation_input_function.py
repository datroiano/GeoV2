from strangle_simulation_inputs_from_earnings import TestCompanies
def companies_bulk_simulation(corrected_strikes):
    raw_tickers = [i['symbol'] for i in corrected_strikes]  # Ensures all data is present in strikes

    for item in enumerate(corrected_strikes):
        ticker = item[1]['symbol']
        strike1 = item[1]['target_strike']
        strike2 = item[1]['target_strike']
        expiration_date = item[1]['target_expiration_date']
        trade_date = item[1]['trade_date']


simulation = TestCompanies(min_revenue=1000000, from_date="2023-12-01", to_date="2023-12-14",
                           report_hour="", data_limit=60, skipped_tickers=[], max_companies=3)
print(simulation.correct_strikes)

companies_bulk_simulation(simulation.correct_strikes)

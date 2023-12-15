import pandas as pd


class MetaAnalysis:
    def __init__(self, simulation_data):
        self.simulation_data = simulation_data

    def profit_loss_dollars_table(self):
        return [entry['profit_loss_dollars'] for entry in self.simulation_data]

    def profit_loss_percent_table(self):
        return [entry['profit_loss_percent'] for entry in self.simulation_data]

    def create_data_frame(self):
        nested_dict = {}
        for item in self.simulation_data:
            for key, value in item.items():
                if key not in nested_dict:
                    nested_dict[key] = [value]
                else:
                    nested_dict[key].append(value)
        simulation_df = pd.DataFrame(nested_dict)

        return simulation_df

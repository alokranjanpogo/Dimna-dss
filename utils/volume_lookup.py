import pandas as pd


class VolumeLookup:

    def __init__(self, file_path="data/volume_chart.xlsx"):

        self.df = pd.read_excel(file_path)

        self.volume_dict = {}

        self.prepare_lookup()

    def prepare_lookup(self):

        for _, row in self.df.iterrows():

            try:
                base_level = float(row.iloc[0])
                base_volume = float(row.iloc[1])

            except:
                continue

            # exact foot level
            self.volume_dict[round(base_level, 2)] = round(
                base_volume, 2
            )

            columns = list(self.df.columns)

            for col_index in range(2, len(columns)):

                try:

                    increment = float(columns[col_index])

                    additional_volume = float(
                        row.iloc[col_index]
                    )

                    level = round(
                        base_level + increment,
                        2
                    )

                    volume = round(
                        base_volume +
                        additional_volume,
                        2
                    )

                    self.volume_dict[level] = volume

                except:
                    pass

    def get_volume(self, level):

        level = round(level, 2)

        if level in self.volume_dict:
            return self.volume_dict[level]

        return None

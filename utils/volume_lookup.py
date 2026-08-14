import pandas as pd


class VolumeLookup:

    def __init__(self):

        self.volume_table = {}

        self.load_volume_data()

    def load_volume_data(self):

        df = pd.read_excel(
            "data/volume_chart.xlsx",
            header=None
        )

        headers = df.iloc[0].tolist()

        for _, row in df.iterrows():

            try:

                base_level = float(row[0])
                base_volume = float(row[1])

            except:
                continue

            self.volume_table[
                round(base_level, 2)
            ] = round(
                base_volume,
                2
            )

            for col in range(2, len(headers)):

                try:

                    increment = float(
                        headers[col]
                    )

                    additional_volume = float(
                        row[col]
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

                    self.volume_table[
                        level
                    ] = volume

                except:
                    pass

    def get_volume(self, level):

        level = round(
            float(level),
            2
        )

        return self.volume_table.get(level)

    def volume_exists(self, level):

        level = round(
            float(level),
            2
        )

        return level in self.volume_table

import pandas as pd


class VolumeLookup:

    def __init__(self):

        self.lookup = {}

        self.load_volume_chart()

    def load_volume_chart(self):

        df = pd.read_excel(
            "data/volume_chart.xlsx",
            header=None
        )

        # Header row containing
        # 1, 0.9, 0.8 ... 0.01
        headers = df.iloc[5].tolist()

        # Volume data starts after that
        data = df.iloc[6:]

        for _, row in data.iterrows():

            try:

                base_level = float(row[0])

                base_volume = float(row[1])

            except:
                continue

            # Exact level volume
            self.lookup[
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

                    add_volume = float(
                        row[col]
                    )

                    level = round(
                        base_level + increment,
                        2
                    )

                    volume = round(
                        base_volume + add_volume,
                        2
                    )

                    self.lookup[
                        level
                    ] = volume

                except:
                    continue

    def get_volume(self, level):

        level = round(
            float(level),
            2
        )

        if level in self.lookup:
            return self.lookup[level]

        nearest = min(
            self.lookup.keys(),
            key=lambda x: abs(x - level)
        )

        return self.lookup[nearest]

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

        headers = [
            1,
            0.9,
            0.8,
            0.7,
            0.6,
            0.5,
            0.4,
            0.3,
            0.2,
            0.1,
            0.09,
            0.08,
            0.07,
            0.06,
            0.05,
            0.04,
            0.03,
            0.02,
            0.01
        ]

        data = df.iloc[6:]

        for _, row in data.iterrows():

            try:

                level = float(row[0])

                base_volume = float(row[1])

            except:
                continue

            self.lookup[
                round(level, 2)
            ] = base_volume

            for i, increment in enumerate(headers):

                try:

                    add_volume = float(
                        row[i + 2]
                    )

                    exact_level = round(
                        level + increment,
                        2
                    )

                    exact_volume = round(
                        base_volume +
                        add_volume,
                        2
                    )

                    self.lookup[
                        exact_level
                    ] = exact_volume

                except:
                    pass

    def get_volume(self, level):

        try:

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

        except:

            return 0

    def get_all_levels(self):

        return self.lookup
        

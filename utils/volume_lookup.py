import pandas as pd


class VolumeLookup:

    def __init__(self):

        self.lookup = {}

        self.load_volume_chart()

        print(
            "Levels Loaded:",
            len(self.lookup)
        )

    def load_volume_chart(self):

        df = pd.read_excel(
            "data/volume_chart.xlsx",
            header=None
        )

        # Actual chart headers
        headers = df.iloc[6].tolist()

        # Actual volume data starts after that
        data = df.iloc[7:]

        for _, row in data.iterrows():

            try:

                base_level = float(row.iloc[0])
                base_volume = float(row.iloc[1])

            except Exception:
                continue

            self.lookup[
                round(base_level, 2)
            ] = round(
                base_volume,
                2
            )

            for col in range(
                2,
                len(headers)
            ):

                try:

                    increment = float(
                        headers[col]
                    )

                    add_volume = float(
                        row.iloc[col]
                    )

                    level = round(
                        base_level + increment,
                        2
                    )

                    volume = round(
                        base_volume + add_volume,
                        2
                    )

                    self.lookup[level] = volume

                except Exception:
                    continue

    def get_volume(
        self,
        level
    ):

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

        except Exception:

            return 0

    def get_all_levels(self):

        return self.lookup
        

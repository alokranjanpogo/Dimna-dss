import pandas as pd


class VolumeLookup:

    def __init__(self):

        self.lookup = {}

        self.load_volume_chart()

        print(
            "Volume Lookup Records:",
            len(self.lookup)
        )

    def load_volume_chart(self):

        df = pd.read_excel(
            "data/volume_chart.xlsx",
            header=None
        )

        headers = df.iloc[5].tolist()

        data = df.iloc[6:]

        for _, row in data.iterrows():

            try:

                base_level = float(row.iloc[0])
                base_volume = float(row.iloc[1])

            except:
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
                        base_volume +
                        add_volume,
                        2
                    )

                    self.lookup[
                        level
                    ] = volume

                except:
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

            return self.lookup.get(
                level,
                None
            )

        except:

            return None

    def get_all_levels(self):

        return self.lookup

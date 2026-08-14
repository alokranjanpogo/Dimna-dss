import pandas as pd


class VolumeLookup:

    def __init__(self):

        self.df = pd.read_excel(
            "data/volume_chart.xlsx",
            header=None
        )

        self.lookup = {}

        self.prepare_lookup()

    def prepare_lookup(self):

        headers = self.df.iloc[5].tolist()

        data = self.df.iloc[6:]

        for _, row in data.iterrows():

            try:

                base_level = float(row[0])
                base_volume = float(row[1])

            except:
                continue

            self.lookup[
                round(base_level, 2)
            ] = round(
                base_volume,
                2
            )

            for i in range(2, len(headers)):

                try:

                    increment = float(
                        headers[i]
                    )

                    additional = float(
                        row[i]
                    )

                    level = round(
                        base_level +
                        increment,
                        2
                    )

                    volume = round(
                        base_volume +
                        additional,
                        2
                    )

                    self.lookup[
                        level
                    ] = volume

                except:
                    pass

    def get_volume(
        self,
        level
    ):

        level = round(
            level,
            2
        )

        return self.lookup.get(
            level
        )
        

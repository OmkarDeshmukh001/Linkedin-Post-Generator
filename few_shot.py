import pandas as pd


class FewShotPosts:

    def __init__(self, posts):

        self.df = None
        self.unique_tags = []

        self.load_posts(posts)

    def load_posts(self, posts):

        self.df = pd.json_normalize(posts)

        self.df["length"] = self.df["line_count"].apply(
            self.categorize_length
        )

        all_tags = self.df["tags"].apply(
            lambda x: x
        ).sum()

        self.unique_tags = sorted(
            list(set(all_tags))
        )

    def get_filtered_posts(
        self,
        length,
        language,
        tag=None
    ):

        df_filtered = self.df[
            (self.df["language"] == language) &
            (self.df["length"] == length)
        ]

        if tag:

            df_filtered = df_filtered[
                df_filtered["tags"].apply(
                    lambda tags: tag in tags
                )
            ]

        return df_filtered.to_dict(
            orient="records"
        )

    def get_best_examples(
        self,
        length,
        language,
        tag=None,
        max_examples=2
    ):

        df_filtered = self.df[
            (self.df["language"] == language) &
            (self.df["length"] == length)
        ]

        if tag:

            df_filtered = df_filtered[
                df_filtered["tags"].apply(
                    lambda tags: tag in tags
                )
            ]

        if "engagement" in df_filtered.columns:

            df_filtered = df_filtered.sort_values(
                by="engagement",
                ascending=False
            )

        return df_filtered.head(
            max_examples
        ).to_dict(orient="records")

    def categorize_length(self, line_count):

        if line_count < 5:
            return "Short"

        elif 5 <= line_count <= 10:
            return "Medium"

        else:
            return "Long"

    def get_tags(self):

        return self.unique_tags

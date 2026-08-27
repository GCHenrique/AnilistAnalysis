import pandas as pd


def get_completed(df: pd.DataFrame) -> pd.DataFrame:
    df_completed = df[df["status"] == "COMPLETED"].copy()

    return df_completed.sort_values(["media.title.romaji"])


def get_both_list_same_animes(
    list1: pd.DataFrame, list2: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    titles1 = set(list1["media.title.romaji"].dropna())
    titles2 = set(list2["media.title.romaji"].dropna())

    common_titles = titles1.intersection(titles2)

    filtered1 = list1[list1["media.title.romaji"].isin(common_titles)].copy()
    filtered2 = list2[list2["media.title.romaji"].isin(common_titles)].copy()

    filtered1 = remove_duplicates(filtered1)
    filtered2 = remove_duplicates(filtered2)

    return filtered1, filtered2


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df_filtered = df.drop_duplicates(subset="media.title.romaji", keep="first").copy()

    return df_filtered


def get_only_with_scores(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df[(df["score"].notna()) & (df["score"] != 0)].copy()
    return new_df  # anilist scores default to zero when they are not given a specific value.
    # this would break the correlation so I removed it (and NaN for good measure)

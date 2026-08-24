from . import api
from . import clean
from . import stats
from . import plots

import sys


def run_comparison_2():
    username1 = input("Input username: ")
    username2 = input("Input second username: ")

    df1 = api.fetch_user_data(username1)
    df2 = api.fetch_user_data(username2)

    print("Cleaning data")

    df1_completed = clean.get_completed(df1)
    df2_completed = clean.get_completed(df2)

    df1_filtered = clean.get_only_with_scores(df1_completed)
    df2_filtered = clean.get_only_with_scores(df2_completed)

    del df1_completed, df2_completed  # freeing space in memory

    df1_filtered, df2_filtered = clean.get_both_list_same_animes(
        df1_filtered, df2_filtered
    )

    if df1_filtered.empty:
        print("There are no anime in common")
        sys.exit(0)

    df1_filtered_scores = df1_filtered["score"].to_numpy()
    df2_filtered_scores = df2_filtered["score"].to_numpy()

    del df1_filtered, df2_filtered  # again freeing space in memory

    df1_filtered_scores = stats.normalize_to_Z(df1_filtered_scores)
    df2_filtered_scores = stats.normalize_to_Z(df2_filtered_scores)

    plots.plot_creation(df1_filtered_scores, df2_filtered_scores)

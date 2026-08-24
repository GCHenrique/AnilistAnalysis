import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sys


def get_completed(df: pd.DataFrame) -> pd.DataFrame:
    df_completed = df[df["status"] == "COMPLETED"].copy()

    return df_completed.sort_values(["media.title.romaji"])


def get_both_list_same_animes(
    list1: pd.DataFrame, list2: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    titles1 = set(list1["media.title.romaji"].dropna())
    titles2 = set(list2["media.title.romaji"].dropna())

    common_titles = titles1.intersection(titles2)

    filtered1 = (
        list1[list1["media.title.romaji"].isin(common_titles)]
        .drop_duplicates(subset="media.title.romaji", keep="first")
        .copy()
    )

    filtered2 = (
        list2[list2["media.title.romaji"].isin(common_titles)]
        .drop_duplicates(subset="media.title.romaji", keep="first")
        .copy()
    )

    return filtered1, filtered2


def get_only_with_scores(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df[df["score"].notna() & df["score"] != 0].copy()
    new_df = normalize_scores(new_df)
    return new_df  # anilist scores default to zero when they are not given a specific value.
    # this would break the correlation so I removed it (and NaN for good measure)


def normalize_scores(
    df: pd.DataFrame,
) -> pd.DataFrame:  # because anilist scores can come in 0-10, 0-100 and 0-3 format
    max_score = df["score"].max()

    if max_score <= 3:
        df = df.copy()
        df["score"] = df["score"] * (100 / 3)
    elif max_score <= 10:
        df = df.copy()
        df["score"] = df["score"] * 10

    return df


query_string = """
query ($username: String) {
  MediaListCollection(userName: $username, type: ANIME) {
    lists {
      name
      entries {
        media {
          title {
            romaji
          }
          meanScore
          status
        }
        score
        status
      }
    }
  }
}
"""

url = "https://graphql.anilist.co"

username1 = input("Input username: ")
username2 = input("Input second username: ")

variables1 = {"username": username1}
variables2 = {"username": username2}

response1 = requests.post(url, json={"query": query_string, "variables": variables1})
response2 = requests.post(url, json={"query": query_string, "variables": variables2})

data1 = response1.json()
data2 = response2.json()

if "errors" in data1:
    print(
        f"Error fetching data for: {username1}; {data1['errors'][0]['status']}: {data1['errors'][0]['message']}"
    )
    sys.exit()
elif "errors" in data2:
    print(
        f"Error fetching data for: {username2}; {data2['errors'][0]['status']}: {data2['errors'][0]['message']}"
    )
    sys.exit()
else:
    data1 = data1["data"]["MediaListCollection"]
    data2 = data2["data"]["MediaListCollection"]

df1 = pd.json_normalize(data1["lists"], record_path="entries", meta=["name"])
df2 = pd.json_normalize(data2["lists"], record_path="entries", meta=["name"])

columns = df1.columns.tolist()

df1_completed = get_completed(df1)
df2_completed = get_completed(df2)

df1_filtered = get_only_with_scores(df1_completed)
df2_filtered = get_only_with_scores(df2_completed)

del df1_completed, df2_completed  # freeing space in memory

df1_filtered, df2_filtered = get_both_list_same_animes(df1_filtered, df2_filtered)

if df1_filtered.empty:
    print("There are no anime in common")
    sys.exit()

df1_filtered_scores = df1_filtered["score"].to_numpy()
df2_filtered_scores = df2_filtered["score"].to_numpy()

del df1_filtered, df2_filtered  # again freeing space in memory

try:
    df1_filtered_scores = (
        df1_filtered_scores - df1_filtered_scores.mean()
    ) / df1_filtered_scores.std(ddof=0)

    df2_filtered_scores = (
        df2_filtered_scores - df2_filtered_scores.mean()
    ) / df2_filtered_scores.std(ddof=0)

except ZeroDivisionError:
    df1_filtered_scores = df1_filtered_scores - df1_filtered_scores.mean()
    df2_filtered_scores = df2_filtered_scores - df2_filtered_scores.mean()

corr = np.corrcoef(df1_filtered_scores, df2_filtered_scores)[0, 1]
beta, alpha = np.polyfit(df1_filtered_scores, df2_filtered_scores, 1)
x = np.linspace(df1_filtered_scores.min(), df1_filtered_scores.max(), 100)
y = alpha + beta * x

plt.scatter(
    df1_filtered_scores,
    df2_filtered_scores,
    marker=".",
    color="red",
    label="Z corrected data points",
)

plt.plot(x, y, "-", color="blue", label=f"Correlation: {corr:.4f}")
plt.legend()

plt.grid(alpha=0.2)

plt.show()

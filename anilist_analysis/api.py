import pandas as pd
import requests


class AnilistAPIError(Exception):
    pass


def fetch_user_data(username: str) -> pd.DataFrame:
    print(f"Fetching data for {username}")
    QUERY_STRING = """
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

    URL = "https://graphql.anilist.co"

    variables = {"username": username}

    response = requests.post(URL, json={"query": QUERY_STRING, "variables": variables})

    data = response.json()

    if "errors" in data:
        raise AnilistAPIError(
            f"Error fetching data for: {username}; {data['errors'][0]['status']}: {data['errors'][0]['message']}"
        )
    else:
        data = data["data"]["MediaListCollection"]

    df = pd.json_normalize(data["lists"], record_path="entries", meta=["name"])

    if df.empty:
        print(f"No entries for {username}")

    print(f"Received {len(df)} entries for {username}")

    return df

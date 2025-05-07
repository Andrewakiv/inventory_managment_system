import pandas as pd


def get_abc_statistics(data):
    df = pd.DataFrame(list(data))
    df["ttl_expenses_pu"] = df["ttl_expenses_pu"].astype(float)

    total = df["ttl_expenses_pu"].sum() or 1
    df["percent"] = round(df["ttl_expenses_pu"] * 100 / total, 2)
    df["cumulative_percent"] = df["percent"].cumsum().round(2)
    return df

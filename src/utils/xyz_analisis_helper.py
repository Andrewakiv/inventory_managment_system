import pandas as pd


def get_xyz_statistics(data):
    df = pd.DataFrame.from_records(data)

    if df.empty:
        return []

    df["month"] = pd.to_datetime(df["transaction__date"]).dt.to_period("M")

    stats = (
        df.groupby("id")["ttl_amount_pu"]
        .agg(["mean", "std"])
        .rename(columns={"mean": "avg", "std": "std_dev"})
    )

    stats["cv"] = (stats["std_dev"] / stats["avg"])

    stats = stats.reset_index()

    material_map = df.drop_duplicates("id").set_index("id")["name"].to_dict()
    stats["name"] = stats["id"].map(material_map)
    return stats

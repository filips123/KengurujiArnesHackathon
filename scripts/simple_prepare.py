import json
import os
import sys
from datetime import timedelta
from pathlib import Path

import pandas as pd


def prepare_data(target_gauge_id, predict_next_hours, use_last_hours=72):
    print(f"Preparing data for {target_gauge_id} for {predict_next_hours} hours")

    with open("../dataset/hydro/network.json", encoding="utf-8") as file:
        network = json.load(file)[str(target_gauge_id)]
        network.insert(0, [target_gauge_id, 0.0])

    dataframes = []
    distances = []

    for gauge, distance in network:
        df = pd.read_csv(f"../dataset/hydro/aggregated/{gauge}.csv")
        df["datum"] = pd.to_datetime(df["datum"])
        df.set_index("datum", inplace=True)
        dataframes.append(df["H"])
        distances.append(distance)

    columns = ["DATE", "TARGET"]
    columns.extend([f"DISTANCE_{i}" for i in range(len(distances))])
    columns.extend([f"LEVEL_{i}_{j}" for i in range(len(dataframes)) for j in range(use_last_hours)])

    data = []

    range_start = use_last_hours
    range_end = -predict_next_hours if predict_next_hours else None

    for date in dataframes[0].index[range_start:range_end]:
        values = [date, dataframes[0][date + timedelta(hours=predict_next_hours)], *distances]
        for i, df in enumerate(dataframes):
            values.extend(df[df.index <= date].tail(use_last_hours))
        data.append(values)

    data = pd.DataFrame(data, columns=columns)
    data.set_index("DATE", inplace=True)

    directory = f"../dataset/processed/simple/{target_gauge_id}"
    os.makedirs(directory, exist_ok=True)
    data.to_csv(f"{directory}/{predict_next_hours}.gz", compression="gzip")

    print()


def main():
    predict_next_hours = int(sys.argv[1])

    print("PREPARING DATA\n")

    for file in Path("../dataset/hydro/aggregated").glob("*.csv"):
        try:
            target_gauge_id = int(file.name.replace(".csv", ""))
            prepare_data(target_gauge_id, predict_next_hours)
        except Exception as error:
            print("Error:", error)
            print()


main()

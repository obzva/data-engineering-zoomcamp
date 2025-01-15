"""
Code snippet to convert parquet into csv
"""

import pandas as pd

print("Reading parquet file...")
df = pd.read_parquet("./yellow_tripdata_2024-09.parquet")
print("Reading done!")

print("Exporting csv file...")
df.to_csv("./yellow_tripdata_2024-09.csv", index=False)
print("Exporting done!")
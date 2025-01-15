#!/usr/bin/env python
# coding: utf-8

import argparse
import os 
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db_name = params.db_name
    table_name = params.table_name
    url = params.url
    parquet_data = "downloaded.parquet"
    csv_data = "converted.csv"

    # Clear prev downloads
    print("[Checking previous downloads]")
    if os.path.exists(parquet_data):
        print("[    Previous parquet data exists]")
        os.system(f"rm {parquet_data}")
        print("[    Deleted previous parquet data]")
    if os.path.exists(csv_data):
        print("[    Previous csv data exists]")
        os.system(f"rm {csv_data}")
        print("[    Deleted previous csv data]")
    print("[Checking done]")

    # Download Parquet data
    print("[Downloading parquet data]")
    os.system(f"wget {url} -O {parquet_data}")
    print("[Downloading done]")

    # Convert Parquet into CSV 
    print("[Converting parquet into csv]")
    converter = pd.read_parquet(parquet_data)
    converter.to_csv(csv_data, index=False)
    print("[Converting done]")

    print("[Creating database connection]")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")
    print("[Database connection established]")

    df_iter = pd.read_csv(csv_data, iterator=True, chunksize=100_000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    print("[Data ingesting start]")
    df.head(n=0).to_sql(con=engine, name=table_name, if_exists="replace", index=False)

    chunk_number = 0

    t_start = time()
    df.to_sql(con=engine, name=table_name, if_exists="append", index=False)
    chunk_number += 1
    t_end = time()
    print(f"inserted chunk:{chunk_number}!")
    print(f"---took {t_end - t_start} second!")

    try:
        while True:
            t_start = time()
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(con=engine, name=table_name, if_exists="append", index=False)
            chunk_number += 1
            t_end = time()    
            print(f"inserted chunk:{chunk_number}!")
            print(f"---took {t_end - t_start} second!")
    except StopIteration:
        print("[Data ingesting done]")

    # Clear downloads
    print("[Clearing downloads]")
    os.system(f"rm {parquet_data}")
    os.system(f"rm {csv_data}")
    print("[Clearing done]")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert Parquet data into CSV and then ingest it to PostgreSQL")

    parser.add_argument('--user', required=True, help="username for the postgres")
    parser.add_argument('--password', required=True, help="password for the postgres")
    parser.add_argument('--host', required=True, help="host for the postgres")
    parser.add_argument('--port', required=True, help="port for the postgres")
    parser.add_argument('--db_name', required=True, help="database name for the postgres")
    parser.add_argument('--table_name', required=True, help="name of the table where we will write results")
    parser.add_argument('--url', required=True, help="url of the parquet data") 

    args = parser.parse_args()

    main(args)
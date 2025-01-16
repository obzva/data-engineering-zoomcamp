#!/usr/bin/env python
# coding: utf-8

import argparse
import os 
import pandas as pd
from sqlalchemy import create_engine
from time import time
import gzip
import shutil

"""
python ingest_gzipped_csv_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db_name=ny_taxi \
    --table_name=green_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
"""

def download_and_extract(url, output_file):
    """Download and extract gzipped file"""
    gz_file = "temp.csv.gz"
    
    # Download gzipped file
    os.system(f"wget {url} -O {gz_file}")
    
    # Extract gz file
    with gzip.open(gz_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # Remove gz file
    os.remove(gz_file)

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db_name = params.db_name
    table_name = params.table_name
    url = params.url
    csv_data = "downloaded.csv"

    # Clear prev downloads
    print("[Checking previous downloads]")
    if os.path.exists(csv_data):
        print("[    Previous csv data exists]")
        os.remove(csv_data)  # Using os.remove instead of os.system
        print("[    Deleted previous csv data]")
    print("[Checking done]")

    # Download and extract gzipped data
    print("[Downloading and extracting gzipped data]")
    download_and_extract(url, csv_data)
    print("[Downloading and extracting done]")

    print("[Creating database connection]")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")
    print("[Database connection established]")

    df_iter = pd.read_csv(csv_data, iterator=True, chunksize=100_000)

    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    print("[Data ingesting start]")
    df.head(n=0).to_sql(con=engine, name=table_name, if_exists="replace", index=False)

    chunk_number = 0

    t_start = time()
    df.to_sql(con=engine, name=table_name, if_exists="append", index=False)
    chunk_number += 1
    t_end = time()
    print(f"inserted chunk:{chunk_number}!")
    print(f"---took {t_end - t_start} seconds!")

    try:
        while True:
            t_start = time()
            df = next(df_iter)
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df.to_sql(con=engine, name=table_name, if_exists="append", index=False)
            chunk_number += 1
            t_end = time()    
            print(f"inserted chunk:{chunk_number}!")
            print(f"---took {t_end - t_start} seconds!")
    except StopIteration:
        print("[Data ingesting done]")

    # Clear downloads
    print("[Clearing downloads]")
    os.remove(csv_data)  # Using os.remove instead of os.system
    print("[Clearing done]")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV to PostgreSQL")

    parser.add_argument('--user', required=True, help="username for postgres")
    parser.add_argument('--password', required=True, help="password for postgres")
    parser.add_argument('--host', required=True, help="host for postgres")
    parser.add_argument('--port', required=True, help="port for postgres")
    parser.add_argument('--db_name', required=True, help="database name for postgres")
    parser.add_argument('--table_name', required=True, help="name of the table where we will write results")
    parser.add_argument('--url', required=True, help="url of the gzipped csv data") 

    args = parser.parse_args()

    main(args)
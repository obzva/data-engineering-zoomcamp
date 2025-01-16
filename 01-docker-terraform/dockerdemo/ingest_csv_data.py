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
    csv_data = "downloaded.csv"

    # Clear prev downloads
    print("[Checking previous downloads]")
    if os.path.exists(csv_data):
        print("[    Previous csv data exists]")
        os.system(f"rm {csv_data}")
        print("[    Deleted previous csv data]")
    print("[Checking done]")

    # Download Parquet data
    print("[Downloading csv data]")
    os.system(f"wget {url} -O {csv_data}")
    print("[Downloading done]")

    print("[Creating database connection]")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")
    print("[Database connection established]")

    df = pd.read_csv(csv_data)

    print("[Data ingesting start]")
    t_start = time()
    df.to_sql(con=engine, name=table_name, if_exists="replace", index=False)
    t_end = time()
    print(f"[Data ingesting done] ---took {t_end - t_start} second!")

    # Clear downloads
    print("[Clearing downloads]")
    os.system(f"rm {csv_data}")
    print("[Clearing done]")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV to PostgreSQL")

    parser.add_argument('--user', required=True, help="username for postgres")
    parser.add_argument('--password', required=True, help="password for postgres")
    parser.add_argument('--host', required=True, help="host for postgres")
    parser.add_argument('--port', required=True, help="port for postgres")
    parser.add_argument('--db_name', required=True, help="database name for postgres")
    parser.add_argument('--table_name', required=True, help="name of the table where we will write results")
    parser.add_argument('--url', required=True, help="url of the csv data") 

    args = parser.parse_args()

    main(args)
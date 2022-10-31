#!/usr/bin/env python3
import os
import time
import csv
from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "test-admin-token"
org = "Pegasust"
bucket = "BTC"

exit_prog = False
URL = os.getenv("INFLUXDB_URL") or "http://localhost:8086"
DATA= os.getenv("DATA") or "data/btc.csv"
print(f"URL: {URL}")
with open(DATA) as btc:
    btc_stream = csv.reader(btc, delimiter=',')
    while not exit_prog:
        with InfluxDBClient(url=URL, token=token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            row = next(btc_stream, None)
            while row is not None:
                # construct the data
                if row[0] == "time":
                    row = next(btc_stream, None)
                    continue
                time_raw = int(row[0])
                data_time = datetime.fromtimestamp(time_raw, tz=timezone.utc)
                close = float(row[1])
                high = float(row[2])
                low = float(row[3])
                open = float(row[4])
                volume = float(row[5])

                data = Point("price")\
                    .tag("currency", "usd")\
                    .field("close", close)\
                    .field("high", high)\
                    .field("low", low)\
                    .field("open", open)\
                    .field("volume", volume)\
                    .time(data_time, WritePrecision.NS)\

                print(f"Writing: {time.ctime()}@ {data}")
                write_api.write(bucket, org, data)
                row = next(btc_stream, None)
                time.sleep(0.05)
            exit_prog = True

        if not exit_prog:
            time.sleep(5)

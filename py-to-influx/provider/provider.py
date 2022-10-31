#!/usr/bin/env python3

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time
import os


# You can generate an API token from the "API Tokens Tab" in the UI
token = "test-admin-token"
org = "Pegasust"
bucket = "BTC"

exit_prog = False
URL = os.getenv("INFLUXDB_URL") or "http://localhost:8086"
print(f"URL: {URL}")
while not exit_prog:
    with InfluxDBClient(url=URL, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = "mem,host=host1 used_percent=23.43234543"
        write_api.write(bucket, org, data)

        for _ in range(5000):
            mem_pct = random.randint(0, 10_000) / 10_000 * 100
            cpu_pct = random.randint(0, 10_000) / 10_000 * 100
            insert_pt = Point("mem").tag("host", "host1")\
                .field("used_percent", mem_pct)\
                .time(datetime.utcnow(), WritePrecision.NS)
            print(f"Writing {insert_pt}")
            write_api.write(bucket, org, insert_pt)

            cpu_pt = Point("cpu").tag("host", "host1")\
                .field("used_percent", cpu_pct)\
                .time(datetime.utcnow(), WritePrecision.MS)
            print(f"Writing {insert_pt}")
            write_api.write(bucket, org, cpu_pt)


            upload_speed_bps = random.randint(0, 2147483647)
            upload_bps = Point("upload").tag("job", "0xdeafbeef")\
                .field("speed (bps)", upload_speed_bps)\
                .time(datetime.utcnow(), WritePrecision.MS)
            print(f"Writing {upload_bps}")
            write_api.write(bucket, org, upload_bps)
            time.sleep(1)
    if not exit_prog:
        time.sleep(5)
    


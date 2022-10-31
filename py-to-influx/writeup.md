# Setting up

# Grafana

- Needed to have Admin role to add a new data source (InfluxDB)
- You could add a new dashboard with panels from Flux queries
- Here is my upload speed query:

```flux
from(bucket:"BTC") |> range(start:-30d) |> filter(fn: (r)=>r._measurement == "upload")
```

- For historical data (that also persists on InfluxDB) like BTC price in 2016:

```flex
from(bucket: "BTC") |> range(start:-7y) |> filter(fn: (r)=>r._measurement =="price")
```
- Note that Grafana also has candlestick built-in as a way to visualize the graph
  - It also supports volume channel


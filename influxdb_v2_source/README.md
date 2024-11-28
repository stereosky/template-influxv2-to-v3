# InfluxDB v2 Source
A service that queries an InfluxDB v2 bucket at set intervals and writes all measurements and data to a Kafka topic.

Requires the following environment variables to be set:

| Variable   |      Description      |  Example |
|----------|---------------------------------------|------|
| `OUTPUT_TOPIC` |  The output topic to store the results fetched from the InfluxDB v2 queries | `influxdb-v2-data` |
| `INFLUXDB_HOST` | The address of the InfluxDB v2 instance | `https://influxdbv2-uprelq3jh2vyt6.eu-west-1.timestream-influxdb.amazonaws.com:8086` |
| `INFLUXDB_ORG` |   The configured organization in the InfluxDB v2 instance | `AcmeInc` |
| `INFLUXDB_BUCKET` | The name of the InfluxDB v2 bucket that stores the source data to be synced |    `machine-telemetry-v2` |
| `INFLUXDB_TOKEN` | The configured API Token to access the InfluxDB v2 instance (defined as a secret in Quix) |   `Rm3545345357qnv-gOX54346346EHr-g1YSB79T29w_5VdwEuXWK6gg535g34232yDX_VAYfA33RFd4Xw==` |
| `TASK_INTERVAL` | Defines both how often the query should be run against the database and the max age of the data to return. See the InfluxDB documentation for a full list of valid interval values | `1m` |

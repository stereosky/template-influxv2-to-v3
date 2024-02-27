# InfluxDB V2 Source
A service that queries your chosen V2 InfluxDB bucket at a configurable interval and writes all measurements and associated data to a Kafka topic.

The **InfluxDB V2 Source** service requires the following environment variables to be set:

| Variable   |      Description      |  Example |
|----------|---------------------------------------|------|
| `output` |  The output topic to store the result of the InfluxDB V2 queries. | `influxv2-data` |
| `INFLUXDB_ORG` |   The configured organization in the InfluxDB V2 instance. |  `AcmeInc` |
| `INFLUXDB_HOST` | The address of the InfluxDB V2 instance. | `https://influxdb-production-v2.up.railway.app` |
| `task_interval` | Defines both how often the query should be run agains the database and the max age of the data to return. See the InfluxDB documentation for a full list of valid interval values. |    `5m` |
| `INFLUXDB_BUCKET` | The name of the InfluxDB bucket that stores the required data.  |    `machine-telemetry-v2` |
| `INFLUXDB_TOKEN` | The influxDBV2 access token (defined as a secret in Quix). |   `Rm3545345357qnv-gOX54346346EHr-g1YSB79T29w_5VdwEuXWK6gg535g34232yDX_VAYfA33RFd4Xw==` |

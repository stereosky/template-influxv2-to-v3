# Template: Sync data from InfluxDB v2 to InfluxDB v3 

This template creates a basic two-step pipeline that you can use to keep an InfluxDB v3 bucket (synonymous with "database") synchronized with an InfluxDB v2 bucket. The pipeline periodically queries the InfluxDB v2 bucket for all measurements and data using the configured task interval. When new records are detected, they are produced to the configured Kafka topic. A consumer process listens to this topic for new records and filters them for the configured tags and fields. Finally, the filtered records are written as points (synonymous with "rows") to the corresponding InfluxDB v3 bucket.

The template will create two services:

1. **InfluxDB v2 Source**
A service that queries an InfluxDB v2 bucket at set intervals and writes all measurements and data to a Kafka topic.

2. **InfluxDB v3 Sink**
 A service that continuously listens to a Kafka topic and writes new data to an InfluxDB v3 bucket, only including the configured tags and fields.


## InfluxDB v2 Source

Requires the following environment variables to be set:

| Variable   |      Description      |  Example |
|----------|---------------------------------------|------|
| `OUTPUT_TOPIC` |  The output topic to store the results fetched from the InfluxDB v2 queries | `influxdb-v2-data` |
| `INFLUXDB_HOST` | The address of the InfluxDB v2 instance | `https://influxdbv2-uprelq3jh2vyt6.eu-west-1.timestream-influxdb.amazonaws.com:8086` |
| `INFLUXDB_ORG` |   The configured organization in the InfluxDB v2 instance | `AcmeInc` |
| `INFLUXDB_BUCKET` | The name of the InfluxDB v2 bucket that stores the source data to be synced |    `machine-telemetry-v2` |
| `INFLUXDB_TOKEN` | The configured API Token to access the InfluxDB v2 instance (defined as a secret in Quix) |   `Rm3545345357qnv-gOX54346346EHr-g1YSB79T29w_5VdwEuXWK6gg535g34232yDX_VAYfA33RFd4Xw==` |
| `TASK_INTERVAL` | Defines both how often the query should be run against the database and the max age of the data to return. See the InfluxDB documentation for a full list of valid interval values | `1m` |


## InfluxDB v3 Sink

Requires the following environment variables to be set:

| Variable   |      Description      |  Example |
|----------|---------------------------------------|------|
| `INPUT_TOPIC` | The input topic from which to consume the InfluxDB v2 data | `influxdb-v2-data` |
| `INFLUXDB_HOST` | The address of the InfluxDB v3 instance | `https://us-east-1-2.aws.cloud2.influxdata.com` |
| `INFLUXDB_ORG` |  The configured organization in the InfluxDB v3 instance | `AcmeInc` |
| `INFLUXDB_BUCKET` | The name of the InfluxDB v3 bucket to store the synced data |   `machine-telemetry-v3` |
| `INFLUXDB_TOKEN` | The configured API Token to access the InfluxDB v3 instance (defined as a secret in Quix) |   `Rm3545345357qnv-gOX54346346EHr-g1YSB79T29w_5VdwEuXWK6gg535g34232yDX_VAYfA33RFd4Xw==` |
| `INFLUXDB_TAG_KEYS` | A list of tags to select when when writing the data to InfluxDB v3 (all others will be ignored) |  `['machineID','barcode','provider']` |
| `INFLUXDB_FIELD_KEYS` | A list of fields to select when when writing the data to InfluxDB v3 (all others will be ignored) |  `['temperature','load','power','vibration']` |

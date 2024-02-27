# Template: Sync data from InfluxDB V2 to InfluxDB V3 

This template creates a basic two-step pipeline that you can use to keep an InfluxDB V3 database synchronized with an InfluxDB V2 bucket. The pipeline periodically queries the InfluxDB V2 bucket for all measurements and data. When new records are detected, they are sent to a Kafka topic. A consumer process listens for new records and filters them for user-specified tags and fields. Finally, the filtered records are written as points to the corresponding InfluxDB V3 database.

The template will create two services:

1. **InfluxDB V2 Source**
A service that queries your chosen V2 InfluxDB bucket at a configurable interval and writes all measurements and associated data to a Kafka topic.

2. **InfluxDB V3 Sink**
 A service that continuously listens to the "influxV2-data" Kafka topic and writes new data to your chosen InfluxDB V3 database while only including your chosen tags and fields.



## InfluxDB V2 Source

The **InfluxDB V2 Source** service requires the following environment variables to be set:

| Variable   |      Description      |  Example |
|----------|---------------------------------------|------|
| `output` |  The output topic to store the result of the InfluxDB V2 queries. | `influxv2-data` |
| `INFLUXDB_ORG` |   The configured organization in the InfluxDB V2 instance. |  `AcmeInc` |
| `INFLUXDB_HOST` | The address of the InfluxDB V2 instance. | `https://influxdb-production-v2.up.railway.app` |
| `task_interval` | Defines both how often the query should be run agains the database and the max age of the data to return. See the InfluxDB documentation for a full list of valid interval values. |    `5m` |
| `INFLUXDB_BUCKET` | The name of the InfluxDB bucket that stores the required data.  |    `machine-telemetry-v2` |
| `INFLUXDB_TOKEN` | The influxDBV2 access token (defined as a secret in Quix). |   `Rm3545345357qnv-gOX54346346EHr-g1YSB79T29w_5VdwEuXWK6gg535g34232yDX_VAYfA33RFd4Xw==` |




## InfluxDB V3 Sink

The **InfluxDB V3 Sink** service requires the following environment variables to be set:

| Variable   |      Description      |  Example |
|----------|---------------------------------------|------|
| `input`          |  The input topic from which to pull the  InfluxDB V2 data.  | `influxv2-data` |
| `INFLUXDB_ORG`   |  The configured organization in the InfluxDB V3 instance.      | `AcmeInc` |
| `INFLUXDB_HOST`  | The address of the InfluxDB V3 Serverless Cloud instance.  | `https://us-east-1-2.aws.cloud2.influxdata.com` |
| `INFLUXDB_DATABASE` | The name of the InfluxDB database (aka bucket) to store the migrated data. |  `machine-telemetry-v3` |
| `INFLUXDB_TOKEN` | The influxDBV3 access token (defined as a secret in Quix).  |   `Rm3545345357qnv-gOX54346346EHr-g1YSB79T29w_5VdwEuXWK6gg535g34232yDX_VAYfA33RFd4Xw==` |
| `INFLUXDB_TAG_KEYS` | A list of tags to look for in the migrated data (all others will be ignored). |  `['machineID','barcode','provider']` |
| `INFLUXDB_FIELD_KEYS` | A list of fields to look for in the migrated data (all others will be ignored).  |  `['temperature','load','power','vibration']` |
| `CONSUMER_GROUP_NAME` | The name of the Kafka consumer group (usually only needs to be changed when testing) | `influxv2-reader` |


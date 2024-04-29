# InfluxDB v3 Sink
A service that continuously listens to a Kafka topic and writes new data to your chosen InfluxDB v3 database while only including your chosen tags and fields.

The **InfluxDB v3 Sink** service requires the following environment variables to be set:

| Variable   |      Description      |  Example |
|----------|---------------------------------------|------|
| `input`          |  The input topic from which to pull the  InfluxDB v2 data.  | `influxv2-data` |
| `INFLUXDB_ORG`   |  The configured organization in the InfluxDB v3 instance.      | `AcmeInc` |
| `INFLUXDB_HOST`  | The address of the InfluxDB v3 Serverless Cloud instance.  | `https://us-east-1-2.aws.cloud2.influxdata.com` |
| `INFLUXDB_DATABASE` | The name of the InfluxDB database (aka bucket) to store the migrated data. |  `machine-telemetry-v3` |
| `INFLUXDB_TOKEN` | The InfluxDB v3 access token (defined as a secret in Quix).  |   `Rm3545345357qnv-gOX54346346EHr-g1YSB79T29w_5VdwEuXWK6gg535g34232yDX_VAYfA33RFd4Xw==` |
| `INFLUXDB_TAG_KEYS` | A list of tags to look for in the migrated data (all others will be ignored). |  `['machineID','barcode','provider']` |
| `INFLUXDB_FIELD_KEYS` | A list of fields to look for in the migrated data (all others will be ignored).  |  `['temperature','load','power','vibration']` |
| `CONSUMER_GROUP_NAME` | The name of the Kafka consumer group (usually only needs to be changed when testing) | `influxv2-reader` |

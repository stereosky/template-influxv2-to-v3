import os
import random
import json
import logging
from time import sleep

# import vendor-specfic modules
from quixstreams import Application
import influxdb_client

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize parameters from environment
KAFKA_BROKER_ADDRESS = os.getenv("KAFKA_BROKER_ADDRESS")
OUTPUT_TOPIC = os.getenv("OUTPUT_TOPIC", "influxdb-v2-data")
INFLUXDB_HOST = os.getenv("INFLUXDB_HOST")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")
TASK_INTERVAL = os.getenv("TASK_INTERVAL", "1m")

# Create a Quix Application
app = Application(
    broker_address=KAFKA_BROKER_ADDRESS,
    consumer_group="influxdb-v2-reader",
    auto_offset_reset="latest",
    auto_create_topics=True,
)

topic = app.topic(OUTPUT_TOPIC)

# Create an InfluxDB v2 client
influxdb2_client = influxdb_client.InfluxDBClient(
    url=INFLUXDB_HOST,
    org=INFLUXDB_ORG,
    token=INFLUXDB_TOKEN,
)

query_api = influxdb2_client.query_api()

# Global variable to control the main loop's execution
run = True

# Helper function to convert time intervals (like 1h, 2m) into seconds for consistent processing.
# This function is useful for determining the frequency of certain operations.
UNIT_SECONDS = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
    "y": 31536000,
}


def interval_to_seconds(interval: str) -> int:
    try:
        return int(interval[:-1]) * UNIT_SECONDS[interval[-1]]
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(
                "interval format is {int}{unit} i.e. '30s'; "
                f"valid units: {list(UNIT_SECONDS.keys())}")
    except KeyError:
        raise ValueError(
            f"Unknown interval unit: {interval[-1]}; "
            f"valid units: {list(UNIT_SECONDS.keys())}")


interval_seconds = interval_to_seconds(TASK_INTERVAL)


def is_dataframe(result):
    return type(result).__name__ == "DataFrame"


# Function to fetch data from InfluxDB and send it to Quix.
# It runs in a continuous loop, periodically fetching data based on the interval.
def get_data():
    # Run in a loop until the main thread is terminated
    while run:
        try:            
            # Query InfluxDB 2.0 using Flux
            flux_query = f'''
            from(bucket: "{INFLUXDB_BUCKET}")
                |> range(start: -{TASK_INTERVAL})
                |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            '''
            logger.info(f"Sending query: {flux_query}")

            table = query_api.query_data_frame(query=flux_query,org=INFLUXDB_ORG)

            # Renaming time column to distinguish it from other timestamp types
            # table.rename(columns={"_time": "original_time"}, inplace=True)

            # If the query returns tables with different schemas, the result will be a list of dataframes.
            if isinstance(table, list):
                for item in table:
                    item.rename(columns={"_time": "original_time"}, inplace=True)
                    json_result = item.to_json(orient="records", date_format="iso")
                    yield json_result
                    logger.info("Published multiple measurements to Quix")
            elif is_dataframe(table) and len(table) > 0:
                    table.rename(columns={"_time": "original_time"}, inplace=True)
                    json_result = table.to_json(orient="records", date_format="iso")
                    yield json_result
                    logger.info("Published single measurement to Quix")
            elif is_dataframe(table) and len(table) < 1:
                    logger.info("No results.")

            logger.info(f"Trying again in {interval_seconds} seconds...")
            sleep(interval_seconds)

        except Exception as e:
            logger.info("query failed")
            logger.info(f"error: {e}")
            flush=True
            sleep(1)


def main():
    """
    Read data from the Query and publish it to Kafka
    """
    # Create a pre-configured Producer object.
    # Producer is already setup to use Quix brokers.
    # It will also ensure that the topics exist before producing to them if
    # Application.Quix is initialized with "auto_create_topics=True".
    with app.get_producer() as producer:
        for res in get_data():
            # Parse the JSON string into a Python object
            records = json.loads(res)
            for index, obj in enumerate(records):
                # Generate a unique message_key for these rows
                message_key = f"INFLUXDB_V2_DATA_{str(random.randint(1, 100)).zfill(3)}_{index}"
                # Publish the data to the topic
                producer.produce(
                    topic=topic.name,
                    key=message_key,
                    value=json.dumps(obj),
                )
                logger.info(f"Produced message with key: {message_key}, value: {obj}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Exiting.")

import json
import logging
from random import randint

from kombu import Connection
import uuid
from time import sleep

from dasy.settings import RABBITMQ_URL

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Producer:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def get_random_number(self, x):
        return x + f"_index_{randint(0, 500000)}"

    def publish_data(self, conn, table):
        random_name = "q" + str(uuid.uuid4()).replace("-", "")
        random_queue = conn.SimpleQueue(random_name)
        logger.info(f"table name is {table}")
        logger.info("processing")
        if table == "products":
            for data in self.data_frame:
                logger.info("publishing data for products..")
                data["index"] = data.index
                data["sku"] = data["sku"] + "_index_" + data.index.map(str)
                data = data[["name", "sku", "description"]]
                random_queue.put(json.dumps(data.to_json()))
        elif table == "product_count":
            for data in self.data_frame:
                logger.info("publishing data for product_count..")
                data = data[["name", "no_of_products"]]
                random_queue.put(json.dumps(data.to_json()))
        random_queue.close()
        return random_name

    def producer_init(self, table):
        with Connection(RABBITMQ_URL) as conn:
            control_queue = conn.SimpleQueue("control_queue")
            _a = 0
            while True:
                logger.info("publishing data")
                y_name = self.publish_data(conn, table)
                message = y_name
                control_queue.put(message)
                print("Sent: {0}".format(message))
                _a += 1
                sleep(0.3)
                if _a > 20:
                    break

            control_queue.close()

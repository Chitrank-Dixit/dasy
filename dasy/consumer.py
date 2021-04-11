import json
import logging

import pandas as pd
from kombu import Connection, Queue

from dasy.settings import RABBITMQ_URL

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Consumer:
    def __init__(self, engine, table_name):
        self.engine = engine
        self.table_name = table_name

    def process_msg(self, queue):
        with Connection(RABBITMQ_URL) as _conn:
            sub_queue = _conn.SimpleQueue(str(queue))
            while True:
                logger.info("processing message")
                try:
                    logger.info("processing")
                    _msg = sub_queue.get(block=False)
                    data = pd.read_json(json.loads(_msg.payload))
                    logger.info("data retrieved")
                    data.to_sql(self.table_name, con=self.engine, index=False, if_exists="append", method="multi")
                    _msg.ack()
                except Exception:
                    break
            sub_queue.close()
            chan = _conn.channel()
            dq = Queue(name=str(queue), exchange="")
            bdq = dq(chan)
            bdq.delete()

    def consumer_init(self, is_test=False):
        with Connection(RABBITMQ_URL) as conn:
            rec = conn.SimpleQueue("control_queue")
            logger.info(f"{is_test}")
            if is_test:
                while True:
                    logger.info("retrieving test payload")
                    msg = rec.get(block=False)
                    logger.info(msg.payload)
                    entry = msg.payload
                    msg.ack()
                    self.process_msg(entry)
                    return None
            else:
                while True:
                    logger.info("retrieving payload")
                    msg = rec.get(block=True)
                    entry = msg.payload
                    msg.ack()
                    self.process_msg(entry)

import logging

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dasy.settings import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from dasy.producer import Producer
from dasy.consumer import Consumer

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DBUtils:
    def __init__(self):
        pass

    def get_engine(self):
        return create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

    def get_router(self):
        engine = self.get_engine()
        session = sessionmaker(bind=engine)
        return session()


class ProductsProcessor:
    def run_producer(self, write_from_path, engine):
        table = None
        logger.info(f"{write_from_path} is")
        if write_from_path == "product_count":
            table = "product_count"
            data_frame = pd.read_sql_query(
                """
                SELECT name ,COUNT(*) AS no_of_products FROM products GROUP BY "name";
            """,
                con=engine,
                chunksize=1000,
            )
            logger.info(f"{write_from_path} is reached")
        else:
            table = "products"
            data_frame = pd.read_csv(f"{write_from_path}", sep=",", iterator=True, chunksize=1000)
        logger.info("pushing records to queue")
        producer = Producer(data_frame=data_frame)
        producer.producer_init(table=table)

    def run_consumer(self, table_name, is_test=False):
        db_utils = DBUtils()
        logger.info("processing records from queue")
        consumer = Consumer(engine=db_utils.get_engine(), table_name=table_name)
        consumer.consumer_init(is_test=is_test)

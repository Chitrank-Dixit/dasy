import click
from dasy.migrations import Migrations
from dasy.utils import ProductsProcessor, DBUtils


@click.command()
@click.option("-w", "--write-from", default=False, help="write data to the db")
@click.option("-r", "--read-from", default=False, help="read data from the db")
@click.option("-m", "--migrate", default=False, help="migrate db")
@click.option("-t", "--test", default=False, help="to test producer consumer flow")
def checkCommand(write_from, read_from, migrate, test):
    """
    CLI tool to process large files
    """
    products_processor = ProductsProcessor()
    if write_from:
        if write_from == "products":
            write_from = "./data/products.csv"
        db_utils = DBUtils()
        engine = db_utils.get_engine()
        products_processor.run_producer(write_from_path=write_from, engine=engine)
        click.echo("records queued...")
    elif read_from:
        is_test = False
        if bool(test):
            is_test = True
        products_processor.run_consumer(table_name=read_from, is_test=is_test)
        click.echo("records stored in db...")
    elif migrate:
        migration = Migrations()
        migration.run(direction=migrate)

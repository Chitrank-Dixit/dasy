import logging
from urllib.parse import urlsplit

from pkg_resources import resource_filename
import os
import sys

import psycopg2

from dasy.settings import DB_URL, DB_NAME

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Migrations:

    def parse_pgurl(self, db_url):
        """
        Given a SQLAlchemy-compatible Postgres url, return a dict with
        keys for user, password, host, port, and database.
        """

        parsed = urlsplit(db_url)
        return {
            'user': parsed.username,
            'password': parsed.password,
            'database': parsed.path.lstrip('/'),
            'host': parsed.hostname,
            'port': parsed.port,
        }

    def run(self, direction="forward"):
        conn = psycopg2.connect(application_name=DB_NAME, **self.parse_pgurl(DB_URL))
        conn.autocommit = True
        cur = conn.cursor()
        migrations_folder = resource_filename('dasy', 'migrations')
        migration_names = [
            i for i in os.listdir(migrations_folder) if (
                i != '__pycache__' and os.path.isdir(os.path.join(migrations_folder, i))
            )
        ]

        logger.info('Found migrations: ' + ', '.join(migration_names))

        to_run = None
        if direction == 'forward':
            try:
                cur.execute('SELECT name FROM migration_history ORDER BY name;')
                completed_migrations = [m[0] for m in cur]
            except psycopg2.ProgrammingError:
                # The first migration creates the migration_history table.  So the query
                # on that table will fail if we have never run migrations.
                completed_migrations = []

            logger.info('Already run: ' + ', '.join(completed_migrations))

            to_run = sorted(list(set(migration_names).difference(completed_migrations)))
        elif direction == 'backward':
            to_run = sorted(list(set(migration_names)))
            to_run = to_run[::-1]

        if not len(to_run):
            logger.info('No migrations need running.')
            return
        logger.info('Migrations to run: ' + ', '.join(to_run))

        for m in to_run:
            logger.info('Running %s.' % m)
            script = os.path.join(migrations_folder, m, f'{direction}.sql')
            sql = open(script).read()
            try:
                cur.execute(sql)
            except Exception as e:
                logger.info(f"Error Occurred {e.args}")




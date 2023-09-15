import sqlite3

import psycopg2
from dataclasses import astuple, fields
from data_classes import (Genre, Person, GenreFilmwork,
                          PersonFilmwork, Filmwork, TABLE_TO_DATACLASS)
from settings import DSL, DB_PATH, TABLE_COLUMNS_NAME, BATCH_SIZE
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO, filename="load_data_log.log")


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


class SQLiteExtractor():
    def __init__(self, conn):
        self.conn = conn
 
    def upload_batches(self, table_name, postgres_saver):
        conn = self.conn
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        data_class = TABLE_TO_DATACLASS[table_name]
        column_names = ', '.join(field.name for field in fields(data_class))
        query = f"""
                SELECT {column_names}
                FROM {table_name};
                """
        try:
            curs.execute(query)
        except sqlite3.Error as err:                
            logging.error(err)
        while True:
            batch = curs.fetchmany(BATCH_SIZE)
            if not batch:
                break
            data = []
            for result in batch:
                data.append(data_class(**dict(result)))                  
            postgres_saver.insert_data(data, table_name)
                       
   
class PostgresSaver():
    def __init__(self, conn):
        self.conn = conn

    def insert_data(self, data, table_name):
        conn = self.conn
        column_names = TABLE_COLUMNS_NAME[table_name]
        column_placeholders = ', '.join(['%s'] * len(column_names))
        items = [astuple(item) for item in data]
        with conn.cursor() as cursor:
            args = ', '.join(cursor.mogrify(f"({column_placeholders})", item).decode('utf-8') for item in items)
            column_names = ', '.join(column_names)
            query = f"""
                    INSERT INTO content.{table_name} ({column_names})
                    VALUES {args}
                    ON CONFLICT (id) DO NOTHING;
                    """
            try:
                cursor.execute(query)
            except psycopg2.Error as err:
                logging.error(err)
            conn.commit()


def load_from_sqlite(connection, pg_conn):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)
    for table_name in TABLE_TO_DATACLASS:
        sqlite_extractor.upload_batches(table_name, postgres_saver)


if __name__ == '__main__':

    with conn_context(DB_PATH) as sqlite_conn, psycopg2.connect(**DSL) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

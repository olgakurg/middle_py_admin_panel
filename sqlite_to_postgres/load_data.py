import sqlite3

import psycopg2
from dataclasses import astuple, fields
from data_classes import (Genre, Person, GenreFilmwork,
                          PersonFilmwork, Filmwork, table_to_dataclass)
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

    def extract_to_dataclasses(self, table_name, iteration):
        data_class = table_to_dataclass[table_name]
        column_names = ', '.join(field.name for field in fields(data_class))
        skipped_num = BATCH_SIZE * (iteration-1)
        query = f"""
                SELECT {column_names}
                FROM {table_name}
                ORDER BY created_at
                LIMIT {BATCH_SIZE}
                OFFSET {skipped_num};
                """
        conn = self.conn
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        try:
            curs.execute(query)
        except sqlite3.Error as err:
            logging.error(err)
        results = curs.fetchall()
        lst = []
        for result in results:
            lst.append(data_class(**dict(result)))
        return lst


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
    for table_name in table_to_dataclass:
        current_batch_size = BATCH_SIZE
        iteration = 0
        while current_batch_size >= BATCH_SIZE:
            iteration += 1
            data = sqlite_extractor.extract_to_dataclasses(table_name, iteration)
            current_batch_size = len(data)
            postgres_saver.insert_data(data, table_name)


if __name__ == '__main__':

    with conn_context(DB_PATH) as sqlite_conn, psycopg2.connect(**DSL) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

from .common import process_file
from langchain.document_loaders.csv_loader import CSVLoader
from sqlite3 import Connection


def process_csv(conn: Connection, file, stats_db):
    return process_file(conn, file, CSVLoader, ".csv", stats_db=stats_db)

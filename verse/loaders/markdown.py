from .common import process_file
from langchain.document_loaders import UnstructuredMarkdownLoader
from sqlite3 import Connection


def process_markdown(conn: Connection, file, stats_db):
    return process_file(
        conn, file, UnstructuredMarkdownLoader, ".md", stats_db=stats_db
    )

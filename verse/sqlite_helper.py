# import sqlite3
from typing import Any
from sqlite3 import Connection
from datetime import datetime
import pytz

DB_NAME = "docdatabase.sqlite"
TABLE_NAME = "metadata"
TBL_CHAT_HISTORY = "chathistory"


def create_table(conn: Connection) -> None:
    cursor = conn.cursor()
    create_query = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
        id NUMERIC PRIMARY KEY,
        filehash TEXT NOT NULL,
        filename TEXT NOT NULL);"""
    cursor.execute(create_query)

    create_chathistory_query = f"""CREATE TABLE IF NOT EXISTS {TBL_CHAT_HISTORY}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        qsha NUMERIC NOT NULL,
        model TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        source TEXT,
        eventtime DATETIME);"""
    cursor.execute(create_chathistory_query)
    conn.commit()


def fetch_history(conn: Connection, model: str) -> list[Any]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM chathistory WHERE model=? ORDER BY eventtime DESC", (model,)
    )
    return cursor.fetchall()


def insert_chathistory(
    conn: Connection, model: str, question: str, answer: str, source: str
) -> None:
    tz = pytz.timezone("Europe/Berlin")
    command = """INSERT INTO chathistory(qsha,model,question,answer,source, eventtime) VALUES (?, ?, ?, ?, ?, ?)"""
    cur = conn.cursor()
    cur.execute("BEGIN")
    try:
        cur.execute(
            command,
            (
                hash(question),
                model,
                question,
                answer,
                source,
                datetime.now(tz).strftime("%d-%m-%Y %H:%M:%S"),
            ),
        )
        conn.commit()
    except conn.Error as e:
        print("Got an error: ", e)
        print("Aborting...")
        cur.execute("ROLLBACK")


def insert(conn: Connection, id: int, filehash: str, filename: str) -> None:
    command = """INSERT INTO {TABLE_NAME} VALUES (?, ?, ?)"""
    cur = conn.cursor()
    cur.execute("BEGIN")
    try:
        cur.execute(
            command,
            (
                id,
                filehash,
                filename,
            ),
        )
        conn.commit()
    except conn.Error as e:
        print("Got an error: ", e)
        print("Aborting...")
        cur.execute("ROLLBACK")


def insertmany(conn: Connection, datalist: list[tuple[int, str, str]]) -> None:
    cursor = conn.cursor()
    try:
        cursor.executemany(f"""INSERT INTO {TABLE_NAME} VALUES(?, ?, ?)""", datalist)
    except conn.Error as e:
        print("Got an error: ", e)
        print("Aborting...")
        cursor.execute("ROLLBACK")


def fetchall(conn: Connection):
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM {TABLE_NAME}""")
    return cursor.fetchall()


def droptable(conn: Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM {TABLE_NAME};""")
    conn.commit()
    print("Dropping Table!")
    return True


def is_id_exists(conn: Connection, id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM {TABLE_NAME} WHERE id = {id}""")
    data = cursor.fetchone()
    return True if data else False


def shutdown(conn: Connection):
    conn.close()

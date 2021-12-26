# Connection to the Database
import sqlite3


# Table names
TABLE_NOVELS = "novels"
TABLE_MANGAS = "mangas"
TABLE_ANIME = "anime"
TABLE_BOOKS = "books"

# Column names
COL_NOVEL_ID = "novel_id"
COL_NOVEL_TITLE = "title"
COL_NOVEL_LOCATION = "location"
COL_NOVEL_COVER = "cover"

COL_MANGA_ID = "manga_id"
COL_MANGA_TITLE = "title"
COL_MANGA_LOCATION = "location"
COL_MANGA_COVER = "cover"

COL_BOOK_ID = "book_id"
COL_BOOK_TITLE = "title"
COL_BOOK_AUTHOR = "author"
COL_BOOK_LOCATION = "location"


class DB:
    def __init__(self) -> None:
        self.conn = None
        self.cursor = None
        # Connect to the database
        self.connection()

        # Set the schema
        self.set_schema()

    def connection(self):
        """
        Connect to the Database.
        """
        self.conn = sqlite3.connect("cj/data/cj.db")
        # Set the row factory to return a dictionary
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        """
        Close any cursors and connections.
        """
        self.cursor.close()
        self.conn.close()

    def set_schema(self):
        """
        Setup the schema for the database.
        """
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NOVELS} (
                {COL_NOVEL_ID} INTEGER PRIMARY KEY,
                {COL_NOVEL_TITLE} TEXT,
                {COL_NOVEL_LOCATION} TEXT,
                {COL_NOVEL_COVER} TEXT
            )
        """)
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_MANGAS} (
                {COL_MANGA_ID} INTEGER PRIMARY KEY,
                {COL_MANGA_TITLE} TEXT,
                {COL_MANGA_LOCATION} TEXT,
                {COL_MANGA_COVER} TEXT
            )
        """)
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_BOOKS} (
                {COL_BOOK_ID} INTEGER PRIMARY KEY,
                {COL_BOOK_TITLE} TEXT,
                {COL_BOOK_AUTHOR} TEXT,
                {COL_BOOK_LOCATION} TEXT
            )
        """)

        self.conn.commit()
        self.close()

    # Helper methods for executing queries, inserting, and updating
    def execute(self, query: str, values: tuple = None) -> None:
        """
        Execute a query.
        """
        self.connection()
        self.cursor.execute(query, values)
        self.commit()

    def insert(self, table: str, values: tuple) -> None:
        """
        Insert values into a table.
        """
        self.execute(f"INSERT INTO {table} VALUES {values}")

    def update(self, table: str, values: tuple, where: str) -> None:
        """
        Update values in a table.
        """
        self.execute(f"UPDATE {table} SET {values} WHERE {where}")

    def commit(self):
        """
        Commit the changes to the database And close after close the connection.
        """
        self.conn.commit()
        self.close()

    def query(self, query: str, values: tuple = None) -> list:
        """
        Query the database.
        """
        self.connection()
        self.execute(query, values)
        return self.cursor.fetchall()
    
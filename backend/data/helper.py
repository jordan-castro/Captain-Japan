import sqlite3
from os import getcwd
# from backend.utils.private_key_handler import save_locally

# Database values (Tables, columns, etc)


SCRAPE_TABLE = "scrape"
# Columns for scrape
SCRAPE_ID = "scrapeid"
SCRAPE_TITLE = "title"
SCRAPE_TYPE = "type"
SCRAPE_COVER = "cover"
SCRAPE_SOURCE = "source"


USERS_TABLE = "users"
# Columns for users
USER_ID = "userid"
USER_NAME = "name"
USER_JOIN_DATE = "joined_date"
USER_WALLET = "wallet"
USER_PATH_TO_SK = "path_to_sk"
USER_PSEUDO = "pseudo"
USER_SUB_TYPE = "subscription_type"
USER_LAST_PAYED = "last_payed"


DOWNLOADS_TABLE = "donwloads"
# Columns for downlaods
DOWNLOAD_ID = "downlaodid"
DOWNLOAD_SCRAPE_ID = SCRAPE_ID
DOWNLOAD_USER_ID = USER_ID
DOWNLOAD_NAME = "name"
DOWNLOAD_DATE = "date"
DOWNLOAD_LOC = "location"


APP_DATA_TABLE = "app_data"
# Columns for app_data
APP_DATA_ID = "id"
APP_VERSION = "version"
APP_DATABASE_VERSION = "db_version"


class DbHelper:
    def __init__(self, update=False):
        # Initiate connection
        self.con = sqlite3.connect(f"{getcwd()}/backend/data/cptjpn.db")
        # Setup row factory
        self.con.row_factory = sqlite3.Row

        if update:
            self.update_db()
        else:
            self.setup_db()

    def setup_db(self):
        cursor = self.con.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {DOWNLOADS_TABLE} (
                {DOWNLOAD_ID} INTEGER PRIMARY KEY,
                {DOWNLOAD_SCRAPE_ID} INTEGER NOT NULL,
                {DOWNLOAD_USER_ID} INTEGER NOT NULL,
                {DOWNLOAD_NAME} TEXT,
                {DOWNLOAD_DATE} INTEGER,
                {DOWNLOAD_LOC} TEXT
            ); 
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {USERS_TABLE} (
                {USER_ID} INTEGER PRIMARY KEY,
                {USER_NAME} TEXT,
                {USER_JOIN_DATE} INTEGER,
                {USER_WALLET} TEXT,
                {USER_PATH_TO_SK} TEXT,
                {USER_PSEUDO} TEXT,
                {USER_SUB_TYPE} INTEGER,
                {USER_LAST_PAYED} INTEGER
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {SCRAPE_TABLE} (
                {SCRAPE_ID} INTEGER PRIMARY KEY,
                {SCRAPE_TITLE} TEXT,
                {SCRAPE_COVER} TEXT,
                {SCRAPE_SOURCE} TEXT NOT NULL,
                {SCRAPE_TYPE} INTEGER NOT NULL
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {APP_DATA_TABLE} (
                {APP_DATA_ID} INTEGER PRIMARY KEY,
                {APP_DATABASE_VERSION} INTEGER NOT NULL,
                {APP_VERSION} INTEGER NOT NULL
            )
            """
        )

        self.con.commit()
        cursor.close()

    def update_db(self):
        cursor = self.con.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {DOWNLOADS_TABLE};")
        cursor.execute(f"DROP TABLE IF EXISTS {USERS_TABLE};")
        cursor.execute(f"DROP TABLE IF EXISTS {SCRAPE_TABLE};")
        cursor.execute(f"DROP TABLE IF EXISTS {APP_DATA_TABLE};")
        
        self.con.commit()
        cursor.close()
        self.setup_db()
        
    def insert(self, table, row: dict):
        """
        Insert a new <row> into <table>.

        Params:
            - <table: str> the table name to insert into.
            - <row: dict> the row to insert
        """
        # Grab the data
        keys = row.keys()
        values = row.values()
        # Create SQL fields and values
        sql_fields = " , ".join(list(map(lambda key: str(key), keys)))
        sql_values = " , ".join(list(map(lambda value: "?", values)))

        # The SQL statement
        sql = f"INSERT INTO {table} ({sql_fields}) VALUES ({sql_values});"
        # Cursor
        cursor = self.con.cursor()
        cursor.execute(sql, tuple(list(values)))
        self.con.commit()
        cursor.close()

    def delete(self, table, id: int):
        """
        Delete a row based on its id.

        Params:
            - <table: str> The table to delete from.
            - <id: int> The id of the row
        """
        cursor = self.con.cursor()

        cursor.execute(f"DELETE FROM {table} WHERE id = {id};")

        self.con.commit()
        cursor.close()

    def query_specific(self, table, where=None, order=None):
        """
        Query from a specific table with a where claus.

        Params:
            - <table: str> the table to query from.

        Return: <list(Row)>
        """
        cursor = self.con.cursor()

        # The sql to execute
        sql = f"SELECT * FROM {table} "

        # Check params passed
        if where:
            sql += f"WHERE {where} "
        if order:
            sql += f"ORDER {order} "

        rows = cursor.execute(f"{sql};").fetchall()
        cursor.close()
        return list(map(lambda row: dict(row), rows))

    def query_downloads(self):
        """
        Query the downloads table.
        
        Return <list(Row)>
        """
        return self.query_specific(DOWNLOADS_TABLE)

    def query_users(self):
        """
        Query the users table.

        Return: <list(Row)>
        """
        return self.query_specific(USERS_TABLE)

    def delete_total(self, table):
        """
        Delete all from a table.

        Params:
            - <table: str> the table to delete from
        """
        cursor = self.con.cursor()
        cursor.execute(f"DELETE FROM {table}")
        self.con.commit()
        cursor.close()

    def close_db(self):
        self.con.close()

if __name__ == "__main__":
    db_helper = DbHelper(True)
    # db_helper.delete_total(USERS_TABLE)
    # db_helper.insert(USERS_TABLE, {
    #     USER_NAME: "James Garfield",
    #     USER_JOIN_DATE: 0,
    #     USER_WALLET: "0xf557844ed14133d9d18f266b2c7a748113aC4bE9", # Public Key from Local blockchain
    #     USER_PATH_TO_SK: save_locally(1, "0xee8686db60eb4babb47a8ee73065e2c9ba1795a8e296c0f94968a9ccd4cadd92"), # Private key from local blockchain
    #     USER_PSEUDO: "James",
    # })
    print(db_helper.query_users())

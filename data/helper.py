import sqlite3
from os import getcwd

# Database values (Tables, columns, etc)
DOWNLOADS_TABLE = "donwloads"
# Columns for downlaods
DOWNLOAD_ID = "id"
DOWNLOAD_TITLE = "title"
DOWNLOAD_NAME = "name"
DOWNLOAD_DATE = "date"
DOWNLOAD_LOC = "location"
DOWNLOAD_IMAGE = "image"


USERS_TABLE = "users"
# Columns for users
USER_ID = "id"
USER_NAME = "name"
USER_JOIN_DATE = "joined_date"
USER_WALLET = "wallet"
USER_PSEUDO = "pseudo"
USER_SUB_TYPE = "subscription_type"
USER_LAST_PAYED = "last_payed"


class DbHelper:
    def __init__(self, update=None):
        # Initiate connection
        self.con = sqlite3.connect(f"{getcwd()}/data/cptjpn.db")
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
                {DOWNLOAD_TITLE} TEXT,
                {DOWNLOAD_NAME} TEXT,
                {DOWNLOAD_DATE} INTEGER,
                {DOWNLOAD_LOC} TEXT,
                {DOWNLOAD_IMAGE} TEXT
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
                {USER_PSEUDO} TEXT,
                {USER_SUB_TYPE} INTEGER NOT NULL,
                {USER_LAST_PAYED} INTEGER
            )
            """
        )
        self.con.commit()
        cursor.close()

    def update_db(self):
        cursor = self.con.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {DOWNLOADS_TABLE};")
        cursor.execute(f"DROP TABLE IF EXISTS {USERS_TABLE};")
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
    db_helper = DbHelper()
    # db_helper.insert(DOWNLOADS_TABLE, {
    #     DOWNLOAD_NAME: "test",
    #     DOWNLOAD_DATE: int(time.time()),
    #     DOWNLOAD_LOC: "home",
    #     DOWNLOAD_IMAGE: "none"
    # })
    print(db_helper.query_downloads())

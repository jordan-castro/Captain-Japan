from backend.data.helper import DbHelper, APP_DATA_TABLE, APP_DATA_ID, APP_VERSION, APP_DATABASE_VERSION


class AppData:
    def __init__(self, version, db_version, id=None):
        self.version = version
        self.db_version = db_version
        self.id = id

    def sql_format(self):
        """
        Return object as SQL row.

        Returns: <dict>
        """
        row = {
            APP_VERSION: self.version,
            APP_DATABASE_VERSION: self.db_version
        }
        # Check for ID
        if self.id:
            row[APP_DATA_ID] = self.id

        return row

    @staticmethod
    def from_sql(row):
        """
        Convert SQL row to AppData object.
        
        Return: <AppData>
        """
        return AppData(
            version=row[APP_VERSION],
            db_version=row[APP_DATABASE_VERSION],
            id=row[APP_DATA_ID]
        )
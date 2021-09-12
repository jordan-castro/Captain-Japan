from backend.data.helper import DOWNLOAD_ID, DOWNLOAD_NAME, DOWNLOAD_LOC, DOWNLOAD_DATE, DOWNLOAD_SCRAPE_ID, DOWNLOAD_USER_ID
import time


class Download:
    def __init__(self, name, location, user_id, scrape_id=None, date=None, id=None):
        self.id = id
        self.name = name
        self.date = date or int(time.time())
        self.location = location
        self.user_id = user_id
        self.scrape_id = scrape_id


    def sql_format(self, scrape_id=None):
        """
        Return object in sql object.

        Return: <dict>
        """
        data = {
            DOWNLOAD_NAME: self.name,
            DOWNLOAD_DATE: self.date,
            DOWNLOAD_LOC: self.location,
            DOWNLOAD_USER_ID: self.user_id,
            DOWNLOAD_SCRAPE_ID: self.scrape_id or scrape_id
        }

        # Check if id exists and put it on if it does
        if self.id:
            data[DOWNLOAD_ID] = self.id
        
        return data

    @staticmethod
    def from_sql(row):
        """
        Create a Download object from a SQL row.

        Return <Download>
        """
        return Download(
            id=row[DOWNLOAD_ID],
            name=row[DOWNLOAD_NAME],
            user_id=row[DOWNLOAD_USER_ID],
            scrape_id=row[DOWNLOAD_SCRAPE_ID],
            location=row[DOWNLOAD_LOC],
            date=row[DOWNLOAD_DATE]
        )
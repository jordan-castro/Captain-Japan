from backend.data.helper import DOWNLOADS_TABLE, DOWNLOAD_ID, DOWNLOAD_TITLE, DOWNLOAD_NAME, DOWNLOAD_IMAGE, DOWNLOAD_LOC, DOWNLOAD_DATE
import time


class Download:
    def __init__(self, title, name, location, image, date=None, id=None):
        self.id = id
        self.title = title
        self.name = name
        self.date = date or int(time.time())
        self.location = location
        self.image = image
    
    def sql_format(self):
        """
        Return object in sql object.

        Return: <dict>
        """
        data = {
            DOWNLOAD_TITLE: self.title,
            DOWNLOAD_NAME: self.name,
            DOWNLOAD_DATE: self.date,
            DOWNLOAD_LOC: self.location,
            DOWNLOAD_IMAGE: self.image or ""
        }

        # Check if id exists and put it on if it does
        if self.id:
            data[DOWNLOAD_ID] = self.id
        
        return data
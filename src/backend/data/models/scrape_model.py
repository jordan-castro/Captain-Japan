from src.backend.data.helper import SCRAPE_TABLE, SCRAPE_TYPE, SCRAPE_SOURCE, SCRAPE_COVER, SCRAPE_TITLE, SCRAPE_ID, DbHelper


class Scrape:
    def __init__(self, type, source, title, id=None, cover=None):
        self.type = type
        self.source = source
        self.title = title
        self.id = id
        self.cover = cover

    def sql_format(self):
        """
        Convert the Scrape object to it's SQL counterpart.

        Returns: <dict>
        """
        row = {
            SCRAPE_TYPE: self.type,
            SCRAPE_TITLE: self.title,
            SCRAPE_SOURCE: self.source
        } 
        # Check if ID is passed
        if self.id:
            row[SCRAPE_ID] = self.id
        # Check if cover is passed
        if self.cover:
            row[SCRAPE_COVER] = self.cover
        # Return row
        return row

    @staticmethod
    def from_sql(row):
        """
        Convert a SQL row to Scrape object.

        Returns: <Scrape>
        """
        return Scrape(
            type=row[SCRAPE_TYPE],
            source=row[SCRAPE_SOURCE],
            title=row[SCRAPE_TITLE],
            id=row[SCRAPE_ID],
            cover=row[SCRAPE_COVER]
        )
### File to handle the holding of any sources
import os

from flask import json


class Source(object):
    def __init__(self, short, long, type, cover):
        self.short = short
        self.long = long
        self.type = type
        self.cover = cover
        super().__init__()

    def to_json(self):
        """
        Convert a scrape to json.
        """
        return {
            "short": self.short.lower(),
            "long": self.long,
            "type": self.type,
            "cover": self.cover
        }

    @staticmethod
    def from_json(json):
        """
        Generate a Source from json.
        """
        return Source(
            short=json['short'],
            long=json['long'],
            type=json['type'],
            cover=json['cover']
        )


def sources_path():
    return os.getcwd() + "/sources.json"


def read_sources():
    """
    Get a list of all sources available for scraping.

    Returns: <list(Source)>
    """
    data = []
    # Open the json file
    with open(sources_path(), 'r') as sources:
        data = json.load(sources)
    return list(
        map(lambda d: Source.from_json(d),data)
    )


def add_source(source: Source):
    """
    Create a new source.

    Params:
        - <source: Source> The source to add.
    """
    # Open the file first
    data = None
    with open(sources_path(), 'r') as sources:
        data = json.load(sources)
    data.append(source.to_json())
    # Update 
    with open(sources_path(), 'w') as sources:
        json.dump(data, sources)


# if __name__ == "__main__":
#     print(list(map(lambda s: s.to_json(), read_sources())))
    # add_source(Source(
    #     short="lnp",
    #     long="Light Novel Pub",
    #     type=0,
    #     cover=None
    # ))
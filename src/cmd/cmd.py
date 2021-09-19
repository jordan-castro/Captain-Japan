### The command line interface for operating captain japan
import optparse
import json
from src.backend.generator.epub_generator import generate_epub
from src.backend.data.helper import DbHelper
from src.backend.data.models.download_model import Download
from src.backend.api.download_handler import handle_download
from src.backend.api.scrape_handler import add_scrape, grab_scrape
from src.backend.data.models.scrape_model import Scrape
from src.backend.utils.globals import results


def main():
    parser = optparse.OptionParser('usage %prog ')
    parser.add_option('-s', dest='source_file', type='string', help='The location of the json source file.')
    parser.add_option('-e', '--epub', action="store_false", dest='epub', default=True, help='Should we convert contents of source to epub.')

    (options, args) = parser.parse_args()
    source_file = options.source_file
    epub = options.epub == False

    if not source_file:
        print("No source file was passed.")
        exit(0)

    if not 'json' in source_file.split('.')[-1]:
        print(f"{source_file} is not a valid source file!")
        exit(0)
    
    # Alright looks good. Let's get to downloading
    data = read_source_file(source_file)

    # if epub:
    #     # Chequea que la data si existe
    #     if not 'chapters' in data:
    #         print("There aren't any chapters to gen epub from!")
    #         exit(0)
    #     else:
    #         chapters = data['chapters']
    #         if not type(chapters) == list:
    #             print("We need a list of chapters.")
    #             exit(0)
    #     if not 'title' in data:
    #         title = input("What's the epub title?")
    #         if not title:
    #             print(f"User input: '{title}' is not a title")
    #             exit(0)
    #     else:
    #         title = data['title']
    #     # Generate a epub with the data passed
    #     generate_epub(chapters, title)
    #     exit(0)

    # Check if this is a new scrape
    if 'scrape' in data:
        scrape_data = data['scrape']
        scrape = Scrape(
            type=scrape_data['type'],
            source=scrape_data['source'],
            title=scrape_data['title'],
            cover=scrape_data['cover']
        )
        # Set the id
        scrape_id = add_scrape(scrape)
    else:
        # Grab the scrape.
        scrape_id = data['scrape_id']
        scrape = grab_scrape(scrape_id)

    # Check if we are downloading
    if 'download' in data:
        # Clear the results
        download_data = data['download']

        # Check if black list exists
        if 'black_list' in download_data:
            black_list = download_data['black_list'].split(',')
        else:
            black_list = []

        downloads = handle_download(
            title=download_data['title'],
            type=int(scrape.type),
            d_range=list(range(download_data['start'], download_data['end'])),
            source=scrape.source,
            scraped_id=int(scrape_id),
            blacklist=black_list
        )

        # Prettify output   
        print(json.dumps(downloads, indent=4))
        print()

        print(results.successfull)
        print("BAKA! It worked, but it's not because I like you or anything. BAKA!")
        print(f"\n{results.compiler_sugesstions}")
        print("BAKA! Something did not work out correctly!")

        if epub:
            print("Generating EPUB --- ")
            epub_path = generate_epub(
                list(
                    map(
                        lambda d: Download.from_sql(d), 
                        downloads
                    )
                ), 
            download_data['title'])
            print(f"Generated EPUB at {epub_path}")
            print("Happy Reading!")
            exit(1)


def read_source_file(path):
    """
    Read the source file .json file.

    Return <dict>
    """
    with open(path, 'r') as source:
        try:
            return json.load(source)   
        except:
            print(f"Issue in opening {path}.\nAre you sure it is a valid json file?")
            exit(0)


if __name__ == "__main__":
    db = DbHelper(True)
    db.close_db()
    main()
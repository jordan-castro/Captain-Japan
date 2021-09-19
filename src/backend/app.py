# This connects the backend business logic with the front end (HTML web app)
from src.backend.api.sources import read_sources
from src.backend.data.models.scrape_model import Scrape
from src.backend.api.scrape_handler import add_scrape, grab_scrapes
from src.backend.api.settings_handler import app_settings
from src.backend.api.download_handler import grab_scrape_downloads, handle_download
from flask import Flask, redirect, request, jsonify
from src.backend.server import CaptainJapanServer
from threading import Thread


# Server handler
server = CaptainJapanServer(host='localhost', port=8080)
t = Thread(target=server.start_server)
t.start()

# The API handler
app = Flask(__name__)


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# Declare routes
@app.route("/")
def home():
    """
    The home route. Takes user to CPTN_F web pages.
    """
    return "Welcome to Captain Japan!!!!"


@app.route("/download", methods=['POST'])
def download_route():
    # Grab the data
    data = request.get_json()
    # Time to parse some stuff
    download_title = data['title']
    download_type = data['type']
    download_chapter_start = int(data['start'])
    download_chapter_end = int(data['end'])
    download_scraped_id = int(data['id'])
    download_source = data['source']
    download_black_list = data['blacklist'].split(',')

    # Handle the download
    downloads = handle_download(
        download_title,
        download_type,
        list(range(download_chapter_start, download_chapter_end)),
        download_source,
        download_scraped_id,
        download_black_list
    )

    return jsonify(downloads)


@app.route('/search/<type>/<title>')
def search_route(type, title):
    return f'{title} {type}'


@app.route('/scrapes/add', methods=['POST'])
def add_scrape_route():
    # Grab the data
    data = request.get_json()
    # Parse
    scrape_title = data['title']
    scrape_type = data['type']
    scrape_cover = data['cover']
    scrape_source = data['source']

    try:
        add_scrape(
            Scrape(
                title=scrape_title,
                type=scrape_type,
                source=scrape_source,
                cover=scrape_cover
            )
        )
        return '1'
    except:
        return '0'


@app.route('/scrapes')
def scrapes_route():
    # Grab the scraped of the DB.
    scrapes = grab_scrapes()
    return jsonify(scrapes)


@app.route('/downloads/<scrape_id>')
def scrape_downloads_route(scrape_id):
    # Grab the downloads of the scrape id passed
    scrape_downloads = grab_scrape_downloads(scrape_id)
    return jsonify(scrape_downloads)


@app.route('/sources')
def sources_route():
    # Busca los sources
    sources = read_sources()
    return jsonify(
        list(
            map(
                lambda source: source.to_json(),
                sources
            )
        )
    )

# @app.route('/downloads/<user_id>')
# def user_downloads_route(user_id):
#     # Grab the downloads of the user passed
#     user_downloads = grab_user_downloads(user_id)
#     # Check res
#     if not user_downloads:
#         return '0'
#     else:
#         return jsonify(list(map(lambda d: d.sql_format(), user_downloads)))


# @app.route('/signup', methods=['POST'])
# def signup_route():
#     # Grab the data
#     data = request.get_json()
#     # Parse
#     user_f_name = data['fname']
#     user_l_name = data['lname']
#     user_pseudo = data['pseudo']

#     # Return the json from the user sign up
#     user = signup(user_f_name, user_l_name, user_pseudo)
#     return jsonify(user.sql_format())


# @app.route('/user-data', methods=['POST'])
# def user_data_router():
#     # Grab the user id passed
#     user_id = request.get_json()['userid']
#     # Query the user
#     user = grab_user(user_id)
#     return jsonify(user.sql_format())


@app.route("/close")
def route_close():
    """
    Route to close the server when done with app.
    """
    # t = Thread(target=server.close_server)
    # t.start()
    server.close_server()
    # Close the applicacion
    exit(0)


@app.route("/settings")
def route_settings():
    """
    Route to grab the settings of the application.
    """
    return jsonify(app_settings())


if __name__ == "__main__":
    # Run the app
    app.run(host=server.host, port=server.port + 10)

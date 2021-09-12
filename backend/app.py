# This connects the backend business logic with the front end (HTML web app)
from backend.api.download_handler import handle_download
from flask import Flask, redirect, request, jsonify
from flaskwebgui import FlaskUI
from backend.server import CaptainJapanServer
from threading import Thread


# Server handler
server = CaptainJapanServer(host='localhost', port=8080)
t = Thread(target=server.start_server)
t.start()

# The API handler
app = Flask(__name__)
# Convert WEB to Desktop GUI
ui = FlaskUI(app)


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


@app.route("/close")
def route_close():
    """
    Route to close the server when done with app.
    """
    server.close_server()


if __name__ == "__main__":
    # Run the app
    app.run(host=server.host, port=server.port + 10)
    # ui.run() 
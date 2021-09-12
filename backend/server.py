### Captain Japan's local server
import http.server
import socketserver


class CaptainJapanServer:
    """
    Captain Japan Server Handler.

    Important: Does not handle API only hosting of CPT_F pages.
    
    Note: Run's locally. Treats Users computer as a Server.
    """
    def __init__(self, host='0.0.0.0', port=344):
        Handler = http.server.SimpleHTTPRequestHandler
        self.port = port
        self.host = host
        self.server = socketserver.TCPServer((self.host, self.port), Handler)

    def start_server(self):
        """
        Starts the Captain Japan server.
        """
        print(f"Serving at {self.host}:{self.port}")
        self.server.serve_forever()

    def close_server(self):
        """
        Close the Captain Japan server.
        """
        print("Shutting down bub")
        self.server.shutdown()


if __name__ == "__main__":
    import time
    import threading

    cpts = CaptainJapanServer()
    t = threading.Thread(target=cpts.start_server)
    t.start()
    # cpts.start_server()
    for x in range(10):
        time.sleep(1)
        print(x)
    cpts.close_server()
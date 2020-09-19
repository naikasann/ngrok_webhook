import http.server
import json

class MyHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self):
        pass

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
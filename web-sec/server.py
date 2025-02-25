#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler


class RedirectHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)  # HTTP 302 Found (redirect)
        self.send_header("Location", "http://127.0.0.1/get_flag.php")
        self.end_headers()


port = 8001
server = HTTPServer(("0.0.0.0", port), RedirectHandler)
print(
    f"Serving at http://0.0.0.0:{port} (redirects to http://127.0.0.1/get_flag.php)")
server.serve_forever()

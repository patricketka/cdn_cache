import http.server

PORT = 40011


class handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'hello world!')


def main():
    server = http.server.HTTPServer(('', PORT), handler)
    print("serving")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print('server stopped')


if __name__ == "__main__":
    main()

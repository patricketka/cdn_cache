import http.server
import http.client
import sys

PORT = 40011

FILES = {}
FILE_RETRIEVER = http.client.HTTPConnection('cs5700cdnorigin.ccs.neu.edu', 8080)

def deploy_cache():
    CACHE_SIZE = 0
    with open('pageviews.csv', 'r', errors='ignore') as wiki_views:
        page_views = wiki_views.readlines()
        i = 0
        while CACHE_SIZE < 20000000:
            path = '/' + page_views[i].split(',')[0]
            FILE_RETRIEVER.request('GET', path)
            page_response = FILE_RETRIEVER.getresponse().read()
            FILES[path] = page_response
            CACHE_SIZE += sys.getsizeof(page_response)
            i += 1
            if i == 30:
                break


class handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path in FILES.keys():
            print('cached')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(FILES[self.path]))
        else:
            print('origin request')
            FILE_RETRIEVER.request('GET', self.path)
            response = FILE_RETRIEVER.getresponse()
            response_code = response.getcode()
            response_data = response.read()
            self.send_response(response_code)
            self.end_headers()
            if response_code == 200:
                self.wfile.write(response_data)


def main():
    deploy_cache()
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

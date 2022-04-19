#!/usr/bin/env python3
import http.server
import http.client
import os
import sys
import argparse
from socketserver import BaseRequestHandler
from typing import Tuple, Callable


class handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/grading/beacon':
            self.send_response(204)
            self.end_headers()
        elif self.path == '/kill':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Exit')
            raise sys.exit()
        else:
            code, response = self.__getattribute__('server').retrieve_file(self.path)
            self.send_response(code)
            self.end_headers()
            if code == 200:
                self.wfile.write(response)


class server(http.server.HTTPServer):

    def __init__(self, serverName, port, server_address: Tuple[str, int],
                 RequestHandlerClass: Callable[..., BaseRequestHandler]):
        self.origin_connection = http.client.HTTPConnection(serverName, port)
        self.files = {}
        super().__init__(server_address, RequestHandlerClass)

    def retrieve_file(self, path):
        if path in self.files.keys():
            return 200, self.files[path]
        else:
            self.origin_connection.request('GET', path)
            response = self.origin_connection.getresponse()
            code = response.getcode()
            response = response.read()
            return code, response

    def deploy_cache(self):
        CACHE_SIZE = 0
        with open('pageviews.csv', 'r', errors='ignore') as wiki_views:
            page_views = wiki_views.readlines()
            i = 0
            while CACHE_SIZE < 20000000:
                path = '/' + page_views[i].split(',')[0]
                self.origin_connection.request('GET', path)
                page_response = self.origin_connection.getresponse().read()
                self.files[path] = page_response
                CACHE_SIZE += sys.getsizeof(page_response)
                i += 1
                if i == 30:
                    break


def parse_arguments():
    """Parse the command line arguments to determine how program should run
    :return: A list of arguments passed in through the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, required=True)
    parser.add_argument('-o', type=str, required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()
    port_number = args.p
    origin_server = args.o
    my_server = server(origin_server, 8080, ('', port_number), handler)
    my_server.deploy_cache()
    try:
        my_server.serve_forever()
    except ValueError:
        print('yep')
        pass

    my_server.server_close()


main()


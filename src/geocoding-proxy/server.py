#!/usr/bin/python3

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
import time
import urllib.request
from urllib.parse import urlparse, parse_qs
import json
import argparse


urlTemplates = [
    'https://maps.googleapis.com/maps/api/geocode/outputFormat?address=%s&key=%s',
    'https://geocoder.cit.api.here.com/6.2/geocode.json?app_id=%s&app_code=%s&searchtext=%s'
    ]

genericErrorMessage = "An unknown error occurred"
encoding = "utf-8"

class GeocodingProxyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # TODO - invoke external geocoding services
        # until then...
        parsed_url = urlparse(self.path)
        qs_dict = parse_qs(parsed_url.query)
        self.wfile.write(bytes("<p>path: %s</p>" % parsed_url.path, encoding))
        self.wfile.write(bytes("<p>qs_dict: %s</p>" % qs_dict, encoding))
        self.huzza()
        
    def huzza(self, code = HTTPStatus.OK):
        self.send_response(code or HTTPStatus.OK)
        
    def oops(self, msg: str = genericErrorMessage, code: int = HTTPStatus.INTERNAL_SERVER_ERROR):
        self.wfile.write(bytes(msg or genericErrorMessage, encoding))
        self.send_response(code or HTTPStatus.INTERNAL_SERVER_ERROR)
        
parser = argparse.ArgumentParser()
parser.add_argument("--googleapikey", help="Your api_key to Google's geocoding service")
parser.add_argument("--hereapikey", help="Your app_id to HERE's geocoding service")
parser.add_argument("--hereapicode", help="Your app_code to HERE's geocoding service")
parser.add_argument("--host", help="hostname, default is empty meaning localhost")
parser.add_argument("--port", help="Port on which to listen, default is 8080", type=int)

args = parser.parse_args()
address = (args.host or "localhost", args.port or 8080)
server = HTTPServer(address, GeocodingProxyServer)
print(time.asctime(), "Server Starts - %s:%s" % address)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
print(time.asctime(), "Server Stops - %s:%s" % address)


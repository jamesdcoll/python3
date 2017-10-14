#!/usr/bin/python3

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib.request
import json
import argparse


urlTemplates = [
    'https://maps.googleapis.com/maps/api/geocode/outputFormat?address=%s&key=%s',
    'https://geocoder.cit.api.here.com/6.2/geocode.json?app_id=%s&app_code=%s&searchtext=%s'
    ]

class GeocodingProxyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))

parser = argparse.ArgumentParser()
parser.add_argument("--googleapikey", help="Your api_key to Google's geocoding service")
parser.add_argument("--hereapikey", help="Your app_id to HERE's geocoding service")
parser.add_argument("--hereapicode", help="Your app_code to HERE's geocoding service")
parser.add_argument("--host", help="hostname, default is empty meaning localhost")
parser.add_argument("--port", help="Port on which to listen, default is 8080", type=int)

args = parser.parse_args()
address = (args.host or 'localhost', args.port or 8080)

server = HTTPServer(address, GeocodingProxyServer)
print(time.asctime(), "Server Starts - %s:%s" % address)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
print(time.asctime(), "Server Stops - %s:%s" % address)


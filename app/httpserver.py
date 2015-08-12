#!/usr/bin/python

"""
Save this file as server.py
>>> python server.py 0.0.0.0 8001
serving on 0.0.0.0:8001

or simply

>>> python server.py
Serving on localhost:8000

You can use this to test GET and POST methods.

"""

import SimpleHTTPServer
import SocketServer
import logging
import cgi
from pprint import pprint
import sys
from os import path
import json

sys.path.append("../script")
if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
    I = sys.argv[1]
elif len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    I = ""
else:
    PORT = 8000
    I = ""

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)

        if self.path == "/pageFour":
            length = int(self.headers.getheader('content-length'))
            data = self.rfile.read(length)
            configuration_details = json.loads(data)
            print configuration_details["Connection Details"][0]["hostname"]
            from ptolemy import get_network_flow
            filename = get_network_flow(configuration_details)
            f = open (filename["svg"],"r")
            contents = f.read ()
            self.wfile.write (contents) 
            f.close ()
            return

        elif self.path == "/download-sample-template":
            f = open ("templates/sample.ptpl","r")
            contents = f.read ()
            self.wfile.write (contents) 
            f.close ()
            return
        else:
            logging.warning("======= POST VALUES =======")
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
httpd.serve_forever()
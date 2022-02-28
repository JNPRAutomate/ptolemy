#!/usr/bin/env/python

"""
Save this file as server.py
>>> python httpserver.py 0.0.0.0 8001
serving on 0.0.0.0:8001

or simply

>>> python httpserver.py
Serving on localhost:8000

You can use this to test GET and POST methods.

"""

import http.server
import socketserver
import logging
# import cgi
# from pprint import pprint
import sys
# from os import path
import os.path
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


class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)

        if self.path == "/download-sample-template":
            f = open("templates/sample.ptpl", "r")
            contents = f.read()
            self.wfile.write(contents)
            f.close()
            return
        else:
            # All the downloads have different requirement
            # that download template
            configuration_details = self.load_configuration()
            filename = configuration_details["Filename"]
            if self.path == "/pageFour":
                from ptolemy import get_network_flow  # type: ignore
                get_network_flow(configuration_details)
                filename = self.get_file_name(filename, "svg")
                f = open(filename, "r")
                contents = f.read()
                f.close()
                # logging.warning(f"Contents = {contents}")
                self.wfile.write(contents.encode())
                return
            elif self.path == "/download-svg":
                filename = self.get_file_name(filename, "svg")
                f = open(filename, "r")
                contents = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml")
                self.send_header("Content-Length", len(contents))
                self.end_headers()
                self.wfile.write(contents)
                f.close()
                return
            elif self.path == "/download-pdf":
                filename = self.get_file_name(filename, "pdf")
                f = open(filename, "r")
                contents = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Length", len(contents))
                self.end_headers()
                self.wfile.write(contents)
                f.close()
                return
            elif self.path == "/download-dot":
                filename = self.get_file_name(filename, "dot")
                f = open(filename, "r")
                contents = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/dot")
                self.send_header("Content-Length", len(contents))
                self.end_headers()
                self.wfile.write(contents)
                f.close()
                return
            elif self.path == "/download-png":
                filename = self.get_file_name(filename, "png")
                f = open(filename, "r")
                contents = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", len(contents))
                self.end_headers()
                self.wfile.write(contents)
                f.close()
                return
            elif self.path == "/download-json":
                filename = self.get_file_name(filename, "json")
                f = open(filename, "r")
                contents = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", len(contents))
                self.end_headers()
                self.wfile.write(contents)
                f.close()
                return
            # elif self.path == "/download-all":
            #     f = open (filename,"r")
            #     contents = f.read ()
            #     self.wfile.write (contents)
            #     f.close ()
            #     return
            elif self.path == "/view-log":
                filename = self.get_file_name(filename, "log")
                f = open(filename, "r")
                contents = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", len(contents))
                self.end_headers()
                self.wfile.write(contents)
                f.close()
                return
            else:
                logging.warning("======= POST VALUES =======")
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def load_configuration(self):
        length = int(self.headers.get('content-length'))
        data = self.rfile.read(length)
        configuration_details = json.loads(data)
        return configuration_details

    def get_file_name(self, receivedfilename, extension):
        filename = f"{os.path.sep}{extension}{os.path.sep}{receivedfilename}"
        return f"generated{filename}.{extension}"


Handler = ServerHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print(
    "Serving at: http://%(interface)s:%(port)s"
    % dict(interface=I or "localhost", port=PORT)
)
httpd.serve_forever()

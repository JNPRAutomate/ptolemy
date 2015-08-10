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
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        jd = json.loads(data)
        print jd["Connection Details"][0]["hostname"]
        # self.send_response(200, "OK")

        print "#####"
        #self.finish()
        #self.connection.close()

        if self.path == "/pageFour":
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            print postvars.get ("configuration", "asd")
            for key in postvars:
                print key
                '''
                f = open (filename)
                        contents = f.read ()
                        self.wfile.write (contents)
                        f.close ()
                '''
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == "/download-sample-template":
            # script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            #file_path = path.relpath()
            # abs_file_path = os.path.join(script_dir, rel_path)
            f = open ("templates/sample.ptpl","r")
            contents = f.read ()
            self.wfile.write (contents) 
            f.close ()
        else:
            # form = cgi.FieldStorage(
            #     fp=self.rfile,
            #     headers=self.headers,
            #     environ={'REQUEST_METHOD':'POST',
            #              'CONTENT_TYPE':self.headers['Content-Type'],
            #              }
            #              )
            logging.warning("======= POST VALUES =======")
            # for item in form.list:
            #     logging.warning(item)
            # logging.warning("\n")
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
httpd.serve_forever()
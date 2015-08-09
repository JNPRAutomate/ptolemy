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

import sys


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
        #else if (self: 
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

print "@rochacbruno Python http server version 0.1 (for testing purposes only)"
print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
httpd.serve_forever()





















# import sys
# import BaseHTTPServer
# from SimpleHTTPServer import SimpleHTTPRequestHandler


# HandlerClass = SimpleHTTPRequestHandler
# ServerClass  = BaseHTTPServer.HTTPServer
# Protocol     = "HTTP/1.0"

# if sys.argv[1:]:
#     port = int(sys.argv[1])
# else:
#     port = 8000
# server_address = ('', port)

# HandlerClass.protocol_version = Protocol
# httpd = ServerClass(server_address, HandlerClass)

# sa = httpd.socket.getsockname()
# print "Serving HTTP on", sa[0], "port", sa[1], "..."
# httpd.serve_forever()
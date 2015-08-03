from BaseHTTPServer import BaseHTTPRequestHandler


class GetHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        print "GPath:", self.path
        if self.path == "/asd.svg":
            filename = "asd.svg"
        elif self.path == "/xeditable.js":
            filename = "xeditable.js"
        else:    
            filename = "index.html"
        f = open (filename)
        contents = f.read ()
        self.wfile.write (contents) 
        f.close ()

        return

    def do_POST (self):
        print "PPath:", self.path
        if self.path == "/asd.svg":
            filename = "asd.svg"
        f = open (filename)
        contents = f.read ()
        self.wfile.write (contents) 
        f.close ()

        return


def startServer ():
    port = 8888
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('', 8888), GetHandler)
    server.serve_forever ()


def main ():
    startServer ()



if __name__ == '__main__':
    main ()
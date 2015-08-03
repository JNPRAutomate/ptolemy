"""
Example of setting up CORS with Bottle.py.
"""
from pprint import pprint
from bottle import Bottle, request, response, run
import json
app = Bottle()

@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.route('/ptolemy', method=['OPTIONS', 'GET','POST'])
def examples():
    """
    If you are using something like Spine.js you'll need to
    handle requests for the OPTIONS method. I haven't found a
    DRY way to handle this yet. I tried setting up a hook for before_request,
    but was unsuccessful for now.
    """
    if request.method == 'OPTIONS':
        return {}
    else:
    	PythonDict['POST'] = {}
    	for item in request.POST:
    		PythonDict['POST'][item]=request.POST.get(item)
    	return json.dumps(PythonDict, indent=3)+"\n"


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--host", dest="host", default="localhost",
                      help="hostname or ip address", metavar="host")
    parser.add_option("--port", dest="port", default=8080,
                      help="port number", metavar="port")
    (options, args) = parser.parse_args()
    run(app, host=options.host, port=int(options.port))


# postData = request.body.read()
    	# print(postData)
    	# pprint(request.forms.get("user"))
     #    return {'examples': [{
     #        'id': 1,
     #        'name': 'Foo'},{
     #        'id': 2,
     #        'name': 'Bar'}
     #    ]}





# from bottle import route, run, template

# @route('/ptolemy')
# def index():
#     return template('<b>Hello {{name}} Your program is working!!</b>!',name='Animesh')

# run(host='localhost', port=8080)

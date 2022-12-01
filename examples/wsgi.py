import os
import sys
from wsgiref import simple_server, util

from wsgiref.simple_server import make_server
from wsgitalkback import *

if __name__ == "__main__":
    # Get the path and port from command-line arguments
	path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
	port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
	
	sys.path.insert(0,os.getcwd() + os.sep + "app")
	import gate

	# Make and start the server until control-c
	httpd = simple_server.make_server("", port, gate.application)
	print(f"Serving {path} on port {port}, control-C to stop")
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("Shutting down.")
		httpd.server_close()
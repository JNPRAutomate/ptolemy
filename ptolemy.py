#!/usr/bin/env/python

import sys
import getopt
from csv_parser import CSVParser
from lldp_network import L1NetworkFlow
from pprint import pprint

def main(argv):
	user_arguments = {}
	try:
		opts, args = getopt.getopt(argv, "i:u:p:o:f:", ["in=", "user=","password=","log-path=","log-all","log-device","out=","out-all","out-device","out-format="])
	except getopt.GetoptError:
		#usage()
		sys.exit(2)
	for opt,args in opts:
		if opt in ("-h", "--help"):
			#usage()
			sys.exit()
		elif opt in ("-i","--in"):
			user_arguments["CSV File Path"] = args
		elif opt in ("-u","--user"):
			user_arguments["User"] = args
		elif opt in ("-p","--password"):
			user_arguments["Password"] = args
		elif opt in ("-o","--out"):
			user_arguments["Output Path"] = args
		elif opt == "--log-path":
			user_arguments["Log Path"] = args
		elif opt == "--log-device":
			user_arguments["Log Device"] = True
		elif opt == "--log-all":
			user_arguments["Log All"] = True
		elif opt == "--out-all":
			user_arguments["Output All"] = True
		elif opt == "--out-device":
			user_arguments["Output Device"] = True
		elif opt == "--out-format":
			user_arguments["Format"] = args
		else:
			print "Invalid Command"
			#usage()
	csv_parser = CSVParser()
	connection_data = csv_parser.parse(user_arguments)
	network = L1NetworkFlow()
	network.get_network_flow(connection_data)

if __name__ == "__main__":
    main(sys.argv[1:])


		
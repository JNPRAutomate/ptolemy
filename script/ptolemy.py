#!/usr/bin/env/python

import sys
import getopt
from csv_parser import CSVParser
from lldp_network import L1NetworkFlow
from pprint import pprint

def main(argv):
	user_arguments = {}
	try:
		opts, args = getopt.getopt(argv, "i:u:p:o:f:", ["in=", "user=","password=","log-path=","log","log-all","log-device","out=","out-all","out-device","out-format="])
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
		elif opt == "--log":
			user_arguments["Log"] = "Log"
		elif opt == "--log-device":
			user_arguments["Log"] = "Log Device"
		elif opt == "--log-all":
			user_arguments["Log"] = "Log All"
		elif opt == "--out-all":
			user_arguments["Output"] = "Output All"
		elif opt == "--out-device":
			user_arguments["Output"] = "Output Device"
		elif opt == "--out-format":
			user_arguments["Format"] = args
		else:
			print "Invalid Command"
			#usage()
	csv_parser = CSVParser()
	connection_data = csv_parser.parse(user_arguments)
	network = L1NetworkFlow()
	network.get_network_flow(connection_data)

def get_network_flow(configuration_details):
	# Parse the details
	global_credentials = configuration_details["Global Credentials"]
	filename = configuration_details["Filename"]
	device_data = {"data":[]}
	if global_credentials == "None":
		connection_details = configuration_details["Connection Details"]
		for connection in connection_details:
			device = {}
			device["Hostname"] = connection["hostname"]
			device["Username"] = connection["username"]
			device["Password"] = connection["password"]
			device["SSH Key Path"] = ""
			device["Port"] = connection["port"]
			device_data["data"].append(device)
	else:
		global_username = global_credentials["username"]
		global_password = global_credentials["password"]
		connection_details = configuration_details["Connection Details"]
		for connection in connection_details:
			device = {}
			device["Hostname"] = connection["hostname"]
			device["Username"] = global_username
			device["Password"] = global_password
			device["SSH Key Path"] = ""
			device["Port"] = connection["port"]
			device_data["data"].append(device)
	network = L1NetworkFlow()
	network.get_network_flow_external(device_data["data"],filename)
	# return filename

if __name__ == "__main__":
    main(sys.argv[1:])


		
#!/usr/bin/env/python

import csv

connection_data = {"data":[]}

class CSVParser:

	def parse(self, args):
		if args.lower().endswith(".csv"):
			f = open(args)
			reader = csv.DictReader(f, delimiter=',')
			for line in reader:
				connection = {}
				connection["Hostname"] = line["Hostname"]
				connection["Username"] = line["Username"]
				connection["Password"] = line["Password"]
				connection["SSH Key Path"] = line["SSH Key Path"]
				connection["Port"] = line["Port"]
				connection_data["data"].append(connection)
			f.close()
			print "CSV file "+args+ " parsed"
			return connection_data["data"]




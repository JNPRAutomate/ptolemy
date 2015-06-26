#!/usr/bin/env/python

import csv

device_data = {"data":[]}

class CSVParser:

	def parse(self, file_name):
		if file_name.lower().endswith(".csv"):
			f = open(file_name)
			reader = csv.DictReader(f, delimiter=',')
			for line in reader:
				device = {}
				device["Hostname"] = line["Hostname"]
				device["Username"] = line["Username"]
				device["Password"] = line["Password"]
				device["SSH Key Path"] = line["SSH Key Path"]
				device["Port"] = line["Port"]
				device_data["data"].append(device)
			f.close()
			print "CSV file "+file_name+ " parsed"
			return device_data["data"]




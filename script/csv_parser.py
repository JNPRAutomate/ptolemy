#!/usr/bin/env/python

import csv
from pprint import pprint

device_data = {"data":[]}
argument_keys = ("Hostname","Username","Password","SSH Key Path","Output Path","Log Path","Log Type","Output Type", "Format","Port")

class CSVParser:

	def parse(self, user_arguments):
		file_name = user_arguments.get("CSV File Path")
		if file_name and file_name.lower().endswith(".csv"):
			f = open(file_name)
			reader = csv.DictReader(f, delimiter=',')
			for line in reader:
				device = {}
				for key in argument_keys:
					# print key 
					# print line.get(key)
					device[key] = self.set_value(device,user_arguments,key,line.get(key))
				device_data["data"].append(device)
			f.close()
			#pprint(device_data)
			return device_data["data"]


	def set_value(self, device, dictionary, key, parsed_value):
		if dictionary.get(key) and dictionary[key]:
			device[key] = dictionary[key]
			# print key + " value set to "+ device[key]
		else:
			device[key] = parsed_value
		return device[key]



	




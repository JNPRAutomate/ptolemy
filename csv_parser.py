#!/usr/bin/env/python

import csv
from pprint import pprint

device_data = {"data":[]}

class CSVParser:

	def parse(self, user_arguments):
		file_name = user_arguments.get("CSV File Path")
		if file_name and file_name.lower().endswith(".csv"):
			f = open(file_name)
			reader = csv.DictReader(f, delimiter=',')
			for line in reader:
				device = {}
				device["Hostname"] = line["Hostname"]
				self.set_value(device,user_arguments,"Username",line["Username"])
				self.set_value(device,user_arguments,"Password",line["Password"])
				self.set_value(device,user_arguments,"SSH Key Path",line["SSH Key Path"])
				#self.set_value(device,user_arguments, "Username",line["Username"])
				#self.set_value(device,user_arguments, "Username",line["Username"])
				#self.set_value(device,user_arguments, "Username",line["Username"])
				device["Port"] = line["Port"]
				device_data["data"].append(device)
			f.close()
			#pprint(device_data)
			return device_data["data"]


	def set_value(self, device, dictionary, key, parsed_value):
		if dictionary.get(key) and dictionary[key]:
			device[key] = dictionary[key]
		else:
			device[key] = parsed_value



	




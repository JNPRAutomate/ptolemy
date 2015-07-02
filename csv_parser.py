#!/usr/bin/env/python

import csv
import getpass

device_data = {"data":[]}

class CSVParser:

	def parse(self, file_name):
		if file_name.lower().endswith(".csv"):
			f = open(file_name)
			reader = csv.DictReader(f, delimiter=',')
			for line in reader:
				device = {}
				hostname = line["Hostname"]
				device["Hostname"] = hostname
				username = line["Username"]
				device["Username"] = username
				#check if password is given or you need to enter it
				password = line["Password"]
				print password
				if password == "!!PROMPT!!":
					print "Entered"
					password = self.get_password(hostname,username)
				device["Password"] = password
				device["SSH Key Path"] = line["SSH Key Path"]
				device["Port"] = line["Port"]
				device_data["data"].append(device)
			f.close()
			return device_data["data"]

	def get_password(self,hostname,username):
		print 'Enter password associated with Hostname: '+hostname+' and Username: '+username 
		password = getpass.getpass()
		if not password:
			print "Password can't be empty. Please re-enter you password."
			return self.get_password(self,hostname,username)

		return password




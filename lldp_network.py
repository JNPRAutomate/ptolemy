from jnpr.junos import Device
from jnpr.junos.op.lldp import *
from pygraphviz import *
import time
import datetime
import os.path
import json
import traceback


class L1NetworkFlow():

	def get_network_flow(self, device_data):

		# A dictionary structure to have Host Names / Mac Addresses as Key and 
		# LLDP neighbour information as Values.
		lldp_neighbours_dict = {}
		lldp_neighbours_graph = AGraph()
		nodes = set()

		# set some default node attributes
		#def set_default_attributes:
		lldp_neighbours_graph.node_attr['style']='rounded,filled'
		lldp_neighbours_graph.node_attr['shape']='box'
		lldp_neighbours_graph.node_attr['fixedsize']='false'
		lldp_neighbours_graph.node_attr['fontcolor']='red'
		lldp_neighbours_graph.node_attr['fillcolor']='yellow'
		lldp_neighbours_graph.node_attr['fontname']='times'

		for connection in device_data:
			print "------------------------------------------------------------------------"
			print ''

			dev = None
			# Connect to the device
			print "INFO["+self.get_timestamp('%Y-%m-%d %H:%M:%S')+"] Connecting to "+connection["Hostname"]
			if connection["SSH Key Path"]:
				dev = self.get_device(connection["Username"], connection["Hostname"], connection["SSH Key Path"], connection["Port"] )
			else:
				dev = self.get_device(connection["Username"], connection["Hostname"], connection["Port"], connection["Password"] )

			
			print "INFO["+self.get_timestamp('%Y-%m-%d %H:%M:%S')+"] Waiting for connections to establish..."

			connected = False
			try:
				dev.open()
				connected = True
				# Temporary and won't work in actual scenario. Find a way to work with MAC Addresses or something that is unique in actual campus network for devices
				host = dev.facts["hostname"]
				print "INFO["+self.get_timestamp('%Y-%m-%d %H:%M:%S')+ "] Host: "+connection["Hostname"]+" User: "+connection["Username"]+" connected"
			except:
				print(traceback.format_exc())
				host = connection["Hostname"]
				print "ERROR["+self.get_timestamp('%Y-%m-%d %H:%M:%S')+ "] Host: "+connection["Hostname"]+" User: "+connection["Username"]+" connection failed"
			
			

			print "Source System Name : "+host

			if host not in nodes:
				nodes.add(host)
				lldp_neighbours_graph.add_node(host)
				if not connected:
					lldp_neighbours_graph.node_attr['fontcolor']='white'
					lldp_neighbours_graph.node_attr['fillcolor']='red'
					continue

			print "LLDP Neighbours for host : "+ connection["Hostname"]+" port : "+connection["Port"]
			
			neighbour_dict = self.generate_graph(dev,nodes,lldp_neighbours_graph)

			# Store the values in the dictionary
			lldp_neighbours_dict[host] = neighbour_dict
			print "LLDP neighbors added for host "+connection["Hostname"]
			dev.close()
		
		# Write the graph to a dot file
		graph_file_name = self.get_generated_filename("lldp_neighbours_graph_","dot")
		lldp_neighbours_graph.write(graph_file_name) # write to simple.dot
		print "Wrote graph to "+graph_file_name 

		# Write the dictionary to a JSON file for better readability
		json_file_name = self.get_generated_filename("lldp_neighbours_json_","json")
		# Open the file (w+ creates the file if it doesn't exist)
		output_file = open(json_file_name,'w+')
		output_file.write(json.dumps(lldp_neighbours_dict, indent = 4, sort_keys = True))
		print "Wrote JSON to "+json_file_name

	def get_device(self,username,hostname,password,portNumber):
		if not portNumber:
			dev = Device( user=username, host=hostname, password=password )
		else:
			dev = Device( user=username, host=hostname, password=password, port=portNumber )
		print "Username : "+ username
		return dev

	def get_device(self,username,hostname,ssh_private_key_file_path,portNumber):
		if not portNumber:
			dev = Device( user=username, host=hostname, ssh_private_key_file=ssh_private_key_file_path)
		else:
			dev = Device( user=username, host=hostname, ssh_private_key_file=ssh_private_key_file_path, port=portNumber )
		print "Username : "+ username
		print "SSH Key Path : "+ssh_private_key_file_path
		return dev

	def get_lldp_neighbors(self,dev):
		return LLDPNeighborTable(dev).get()

	def generate_graph(self, dev,nodes,lldp_neighbours_graph):
		# get the lldp neighbors
		lldp_neighbours = self.get_lldp_neighbors(dev)
		host = dev.facts["hostname"]

		neighbour_dict = {}
		for neighbour in lldp_neighbours:
			neighbour_info = {}
			print ''
			neighbour_info["local_int"] = neighbour.local_int
			neighbour_info["local_parent"] = neighbour.local_parent
			neighbour_info["remote_type"] = neighbour.remote_type
			neighbour_info["remote_chassis_id"] = neighbour.remote_chassis_id
			neighbour_info["remote_port_desc"] = neighbour.remote_port_desc
			neighbour_info["remote_sysname"] = neighbour.remote_sysname

			# print the values on the screen
			print "Destination System Name:", neighbour.remote_sysname
			print "Port Descriptione:" , neighbour.remote_port_desc
			print "Local Interface:", neighbour.local_int
			print "Parent Interface Name:" , neighbour.local_parent
			print "Chassis Id:", neighbour.remote_chassis_id
			print "Chassis Id Subtype:" , neighbour.remote_type
			print ''
			
			# Add node to create edge if it doesn't exist
			if neighbour.remote_sysname not in nodes:
				nodes.add(neighbour.remote_sysname)
				lldp_neighbours_graph.add_node(neighbour.remote_sysname)

			# Create an edge between host and neighbour
			source = lldp_neighbours_graph.get_node(host)
			destination = lldp_neighbours_graph.get_node(neighbour.remote_sysname)
			# Add data to the labels
			destination.attr['label'] = "< System Name: "+neighbour.remote_sysname +"<br/>Port Description: " + neighbour.remote_port_desc+"<br/>Local Interface: "+ neighbour.local_int+"<br/>Parent Interface Name: " + neighbour.local_parent+"<br/>Chassis Id: "+ neighbour.remote_chassis_id+"<br/>Chassis Id Subtype: " + neighbour.remote_type+"<br/> >"
			destination.attr['labelloc'] = 'b'
			lldp_neighbours_graph.add_edge(source,destination)
			lldp_neighbours_graph.get_edge(source,destination).attr['dir'] = 'both'
			lldp_neighbours_graph.get_edge(source,destination).attr['taillabel'] = neighbour.remote_port_desc
			lldp_neighbours_graph.get_edge(source,destination).attr['style'] = 'bold'
			lldp_neighbours_graph.get_edge(source,destination).attr['color'] = 'blue'

			#Add this to neighbor dictionary
			neighbour_dict["Destination System: "+neighbour.remote_sysname] = neighbour_info

		return neighbour_dict


	def get_generated_filename(self,filename, extension):
		# append the file name with local time stamp
		stringTimeStamp = self.get_timestamp('%Y_%m_%d_%H%M%S')
		filename = "generated" + os.path.sep + extension + os.path.sep + filename + stringTimeStamp + "." + extension
		directory = os.path.dirname(filename)
		if not os.path.exists(directory):
		    os.makedirs(directory)
		return filename

	def get_timestamp(self,stringFormat):
		timestamp = time.time()
		stringTimeStamp = datetime.datetime.fromtimestamp(timestamp).strftime(stringFormat)
		return stringTimeStamp
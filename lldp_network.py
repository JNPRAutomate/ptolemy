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

			dev = None
			# Connect to the device 
			if not connection["Port"]:
				dev = Device( user=connection["Username"], host=connection["Hostname"], password=connection["Password"] )

			elif connection["SSH Key Path"]:
				dev = Device( user=connection["Username"], host=connection["Hostname"], ssh_private_key_file=connection["SSH Key Path"], port=connection["Port"] )
				print "Username : "+ connection["Username"]
				print "SSH Key Path : "+connection["SSH Key Path"]
				print "SSH Key :"
			else:
				dev = Device( user=connection["Username"], host=connection["Hostname"], port=connection["Port"], password=connection["Password"] )


			# Temporary and won't work in actual scenario. Find a way to work with MAC Addresses
			host = connection["Hostname"]+connection["Port"]

			print "Host : "+connection["Hostname"]

			connected = False
			try:
				dev.open()
				connected = True
			except:
				print(traceback.format_exc())
			
			if host not in nodes:
				nodes.add(host)
				lldp_neighbours_graph.add_node(host)
				if not connected:
					lldp_neighbours_graph.node_attr['fontcolor']='white'
					lldp_neighbours_graph.node_attr['fillcolor']='red'
					continue

			print "LLDP Neighbours for host : "+ connection["Hostname"]+" port : "+connection["Port"]
			
			
			lldp_neighbours = LLDPNeighborTable(dev).get()
			neighbour_dict = {}
			print "Local Interface, Parent Interface name, Chassis Id Subtype, Chassis Id, Remote Port Description,System Name"
			for neighbour in lldp_neighbours:
				print ''
				neighbour_dict["local_int"] = neighbour.local_int
				neighbour_dict["local_parent"] = neighbour.local_parent
				neighbour_dict["remote_type"] = neighbour.remote_type
				neighbour_dict["remote_chassis_id"] = neighbour.remote_chassis_id
				neighbour_dict["remote_port_desc"] = neighbour.remote_port_desc
				neighbour_dict["remote_sysname"] = neighbour.remote_sysname

				# print the values on the screen
				print "System Name:", neighbour.remote_sysname
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


	def get_generated_filename(self,filename, extension):
		# append the file name with local time stamp
		timestamp = time.time()
		stringTimeStamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y_%m_%d_%H%M%S')
		filename = "generated" + os.path.sep + extension + os.path.sep + filename + stringTimeStamp + "." + extension
		directory = os.path.dirname(filename)
		if not os.path.exists(directory):
		    os.makedirs(directory)
		return filename
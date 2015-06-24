#!/usr/bin/env/python

import sys
import getopt
from csv_parser import CSVParser
from jnpr.junos import Device
from jnpr.junos.op.lldp import *
from pygraphviz import *
import time
import datetime
import os.path

class L1NetworkFlow():

	def get_network_flow(self, connection_data):
		# temporary variable to print the SRX numbers. Must go with proper impl
		count = 1

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

		for connection in connection_data:
			dev = None
			# Connect to the device 
			if not connection["Port"]:
				dev = Device( user=connection["Username"], host=connection["Hostname"], password=connection["Password"] )
			elif connection["SSH Key Path"]:
				dev = Device( user=connection["Username"], host=connection["Hostname"], ssh_private_key_file=connection["SSH Key Path"], port=connection["Port"] )
				print "Username : "+ connection["Username"]
				print "SSH Key Path : "+connection["SSH Key Path"]
				print "SSH Key :"
				try:
					ssh_private_key_file = open(connection["SSH Key Path"], "rU")
					print ssh_private_key_file.read()
					ssh_private_key_file.close()
					print 
				except IOError:
					print "Error! Could not open file!"
			else:
				dev = Device( user=connection["Username"], host=connection["Hostname"], port=connection["Port"], password=connection["Password"] )

			print "Host : "+connection["Hostname"]

			dev.open()

			print dev.facts

			print "------------------------------------------------------------------------"
			
			# Temporary and won't work in actual scenario. Find a way to work with MAC Addresses
			host = dev.facts["hostname"]
			if host not in nodes:
				nodes.add(host)
				lldp_neighbours_graph.add_node(host)
			print "LLDP Neighbours for ", host
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
			count += 1

		#print(lldp_neighbours_graph.string()) # print to screen
		# append the file name with local time stamp
		timestamp = time.time()
		stringTimeStamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y_%m_%d_%H%M%S')
		filename = "generated"+os.path.sep+"dot"+os.path.sep+"lldp_neighbours_graph_"+stringTimeStamp+".dot"
		directory = os.path.dirname(filename)
		if not os.path.exists(directory):
		    os.makedirs(directory)
		lldp_neighbours_graph.write(filename) # write to simple.dot
		print "Wrote "+filename 


def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hf:c:", ["file", "commandline"])
	except getopt.GetoptError:
		#usage()
		sys.exit(2)
	for opt,args in opts:
		if opt in ("-h", "--help"):
			#usage()
			sys.exit()
		elif opt in ("-f","--file"):
			csv_parser = CSVParser()
			connection_data = csv_parser.parse(args)
		elif opt in ("-c", "--commandline"):
			print "Command Line option chosen"
		else:
			print "Invalid Command"
			#usage()
	network = L1NetworkFlow()
	network.get_network_flow(connection_data)


# def breadth_first_search(node):
# 	visited, queue = set(), [start]
# 	while queue:
#         vertex = queue.pop(0)
#         if vertex not in visited:
#             visited.add(vertex)
#             queue.extend(graph[vertex] - visited)
#     return visited



if __name__ == "__main__":
    main(sys.argv[1:])


		
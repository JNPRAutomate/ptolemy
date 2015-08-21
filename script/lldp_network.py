from jnpr.junos import Device
from jnpr.junos.op.lldp import *
from pygraphviz import *
import time
import datetime
import os.path
import json
import traceback
import getpass
from pprint import pprint
import xml.etree.cElementTree as ET
import socket
from jnpr.junos.exception import RpcError
import logging

class L1NetworkFlow():


	def __init__(self):
		self.lldp_neighbours_dict = {}
		self.live_nodes = set()
		self.filename = ""
		self.useCurrentTimeStamp = True
		self.externalFlag = False

	def get_network_flow_external(self, device_data, filename):
		self.receivedfilename = filename
		self.useCurrentTimeStamp = False
		self.externalFlag = True
		self.get_network_flow(device_data)

	def get_network_flow(self, device_data):

		global_username = None
		global_password = None
		global_ssh= None

		# Logger Setup
		self.logger = logging.getLogger('Ptolemy')

		# create console handler and set level to debug
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		logFileName = self.get_generated_filename("","log")
		# Add File Handler for Logging
		hdlr = logging.FileHandler(logFileName)
		hdlr.setLevel(logging.DEBUG)
		#create a formatter
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		# Add formatters to the Handlers
		hdlr.setFormatter(formatter)
		ch.setFormatter(formatter)

		# Add Handlers to the Formatter
		self.logger.addHandler(hdlr) 
		# Use the Stream Handler only when it's not called from app
		if not self.externalFlag:
			self.logger.addHandler(ch)
		
		self.logger.setLevel(logging.DEBUG)
		self.logger.info("Welcome to Ptolemy - The Network Cartographer")

		# pprint(device_data)

		for connection in device_data:
			self.logger.info("------------------------------------------------------------------------")
			self.logger.info("")

			dev = None
			if connection["Password"] == "!!PROMPT!!":
				connection["Password"] = self.get_password(connection["Hostname"],connection["Username"])

			# Connect to the device
			self.logger.info("Connecting to %s",connection["Hostname"])

			if connection["SSH Key Path"]:
				dev = self.get_device(connection["Username"], connection["Password"],connection["Hostname"], connection["SSH Key Path"], connection["Port"] )
			else:
				dev = self.get_device_nossh(connection["Username"], connection["Hostname"], connection["Port"], connection["Password"] )

		
			self.logger.info("Waiting for connections to establish...");

			host = connection["Hostname"]
			try:
				dev.open()
				host = dev.facts["hostname"]
				self.live_nodes.add(host)
				# Temporary and won't work in actual scenario. Find a way to work with MAC Addresses or something that is unique in actual campus network for devices
				self.logger.info("Host: "+connection["Hostname"]+" User: "+connection["Username"]+" connected")
			except Exception, e:
				self.logger.error(e)
				self.logger.error("Host: "+connection["Hostname"]+" User: "+connection["Username"]+" connection failed")
				continue
				
			self.logger.info( "Source System Name : "+ host )

			self.logger.info( "LLDP Neighbours for host : "+ connection["Hostname"]+" port : "+connection["Port"] )
			
			neighbour_dict = self.get_lldp_neighbors(dev)

			# Store the values in the dictionary
			self.lldp_neighbours_dict[host] = neighbour_dict
			self.logger.info( "LLDP neighbors retrieved for host "+connection["Hostname"] )
			dev.close()
		

		#Generate the JSON file from the Dictionary
		self.write_json(self.lldp_neighbours_dict)

		#Generate the graph from the datastructures generated
		filename = self.generate_graph(self.lldp_neighbours_dict,self.live_nodes)
		# return filename

	def get_password(self,hostname,username):
		self.logger.info( 'Enter password associated with Hostname: '+hostname+' and Username: '+username )
		password = getpass.getpass()
		if not password:
			self.logger.info( "Password can't be empty. Please re-enter you password." )
			return self.get_password(self,hostname,username)

		return password

	def get_global_password(self):
		username =  raw_input('Enter global username to be used:  ')
		self.logger.info( 'Enter global password for Username: '+ username )
		password = getpass.getpass()
		while not password:
			self.logger.info( "Password can't be empty. Please re-enter your password." )
			password = getpass.getpass()

		return username, password

	def get_global_ssh(self):
		username = raw_input('Enter global username to be used:  ')
		ssh_path = raw_input('Enter global SSH File Path for Username: '+ username )
		while not ssh_path:
			self.logger.info( "SSH File path can't be empty. Please re-enter the path." )
			ssh_path = raw_input('Enter global SSH File Path for Username: '+ username )

		return username, ssh_path

	def get_device_nossh(self,username,hostname,portNumber,password):
		# trim the whitespaces
		portNumber = portNumber.strip()
		if not portNumber:
			dev = Device( user=username, host=hostname, password=password )
		else:
			self.logger.info( "Connect to Port : "+portNumber )
			dev = Device( user=username, host=hostname, password=password, port=portNumber )
		self.logger.info( "Username : "+ username )
		return dev

	def get_device(self,username,hostname,password,ssh_private_key_file_path,portNumber):
		if not portNumber:
			dev = Device( user=username, host=hostname, ssh_private_key_file=ssh_private_key_file_path)
		else:
			dev = Device( user=username, host=hostname, ssh_private_key_file=ssh_private_key_file_path, port=portNumber )
		self.logger.info( "Username : "+ username )
		return dev

	def get_lldp_neighbors(self,dev):
		# get the lldp neighbors
		#lldp_neighbours = self.get_lldp_neighbors(dev)
		host = dev.facts["hostname"]
		neighbour_dict = {}
		try:
			lldp_neighbours_information = dev.rpc.get_lldp_neighbors_information()
			lldp_neighbours = lldp_neighbours_information.getchildren()
			for neighbour in lldp_neighbours:
				neighbour_info = {}
				neighbour_details = neighbour.getchildren()
				for detail in neighbour_details:
					if detail.tag == 'lldp-remote-system-name':
						neighbour_info["Remote System Name"] = detail.text
					elif detail.tag == 'lldp-remote-port-id' or detail.tag == 'lldp-remote-port-description':
						# Above if statement in a Hack since some of the systems has lldp-remote-port-id and 
						# some have lldp-remote-port-description as their remote port identification
						neighbour_info["Remote Port Id"] = detail.text
					elif detail.tag == 'lldp-local-port-id':
						neighbour_info["Local Port Id"] = detail.text
					# elif detail.tag == 'lldp-local-parent-interface-name':
					# 	neighbour_info["Local Parent Interface Name"] = detail.text
					# elif detail.tag == 'lldp-remote-chassis-id':
					# 	neighbour_info["Remote Chassis Id"] = detail.text
					# elif detail.tag == 'lldp-remote-port-id-subtype' or detail.tag == 'lldp-remote-chassis-id-subtype':
					# 	neighbour_info["Remote Port Id Subtype"] = detail.text

				try:
					# print the values on the screen
					#print "Destination System Name:", neighbour_info["Remote System Name"]
					self.logger.info( "Remote Port Id: " + neighbour_info["Remote Port Id"] +"")
					self.logger.info( "Local Port Id: "+ neighbour_info["Local Port Id"] +"")
					#print "Local Parent Interface Name:" , neighbour_info["Local Parent Interface Name"]
					#print "Remote Chassis Id:", neighbour_info["Remote Chassis Id"]
					#print "Remote Chassis Id Subtype:" , neighbour_info["Remote Port Id Subtype"]
					self.logger.info( '' )
				except KeyError, e:
					self.logger.error(traceback.format_exc)
					# Do Nothing and just eat the exception
					# Some keys are not present in all systems
				if "Destination System: "+neighbour_info["Remote System Name"] in neighbour_dict:
					neighbour_dict["Destination System: "+neighbour_info["Remote System Name"]].update(neighbour_info)
				else:
					neighbour_dict["Destination System: "+neighbour_info["Remote System Name"]] = neighbour_info
		except RpcError, e:
			self.logger.info( "LLDP is not supported on this device." )
			#Add this to neighbor dictionary

		return neighbour_dict

	def generate_graph(self, dictionary, live_nodes):
		lldp_neighbours_graph = AGraph(strict = False, directed = True, overlap = "scale", splines="ortho", nodesep="0.5", rankdir = "LR")
		added = set()
		edge_count ={}
		added_edges = {}
		# Set the style attributes of the graph
		lldp_neighbours_graph.node_attr['style']='rounded'
		lldp_neighbours_graph.node_attr['shape']='box'
		lldp_neighbours_graph.node_attr['fixedsize']='false'
		lldp_neighbours_graph.node_attr['labelloc']='c'
		lldp_neighbours_graph.node_attr['fontname']='times'
		lldp_neighbours_graph.node_attr['fontcolor']='purple'
		lldp_neighbours_graph.node_attr['sep']='5'

		# Get the data from the dictionary and work on in
		for source in dictionary.keys():
			if source not in edge_count:
				edge_count[source] = 0
			# Create an edge between host and neighbour
			destination_systems = dictionary[source]
			if not destination_systems:
				lldp_neighbours_graph.add_node(source)
			else:
				# If there are remote connections
				for remote_sysname in destination_systems.keys():
					remote = destination_systems[remote_sysname]
					destination = remote["Remote System Name"] 
					local_port = remote["Local Port Id"]
					remote_port = remote["Remote Port Id"]
					# Check if same connection is already mapped between the nodes
					if source+"_to_"+destination in added_edges.keys() and local_port+"_to_"+remote_port == added_edges[source+'_to_'+destination]:
						continue
					elif destination+"_to_"+source in added_edges.keys() and remote_port+"_to_"+local_port == added_edges[destination+"_to_"+source]:
						continue
					# proceed if the connection doesn't exist
					key_str = local_port+"_"+remote_port
					# Hack to prevent edge labels overlapping edges
					#lldp_neighbours_graph.add_edge(source,destination,key=key_str+"invi",dir='both', style='invis', headlabel=remote_port+"invi", taillabel=local_port+"invi", minlen = 5)
					# Draw the actual edge
					lldp_neighbours_graph.add_edge(source,destination,key=key_str,dir='both', headlabel="    "+remote_port+"    ", taillabel="    "+local_port+"    ", style='bold',color='blue', minlen=3)
					# Hack to prevent edge labels overlapping edges
					#lldp_neighbours_graph.add_edge(source,destination,key=key_str+"invi1",dir='both', style='invis', headlabel=remote_port+"invi1", taillabel=local_port+"invi1", minlen = 5)
					# Add the edge to a dictionary so that bi directional edges don't get repeated
					added_edges[source+'_to_'+destination] = local_port+"_to_"+remote_port

					#maintain a count of number of edges per node
					if destination in edge_count:
						# using destination so that dead nodes or nodes not listed in CSV also get covered
						edge_count[destination] = edge_count[destination] + 1
					else:
						edge_count[destination] = 1
					# increase the number of outgoing edges too
					edge_count[source] = edge_count[source] + 1
					#lldp_neighbours_graph.add_edge(source,destination,key=key_str,dir='both',labelfloat = False, labeljust='c', taillabel=remote_port, headlabel=local_port, style='bold',color='blue')
					# Check if the node is live or dead and update the attribute if needed
					if destination not in live_nodes:
						node = lldp_neighbours_graph.get_node(destination)
						node.attr['fontcolor'] = 'red'

		# Resize all the nodes based on the number of incoming and outgoing nodes edges
		for node in lldp_neighbours_graph.nodes():
			if edge_count[node] > 0:
				node.attr['height'] = 0.3 * edge_count[node]
				node.attr['width'] = 0.3 * edge_count[node]
			else:
				node.attr['height'] = 2
				node.attr['fontcolor'] = 'orange'

		# Generate the graph once the whole topology is parsed
		filename = self.write_graph(lldp_neighbours_graph)
		# return filename

	def get_generated_filename(self,filename, extension):
		# append the file name with local time stamp
		if self.useCurrentTimeStamp:
			stringTimeStamp = self.get_timestamp('%Y_%m_%d_%H%M%S')
			filename = "generated" + os.path.sep + extension + os.path.sep + filename + stringTimeStamp + "." + extension
		else :
			filename = "generated" + os.path.sep + extension + os.path.sep + self.receivedfilename + "." + extension
		directory = os.path.dirname(filename)
		if not os.path.exists(directory):
		    os.makedirs(directory)
		return filename

	def get_timestamp(self,stringFormat):
		timestamp = time.time()
		stringTimeStamp = datetime.datetime.fromtimestamp(timestamp).strftime(stringFormat)
		return stringTimeStamp

	def write_graph(self, graph):
		# Write the graph to a dot file
		graph_file_name = self.get_generated_filename("graph_","dot")
		graph.write(graph_file_name)
		self.logger.info( '' )
		self.logger.info( "Wrote graph to "+graph_file_name )
			
		#neato, dot, twopi, circo, fdp, nop, wc, acyclic, gvpr, gvcolor, ccomps, sccmap, tred, sfdp.
		# Write the graph to a SVG file
		graph_file_name = self.get_generated_filename("graph_","svg")
		graph.draw(graph_file_name,prog='dot') 
		self.logger.info( '' )
		self.logger.info( "Wrote graph to DOT SVG file "+graph_file_name )
		


	def write_json(self, dictionary):
		# Write the dictionary to a JSON file for better readability
		json_file_name = self.get_generated_filename("lldp_neighbours_json_","json")
		# Open the file (w+ creates the file if it doesn't exist)
		output_file = open(json_file_name,'w+')
		output_file.write(json.dumps(dictionary, indent = 4, sort_keys = True))
		self.logger.info( '' )
		self.logger.info( "Wrote JSON to "+json_file_name )
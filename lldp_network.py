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

class L1NetworkFlow():


	def __init__(self):
		self.lldp_neighbours_dict = {}
		self.live_nodes = set()

	def get_network_flow(self, device_data):

		global_username = None
		global_password = None
		global_ssh= None

		for connection in device_data:
			print "------------------------------------------------------------------------"
			print ''

			dev = None
			# # Check if global credentials are to be entered
			# if connection["Username"] == "!!GLOBAL!!" and connection["Password"] == "!!GLOBAL!!":
			# 	if not (global_username and global_password):
			# 		global_username, global_password = self.get_global_password()
			# 	connection["Username"] = global_username
			# 	connection["Password"] = global_password
			# elif connection["Username"] == "!!GLOBAL!!" and connection["SSH Key Path"] == "!!GLOBAL!!":
			# 	if not (global_username and global_ssh):
			# 		global_username, global_ssh = self.get_global_ssh()
			# 	connection["Username"] = global_username
			# 	connection["SSH Key Path"] = global_ssh
			#check if password is given or you need to enter it
			#el
			if connection["Password"] == "!!PROMPT!!":
				connection["Password"] = self.get_password(connection["Hostname"],connection["Username"])

			# Connect to the device
			print "INFO["+self.get_timestamp('%Y-%m-%d %H:%M:%S')+"] Connecting to "+connection["Hostname"]
			if connection["SSH Key Path"]:
				dev = self.get_device(connection["Username"], connection["Password"],connection["Hostname"], connection["SSH Key Path"], connection["Port"] )
			else:
				dev = self.get_device_nossh(connection["Username"], connection["Hostname"], connection["Port"], connection["Password"] )

			
			print "INFO["+self.get_timestamp('%Y-%m-%d %H:%M:%S')+"] Waiting for connections to establish..."

			# !!!!!NOT ALL Systems have Reverse DNS Lookup- Won't work.
			# Reverse DNS look up each node and get it's hostname
			#host_add = connection["Hostname"]
			#host = socket.gethostbyaddr(host_add)
			#self.nodes.add(host)
			host = connection["Hostname"]
			try:
				dev.open()
				host = dev.facts["hostname"]
				self.live_nodes.add(host)
				# Temporary and won't work in actual scenario. Find a way to work with MAC Addresses or something that is unique in actual campus network for devices
				print "INFO["+self.get_timestamp('%Y-%m-%d %H:%M:%S')+ "] Host: "+connection["Hostname"]+" User: "+connection["Username"]+" connected"
			except:
				print(traceback.format_exc())
				print "ERROR["+self.get_timestamp('%Y-%m-%d %H:%M:%S')+ "] Host: "+connection["Hostname"]+" User: "+connection["Username"]+" connection failed"
				continue
				
			print "Source System Name : "+ host

			print "LLDP Neighbours for host : "+ connection["Hostname"]+" port : "+connection["Port"]
			
			neighbour_dict = self.get_lldp_neighbors(dev)

			# Store the values in the dictionary
			self.lldp_neighbours_dict[host] = neighbour_dict
			print "LLDP neighbors retrieved for host "+connection["Hostname"]
			dev.close()
		

		#Generate the JSON file from the Dictionary
		self.write_json(self.lldp_neighbours_dict)

		#Generate the graph from the datastructures generated
		self.generate_graph(self.lldp_neighbours_dict,self.live_nodes)

	def get_password(self,hostname,username):
		print 'Enter password associated with Hostname: '+hostname+' and Username: '+username 
		password = getpass.getpass()
		if not password:
			print "Password can't be empty. Please re-enter you password."
			return self.get_password(self,hostname,username)

		return password

	def get_global_password(self):
		username =  raw_input('Enter global username to be used:  ')
		print 'Enter global password for Username: '+ username 
		password = getpass.getpass()
		while not password:
			print "Password can't be empty. Please re-enter your password."
			password = getpass.getpass()

		return username, password

	def get_global_ssh(self):
		username = raw_input('Enter global username to be used:  ')
		ssh_path = raw_input('Enter global SSH File Path for Username: '+ username )
		while not ssh_path:
			print "SSH File path can't be empty. Please re-enter the path."
			ssh_path = raw_input('Enter global SSH File Path for Username: '+ username )

		return username, ssh_path

	def get_device_nossh(self,username,hostname,portNumber,password):
		# trim the whitespaces
		portNumber = portNumber.strip()
		if not portNumber:
			dev = Device( user=username, host=hostname, password=password )
		else:
			print "Connect to Port : "+portNumber
			dev = Device( user=username, host=hostname, password=password, port=portNumber )
		print "Username : "+ username
		return dev

	def get_device(self,username,hostname,password,ssh_private_key_file_path,portNumber):
		if not portNumber:
			dev = Device( user=username, host=hostname, ssh_private_key_file=ssh_private_key_file_path)
		else:
			dev = Device( user=username, host=hostname, ssh_private_key_file=ssh_private_key_file_path, port=portNumber )
		print "Username : "+ username
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
					print "Remote Port Id:" , neighbour_info["Remote Port Id"]
					print "Local Port Id:", neighbour_info["Local Port Id"]
					#print "Local Parent Interface Name:" , neighbour_info["Local Parent Interface Name"]
					#print "Remote Chassis Id:", neighbour_info["Remote Chassis Id"]
					#print "Remote Chassis Id Subtype:" , neighbour_info["Remote Port Id Subtype"]
					print ''
				except KeyError, e:
					pass
					# Do Nothing and just eat the exception
					# Some keys are not present in all systems
				if "Destination System: "+neighbour_info["Remote System Name"] in neighbour_dict:
					neighbour_dict["Destination System: "+neighbour_info["Remote System Name"]].update(neighbour_info)
				else:
					neighbour_dict["Destination System: "+neighbour_info["Remote System Name"]] = neighbour_info
		except RpcError, e:
			print "ERROR["+self.get_timestamp('%Y-%m-%d %H:%M:%S')+ "] LLDP is not supported on this device."
			#Add this to neighbor dictionary

		return neighbour_dict

	def generate_graph(self, dictionary, live_nodes):
		lldp_neighbours_graph = AGraph(strict = False, directed = True, overlap = "scale", splines="ortho", nodesep="1", rankdir = "LR")
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
					lldp_neighbours_graph.add_edge(source,destination,key=key_str,dir='both', headlabel="    "+remote_port+"    ", taillabel="    "+local_port+"    ", style='bold',color='blue', minlen=5)
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
				node.attr['height'] = edge_count[node]
				node.attr['width'] = edge_count[node]
			else:
				node.attr['height'] = 2
				node.attr['fontcolor'] = 'orange'

		# Generate the graph once the whole topology is parsed
		self.write_graph(lldp_neighbours_graph)

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

	def write_graph(self, graph):
		# Write the graph to a dot file
		graph_file_name = self.get_generated_filename("lldp_neighbours_graph_","dot")
		graph.write(graph_file_name) # write to simple.dot
		print ''
		print "Wrote graph to "+graph_file_name 

		# Write the graph to a dot file
		# graph_file_name = self.get_generated_filename("lldp_neighbours_graph_","png")
		# graph.draw(graph_file_name, prog="neato") # draw to png using circo
		# print ''
		# print "Wrote graph to image file "+graph_file_name 


	def write_json(self, dictionary):
		# Write the dictionary to a JSON file for better readability
		json_file_name = self.get_generated_filename("lldp_neighbours_json_","json")
		# Open the file (w+ creates the file if it doesn't exist)
		output_file = open(json_file_name,'w+')
		output_file.write(json.dumps(dictionary, indent = 4, sort_keys = True))
		print ''
		print "Wrote JSON to "+json_file_name
#!/usr/bin/env/python

import sys
import getopt
from csv_parser import CSVParser
from lldp_network import L1NetworkFlow


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


		
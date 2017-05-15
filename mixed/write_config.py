import argparse

import writing

# Setup for parsing command line arguments
# see writing module for options
parser = argparse.ArgumentParser(prog="config file writer", description='Writes the config files the commander uses.')
group = parser.add_mutually_exclusive_group()
parser.add_argument('-n','--folder', metavar="config_folder", default = "config", help= "folder to place config files. Topics will be sorted out automatically." )
group.add_argument('-w','--write_weights', metavar="filename", nargs='?', const = "example.out", help='write weights config files for commander' )
group.add_argument('-p','--write_parameters', metavar="filename", nargs='?', const = "example.out", help='write parameter config files for commander',)
group.add_argument('-t','--write_topology', metavar="filename", nargs='?', const = "example.out", help='write topology config files for commander',)

args = parser.parse_args()


if args.write_parameters:
	print "Writing parametrs config file."
	topic = writing.ParametersWriter(config_folder = args.folder)
	topic.write(filename=args.write_parameters)

elif args.write_topology:
	print "Writing topology config file."
	topic = writing.TopologyWriter(config_folder = args.folder)
	topic.write(filename=args.write_topology)

elif args.write_weights:
	print "Writing weights config file."
	topic = writing.WeightsWriter(config_folder = args.folder)
	topic.write(filename=args.write_weights)
	
else:
	print "No command selected. Run write_config.py -h for options."

import argparse

import writing

# Setup for parsing command line arguments
# see writing module for options
parser = argparse.ArgumentParser(prog="config file writer", description='Writes the config files the commander uses.')
parser.add_argument('-a','--write_all_parameters', action='store_true', help='write all config files for commander' )
parser.add_argument('-p','--write_parameters', action='store_true', help='write parameter config files for commander' )
parser.add_argument('-t','--write_topology', action='store_true', help='write topology config files for commander')
parser.add_argument('-w','--write_weights', action='store_true', help='write weights config files for commander')

args = parser.parse_args()

if args.write_all_parameters:

	args.write_parameters = args.write_topology = args.write_weights = args.write_all_parameters

if args.write_parameters:
	print "Writing parametrs config file."
	topic = writing.ParametersWriter(config_folder = "config")
	topic.write(filename="example.out")

if args.write_topology:
	print "Writing topology config file."
	topic = writing.TopologyWriter(config_folder = "config")
	topic.write(filename="example.out")

if args.write_weights:
	print "Writing weights config file."
	topic = writing.WeightsWriter(config_folder = "config")
	topic.write(filename="example.out")
	

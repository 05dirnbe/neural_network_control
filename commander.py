#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser(description='Generates and sends commands to the controller which interacts with the neural network.')
parser.add_argument('-q', '--quit', metavar="", help='Shutdown controller', type=str, default = "quit" )
parser.add_argument('-p','--pause', metavar="", help='Put controller in idle state', type=str, default = "pause")
parser.add_argument('-rw','--read_weights', metavar="", help='Tell controller to read weights', type=str, default = "read_weights")
parser.add_argument('-ww','--write_weights', metavar="", help='Tell controller to write weights', type=str, default = "write_weights")
parser.add_argument('-rp','--read_parameters', metavar="", help='Tell controller to read parameters', type=str, default = "read_parameters")
parser.add_argument('-wp','--write_parameters', metavar="", help='Tell controller to write parameters', type=str, default = "write_parameters")

args = parser.parse_args()


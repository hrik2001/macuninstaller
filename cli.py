from function import *
from argparse import ArgumentParser
from pprint import pprint

########### Arguements of the program ##############
parser = ArgumentParser()
parser.add_argument("-p", "--path", dest="path", required=True, help="Path to the app you want to search for related files")
parser.add_argument("-c", "--custom-path", nargs = '*',dest = "custom" , help = " Custom Paths where you want to search ")
args = parser.parse_args()
#####################################################

if not args.custom:
	print "macuninstaller is going to do a \u001b[31;1mUsual Scan\u001b[0m"
	pprint(scan(args.path))
else:
	print "macuninstaller is going to do a \u001b[31;1mCustom Scan\u001b[0m"
	pprint(custom_scan(args.path , args.custom))

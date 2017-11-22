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
	print "macuninstaller is going to do a \033[1m\033[31mUsual Scan\033[0m"
	files , folders = scan(args.path)
	print "\033[1m\033[33mFiles:\033[0m"
	print
	print
	pprint(files)
	print
	print
	print("\033[1m\033[35mFolders:\033[0m")
	pprint(folders)
else:
	print "macuninstaller is going to do a \033[1m\033[31mCustom Scan\033[0m"
	files , folders = custom_scan(args.path , args.custom)
	print "\033[1m\033[33mFiles:\033[0m"
	print
	print
	pprint(files)
	print
	print
	print("\033[1m\033[35mFolders:\033[0m")
	pprint(folders)

	
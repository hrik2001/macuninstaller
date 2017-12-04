from function import *
from argparse import ArgumentParser


########### Arguements of the program ##############
parser = ArgumentParser()
parser.add_argument("-p", "--path", dest="path", required=True, help="Path to the app you want to search for related files")
parser.add_argument("-c", "--custom-path", nargs = '*',dest = "custom" , help = " Custom Paths where you want to search ")
args = parser.parse_args()
#####################################################

if not args.custom:
	print "\n"
	print "macuninstaller is going to do an \033[1m\033[31mUsual Scan\033[0m"
	files , folders = thread_scanner(args.path)
	files = cleanup(files)
	folders = cleanup(folders)
	print "\n"*2
	print "\033[1m\033[33mFiles:\033[0m"
	print "\n"*2
	printer(files)
	print "\n"*2
	print("\033[1m\033[35mFolders:\033[0m")
	printer(folders)
else:
	print "\n"
	print "macuninstaller is going to do a \033[1m\033[31mCustom Scan\033[0m"
	print "\n"*2
	files , folders = thread_custom_scanner(args.path , args.custom)
	files = cleanup(files)
	folders = cleanup(folders)
	print "\033[1m\033[33mFiles:\033[0m"
	printer(files)
	print "\n"*2
	print("\033[1m\033[35mFolders:\033[0m")
	printer(folders)


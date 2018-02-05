from function import *
from argparse import ArgumentParser
from function import __doc__ as doc
from sys import version_info , exit
from os import popen , exit
if version_info[0] > 2:
	exit("Only Python2.7 is supported")

########### Arguements of the program ##############
parser = ArgumentParser()
parser.add_argument("-p", "--path", dest="path", required=True, help="Path to the app you want to search for related files")
parser.add_argument("-c", "--custom-path", nargs = '*',dest = "custom" , help = " Custom Paths where you want to search ")
args = parser.parse_args()
#####################################################

if not args.custom:
	print(doc)
	print("\n")
	print("macuninstaller is going to do an \033[1m\033[31mUsual Scan\033[0m")
	print("This may take time")
	files , folders = thread_scanner(args.path)
	files = cleanup(files)
	folders = cleanup(folders)
	chosen_files = selector(files, "Files")
	if chosen_files == 0:
		exit()
	chosen_folders = selector(folders, "Folders")
	if chosen_folders == 0:
		exit()
	files_to_delete = " "
	folders_to_delete = " " + args.path + " "

	for path in chosen_files:
		files_to_delete += " \"" + path + "\" "
	for path in chosen_folders:
		folders_to_delete += " \"" + path + "\" "
	print("Enter your password to delete everything you chose")
	cmd = "sudo rm " + files_to_delete + " ; sudo rm -rf " + folders_to_delete + " ;"
	a = popen(cmd)
	print a.read()
	a.close()
	for stuff in chosen_files:
		if os.path.isfile(stuff):
			print("Files still exists "+ stuff)
	for stuff in chosen_folders:
		if os.path.isdir(stuff):
			print("Folder still exists "+ stuff)
	print("Have a good day!")
else:
	print(doc)
	print("\n")
	print("macuninstaller is going to do a \033[1m\033[31mCustom Scan\033[0m")
	print("This may take time")
	files , folders = thread_custom_scanner(args.path , args.custom)
	files = cleanup(files)
	folders = cleanup(folders)
	chosen_files = selector(files, "Files")
	if chosen_files == 0:
		exit()
	chosen_folders = selector(folders, "Folders")
	if chosen_folders == 0:
		exit()
	files_to_delete = " "
	folders_to_delete = " " + args.path + " "

	for path in chosen_files:
		files_to_delete +=  " \"" + path + "\" "
	for path in chosen_folders:
		folders_to_delete +=  " \"" + path + "\" "

	print("Enter your password to delete everything you chose")
	cmd = "sudo rm " + files_to_delete + " ; sudo rm -rf " + folders_to_delete + " ;"
	a = popen(cmd)
	print a.read()
	a.close()
	for stuff in chosen_files:
		if os.path.isfile(stuff):
			print("Files still exists "+ stuff)
	for stuff in chosen_folders:
		if os.path.isdir(stuff):
			print("Folder still exists "+ stuff)
	print("Have a good day!")
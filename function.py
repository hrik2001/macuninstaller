import os
import plistlib
from subprocess import *
from threading import Thread
import queue
#from pprint import pprint

__author__ = "Rik \"Rik\" Bhattacharya "
__version__ = 0.1
__doc__ = "macuninstaller "+str(__version__)+"\n"+"Copyright hrik2001 2017 Rik \"Rik\" Bhattacharya.\nA command-line program to help you find those hidden files that stay here even when the apps get deleted"

'''
Contains useful functions for the uninstallation process
'''


def read_plist(directory):
	''' This function returns a tuple which contains (bundle_identifier , bundle_name , bundle_signature) of an app '''
	plistfile = plistlib.readPlist(directory)
	bundle_identifier = plistfile['CFBundleIdentifier']
	bundle_signature = plistfile['CFBundleSignature']
	bundle_name = plistfile['CFBundleName']
	return (bundle_identifier , bundle_name , bundle_signature)    #not in order :P


def find_plist(app_dir):
	''' This function returns a string which points to the file location of Info.plist '''
	return app_dir + "/Contents/Info.plist"

def find_user():
	''' This function returns the username of the user, so that we can search user's directory '''
	output = str(check_output(["whoami"]))
	return output[0:len(output)-1]



def dividing_BundleIdentifier(the_identifier):
	''' This function returns the useful bit of information from the bundleidentifier, if the bundleidentifier is zz.yyy.xxx, xxx will be returned '''
	return the_identifier.split(".")[len(the_identifier.split("."))-1]


def important_paths():
	''' List of all the important paths that the program should look into to find the related files '''
	paths = []
	paths.append("/Users/"+find_user()+"/Library")
	paths.append("/Library")
	paths.append("/var")
	paths.append("/System/Library")
	return paths

def finder(path , hints):
	''' This function asks for a path as a parameter, this parameter tells it where to search, another parameter is a list of strings, it will be used to match strings of file/folder names '''
	collection_file = []
	collection_folder = []
	for pwd , subdir , files in os.walk(path):
		for file in files :
			for clue in hints:
				if clue.lower() in file.lower():
					#print pwd+"/"+file
					collection_file.append(pwd+"/"+file)
		for folder in subdir:
			for clue in hints:
				if clue.lower() in folder.lower():
					#print pwd+"/"+folder
					collection_folder.append(pwd+"/"+folder)
	return collection_file , collection_folder


def scan(path_to_app):
	''' Default scan '''
	bundle_identifier , bundle_name , bundle_signature = read_plist(find_plist(path_to_app))
	hints = [dividing_BundleIdentifier(bundle_identifier) , bundle_name , bundle_signature]

	file_list = []
	folder_list = []

	for every_path in important_paths():
		fil , fol = finder(every_path , hints)
		for every_fil in fil :
			file_list.append(every_fil)
		for every_fol in fol :
			folder_list.append(every_fol)
	return file_list , folder_list

def custom_scan(path_to_app , custom_paths):
	''' Custom scan '''
	bundle_identifier , bundle_name , bundle_signature = read_plist(find_plist(path_to_app))
	hints = [dividing_BundleIdentifier(bundle_identifier) , bundle_name , bundle_signature]

	file_list = []
	folder_list = []

	for every_path in custom_paths:
		fil , fol = finder(every_path , hints)
		for every_fil in fil :
			file_list.append(every_fil)
		for every_fol in fol :
			folder_list.append(every_fol)
	return file_list , folder_list

######Threading bullshit##########
#benchedmark this and its good af

def dummy_finder(path , hints, q):
	q.put(finder(path, hints))

def thread_finder(paths , hints):
	q = queue.Queue()
	fil = []
	fol = []
	for path in paths:
		Thread(target=dummy_finder, args=(path, hints, q)).start()
		file_list , folder_list = q.get()
		#fil.append(file_list)
		#fol.append(folder_list)
		for thing in file_list:
			fil.append(thing)
		for thingy in folder_list:
			fol.append(thingy)
	return fil , fol
def thread_scanner(path_to_app):
	bundle_identifier , bundle_name , bundle_signature = read_plist(find_plist(path_to_app))
	hints = [dividing_BundleIdentifier(bundle_identifier) , bundle_name , bundle_signature]
	return thread_finder(important_paths(), hints)

def thread_custom_scanner(path_to_app , custom_paths):
	bundle_identifier , bundle_name , bundle_signature = read_plist(find_plist(path_to_app))
	hints = [dividing_BundleIdentifier(bundle_identifier) , bundle_name , bundle_signature]
	return thread_finder(custom_paths , hints)
##################################

def printer(the_list):
	for things in the_list:
		print things

def cleanup(the_list):
	cleaned_list = []
	for elements in the_list:
		if elements not in cleaned_list:
			cleaned_list.append(elements)
	return cleaned_list

#def file_in_same_folder_checker(file_list , folder_list):
#	cleaned_file_list = []
#	for stuff in file_list:
#		for elements in folder_list:
#			if elements not in stuff:
#				cleaned_file_list.append(stuff)
#	return file_list , folder_list

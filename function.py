import os
import plistlib
from subprocess import *
#from pprint import pprint

__author__ = "Rik \"Rik\" Bhattacharya "
__doc__ = '''
Free and good uninstallers for macOS are not available, so I decided to make my own. This file serves as a library and stores some necessary functions. A combination of these functions will be used to code the uninstaller

Open Source For Life
Free stuff for life

I have nothing else to say

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
	return the_identifier.split(".")[len(the_identifier.split("."))-1]


def important_paths():
	paths = []
	paths.append("/Users/"+find_user()+"/Library")
	paths.append("/Library")
	paths.append("/var")
	paths.append("/System/Library")
	paths.append("/Applications")
	return paths
	
def finder(path , hints):
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


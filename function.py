import os
import plistlib
from subprocess import *
from pprint import pprint

__author__ = "Shatabarto \"Rik\" Bhattacharya "
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
	return output[2:len(output)-3]



def dividing_BundleIdentifier(the_identifier):
	return the_identifier.split(".")

	
def quick_scan(username , arguements):
	#argurments = [ bundle_identifier , bundle_name , bundle_signature]
	file_list=[]
	dir_list=[]
	for pwd , subdir , files in os.walk("/Users/"+username+"/Library/Application Support/"):
		for things in files:
			for stuff in arguements:
				if stuff.lower() in things:
					file_list.append(pwd+"/"+things)
		for stuff in arguements:
			if stuff.lower() in pwd.split("/")[len(pwd.split("/"))-1]:
				dir_list.append(pwd)

	return dir_list , file_list




def full_scan(username , arguements):
#argurments = [ bundle_identifier , bundle_name , bundle_signature]
	file_list=[]
	dir_list=[]
	for pwd , subdir , files in os.walk("/"):
		for things in files:
			for stuff in arguements:
				if stuff.lower() in things:
					file_list.append(pwd+"/"+things)
		for stuff in arguements:
			if stuff.lower() in pwd.split("/")[len(pwd.split("/"))-1]:
				dir_list.append(pwd)

	return dir_list , file_list
	
def uninstaller(app_path , parameter):
	plist_path = find_plist(app_path)
	user = find_user()
	bundle_identifier , bundle_name , bundle_signature = read_plist(plist_path)
	if parameter == "f":
		pprint(full_scan(user,[bundle_identifier , bundle_name , bundle_signature]))
	elif parameter == "q":
		pprint(quick_scan(user,[bundle_identifier , bundle_name , bundle_signature]))
	else :
		print "enter a parameter"


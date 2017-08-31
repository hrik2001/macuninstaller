import os
import re
import plistlib

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


#for root , dirs , files in os.walk("/"):
	#pass




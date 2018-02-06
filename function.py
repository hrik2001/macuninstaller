import os
import plistlib
from subprocess import *
from threading import Thread
from sys import exit 
#from pprint import pprint
from curses import *

try:
	import queue
except ImportError:
	import Queue as queue

__author__ = "Rik \"Rik\" Bhattacharya "
__version__ = 2.0
__doc__ = "macuninstaller "+str(__version__)+"\n"+"Copyright hrik2001 2017 Rik \"Rik\" Bhattacharya.\nA command-line program to help you find those hidden files that stay here even when the apps get deleted"

'''
Contains useful functions for the uninstallation process
'''


def read_plist(directory):
	''' This function returns a tuple which contains (bundle_identifier , bundle_name , bundle_signature) of an app '''
	#This function takes the arguement of the PATH where the Info.plist is stored. Then it reads the CFBundleName and CFBundleIdentifier
	#And returns them. If Info.plist is not found (which will never happen as far as ik), then it will just return the name of the app.
	if os.path.isfile(directory):
		plistfile = plistlib.readPlist(directory)
		bundle_identifier = plistfile['CFBundleIdentifier']
		#bundle_signature = plistfile['CFBundleSignature']
		bundle_name = plistfile['CFBundleName']
		return (bundle_identifier , bundle_name) # , bundle_signature)    #not in order :P
	else:
		a = directory.split("/")[len(directory.split("/"))-2]
		a = a[0:len(a)-4]
		return a , a


def find_plist(app_dir):
	#Just adds Info.plist to the app directory
	''' This function returns a string which points to the file location of Info.plist '''
	if app_dir[len(app_dir)-1] == "/":
		app_dir = app_dir[0:len(app_dir)-1]
	if os.path.isdir(app_dir):
		return app_dir + "/Contents/Info.plist"
	else:
		exit("\033[1m\033[31mError:\033[0m Application doesn't exist.\nmacuninstaller will quit now")

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
	''' Default scan, searches into specific paths '''
	bundle_identifier , bundle_name  = read_plist(find_plist(path_to_app))
	hints = [dividing_BundleIdentifier(bundle_identifier) , bundle_name ]

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
	''' Custom scan, searches into the paths you specify '''
	bundle_identifier , bundle_name = read_plist(find_plist(path_to_app))
	hints = [dividing_BundleIdentifier(bundle_identifier) , bundle_name ]

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
#benchmarked this and its good af

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
	bundle_identifier , bundle_name  = read_plist(find_plist(path_to_app))
	hints = [dividing_BundleIdentifier(bundle_identifier) , bundle_name ]
	return thread_finder(important_paths(), hints)

def thread_custom_scanner(path_to_app , custom_paths):
	bundle_identifier , bundle_name  = read_plist(find_plist(path_to_app))
	hints = [dividing_BundleIdentifier(bundle_identifier) , bundle_name ]
	return thread_finder(custom_paths , hints)
##################################

def printer(the_list):
	#old version used this function
	for things in the_list:
		print(things)

def cleanup(the_list):
	#sometimes the file_list and the folder_list will contain the same files or folders (because of the loop)
	#so this just cleans it up
	cleaned_list = []
	for elements in the_list:
		if elements not in cleaned_list:
			cleaned_list.append(elements)
	return cleaned_list

def probably_wrong_paths():
	#a function to tell the inexperienced user what could be the wrong directory. But remember paths containing these could be right too. :)
	signs = []
	signs.append("/Library/Java")
	signs.append("/Library/Python")
	signs.append("/Library/Perl")
	signs.append("/Library/Ruby")
	signs.append("/System/Library/Frameworks/")
	return signs

def checker(element):
	#checks if the file is recommended or not
	a = 0
	for thing in probably_wrong_paths():
		if thing in element:
			a+=1
	return not a


def safe_printer(the_list):
	#prints with emojis for the user
	for stuff in the_list:
		if checker(stuff):
			print('\xf0\x9f\x98\x80 '+stuff) #smiley face
		else:
			print('\xf0\x9f\xa4\xa8 '+stuff) #confused face




def chooser():
	script = '''
	set question to display dialog "Which kind of scan do you want" buttons {"Default Scan", "Custom Scan"} default button 1
	set answer to button returned of question

	if answer is equal to "Default Scan" then
	do shell script "echo 1"
	else
	do shell script "echo 0"
	end if


	'''
	cmd = "osascript -e"+"'"+script+"'"
	output = os.popen(cmd).read()

	if output[0]=="1":
		return 1
	else:
		return 0

def displayer_applescript(the_list , title , prompt):
	cmd = '''set chs to choose from list {%s} with title "%s" with prompt "%s" OK button name "Done!" cancel button name "Choose None" with multiple selections allowed
	do shell script "echo "  & chs'''
	string_list = ""
	for stuff in the_list:
		if checker(stuff):
			string_list+="\"\xf0\x9f\x98\x80 "+stuff+":\","
		else:
			string_list+="\"\xf0\x9f\xa4\xa8 "+stuff+":\","
	string_list = string_list[0:len(string_list)-1]
	cmd = cmd % (string_list , title , prompt)
	output = os.popen("osascript -e" + "\'" + cmd + "\'").read()
	if "false" in output:
		return []
	else:
		#output = output[0:len(output)-1]
		output = output.split(":")#[0:len(output)-1]
		output = output[0:len(output)-1]
		for i in range(len(output)):
			output[i] = output[i][5:len(output[i])]
		return output

def folder_asker_applescript():
	cmd = '''set theName to the text returned of (display dialog "Write the paths of folder and seperate them via commas" default answer "%s" with title " Custom Folders Chooser")
	do shell script "echo " & theName'''
	imp_paths = ""
	for stuff in important_paths():
		imp_paths+=stuff+","
	cmd = cmd % imp_paths
	output = os.popen("osascript -e" + "\'" + cmd + "\'").read()
	output = output.split(",")
	folders = []
	for stuff in output:
		folders.append(stuff.strip())
	return folders

def app_chooser_applescript():
	cmd = '''set a to choose file with prompt "Select the app you want to uninstall" of type {"com.apple.application"} with multiple selections allowed
	set p to POSIX path of a
	do shell script "echo " & p'''
	output = os.popen("osascript -e" + "\'" + cmd + "\'").read()
	return output[0:len(output)-1]

def applescript_default_scanner():
	path_of_app = app_chooser_applescript()
	notification_scan_started("Default")
	files , folders = thread_scanner(path_of_app)
	files = cleanup(files)
	folders = cleanup(folders)
	#if test == "test":
	#printer(files)
	#printer(folders)
	notification("Default")
	files = displayer_applescript(files , "Files Found" , "Choose the Files you want to delete")
	folders = displayer_applescript(folders , "Folders Found" , "Choose the Folders you want to delete")
	printer(files)
	printer(folders)
	files_to_delete = " "
	folders_to_delete = " "

	for stuff in files:
		files_to_delete+=stuff+" "
	for stuff in folders:
		folders_to_delete+=stuff+" "

	folders_to_delete += path_of_app + " "
	cmd = "rm " + files_to_delete + " ; rm -rf " + folders_to_delete + " ;"
	ascript = "do shell script \"%s\" with administrator privileges" % cmd
	ascript = "osascript -e \'" + ascript + "\'"
	ascript = os.popen(ascript)
	ascript.close()



	#test part

	for stuff in files:
		if os.path.isfile(stuff):
			print("Files still exists "+ stuff)
	for stuff in folders:
		if os.path.isdir(stuff):
			print("Folder still exists "+ stuff)


def applescript_custom_scanner():
	path_of_app = app_chooser_applescript()
	custom_folders = folder_asker_applescript()
	notification_scan_started("Custom")
	files , folders = thread_custom_scanner(path_of_app , custom_folders)
	files = cleanup(files)
	folders = cleanup(folders)
	notification("Custom")
	#if test == "test":
	#printer(files)
	#printer(folders)
	files = displayer_applescript(files , "Files Found" , "Choose the Files you want to delete")
	folders = displayer_applescript(folders , "Folders Found" , "Choose the Folders you want to delete")


	printer(files)
	printer(folders)

	files_to_delete = " "
	folders_to_delete = " "

	for stuff in files:
		#os.remove(stuff)
		files_to_delete+=stuff+" "
	for stuff in folders:

		folders_to_delete+=stuff+" "

	folders_to_delete += path_of_app + " "
	cmd = "rm " + files_to_delete + " ; rm -rf " + folders_to_delete + " ;"
	ascript = "do shell script \"%s\" with administrator privileges" % cmd
	ascript = "osascript -e \'" + ascript + "\'"
	ascript = os.popen(ascript)
	ascript.close()



	#test part

	for stuff in files:
		if os.path.isfile(stuff):
			print("Files still exists "+ stuff)
	for stuff in folders:
		if os.path.isdir(stuff):
			print("Folder still exists "+ stuff)


def notification(text):
	cmd = '''display notification "Choose Files/Folders to delete" with title "macuninstaller" subtitle "%s scan complete"''' % text
	os.popen("osascript -e "+ "\'"+cmd+"\'")


def notification_scan_started(text):
	cmd = '''display notification "This will take time" with title "macuninstaller" subtitle "%s scan started"''' % text
	os.popen("osascript -e "+ "\'"+cmd+"\'")


def selector(a , stri):
	wah = []
	stdscr = initscr()
	stdscr.move(0,0)
	stdscr.keypad(True)
	noecho()
	printer = stdscr.addstr
	curs_set(0)

	max_row , max_cols = stdscr.getmaxyx()
	limit = max_row - 7

	def line_calc(string):
		div = len(string)/max_cols
		if len(string)%max_cols :
			div+=1
		return div

	printer = stdscr.addstr

	def mov_up(array,d_l):
		count = 0
		i = d_l
		output = ["\n"]
		while 1:
			count+=1
			count+= line_calc(array[i])
			if count > limit :
				break
			if (i) == (len(array) - 1):
				break
			i+=1
		u_l = i
		
		while d_l != (u_l + 1) :
			output.append(array[d_l])
			output.append("\n\n")
			d_l += 1

		return i , output

	def mid_printer(string , a = stdscr.getyx()[0]):
		printer(a , (max_cols - len(string))/2 , string)



	def mov_down(array, d_l):
		count = 0
		i = d_l
		output = ["\n"]
		while 1:
			count+=1
			count+= line_calc(array[i])
			if count > limit :
				break
			if (i) == 0:
				break
			i-=1
		u_l = i
		while u_l != (d_l + 1) :
			output.append(array[u_l])
			output.append("\n\n")
			u_l += 1

		return i , output

	up_l = 0 
	low_l, arr = mov_up(a , 0)
	vir_cur = 0


	def length(arrr):
		r = []
		for stuff in arrr:
			if ( stuff != "\n" ) and (stuff != "\n\n" ):
				r.append(stuff)
		return len(r)

	def highlighter(arrr , r , wah):
		count = 0
		printer("\n")
		for stuff in arrr:
			if ( stuff != "\n" ) and (stuff != "\n\n" ):
				if count == r :
					printer(stuff , A_REVERSE)
					printer("\n\n")
					count += 1
				else:
					if stuff in wah:
						printer(stuff , A_UNDERLINE)
						printer("\n\n")
					else:
						printer(stuff)
						printer("\n\n")
					count += 1

		mid_printer("macuninstaller | " + stri , max_row - 2)
		mid_printer("Space to select, q to quit and enter to proceed" , max_row - 1)

	def cleanup(the_list):
		cleaned_list = []
		for elements in the_list:
			if elements not in cleaned_list:
				cleaned_list.append(elements)
		return cleaned_list


	def adder(arrr , r, wah):
		count = 0
		printer("\n")
		for stuff in arrr:
			if ( stuff != "\n" ) and (stuff != "\n\n" ):
				if count == r :
					if stuff not in wah:
						wah.append(stuff)
					else:
						wah.remove(stuff)
					count += 1
				else:
					count += 1
		return wah
	ar_len = length(arr)
	highlighter(arr , vir_cur, wah)

	while 1:
		key = stdscr.getch()
		stdscr.clear()
		stdscr.move(0,0)
		if key == 113: #q
			stdscr.refresh()
			endwin()
			return 0
		elif key == KEY_DOWN:
			vir_cur += 1
			if vir_cur == ar_len:
				if low_l != len(a) - 1:
					low_l += 1
					up_l , arr = mov_down(a , low_l)
					ar_len = length(arr)
					vir_cur = ar_len - 1
					highlighter(arr , vir_cur, wah)
				else:
					vir_cur -= 1
					highlighter(arr , vir_cur, wah)
			else:
				highlighter(arr , vir_cur, wah)

		elif key == KEY_UP:
			vir_cur -= 1
			if vir_cur == -1 :
				if up_l != 0:
					up_l -= 1
					low_l , arr = mov_up(a , up_l)
					ar_len = length(arr)
					vir_cur = 0
					highlighter(arr , vir_cur, wah)
				else:
					vir_cur += 1
					highlighter(arr , vir_cur, wah)
			else:
				highlighter(arr , vir_cur, wah)
		elif key == ord(" "):
			wah = adder(arr , vir_cur, wah)
			stdscr.move(0,0)
			stdscr.clear()
			highlighter(arr , vir_cur, wah)
		elif key == ord("\n"):
			break
		else:
			stdscr.move(0,0)
			stdscr.clear()
			highlighter(arr , vir_cur, wah)

	stdscr.refresh()
	endwin()

	wah = cleanup(wah)
	return wah



#This is how a 16 year old codes
#Sorry if you find this bad
#
import os
import plistlib
from subprocess import *
from threading import Thread
import queue
from sys import exit
#from pprint import pprint
import tkinter as tk
import shutil

__author__ = "Shatabarto \"Rik\" Bhattacharya "
__version__ = 0.3
__doc__ = "macuninstaller "+str(__version__)+"\n"+"Copyright hrik2001 2017 Shatabarto \"Rik\" Bhattacharya.\nA command-line program to help you find those hidden files that stay here even when the apps get deleted"

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
		print things

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
			print '\xf0\x9f\x98\x80 '+stuff #smiley face
		else:
			print '\xf0\x9f\xa4\xa8 '+stuff #confused face


def displayer(the_list , text):
	root = tk.Tk()
	root.title("macuninstaller")
	root.protocol("WM_DELETE_WINDOW", exit)
	tk.Label(root , text= text , font = "Helvetica 18").pack()
	sb = tk.Scrollbar(orient="vertical")
	text = tk.Text(root, width=40, height=20, yscrollcommand=sb.set)
	sb.config(command=text.yview)
	sb.pack(side="right",fill="y")
	text.pack(side="top",fill="both",expand=True)
	a = [] #contains the boolean value (1/0) , whether the file has been selected or not


	for count in range(len(the_list)):
		a.append(tk.Variable())

		a[count].set(0) #the checkbox is unticked at first that is why, it has the value of 0

	for i in range(len(the_list)):
		cb = tk.Checkbutton(text="%s" % the_list[i],padx=0,pady=0,bd=0, variable= a[i])
		text.window_create("end", window=cb)
		text.insert("end", "\n")

	done_button = tk.Button(root, text="Done!", command=root.destroy ).pack()
	quit_button = tk.Button(root, text="Quit", command=exit ).pack()
	root.mainloop()
	list_returned = {}
	b = -1 #just getting used for indexing in the loop below
	for stuff in a:
		b+=1
		list_returned[the_list[b]] = stuff.get()
	return list_returned

def app_name_asker(text):
	root = tk.Tk()
	root.title("macuninstaller")
	root.protocol("WM_DELETE_WINDOW", exit)
	tk.Label(root , text= text , font = "Helvetica 20").pack()
	app_name = tk.StringVar()
	e = tk.Entry(root, textvariable=app_name , width=40)
	e.pack()
	done_button = tk.Button(root, text="Done!", command=root.destroy ).pack()
	quit_button = tk.Button(root, text="Quit", command=exit ).pack()
	root.mainloop()
	return app_name.get()

def gui_default_scanner():
    app_dir = app_name_asker("Enter the path of the app")

    files , folders = thread_scanner(app_dir)

    files = cleanup(files)
    folders = cleanup(folders)

    file_list = displayer(files, "Files found")
    folder_list = displayer(folders, "Folders found")

    files_to_delete = []
    folders_to_delete = []

    for stuff in file_list.items():
        if stuff[1]:
            files_to_delete.append(stuff[0])

    for stuff in folder_list.items():
        if stuff[1]:
            folders_to_delete.append(stuff[0])


    for stuff in files_to_delete:
		try:
			os.remove(stuff)
		except:
			pass


		#try:
        #	shutil.move(stuff, "/Users/macpc/.Trash")
		#except:
		#	os.remove(stuff)

    for stuff in folders_to_delete:
		try:
			shutil.rmtree(stuff)
		except:
			pass

		#try:
        #	shutil.move(stuff, "/Users/macpc/.Trash")
		#except:
		#	shutil.rmtree(stuff)

    shutil.rmtree(app_dir)

def custom_path_name_asker(text , text2 , array1):
	root = tk.Tk()
	root.title("macuninstaller")
	root.protocol("WM_DELETE_WINDOW", exit)
	tk.Label(root , text= text , font = "Helvetica 20").pack()
	app_name = tk.StringVar()
	dir_names = tk.StringVar()
	imp_dirs = ""
	for stuff in array1:
		imp_dirs += stuff + ','
	dir_names.set(imp_dirs[0:len(imp_dirs)-1])
	e = tk.Entry(root, textvariable=app_name , width=40)
	e.pack()
	tk.Label(root , text= text2 , font = "Helvetica 15").pack()
	f = tk.Entry(root, textvariable=dir_names , width=40)
	f.pack()
	done_button = tk.Button(root, text="Done!", command=root.destroy ).pack()
	quit_button = tk.Button(root, text="Quit", command=exit ).pack()
	root.mainloop()
	app_name = app_name.get()
	dir_names = dir_names.get().split(',')
	names_of_path = []
	for paths in dir_names:
		names_of_path.append(paths.strip())

	return app_name , names_of_path

def gui_custom_scanner():
    app_dir, dir_names = app_name_asker("Enter the path of the app", "Enter the paths where you want to search, seperate the paths with commas.\nSome important paths are already listed here" , important_paths())

    files , folders = thread_custom_scanner(app_dir , dir_names)

    files = cleanup(files)
    folders = cleanup(folders)

    file_list = displayer(files, "Files found")
    folder_list = displayer(folders, "Folders found")

    files_to_delete = []
    folders_to_delete = []

    for stuff in file_list.items():
        if stuff[1]:
            files_to_delete.append(stuff[0])

    for stuff in folder_list.items():
        if stuff[1]:
            folders_to_delete.append(stuff[0])


    for stuff in files_to_delete:
		try:
			os.remove(stuff)
		except:
			pass


		#try:
        #	shutil.move(stuff, "/Users/macpc/.Trash")
		#except:
		#	os.remove(stuff)

    for stuff in folders_to_delete:
		try:
			shutil.rmtree(stuff)
		except:
			pass

		#try:
        #	shutil.move(stuff, "/Users/macpc/.Trash")
		#except:
		#	shutil.rmtree(stuff)

    shutil.rmtree(app_dir)





#This is how a 16 year old codes
#Sorry if you find this bad
#

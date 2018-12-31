from function import *
import os

if os.getuid() != 0:
	cmd = '''display dialog "You need root privileges to run this script mate (HINT: run this python script with sudo)" with icon stop with title "Oops!"'''
	cmd = "osascript -e '" + cmd + "'" 
	a = os.popen(cmd)
	a.read()
	exit()

if chooser():
    applescript_default_scanner()
else:
    applescript_custom_scanner()


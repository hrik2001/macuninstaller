macuninstaller
-------------
macuninstaller is a python script that was written to uninstall mac apps. This script finds all the related files and folders and deletes them for you. You can use both the GUI version and CLI version of macuninstaller.</br>

Download
-----
**MACUNINSTALLER EXISTS AS BOTH APP AND BINARY FILE, SO GET WHAT PLEASES YOU FROM RELEASES**</br>You can checkout the latest releases and can even download the binary from there</br> `https://github.com/hrik2001/macuninstaller/releases/`</br>
And move the binary to this path so that you can directly use it as a command in your terminal :)-</br>
`/usr/local/bin/`</br>
</br>

Or you can download this repository. </br>
`git clone https://github.com/hrik2001/macuninstaller` </br>

Usage
-----
If you are using the python script then type this-</br>
`python cli.py -p /path/to/app` </br> Or this if you are using the binary</br> `macuninstaller -p /path/to/app`
and it will output the possible files and folders that are related to the app you just specified. </br>
You can also do a custom scan where you have to type the path of the app and the directories in which you want to search for files affiliated with the app. </br>
`python cli.py -p /path/to/app -c /path1/ /path2/ /path3/`</br> And for the binary - </br> `macuninstaller -p /path/to/app -c /path1/ /path2/ /path3/`</br>
For the GUI version, just run </br>
`python macuninstaller.py`</br>

UI Help
----
The CLI version is very user friendly, here is a peek :)</br>
![CLI](rsrcs/cli.png)</br>
The CLI version lets you choose the files and folders by using up and down arrow keys, if you want to select/deselect files/folders you can do so with space, if you want to quit the program then press "q". After that you will be asked to type your password and with a breeze your app will be uninstalled.</br>
Here is the look of the GUI</br>**NOTE: YOU HAVE TO RUN THE SCRIPT IN SUDO**</br>
First you have to choose what kind of scan do you want to have for the app you want to uninstall </br>
![Scan Chooser](rsrcs/chooser.png)</br>
For both of the scans you will be greeted with</br>
![App Chooser](rsrcs/app_chooser.png)</br>
For custom scan you would be greeted with this window where it would ask you to type folder names, seperated by comma . macuninstaller will search in those folders. Suggested folders already appear in text field</br>
![Custom Folder Chooser](rsrcs/folder_chooser.png)</br>
Also you will have a suggestor feature which will suggest if the file/folder should be deleted or not. The confused emoji shows that it is not suggested to delete the file and the smiley face for vice versa</br>
![Chooser](rsrcs/file_chooser.png)</br>



Contribution
------------
[hexx112](https://www.reddit.com/user/hexx112) for making the website which is accessible at [macuninstaller](https://hrik2001.github.io/macuninstaller)

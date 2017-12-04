macuninstaller
-------------
macuninstaller is python script which is apparently only available in CLI version (future version will also include a GUI client). It will show you all the possible files and folders that are related to the app you just specified. You can probably redirect the output to some file so that you can check which ones you want to delete and which ones you want to keep.

Usage
-----
First download this repository. </br>
`git clone https://github.com/hrik2001/macuninstaller` </br>
So after downloading the repository, go inside the folder and all you have to do is </br>
`python cli.py -p /path/to/app` </br>
and it will output the possible files and folders that are related to the app you just specified. </br>
You can also do a custom scan where you have to type the path of the app and the directories in which you want to search for files affiliated with the app. </br>
`python cli.py -p /path/to/app -c /path1/ /path2/ /path3/`

Help Needed
-----------
Help is needed for GUI tho.

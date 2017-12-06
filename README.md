macuninstaller
-------------
macuninstaller is python script which is apparently only available in CLI version (future version will also include a GUI client, which will let you uninstall from the GUI). It will show you all the possible files and folders that are related to the app you just specified. You can probably redirect the output to some file so that you can check which ones you want to delete and which ones you want to keep.

Download
-----
You can download the executable</br> `https://github.com/hrik2001/macuninstaller/releases/download/<version>/macuninstaller`</br>
And move it to-</br>
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
`python cli.py -p /path/to/app -c /path1/ /path2/ /path3/`</br> And for the binary - </br> `macuninstaller -p /path/to/app -c /path1/ /path2/ /path3/`

Help Needed
-----------
Help is needed for GUI tho.

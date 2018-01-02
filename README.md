macuninstaller
-------------
macuninstaller is a python script that was written to uninstall mac apps. This script finds all the related files and folders and deletes them for you. You can use both the GUI version and CLI version of macuninstaller. (The CLI version doesn't delete files since there is a high chance of deleting files by mistake)

Download
-----
You can checkout the latest releases and can even download the binary from there</br> `https://github.com/hrik2001/macuninstaller/releases/`</br>
And move it the binary to this path so that you can directly use it as a command in your terminal :)-</br>
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
For the CLI version of the script, there is a cool feature where the script suggests if the file should be deleted or not. A confused emoji appears in front of the path name to suggest that it is not recommended to delete the app, and a smiley face for the opposite. This feature is yet to be implemented in the GUI version.

Contribution
------------
[hexx112](https://www.reddit.com/user/hexx112) for making the website which is accessible at [macuninstaller](https://hrik2001.github.io/macuninstaller)

MacUninstaller
-------------
It is an app uninstaller for macOS which is being developed by Shatabarto "Rik" Bhattacharya. It is being written in python 2.7 purely

Usage
-----
The function `scan(path_to_app)` will scan an app and return 2 arrays of strings which will contain all the files and folders related to that app you specified. The `scan` function will only look for related files in some special locations where there is a high chance of finding files related to an app.
You can also do a custom scan with the function `custom_scan(path_to_app, custom_paths)` . The custom path variable is an array of strings which will contain all the custom paths you want to check into to find files affiliated with your app.

Help Needed
-----------
Help is needed for GUI tho.

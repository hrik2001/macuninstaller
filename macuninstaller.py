from function import *
import shutil
import os

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
    os.remove(stuff)

for stuff in folders_to_delete:
    shutil.rmtree(stuff)

from function import *

app_dir = app_name_asker("Enter the path name")

files , folders = thread_scanner(app_dir)

files = cleanup(files)
folders = cleanup(folders)

file_list = displayer(files)
folder_list = displayer(folders)

files_to_delete = []
folders_to_delete = []

for stuff in file_list.items():
    if stuff[1]:
        files_to_delete.append(stuff[0])

for stuff in folder_list.items():
    if stuff[1]:
        folders_to_delete.append(stuff[0])

printer(files_to_delete)
print "\n"*2
printer(folders_to_delete)

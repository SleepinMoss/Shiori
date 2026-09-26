import os
import json
import shutil

dir = os.path.expanduser("~/.local/share/shiori")
os.makedirs(dir, exist_ok=True)

def loadFile(category, backupName):
    filePath = dir + "/" + category + "/index.json"
    with open(filePath, "r") as index:
        directory: str = json.load(index)
    fileName = directory.split('/')[-1]

    try:
        os.makedirs(f"{dir}/{category}/backup")
    except FileExistsError:
        pass

    if backupName != "backup": shutil.copy(directory, f"{dir}/{category}/backup")
    fileToCopy = dir + "/" + category + "/" + backupName + "/" + fileName
    shutil.copy(fileToCopy , directory)

def createCategory(categoryName, fileBackup):
    # fileBackup is the directory of the to-be-backed-up file
    os.makedirs(f"{dir}/{categoryName}")
    filePath = dir + "/" + categoryName + "/index.json"
    with open(filePath, "w") as index:
        json.dump(fileBackup, index, indent=4)

def createFile(category, fileName):
    filePath = dir + "/" + category + "/index.json"
    with open(filePath, "r") as index:
        directory: str = json.load(index)

    os.makedirs(f"{dir}/{category}/{fileName}")
    shutil.copy(directory, f"{dir}/{category}/{fileName}")

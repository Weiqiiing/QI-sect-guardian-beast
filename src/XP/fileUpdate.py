import csv
import dropbox
from src.data.sectInfo import sectCall
import os


def download_file(file_to, file_from):
    dbx = dropbox.Dropbox(
        os.environ['DROPBOX_TOKEN'])
    f = open(file_to, "w")
    metadata, res = dbx.files_download(file_from)
    f.write(str(res.content)[2:-1])
    f.close()


def upload_file(file_from, file_to):
    dbx = dropbox.Dropbox(
        os.environ['DROPBOX_TOKEN'])
    f = open(file_from, "rb")
    dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)
    f.close()


def openFile(fileName, openIn, listAdd):
    with open(fileName, openIn) as fData:
        reader = csv.reader(fData)
        for row in reader:
            for i in range(len(row)):
                listAdd.append(int(row[i]))
    fData.close()


def writeFile(fileName, openIn, listWrite):
    fData = open(fileName, openIn)
    for allSects in range(len(sectCall)):
        fData.write(str(listWrite[allSects]))
        if allSects != len(sectCall) - 1:
            fData.write(",")
    fData.close()

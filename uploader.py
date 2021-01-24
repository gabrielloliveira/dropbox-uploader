#!/usr/bin/env python3

import getopt
import glob
import os
import sys

import dropbox
from decouple import config

DEFAULT_SQL_DIRECTORY = config("DEFAULT_SQL_DIRECTORY")
DEFAULT_DROPBOX_DIRECTORY = config("DEFAULT_DROPBOX_DIRECTORY")


def get_files_sql():
    os.chdir(fr'{DEFAULT_SQL_DIRECTORY}')
    return glob.glob("*.sql")


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, directory):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), directory, mode=dropbox.files.WriteMode.overwrite)


def main(argv):
    file_from = directory = None
    try:
        opts, args = getopt.getopt(argv, "hf:d:", ["file=", "directory="])
    except getopt.GetoptError:
        print('uploader.py -f <file_name> -d <dropbox_directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('uploader.py -f <file_name> -d <dropbox_directory>')
            sys.exit()
        elif opt in ("-f", "--file"):
            file_from = arg
        elif opt in ("-d", "--directory"):
            directory = arg

    access_token = config('ACCESS_TOKEN')
    transferData = TransferData(access_token)
    if not file_from and not directory:
        for file in get_files_sql():
            directory = f"{DEFAULT_DROPBOX_DIRECTORY}{file.split('/')[-1]}"
            transferData.upload_file(file, directory)
    else:
        transferData.upload_file(file_from, directory)


if __name__ == '__main__':
    main(sys.argv[1:])

#!/usr/bin/env python3

import getopt
import glob
import os
import sys

import dropbox
from decouple import config

DEFAULT_BACKUPS_DIRECTORY = config("DEFAULT_BACKUPS_DIRECTORY")
DEFAULT_DROPBOX_DIRECTORY = config("DEFAULT_DROPBOX_DIRECTORY")


def get_files_sql():
    os.chdir(fr"{DEFAULT_BACKUPS_DIRECTORY}")
    sql_files = glob.glob("*.sql")
    compreesed_sql_files = glob.glob("*.sql.gz")
    return sql_files + compreesed_sql_files


class DropboxUploader:
    def __init__(self):
        self.access_token = config("ACCESS_TOKEN")
        self.client = dropbox.Dropbox(self.access_token)

    def create_directory_if_not_exists(self, directory):
        """create a directory if it doesn't exist"""
        directory = directory[:-1] if directory.endswith("/") else directory
        try:
            self.client.files_get_metadata(directory)
        except dropbox.exceptions.ApiError as err:
            if not err.error.is_path() or err.error.get_path().is_not_found():
                self.client.files_create_folder(directory)

    def upload_list_files(self, files, dropbox_directory):
        self.create_directory_if_not_exists(dropbox_directory)
        for file in files:
            full_directory = fr"{dropbox_directory}{file}"
            print("Uploading " + file + " to Dropbox as " + full_directory + "...")
            self.upload(file, full_directory)

    def upload(self, file, dropbox_directory):
        with open(file, "rb") as f:
            self.client.files_upload(
                f.read(), dropbox_directory, mode=dropbox.files.WriteMode.overwrite
            )


def main(argv):
    file_list = get_files_sql()
    directory = DEFAULT_DROPBOX_DIRECTORY
    try:
        opts, args = getopt.getopt(argv, "hf:d:", ["file=", "directory="])
    except getopt.GetoptError:
        print("uploader.py -f <file_name> -d <dropbox_directory>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("uploader.py -f <file_name> -d <dropbox_directory>")
            sys.exit()
        elif opt in ("-f", "--file"):
            file_list = arg.split(",")
        elif opt in ("-d", "--directory"):
            directory = arg

    if not directory.endswith("/"):
        directory += "/"
    if not directory.startswith("/"):
        directory = "/" + directory

    transfer_data = DropboxUploader()
    transfer_data.upload_list_files(file_list, directory)


if __name__ == "__main__":
    main(sys.argv[1:])

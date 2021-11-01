#!/usr/bin/env python3

import argparse
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

    def clear_directory(self, dropbox_directory):
        dropbox_directory = (
            dropbox_directory[:-1]
            if dropbox_directory.endswith("/")
            else dropbox_directory
        )
        print("🗑 Clearing directory " + dropbox_directory + "...")
        self.client.files_delete_v2(dropbox_directory)

    def upload_list_files(self, files, dropbox_directory, clear_directory=False):
        self.create_directory_if_not_exists(dropbox_directory)
        if clear_directory:
            self.clear_directory(dropbox_directory)
        for file in files:
            full_directory = fr"{dropbox_directory}{file}"
            print("🔄 Uploading " + file + " to Dropbox as " + full_directory + "...")
            self.upload(file, full_directory)
            print("✅ Success " + full_directory)

    def upload(self, file, dropbox_directory):
        with open(file, "rb") as f:
            self.client.files_upload(
                f.read(), dropbox_directory, mode=dropbox.files.WriteMode.overwrite
            )


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="File", required=False)
    parser.add_argument("-d", "--directory", help="Dropbox directory", required=False)
    parser.add_argument(
        "-c",
        "--clear",
        help="Clear Dropbox directory first",
        required=False,
        action="store_true",
    )
    args = parser.parse_args()

    file_list = get_files_sql()
    directory = DEFAULT_DROPBOX_DIRECTORY
    clear = False

    if args.file:
        file_list = args.file.split(",")
    if args.directory:
        directory = args.directory
    if args.clear:
        clear = True

    if not directory.endswith("/"):
        directory += "/"
    if not directory.startswith("/"):
        directory = "/" + directory

    transfer_data = DropboxUploader()
    transfer_data.upload_list_files(file_list, directory, clear_directory=clear)


if __name__ == "__main__":
    main(sys.argv[1:])

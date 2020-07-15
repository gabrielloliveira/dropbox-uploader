import sys, dropbox

from decouple import config


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)


def main():
    access_token = config('ACCESS_TOKEN')
    transferData = TransferData(access_token)

    file_from = 'teste.txt'
    file_to = f'/postgres/{file_from}'

    transferData.upload_file(file_from, file_to)


if __name__ == '__main__':
    main()

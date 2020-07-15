import sys
import getopt
import dropbox

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


def main(argv):
    file_from = ''
    file_to = ''
    try:
        opts, args = getopt.getopt(argv,"hf:d:",["file=","directory="])
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
            file_to = arg
    
    access_token = config('ACCESS_TOKEN')
    transferData = TransferData(access_token)

    transferData.upload_file(file_from, file_to)


if __name__ == '__main__':
    main(sys.argv[1:])

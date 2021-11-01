# dropbox-uploader

A simple Python script for file upload to the dropbox.

## Requirements

* Python >= 3.6

## Installation

* Clone the repository.

* Install dependencies.

```console
pip install -r requirements.txt
```

* Add your ACCESS_TOKEN API.
* Add your DEFAULT_DROPBOX_DIRECTORY
* Add your DEFAULT_SQL_DIRECTORY (folder where backups.sql are stored)

## Usage

* Send a file to the dropbox with the following command:

```console
python uploader.py -f <FILE NAME> -d <DROPBOX DIRECTORY>
```

or

```console
python uploader.py
```

* View help usage with

```console
python uploader.py -h 
```

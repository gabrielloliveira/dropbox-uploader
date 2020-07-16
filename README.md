# dropbox-uploader

A simple Python script for file upload to the dropbox.

## Requirements

* Python >= 3.5

## Installation

* Clone the repository.

* Install dependencies.

```console
pip install -r requirements.txt
```

* Add your ACCESS_TOKEN API.

## Usage

* Send a file to the dropbox with the following command:

```console
python uploader.py -f <FILE NAME> -d <DROPBOX DIRECTORY>
```

## Limitation

For now dropbox-uploader sends only individual files that are in the same folder as the uploader

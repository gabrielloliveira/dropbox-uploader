#!/bin/sh
 
# backup.sh

DATE=$(/bin/date +%Y%m%d%H%M%S)
 
dokku postgres:export [db_name] > "[db_name]-$DATE.dump"

python3 uploader.py -f "[db_name]-$DATE.dump" -d "/postgres/[db_name]-$DATE.dump"

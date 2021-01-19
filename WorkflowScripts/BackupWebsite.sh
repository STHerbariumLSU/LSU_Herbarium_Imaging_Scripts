#!/bin/bash

# need to run this as root
# outlogs should be output to source computer log folder
# Source, destination, and logfolder MUST be folders WITH A TRAILING FORWARD SLASH

# Zip up var, updating files not deleting any
zip -ru /data/varwww.zip /var/www/ 

# Backup log to Collection network drive
rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update /data/varwww.zip /mnt/Collection/ > /data/LSUCollections/ServerLogs/Debugging/varwww.log

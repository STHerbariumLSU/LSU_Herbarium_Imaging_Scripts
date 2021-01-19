#!/bin/bash


# need to run this as root
# outlogs should be output to source computer log folder
# Source, destination, and logfolder MUST be folders WITH A TRAILING FORWARD SLASH



# Set custom extension for log file names
suffix=_server.txt # adding "_server" to end of log file so it is differentiated from files sorted locally

# Set image source and destination folders
# mnt is local long term storage, data is server
source=/mnt/Collection/LSUCollections/
destination=/data/LSUCollections/

# Daily log folder on server
logfolder=/data/LSUCollections/ServerLogs/

# Temp log file used to make file lists
outlog=/data/LSUCollections/ServerLogs/Debugging/RsyncDaily.out 

# Local folder to put long form file lists into
wsLogs=/mnt/Collection/LSUCollections/ServerLogs/

# Backup portal csv files 
csvfolder=/mnt/Collection/LSUCollections/PortalMaps/
csvRemote=/data/LSUCollections/PortalMaps/


# Name today's log after the date
fname=`date +'%Y-%m-%d'`
todaylog=$logfolder$fname$suffix

# print date so i can see how long rsync takes 
echo "starting rsync"
date +"%T"

rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update --include='*/' --include '*JPG' --exclude '*' $source $destination | grep '^>f' | cut -d' ' -f2 > $outlog

echo "starting file resizing"
date +"%T"

while read g;
do
echo $g
echo $g >> $todaylog
mvdPath=$destination$g
convert $mvdPath -units pixelsperinch -density 80x80 -resize 1400x1400^ -quality 80 ${mvdPath%.JPG}_WR.JPG
convert $mvdPath -units pixelsperinch -density 80x80 -resize 200x200^ -quality 80 ${mvdPath%.JPG}_TN.JPG
convert $mvdPath -quality 95 ${mvdPath%.JPG}_L.JPG
done < $outlog

echo "starting log copy"
date +"%T"

# Copy logs to workstation - keep open permissions for 
rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=rwx --update $logfolder $wsLogs 


# Sync all csv files to sassafras folder 
rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update $csvfolder $csvRemote 

# checking if script is running
echo $fname
echo $todaylog

date +"%T"

#!/bin/bash
# Set error log for debugging
elog=/mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScripts/Debugging/WeeklyPortalMap.log
# Write date to error log 
echo "$(date)" &>> $elog
# Set variables 
# Path to daily long form log files
logFolder='/mnt/Collection/LSUCollections/ServerLogs/'
# Path to folder where CSV files for portal mapping will be made
csvFolder='/mnt/Collection/LSUCollections/PortalMaps/'
# Web address for linking images 
webPath="https://cyberfloralouisiana.com/images/LSUCollections/"
# 'True'- Regular log (default is past 7 days but can be edited with nDays flag). 
# 'False' - input specified dates with newDate and oldDate flags
regular='False'
nDays=7
# Year,month,day
oldDate='2021,3,1'
newDate='2021,3,2'
# Path to your python script 
python3 /mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScripts/WeeklyPortalMap.py -l $logFolder -c $csvFolder -w $webPath -r $regular -d $nDays -n $newDate -o $oldDate &>> $elog

# Add extra wait time, a probably unneeded 
sleep 5m

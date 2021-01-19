#!/bin/bash
# Set error log for debugging
elog=/mnt/c/Users/image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScripts/Debugging/MoveLocalImages1.log
# Write date to error log 
echo "$(date)" &>> $elog
# Set variables 
outLogsuffix="local_ws1.txt"
sourceFolder='/mnt/c/Users/image/Desktop/Imaging/'
destinationFolder='/mnt/Collection/LSUCollections/'
barcodeMax=15
barcodeMin=9
csvFolder='/mnt/c/Users/image/Desktop/Imaging/LocalLogs/'
portalFolders="Algae,Bryophyte,Fungi,Lichen,Vascular"
otherFolders="Random"
# Path to your python script 
python3.8 /mnt/c/Users/image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScripts/MoveLocalImages.py -l $outLogsuffix -s $sourceFolder -d $destinationFolder -p $portalFolders -o $otherFolders -x $barcodeMax -n $barcodeMin -c $csvFolder &>> $elog
# Add extra wait time, a probably unneeded 
sleep 5m
#!/bin/bash
# Set error log for debugging
elog=/mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScriptsWS2/Debugging/CountServerLogs.log
# Write date to error log 
echo "$(date)" &>> $elog
# Path to your python script 
python3 /mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScriptsWS2/CountServerLogs.py &>> $elog

# Add extra wait time, a probably unneeded 
sleep 5m
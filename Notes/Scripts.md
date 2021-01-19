# Scripts - 

Needs updating

https://github.com/LizEve/LSU_Herbarium_Imaging_Scripts

## Run on Desktop with Task Scheduler

RunMoveLocal.sh - runs MoveLocalImages.py

MoveLocalImages.py - Checks barcodes in incoming folders, moves to appropriate folder(based on barcode) on storage drive. Put files with names that are too long or too short in BadBarcode folder. Outputs one long form log file per day with all destination file paths. Writes to master log file with number of files and barcodes moved to LaCie, also broken down by collection. Uses long form of logs to count files. This does not count files in the "Random" folder. 
Edits: Barcode maximum and minimum number of characters. Folder paths for any folder used. The name of log files and which folder they are in. 

WakeUp.sh - wakes up the computer to sit and wait for 13 hours at 9:55 PM, this allows the server to connect to the storage drive, in order to copy over files. 
Edits: None. for debugging. 

RunCountServer.sh - runs CountUploadLogs.py at 11PM every day. 
Edits: Path to script and log for debugging.

CountServerLogs.py - Called by Task Scheduler. Writes to master log file with number of files and barcodes moved to the server, also broken down by colletion. Uses long form of log for each day to count files. This does not count files in the "Random" folder. 
Edits: Input file name. Directions in script on where to add file name. This can be used if you need to re-run a count on a list form log file. All paths are editable. 

RunWeeklyCSV.sh - runs LogtoCSV.py at 3PM every week on Sunday.
Edits: Path to script and log for debugging. 

WeeklyCSV.py - Takes all rsync logs that were modified in the last week and creates csv files to upload to Symbiota. 
Edits: Can edit how many days back you want to pull log files from to create a csv for upload to Symbiota. Can also input specific date range to make a csv file for. All paths are editable. 

## Run on server by crontab

rsyncDaily.sh - runs on server to copy files to server and create derivatives. 
Outputs one log file per day (per computer) with all destination file paths. 
Passes current day's log file to CountRsyncLogs.py to count total files/barcodes moved.
errors written to - /data/LSUCollections/Logs/dailyrsynclog.txt
Edits: Only by professional. Except paths of where files come from and go to. 


### Old notes 


## Scripts 

Documents/WorkflowSckriptsWS2
Right click - open with notepad 

CSV change dates - WeeklyCSV.py



### Run on Desktop with Task Scheduler

RunOrganize.sh - runs organizeIncomingImages.py at 9PM every day. 

organizeIncomingImages.py - Checks barcodes in incoming folders, moves to appropriate folder(based on barcode) on storage drive. Put files with names that are too long or too short in BadBarcode folder. Outputs one long form log file per day with all destination file paths. Writes to master log file with number of files and barcodes moved to LaCie, also broken down by collection. Uses long form of logs to count files. This does not count files in the "Random" folder. 
Edits: Barcode maximum and minimum number of characters. Folder paths for any folder used. The name of log files and which folder they are in. 

WakeUp.sh - wakes up the computer to sit and wait for 13 hours at 9:55 PM, this allows the server to connect to the storage drive, in order to copy over files. 
Edits: None. log for debugging. 

RunCountServer.sh - runs CountUploadLogs.py at 11PM every day. 
Edits: Path to script and log for debugging.

CountServerLogs.py - Called by Task Scheduler. Writes to master log file with number of files and barcodes moved to the server, also broken down by colletion. Uses long form of log for each day to count files. This does not count files in the "Random" folder. 
Edits: Input file name. Directions in script on where to add file name. This can be used if you need to re-run a count on a list form log file. All paths are editable. 

RunWeeklyCSV.sh - runs LogtoCSV.py at 3PM every week on Sunday.
Edits: Path to script and log for debugging. 

WeeklyCSV.py - Takes all rsync logs that were modified in the last week and creates csv files to upload to Symbiota. 
Edits: Can edit how many days back you want to pull log files from to create a csv for upload to Symbiota. Can also input specific date range to make a csv file for. All paths are editable. 

### Run on server by crontab: 

rsyncDaily.sh - runs on server to copy files to server and create derivatives. 
Outputs one log file per day (per computer) with all destination file paths. 
Passes current day's log file to CountRsyncLogs.py to count total files/barcodes moved.
errors written to - /data/LSUCollections/Logs/dailyrsynclog.txt
Edits: Only by professional. Except paths of where files come from and go to. 
# Imaging Workflow 

Last update  idk

https://github.com/LizEve/LSU_Herbarium_Imaging_Scripts

1. Turn on camera

2. Wait for EOS to open

3. Check EOS preferences
   1. Confirm that `renameimage.exe` is 'registered' to EOS 
      1. Preferences > Linked Software > Register > Browse - select `renameimage.exe`
         a. Make sure "CR2" is checked 
      2. Full path - `C:Users\Image\Documents\PNWHerbaria\Scripts\renameimage\renameimage.exe`

4. Select portal folder 
   1. In EOS - Preferences > Destination Folder
   2. Select one of the portal folders `C:Users\Image\Desktop\Imaging\`
   3. Personal projects and other special collections that are not going on Symbiota should be imaged in the **Random** folder if you want the images backed up to the server (Sassafrass). Any folders in **Random** will be moved as is to the local backup drive, not sorted into portal folders. 

5. Open DPP in Imaging folder `C:Users\Image\Desktop\Imaging\`

6. Take photo 
   1. A small box will pop up with the current file name and a place to enter the new name

7. Scan barcode
   1. Barcode should appear as new file name - edit with _1 or other number if needed
   2. Click the "rename" button to rename the file 
   3. The small window will close after the file is renamed. If needed you can edit the names later in DPP

Repeat 5. & 6. for all photos

8. Batch edit photos in DPP 
   - if needed, can rename files in DPP using the barcode scanner

9. Convert from CR2 to JPG
   1. Now you are done, make sure to record on paper what specimens you imaged

Weekly - 3PM on Sunday

1. Upload CSV 
   1. CSV files ready for upload are on in the CSVLogs/ folder. On workstation 2 at LSU.
   2. After uploading CSV files please move them to the CSVLogged/ folder. 
   3. If file names are edited and re-uploaded a new CSV file will be made and the file will be under the date it was renamed.

Check on process

Local Logs: Imaging to LaCie Drive - 9PM every day
- Daily lists of files are in Desktop/Imaging/LocalLogs/ with the extension 'local_ws2.txt'
- Daily counts of files are in Desktop/Imaging/LocalLogs/DailyLocalLog.csv

Server Logs: LaCie Drive to Sassafras Server - 10PM every day for transfer 11PM for log counts
- Daily lists of files are in CFLA-LSU-Station2/LSUCollections/Logs/ on the LaCie with the extention '_server_ws2.txt'
- Daily counts of files are in CFLA-LSU-Station2/LSUCollections/Logs/serverLogWS2.csv

The total number of barcodes should match between organizeLog.csv and serverLogWS2.csv. The number of files will be doubled in organizeLog.csv because it counts both JPG and CR2 files. 


## Behind the scenes process

### 9PM

- Ubuntu gets rebooted from Task Scheduler
- Files get moved from the desktop to the LaCie
- Long form logs are written to the Desktop in the folder Desktop/Imaging/DailyLocalLogs/ with the extension '_local_ws2.txt'
- Tally of files appended to the file 'DailyLocalLog.csv' in CFLA-LSU-Station2/LSUCollections/CSVLogs/
- Scripts run: MoveLocalImages.py RunMoveLocal.sh

### 10PM 

- Wakeup script runs on workstation to wake up computer
- Sassafras pulls files from LaCie using scripts on Sassafras
- Long form logs are written in CFLA-LSU-Station2/LSUCollections/ServerLogs/ on the LaCie with the extention '_server_ws2.txt'
- Scripts run: WakeUp.sh(on windows), MoveServerImages.sh(on server)

### 11 PM 

- Task manager reboots ubuntu in case LaCie has disconnected
- Use long form logs from 10PM syncing to tally the total number of files uploaded and writes the results to the file 'DailyServerLog.csv' on the LaCie in the folder CFLA-LSU-Station2/LSUCollections/ServerLogs/
- Scripts run: RunCountServer.sh, CountServerLogs.py


### Weekly 

- Portal Map CSV files are made from the long form logs created in the last week. '_server_ws2.txt'
- The total files in each portal map file are written to the file 'csvLog.csv' on the LaCie in the folder CFLA-LSU-Station2/LSUCollections/CSVLogs/
- These csv portal maps will also be synced to the Sassafras log folder accessible at - https://cyberfloralouisiana.com/images/LSUCollections/Logs/PortalMaps/
- Scripts run: WeeklyPortalMap.py RunWeeklyPortalMap.sh


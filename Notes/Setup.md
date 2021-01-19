
# Setup of Imaging Pipeline

## General 

### Acronyms 

DPP - Digital Photo Professional
EOS - EOS Utility - a program to connect computer to camera

### Programs/versions

Python3 and package downloader like pip. 
Ubuntu 20.04 LTS
Computer with Windows 10
Local backup drives mounted on the window machine. 
Remote server for long-term storage and serving images. 

### System Requirements 

These scripts have been tested using Windows 10, Ubuntu 20.04, and Python 3. All scripts should work on any Linux platform. However, the automation of running scripts daily will be different. 

## Download and edit scripts on imaging computer

### 1. Renaming image files script -  renameimage.exe

#### 1.1 Function description

- Connects to EOS
- Renames incoming image files with user input - ie barcode 
- Every time a photo is taken, EOS opens the program and passes the new file name to the program, where it can be renamed. 

#### 1.2 Download

- `http://www.pnwherbaria.org/documentation/specimenimaging.php`
- Scroll down and click on **Imaging Computer Configuration** to download.  
- This will download a whole folder that is a different imaging pipeline. We only need the script `renameimage.exe` in the folder `PNWHerbaria\Scripts\renameimage\`

#### 1.3 Store locally 

- Put this script somewhere it is easy to find and hard to edit or move. It should stay in the same place forever. 

#### 1.4 Link `renameimage.exe` to EOS

- EOS needs to link directly to `renameimage.exe`, so that when a photograph is taken; EOS passes the default file name to `renameimage.exe`. For each photo taken `renameimage.exe` will open and provide a window to rename the file manually or with a barcode reader.
- Open EOS - Preferences > Linked Software > Register > Browse
  - Click **Preferences**
  - Click **Linked Software**
  - Click **Register**
  - Click **Browse** and link to `renameimage.exe`

### 2. Setup Automated scripts 

#### 2.1 Download ubuntu 

Google a help page or ask IT. 

https://www.microsoft.com/en-us/p/ubuntu-2004-lts/9n6svws3rx71?activetab=pivot:overviewtab


#### 2.2 Download python and pip and packages

Download from website or package manager. Again google or ask IT. 

https://www.python.org/downloads/
Help I used - https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/

```bash
sudo apt update 
sudo apt install python3-pip
```

Install python packages - os, glob, datetime, pandas, itertools, pathlib, shutil, platform, argparse, sys
```bash
python3 -m pip install pandas
```


##### 2.3 Download github folder 

Set up github desktop
Github desktop - https://desktop.github.com/

Clone/download scripts folder
Scripts folder - https://github.com/LizEve/LSU_Herbarium_Imaging_Scripts

Edit "Run*.sh" scripts with appropriate file paths. 
RunCountServer.sh - not yet set up to input variables - edit CountServerLogs.py directly


##### 2.3 Set up task scheduler 

XML files are in the github folder for import. Remember to change file paths to customize

Task Scheduler Library > ImagingWorkflow

General:
Run whether user is logged in or not
Run with highest privileges
Configure for Windows 10

Triggers:
Daily/Weekly  
Stop task if it runs longer than 1 hour

Actions:
Start a program
Program/script: bash.exe
Add arguments: /mnt/c/Users/Image/Documents/GitHub/LSU_Herbarium_Imaging_Scripts/WorkflowScripts/*sh
Start in: C:\Windows\System32

Conditions:
Wake computer to run this task 

Settings:
Allow to be run on demand
Run as soon as possible if missed

(On restart)
Mount Collection Network Drive - C:\Users\Image\Documents\GitHub\LSU_Herbarium_Imaging_Scripts\WorkflowScripts\MountCollectionNetworkDrive.bat

(Everyday)
9PM: Move Local Images - RunMoveLocal.sh
11PM: Run Counter Server Logs - RunCountServer.sh

(Sundays)
3 PM: Make CSV for upload - RunWeeklyPortalMap.sh


## Server

### 1. Mount local backups to remote server

Mount local backups onto server. Google or get help from departmental IT.

### 2. Syncing files scripts - rsyncDaily.sh


#### 2.1 Function description

- This script will copy files from local backup to remote server 
  - Currently CR files are excluded from this copy.
  - Current rsync call is custom for LSU. It changes permissions of the files when they are moved to match the permissions for our server. This includes a custom user group called 'adm'.

#### 2.1a Log files 

- Files are written to output logs based on the date that the log is written.
- If desired there is a depreciated version where logs are made based on the date the file was last modified. Modification date is the last time the contents of the file were altered; simply renaming the file itself should not change the modification date.
- Rsync logs are similar to the organizing logs. They are named based on the date and a trailing custom string.
- For LSU the log names will contain the date, the word 'server' to indicate they are logs for server upload, and the computer they are imaged on.

### 2.2 Download and store locally

- `https://github.com/LizEve/HerbariumRA.git`
  - Copy script from imagining computer or use GitHub to clone 
- Store script somewhere that is executable by root. 
  - This is dependent on how your server and permissions are set up.
  
### 2.3 Edit script 

- `organizeIncomingImages.py` needs to be customized to your needs and server permissions. This may take some trial and error to get it working how you need it to. 

- Edit rsync call if needed 
  - Current rsync call is custom for LSU. It changes permissions of the files when they are moved to match the permissions for our server. This includes a custom user group called 'adm'.
  - Depending on permissions, this script could possibly be run on the imaging computer if needed. 

- **destination** - Folder on the server that you are syncing the files to. 
  
- **source** - Path to the mounted local backup 
  
- **logfolder** - Folder to put log files in. LSU log files are written to backup drives for easy comparison to logs of which files are moved.
  
- **outlog** - Path to a file that is written over daily, info for logs is pulled from this file. 
  
- **suffix** - Log files are named by date, this is whatever string you want trailing the date. LSU log files will reference the computer they are imaged on. 

  
### 3. Set up cron job to run rsyncDaily.sh 

- Cron info - https://www.adminschoice.com/crontab-quick-reference
- Recommend running as root to avoid any file writing or permissions issues. 
- Add rsyncDaily.sh to cron jobs 
  - Open root crontab for editing `sudo crontab -u root -e`
  - Run at 10:15 PM every day. `15 22 * * * /bin/sh /var/www/rsyncDaily.sh &> /data/LSUCollections/Logs/dailyrsynclog.txt`
- Had to change some permissions so that when root writes to the log folder, the permissions stay the same as the rest of the /data/ folder. `sudo vim /etc/logrotate.d/apache2 rsyncDaily.sh`
- Cron jobs need to be executable by root chmod 750


### 4. Set wake up for imaging computers 

- Set up workstations to wake up before rsync script is scheduled to start. 
- Make sure the sleep setting is longer than the time you set between waking them up and running the rsync script. 
- Use task scheduler - `https://www.thewindowsclub.com/wake-up-computer-from-sleep-windows`



## Additional set up notes 

### Windows 10

#### Install Ubuntu 18.04 LTS

Install from Microsoft Store

#### Mount network drives in Ubuntu 

`https://docs.microsoft.com/en-us/archive/blogs/wsl/file-system-improvements-to-the-windows-subsystem-for-linux`


import os
import glob
import datetime
import pandas as pd
import sys


def countFiles(barcodes,files,portals,csvLogFilePath):
    # Takes a list of barcodes, files, portals and a path to write a log file to

    # All the info to keep track of and report 
    numBarcodes=str(len(set(barcodes)))
    numFiles=str(len(files))
    numVascular=str(portals.count('Vascular'))
    numAlgae=str(portals.count('Algae'))
    numBryophyte=str(portals.count('Bryophyte'))
    numFungi=str(portals.count('Fungi')) 
    numLichen=str(portals.count('Lichen'))
    todaysDate=str(datetime.date.today().strftime("%Y-%m-%d"))

    # Header for log file
    firstLine=['CSVDate','Barcodes','Files','Vascular','Algae','Bryophyte','Fungi','Lichen']
    logHeader = ",".join(firstLine)
    
    # Get line to add to csv file
    csvLine = [todaysDate,numBarcodes,numFiles,numVascular,numAlgae,numBryophyte,numFungi,numLichen]
    csvLogLine=",".join(csvLine)

    # If csv file does not exist, create with header 
    if len(files) != 0:
        if not os.path.exists(csvLogFilePath):
            #print(header)
            with open(csvLogFilePath,"w") as csvLogFile:
                csvLogFile.write("%s\n" % logHeader)
                csvLogFile.write("%s\n" % csvLogLine)
                csvLogFile.close()
                
        # If csv file exists, add new line 

        elif os.path.exists(csvLogFilePath):
            print(csvLine)
            with open(csvLogFilePath,"a") as csvLogFile:
                csvLogFile.write("%s\n" % csvLogLine)
                csvLogFile.close()
    else:
        print("no images today")
        
def countImages(logFile,logFolder,csvLogFilePath):


    # Today's date 
    logDate = str(datetime.date.today().strftime("%Y-%m-%d"))

    # Create lists to calculate summary numbers
    barcodes=[]
    files=[]
    portals=[]

    try:
        # Open the file 
        logF = open(logFile,"r")

        # Loop through lines in log file 
        for oPath in logF:

            # Get portal name 
            portal=oPath.split("/")[0]

            # Get path to original image
            path = os.path.split(oPath)[0]

            # Get file name without extension
            fileName=os.path.basename(oPath).split(".")[0]

            # Get barcode 
            barCode=fileName.split("_")[0]

            # Add to portal dict for reporting numbers
            barcodes.append(barCode)
            files.append(fileName)
            portals.append(portal)

        # Write out log file of all the files that got csv'd
        countFiles(barcodes,files,portals,csvLogFilePath)
    except FileNotFoundError:
        print("No files moved today")

def main():

    # Get today's log file from the date and extension
    outLogsuffix = 'server.txt'
    logFileName=str(datetime.date.today().strftime("%Y-%m-%d"))+"_"+outLogsuffix

    # If you need to get a count from an old file, delete hash mark and enter in file name
    #logFileName = _server_ws2.txt

    # Path to log files that are made when images are uploaded to server
    logFolder = '/mnt/Collection/LSUCollections/ServerLogs/'

    # Log file Path
    logFilePath=os.path.join(logFolder,logFileName)

    # Path to a log file that counts the number of files etc in each csv file
    # This log is extremely customized for LSU, if you want to implement it, edit the function

    masterLogFilePath = os.path.join(logFolder,'DailyServerLog.csv')

    # Call function
    countImages(logFilePath,logFolder,masterLogFilePath)

if __name__ == "__main__":
    main()

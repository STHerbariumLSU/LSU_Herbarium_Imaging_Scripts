import os
import glob
import datetime
import pandas as pd


def countFiles(barcodes,files,portals,csvLogFilePath):

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

    if not os.path.exists(csvLogFilePath):
        #print(header)
        with open(csvLogFilePath,"w") as csvLogFile:
            csvLogFile.write("%s\n" % logHeader)
            csvLogFile.write("%s\n" % csvLogLine)
            csvLogFile.close()
             
    # If csv file exists, add new line 

    elif os.path.exists(csvLogFilePath):
        #print(csvLine)
        with open(csvLogFilePath,"a") as csvLogFile:
            csvLogFile.write("%s\n" % csvLogLine)
            csvLogFile.close()

def makeCSV(logFolder,csvFolder,webPath,header,newest,oldest,csvLogFilePath):

    # Get list of all log files edited on specified dates. 
    logFilesList=[]
    #print(oldest,newest)

    # Get all files in Log Folder
    logFolderList = []
    for file in os.listdir(logFolder):
        if file.endswith(".txt"):
            path = os.path.join(logFolder, file)
            logFolderList.append(path)

    # Get all files that were imaged on the specified dates 
    for p in logFolderList:
        #print(path)
        st = os.stat(p)    
        mtime = datetime.date.fromtimestamp(st.st_mtime)
        # If mtime is greater(newer) than oldest date and smaller(older) than newest date
        if mtime >= oldest and mtime <= newest:
            #print(p)
            #print(mtime)
            logFilesList.append(p)

    # Set date name for csv file - today's date 
    logDate = str(datetime.date.today().strftime("%Y-%m-%d"))

    # Create lists to calculate summary numbers
    barcodes=[]
    files=[]
    portals=[]

    # Iterate through log files 
    for logFile in logFilesList:

        # Open the file 
        logF = open(logFile,"r")
        #print(logFile)

        # Loop through lines in log file 
        for oPath in logF:

            # Get portal name 
            portal=oPath.split("/")[0]

            # Get path to csv file line will be written to.
            csvPath = os.path.join(csvFolder,logDate+"_"+portal+".csv")

            # Get path to original image
            path = os.path.split(oPath)[0]

            # Get file name without extension
            fileName=os.path.basename(oPath).split(".")[0]

            # Get barcode 
            barCode=fileName.split("_")[0]

            # Create web ready and thumbnail paths to web address 
            wr=os.path.join(webPath,path,fileName+'_WR.JPG')
            tn=os.path.join(webPath,path,fileName+'_TN.JPG')
            lg=os.path.join(webPath,path,fileName+'_L.JPG')

            # Creat csv file line
            info=[barCode,lg,tn,wr]
            csvLine=','.join(info)

            # If csv file does not exist, create with header 
            if not os.path.exists(csvPath):
                #print(header)
                with open(csvPath,"w") as csvFile:
                    csvFile.write("%s\n" % header)
                    csvFile.write("%s\n" % csvLine)
                    csvFile.close()
                     
            # If csv file exists, add new line 
            elif os.path.exists(csvPath):
                #print(csvLine)
                with open(csvPath,"a") as csvFile:
                    csvFile.write("%s\n" % csvLine)
                    csvFile.close()
            else:
                print("This should never happen")
            
            # Add to portal dict for reporting numbers
            barcodes.append(barCode)
            files.append(fileName)
            portals.append(portal)

    # Write out log file of all the files that got csv'd
    countFiles(barcodes,files,portals,csvLogFilePath)

def main():
    # Set times for the days that you want logs from
    # Days begin and end at midnight. 
    # Ex: Logs from June 3rd-July 10th. 
    # newest = datetime.datetime(year=2020,month=7,day=11)
    # oldest = datetime.datetime(year=2020,month=6,day=3)
    
    newest = datetime.date.today()
    oldest = newest - datetime.timedelta(days=7)

    # Path to log files that are made when images are uploaded to server
    logFolder = '/mnt/e/CFLA-LSU-Station2/LSUCollections/Logs/'
    #logFolder = '/Users/ChatNoir/Projects/HerbariumRA/test/'
    
    # Path to folder where CSV files will be made
    csvFolder='/mnt/e/CFLA-LSU-Station2/LSUCollections/CSVLogs/'
    #csvFolder='/Users/ChatNoir/Projects/HerbariumRA/test/csv/'

    # Web address for linking images 
    webPath = 'http://cyberfloralouisiana.com/images/LSUCollections/' 

    # Header for csv file, compatable with Symbiota

    csvHeader = ['catalogNumber','large JPG','thumbnail','webview']
    header = ",".join(csvHeader)

    # Path to a log file that counts the number of files etc in each csv file
    # This log is extremely customized for LSU, if you want to implement it, edit the function

    csvLogFilePath = os.path.join(csvFolder,'csvLog.csv')

    # Call function
    makeCSV(logFolder,csvFolder,webPath,header,newest,oldest,csvLogFilePath)

if __name__ == "__main__":
    main()

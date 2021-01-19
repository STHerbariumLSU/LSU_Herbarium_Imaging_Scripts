import os
import itertools
#import pathlib2 as pathlib
import pathlib
import shutil 
import platform
import datetime
import pandas as pd

## Add "if file name ends with jpg" add to portal list. to filter out cr2 for portal counts
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
    print(csvLine)
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
            #print(csvLine)
            with open(csvLogFilePath,"a") as csvLogFile:
                csvLogFile.write("%s\n" % csvLogLine)
                csvLogFile.close()
    else:
        print("no images today")

def makeFolders(sourceFolder,destinationFolder,portalFolders,otherFolders):
        # Create folders if needed in both source and destination 
        for x in portalFolders+otherFolders:
            p1=os.path.join(sourceFolder,x)
            p2=os.path.join(destinationFolder,x)
            #print(p1,p2)
            if not os.path.exists(p1):
                pathlib.Path(p1).mkdir(parents=True)
            if not os.path.exists(p2):
                pathlib.Path(p2).mkdir(parents=True)

        # Also make folders named "BadBarcode" and "Logs" in your source folder
        LogPath=os.path.join(sourceFolder,"Logs")
        BadPath=os.path.join(sourceFolder,"BadBarcode")
        #print(LogPath,BadPath)
        if not os.path.exists(LogPath):
            pathlib.Path(LogPath).mkdir(parents=True)
        if not os.path.exists(BadPath):
            pathlib.Path(BadPath).mkdir(parents=True)

def splitNumLet(b,f,errorFilePath):
    '''
    Takes barcode in the format ABC_12345 and splits it into numbers and letters
    If barcode isnt in this format, it returns the original barcode
    '''
    try:
        b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]
        return b_letters,b_numbers
    except ValueError:
        writeError = open(errorFilePath,'a')
        writeError.write("Incorrect barcode format. Will be moved to BadBarcode folder - "+str(f)+'\n')
        writeError.close()
        return b

def creationDate(path_to_file):
    """
    NO Longer used, but can be used if needed. 
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    to transfer this into a human readable date - 
        import datetime 
        str(datetime.datetime.fromtimestamp(int(d)))
    """
    if platform.system() == 'Windows':
        # on windows ctime refers to creation date, NOT change time as on linux. 
        return os.path.getctime(path_to_file)
    else: # Likely on Linux, try to get birth time, default to mod time. 
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime  

def newPathName(sourceFolder,FileName,sourceFilePath,destinationPortalFolder,barcodeMax,barcodeMin,errorFilePath,csvLogFilePath):
    '''
    Use old path to image, image file name, and destination parent folder (portal for LSU) to create a new path to move image. 
    Folder structure comes from barcode
    ex: LSU01020304 -> root/portal/lsu/01/020/LSU01020304.jpg 
    Improperly formated barcodes, or barcodes that are too long will have their destination be in the "BadBarcode" folder in the source folder for manual inspection and editing. 
    '''
    # Isolate barcode, remove anything that comes after . _ or -
    Barcode=FileName.split(".")[0].split("_")[0].split("-")[0]
    if barcodeMax >= len(Barcode) >= barcodeMin: 
        # Split letters and numbers in two, returning two strings. LSU12345678 = LSU, 12345678. 
        # If barcode has the wrong format, the whole barcode will be returned. 
        splitBarcode=splitNumLet(Barcode,FileName,errorFilePath)
        # If the barcode is returned as a single string
        if len(splitBarcode) == 1:
            # File this into a "BadBarcode" folder for manual inspection and editing. 
            newDir = os.path.join(sourceFolder,"BadBarcode",FileName)
            newPath = os.path.join(sourceFolder,"BadBarcode")
        # If the barcode was split into two strings, continue to split and create new file path
        elif len(splitBarcode) == 2:
            Collection,number=splitBarcode
            # Split apart number to create new file path
            lastThree=number[-3:] # this isnt nessecary, just to double check things
            cutoffThree=number[:-3]
            secondFolder=cutoffThree[-3:]
            firstFolder=cutoffThree[:-3]
            # Create folders from barcode and portal information
            # ex: LSU01020304 -> root/portal/lsu/01/020/LSU01020304.jpg 
            newPath=os.path.join(destinationPortalFolder,Collection,firstFolder,secondFolder,FileName.upper())
            # Get directory path to check if folders need to be created
            newDir=os.path.dirname(newPath)
        else:
            writeError = open(errorFilePath,'a')
            writeError.write("Barcode splitting went wrong for- "+str(Barcode)+'\n')
            writeError.close()

    else:
        # File this into a "BadBarcode" folder for manual inspection and editing. 
        newPath = os.path.join(sourceFolder,"BadBarcode",FileName)
        newDir = os.path.join(sourceFolder,"BadBarcode")
    return newDir,newPath,Barcode

def moveFiles(sourceFolder,destinationFolder,portalFolders,otherFolders,barcodeMax,barcodeMin,outLogsuffix,errorFilePath,csvLogFilePath):
    
    # Create lists to calculate summary numbers
    barcodes=[]
    files=[]
    portals=[]

    # Iterate through list of user defined organizing source folders, for LSU these are portal names 
    for folder in portalFolders:
    
        # Get full folder path 
        folderPath=os.path.join(sourceFolder,folder)
        
        # Iterate through files in folder 
        for filename in os.listdir(folderPath):

            # Change file names to uppercase for consistancy later on
            FileName=filename.upper()
            
            # Get full path to source file 
            sourceFilePath=os.path.join(folderPath,filename)

            # Get creation date for source file, or last modification date if creation date cannot be recovered
            #birthDate=creationDate(sourceFilePath)
            
            # Get path to source folder 
            destinationPortalFolder = os.path.join(destinationFolder,folder)
            
            # Create destination file path and folder path 
            # The function newPathName also checks for barcode format and length
            # All files with incorrectly formatted barcodes will be moved to a "BadBarcode" folder NOT on the specified backup 
            destinationFolderPath,destinationFilePath,barCode = newPathName(sourceFolder,FileName,sourceFilePath,destinationPortalFolder,barcodeMax,barcodeMin,errorFilePath,csvLogFilePath)
 
            # For files with CORRECTLY formated barcodes 

            if "BadBarcode" not in destinationFilePath:
                
                try:
                    # If destination nested folders do not exist, create them
                    if not os.path.exists(destinationFolderPath):
                        pathlib.Path(destinationFolderPath).mkdir(parents=True)
                        
                    # Move file to destination    
                    shutil.move(sourceFilePath,destinationFilePath)
                    
                    # Add to portal dict for reporting numbers
                    barcodes.append(barCode)
                    files.append(FileName)
                    # Only count jpg files for counting files in portals. 
                    jpg = FileName.split(".")[-1]
                    if jpg == 'JPG':
                        portals.append(folder)
                    
                    # Create log file based on day script is run 
                    logFileName=str(datetime.date.today().strftime("%Y-%m-%d"))+"_"+outLogsuffix

                    # Old version - Create log file name using the day that the file was created or modified(Ex 2019-06-07) 
                    # Also add customized suffix and file extension to log file name 
                    #logFileName=str(datetime.datetime.fromtimestamp(int(birthDate))).split()[0]+outLogsuffix
                    
                    # Get path to log file 
                    logFilePath=os.path.join(sourceFolder,"Logs",logFileName)

                    # Open log file and write destination file path 
                    writeLog = open(logFilePath,'a')
                    writeLog.write(destinationFilePath+'\n')
                    writeLog.close()
                    
                # If anything under the try statement cannot be completed, an error will be printed to screen.
                except Exception as e:
                    writeError = open(errorFilePath,'a')
                    writeError.write(str(e)+" File failed to move from "+str(sourceFilePath)+' to '+str(destinationFilePath)+'\n')
                    writeError.close()

            # For files with incorrectly formated barcodes
            # File is moved to BadBarcode and not written to the log file
            else:
                try:
                    shutil.move(sourceFilePath,destinationFilePath)

                # If anything under the try statement cannot be completed, an error will be printed to screen.
                except Exception as e:
                    writeError = open(errorFilePath,'a')
                    writeError.write(str(e)+" File failed to move "+str(sourceFilePath)+'\n')
                    writeError.close()

    # Write out log file of all the files that got moved

    countFiles(barcodes,files,portals,csvLogFilePath)

    # Iterate through list of user defined "other" folders, for LSU this is the folder "Random"               
    for folder in otherFolders:
        
        # Get full folder path 
        folderPath=os.path.join(sourceFolder,folder)
        
        # Get files in any nested folders that exists beyond the source folder, for LSU it will be named "Random"
        for filepath in pathlib.Path(folderPath).rglob('*'):
        
            # Ignore folders
            if filepath.is_dir():
                pass
            
            else:
                # For all files get full file path 
                sourceFilePath = filepath.absolute()
                
                # Get destination file path, replicating any nested folders within the main source folder.
                nestedFolderPath=str(sourceFilePath).strip(folderPath)
                destinationFilePath=os.path.join(destinationFolder,folder,nestedFolderPath)
                destinationFolderPath=os.path.dirname(destinationFilePath)
                
                try:
                    # Create desination folders if needed. 
                    if not os.path.exists(destinationFolderPath):
                        pathlib.Path(destinationFolderPath).mkdir(parents=True)  
                    
                    # Move file to destination
                    shutil.move(sourceFilePath,destinationFilePath)
                
                # If anything under the try statement cannot be completed, an error will be printed to screen.
                except Exception as e:
                        print(str(e)+" File failed to move "+str(sourceFilePath))
                

def main():
    ############ BEGIN section to customize 
    # Make sure paths have a trailing forward slash at the end '/'. otherwise everything will fail. 
    # Folder of images on computer
    
    sourceFolder='/mnt/c/Users/Image/Desktop/Imaging/'
    
    # Folder for long term storage 
    
    destinationFolder='/mnt/e/CFLA-LSU-Station2/LSUCollections/'

    # List folders that correspond to how you want to store your images
    # For LSU images are stored based on the portal they will be uploaded to online.
    
    portalFolders=['Algae','Bryophyte','Fungi','Lichen','Vascular']
    
    # Extra folders for one time projects. Barcodes will not be checked, and any nested folders will be moved as is. 
    
    otherFolders=['Random']

    # Maximum length for legitimate barcode, does not count anything trailing an underscore "_"
    
    barcodeMax=15
    barcodeMin=9
    
    # String that will be appended to all out logs. Can customize for each computer. 
    # Make sure this is different from the string appended to your server logs in the rsyncdaily.sh script. 
    # Add whatever file extension you want. ".txt" is reccomended so simple text editors can open the files.
    
    outLogsuffix="local_ws2.txt"
    
    csvFolder='/mnt/c/Users/Image/Desktop/Imaging/LocalLogs/'
    
    csvLogFilePath = os.path.join(csvFolder,'DailyLocalLog.csv')
    
    ############ END section to customize  

    # Create folders if needed 
    # This will also make folders named "BadBarcode" and "Logs" in your source folder
    # Best to hash this out after setup
    #makeFolders(sourceFolder,destinationFolder,portalFolders,otherFolders)
    
    # Initiate a file path where errors will be stored. 

    errorFilePath=os.path.join(sourceFolder,"Logs",str(datetime.date.today())+"-ERRORS.txt")

    # Move the files!!! 

    moveFiles(sourceFolder,destinationFolder,portalFolders,otherFolders,barcodeMax,barcodeMin,outLogsuffix,errorFilePath,csvLogFilePath)

    '''
    Extra notes 
    *File name restrictions*
    File names are expected to start with a barcode. This barcode should start with letters followed by ONLY numbers.
    Folders will be created first using the letters, then using the numbers. 
    Extra notes or tags, such as numbering multiple files should come after an underscore "_"
    Ex: LSU01234567.JPG or LSU01234567_1.JPG
    All file names will be changed to all caps if they are not already. Except those files in the other/random folders
    Run script in Task scheduler on Windows 10 with 
    wsl python3 /mnt/c/Users/Image/Documents/GitHub/HerbariumRA/organizeIncomingImages.py
    '''

if __name__ == "__main__":
    main()
    print("Done")

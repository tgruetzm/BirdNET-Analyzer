#!/usr/bin/python

import numpy as np
from datetime import datetime, timedelta
import soundfile as sf
import glob
from multiprocessing import Pool, Manager
import os
import shutil


inputPaths = ["F:\\","H:\\","G:\\"]
#outputPath = "D:\\NAS\\ORI Audio\\2024\\Audio\\"
outputPathAudio = "E:\\Import"
outputPathMetaData = "Z:\\Owl Research Institute\\Audio\\2025\\Metadata"


def copyFiles(path):
    if glob.glob(path):
        metaFiles = glob.glob(path + "*.txt")
        logFile = glob.glob(path + "*log.txt")
        recId = str(os.path.basename(logFile[0])).split('_')[0]
        current_date = datetime.now()
        current_date_string = current_date.strftime("%Y-%m-%d %H-%M")
        outputPathMetaRec = outputPathMetaData + "\\" + recId + "_" + current_date_string
        if not glob.glob(outputPathMetaRec):
            print("Creating: " + outputPathMetaRec)
            os.mkdir(outputPathMetaRec)
        for file in metaFiles:
            if os.path.basename(file) == "config.txt":
                continue  # Skip this file
            outputFile = outputPathMetaRec + "\\" + os.path.basename(file)
            if glob.glob(outputFile): #skip if exists
                continue
            else:
                print("Copying file: " + file)
                shutil.copy(file, outputPathMetaRec)

        audioFiles = glob.glob(path + "Audio\\*.wv")
        count = len(audioFiles)
        index = 1
        for file in audioFiles:
            if glob.glob(outputPathAudio + "\\" + os.path.basename(file)): #skip if exists
                print("File Exists " + str(index) + "/" + str(count) + " "  + file)
                index +=1
                continue
                
            print("Copying file " + str(index) + "/" + str(count) + " "  + file)
            shutil.copy(file, outputPathAudio)
            index +=1




if __name__ == '__main__':
   
    if not glob.glob(outputPathAudio):
        print("Creating: " + outputPathAudio)
        os.mkdir(outputPathAudio)
    
    if not glob.glob(outputPathMetaData):
        print("Creating: " + outputPathMetaData)
        os.mkdir(outputPathMetaData)
        
    #for file in glob.glob(inputPath):
    #    readFile(file)
    with Pool(3) as p:
        p.map(copyFiles, inputPaths)
        
    p.join()




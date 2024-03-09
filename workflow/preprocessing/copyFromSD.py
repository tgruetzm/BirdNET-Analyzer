#!/usr/bin/python

import numpy as np
from datetime import datetime, timedelta
import soundfile as sf
import glob
from multiprocessing import Pool, Manager
import os
import shutil


inputPaths = ["F:\\","H:\\"]
#outputPath = "D:\\NAS\\ORI Audio\\2024\\Audio\\"
outputPathAudio = "E:\\Audio Import\\Audio"
outputPathMetaData = "E:\\Audio Import\\Metadata"


def copyFiles(path):
    metaFiles = glob.glob(path + "*.txt")
    for file in metaFiles:
        if os.path.basename(file) == "config.txt":
            continue  # Skip this file
        if glob.glob(outputPathMetaData + "\\" + os.path.basename(file)): #skip if exists
            print("Skipping file: " + file)
            continue
        print("Copying file: " + file)
        shutil.copy(file, outputPathMetaData)

    audioFiles = glob.glob(path + "Audio\\*.wav")
    count = len(audioFiles)
    index = 1
    for file in audioFiles:
        if glob.glob(outputPathAudio + "\\" + os.path.basename(file)): #skip if exists
            print("Skipping file " + str(index) + "/" + str(count) + " "  + file)
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
    with Pool(2) as p:
        p.map(copyFiles, inputPaths)
        
    p.join()




#!/usr/bin/python

import numpy as np
from datetime import datetime, timedelta
import soundfile as sf
import glob
from multiprocessing import Pool, Manager

import librosa
import io
import time
import os


inputPath = "E:\\Audio Import\\*.wav"
#outputPath = "D:\\NAS\\ORI Audio\\2024\\Audio\\"
outputPath = "E:\\delete\\"


def readFile(file):
    #try:
    print(file)
    fileArr = file.split("\\")
    fileName = fileArr[len(fileArr)-1]
    outputFile = outputPath + fileName.replace(".wav",".flac")
    if glob.glob(outputFile):
        return
    print("Loading: " + file)


    data, sample_rate = sf.read(file)
    modTime = os.path.getmtime(file)
    print("Writing: " + outputFile)
    sf.write(outputFile, data, samplerate=sample_rate,format="flac")
    os.utime(outputFile, (modTime, modTime))
    #except:
        #print("error")



if __name__ == '__main__':
   
    if not glob.glob(outputPath):
        print("Creating: " + outputPath)
        os.mkdir(outputPath)

    if not glob.glob(inputPath):
        print("RAW audio not found: " + inputPath)
    else:
        files = glob.glob(inputPath)
        
        #for file in glob.glob(inputPath):
        #    readFile(file)

        with Pool(4) as p:
            p.map(readFile, files)
        p.join()




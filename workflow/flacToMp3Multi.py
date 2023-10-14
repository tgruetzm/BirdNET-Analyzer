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

###USE this for 2023 raw to flac processing
###
# Variables
samplingRate = 12000 #12k audio, but actual is a bit slower 

inputPath = "D:\\BirdNet Audio\\2023\\*.flac"
#inputPath  = "D:\\24k PCM audio\\*.pcm" 
#outputPath = "E:\\BirdNet-Audio\\"
#outputPath = "E:\\BirdNet-Audio\\Outdoor Tests\\"
outputPath = "D:\\BirdNet Audio\\2023 mp3\\"


def readFile(file, lock):
    print(file)
    fileNameArr = str(file).split("\\")

    baseName = fileNameArr[len(fileNameArr) -1].replace(".flac",".mp3")
    outputFile = outputPath + baseName

    if glob.glob(outputFile):
        return
    print("Loading: " + file)

    lock.acquire()
    data, samplerate = sf.read(file)
    lock.release()
    modTime = os.path.getmtime(file)
    print("Writing: " + outputFile)
    sf.write(outputFile, data, samplerate=samplerate)
    os.utime(outputFile, (modTime, modTime))
    #except:
        #print("error")



if __name__ == '__main__':
    manager = Manager()
    lock = manager.Lock()
    processPool = Pool(processes=8)
    if not glob.glob(outputPath):
        print("Creating: " + outputPath)
        os.mkdir(outputPath)

    if not glob.glob(inputPath):
        print("RAW audio not found: " + inputPath)
    else:
        rawFiles = []
        
        for file in glob.glob(inputPath):
            result = processPool.apply_async(readFile,(file,lock))

    processPool.close()
    processPool.join()
            #pool.map(lambda file: readFile(file, lock), glob.glob(inputPath))
            #for file in glob.glob(inputPath):
                    #print(file)
                    #fileLoadPool.apply_async(readFile,(file,))
            




#!/usr/bin/python

from scipy.io import wavfile
import noisereduce as nr
import soundfile as sf
import glob
from datetime import datetime
from multiprocessing import Pool, Manager
import os

# Variables
samplingRate = 12000 #12k audio, but actual is a bit slower 
#
inputPath = "D:\\NAS\\ORI Audio\\2024\\Audio\\All\\BM-1short-f0a69_2024-01-30_T17-36-03.flac"
#inputPath = "D:\\BirdNet Audio 2023\\*.flac"
outputPath = "D:\\NAS\\ORI Audio\\2024\\Audio\\All\\"


#inputPath = "C:\\Users\\Troy\\OneDrive\\GGOW Audio 2023\\*.mp3"
#outputPath = "C:\\Users\\Troy\\OneDrive\\GGOW Audio 2023\\NR\\"
#inputPath  = "D:\\24k PCM audio\\*.pcm" 
#outputPath = "E:\\BirdNet-Audio\\"


#def writeOutputFile(outputFile, data, samplerate):
    #sf.write(outputFile, data, samplerate=samplerate)

def processFile(file,p):
    print("Processing: " + file)
    start_time = datetime.now()
    fileParts = file.split("\\")
    fileName = fileParts[len(fileParts)-1]
    outputFile = outputPath + fileName.replace("1short",str(p) + "-1short")
    #if os.path.exists(outputFile):
    #    return
    data, rate = sf.read(file)
    reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=p)
    print(outputFile)
    sf.write(outputFile,reduced_noise, rate)
    delta_time = (datetime.now() - start_time).total_seconds()
    print("Time to NR file: {} seconds".format(delta_time))

if __name__ == '__main__':


    if not glob.glob(inputPath):
        print("RAW audio not found: " + inputPath)

    params = [.2,.4,.6,.8,.95]
    #params = [10,25,50,75,100,200,250]
    for p in params:
        processFile(inputPath,p)

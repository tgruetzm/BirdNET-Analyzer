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
inputPath = "D:\\BirdNet Audio 2023\\*.flac"
#inputPath = "D:\\BirdNet Audio 2023\\*.flac"
outputPath = "E:\\BirdNet Audio 2023\\Audio .8 NR\\"


#inputPath = "C:\\Users\\Troy\\OneDrive\\GGOW Audio 2023\\*.mp3"
#outputPath = "C:\\Users\\Troy\\OneDrive\\GGOW Audio 2023\\NR\\"
#inputPath  = "D:\\24k PCM audio\\*.pcm" 
#outputPath = "E:\\BirdNet-Audio\\"


#def writeOutputFile(outputFile, data, samplerate):
    #sf.write(outputFile, data, samplerate=samplerate)

def processFile(file,lock):
    print("Processing: " + file)
    start_time = datetime.now()
    fileParts = file.split("\\")
    fileName = fileParts[len(fileParts)-1]
    outputFile = outputPath + fileName
    if os.path.exists(outputFile):
        return
    lock.acquire()
    data, rate = sf.read(file)
    lock.release()
    reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=.8)
    sf.write(outputFile,reduced_noise, rate)
    delta_time = (datetime.now() - start_time).total_seconds()
    print("Time to NR file: {} seconds".format(delta_time))

if __name__ == '__main__':

    manager = Manager()
    lock = manager.Lock()
    processPool = Pool(processes=5)
    if not glob.glob(inputPath):
        print("RAW audio not found: " + inputPath)
    for file in glob.glob(inputPath):
        result = processPool.apply_async(processFile,(file,lock))

    processPool.close()
    processPool.join()


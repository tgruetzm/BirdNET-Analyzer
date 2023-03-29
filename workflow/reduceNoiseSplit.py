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
outputPath = "E:\\BirdNet Audio 2023\\Audio .8 NR\\"


#inputPath = "C:\\Users\\Troy\\OneDrive\\GGOW Audio 2023\\*.mp3"
#outputPath = "C:\\Users\\Troy\\OneDrive\\GGOW Audio 2023\\NR\\"
#inputPath  = "D:\\24k PCM audio\\*.pcm" 
#outputPath = "E:\\BirdNet-Audio\\"


#def writeOutputFile(outputFile, data, samplerate):
    #sf.write(outputFile, data, samplerate=samplerate)

def processFile(file,lock):
    start_time = datetime.now()
    fileParts = file.split("\\")
    fileName = fileParts[len(fileParts)-1]
    outputFile = outputPath + fileName
    
    if os.path.isfile(outputFile):
        return
    print("Processing: " + file)
    print("output:" + outputFile)
    start = 0
    duration = samplingRate * 60 * 60
    lock.acquire()
    data, rate = sf.read(file,start=start,frames=duration)
    lock.release()
    while len(data) > 0:
        print("processing: " + str(start))
        reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=.6)
        #sf.write(outputFile,reduced_noise, rate)
        if(os.path.isfile(outputFile)):
            with sf.SoundFile(outputFile, mode = 'r+') as wfile:
                wfile.seek(0,sf.SEEK_END)
                wfile.write(reduced_noise)
        else:
            sf.write(outputFile, reduced_noise, rate,format="flac") # writes to the new file
        start += duration 
        data, rate = sf.read(file,start=start,frames=duration)

    delta_time = (datetime.now() - start_time).total_seconds()
    print("Time to NR file: {} seconds".format(delta_time))

if __name__ == '__main__':

    manager = Manager()
    lock = manager.Lock()
    processPool = Pool(processes=1)
    if not glob.glob(inputPath):
        print("RAW audio not found: " + inputPath)
    for file in glob.glob(inputPath):
        processFile(file,lock)
        #result = processPool.apply_async(processFile,(file,lock))

    processPool.close()
    processPool.join()


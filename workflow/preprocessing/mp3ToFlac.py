#!/usr/bin/python

import numpy as np
from datetime import datetime, timedelta
import soundfile as sf
import glob
from pydub import AudioSegment
from multiprocessing import Pool, Manager

import librosa
import io
import time
import os


inputPath = "E:\\Audio Import\\Audio\\*.mp3"
outputPath = "D:\\NAS\\ORI Audio\\2024\\Audio\\"
#outputPath = "E:\\delete\\"


def processFile(file):
    #try:
    print(file)
    fileArr = file.split("\\")
    fileName = fileArr[len(fileArr)-1]
    outputFileL = outputPath + fileName.replace(".mp3",".L.flac")
    if glob.glob(outputFileL):
        return
    
    outputFileR = outputPath + fileName.replace(".mp3",".R.flac")
    if glob.glob(outputFileR):
        return
    print("Loading: " + file)


    audio = AudioSegment.from_mp3(file)

    audio.export("temp.wav", format="wav")


    data, samplerate = sf.read("temp.wav")

    L_channel = data[:, 0]
    R_channel = data[:, 1]

    print("Writing: " + outputFileL)
    sf.write(outputFileL, L_channel, samplerate=samplerate,format="flac")

    print("Writing: " + outputFileR)
    sf.write(outputFileR, R_channel, samplerate=samplerate,format="flac")



if __name__ == '__main__':
   
    if not glob.glob(outputPath):
        print("Creating: " + outputPath)
        os.mkdir(outputPath)

    if not glob.glob(inputPath):
        print("RAW audio not found: " + inputPath)
    else:
        files = glob.glob(inputPath)
        
    for file in glob.glob(inputPath):
           processFile(file)

    #with Pool(1) as p:
    #    p.map(processFile, files)
    
   # p.join()





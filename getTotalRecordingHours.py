#!/usr/bin/python

import glob
import os
import sys
import audio





results = {}

inputPaths = ["E:\\BirdNet Audio 2023\\Audio\\Blue Mountain\\","E:\\BirdNet Audio 2023\\Audio\\Missions\\"]



if __name__ == '__main__':

    totalLengthSeconds = 0
    for inputPath in inputPaths:
        for file in glob.glob(inputPath + "*.flac"):
            l = audio.getAudioFileLength(file,12000)
            totalLengthSeconds += l

    print("total recording hours: " + str(totalLengthSeconds/60/60))


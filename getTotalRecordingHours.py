#!/usr/bin/python

import glob
import librosa




results = {}

inputPaths = ["D:\\NAS\\ORI Audio\\2024\\Audio\\"]



if __name__ == '__main__':

    totalLengthSeconds = 0
    for inputPath in inputPaths:
        for file in glob.glob(inputPath + "*.flac"):
            print(file)
            l = librosa.get_duration(filename=file)
            totalLengthSeconds += l
            print("current recording hours: " + str(totalLengthSeconds/60/60))

    print("total recording hours: " + str(totalLengthSeconds/60/60))


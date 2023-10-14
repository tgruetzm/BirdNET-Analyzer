#!/usr/bin/python

import glob
import os
import sys






results = {}

inputPaths = ["E:\\BirdNet Audio 2023\\Audio\\Blue Mountain\\","E:\\BirdNet Audio 2023\\Audio\\Missions\\"]



if __name__ == '__main__':

    for inputPath in inputPaths:
        for file in glob.glob(inputPath + "*.flac"):
            fileParts = file.split("\\")
            fileName = fileParts[len(fileParts)-1]
            fileNameParts = fileName.split("_")
            recorder = fileNameParts[0]
            if recorder not in results:
                results[recorder] = recorder

    with open('C:\\Users\\Troy\\Downloads\\processedRecorders.csv', 'w') as f:  
        recorders = dict(sorted(results.items()))
        for r in recorders:
            f.write(r + "\n")



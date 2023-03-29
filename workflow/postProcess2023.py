#!/usr/bin/python

import glob
import subprocess
import os
import soundfile

# define the path to the Python script you want to call
splitResultsScript = 'splitResultsbySpecies.py'
segmentsScript = '..\segments.py'

#python segments.py --threads 1 --slist "E:\BirdNet Audio GGOW 2023\species_list.txt" --results "E:\BirdNet Audio GGOW 2023\Missions\Strix varia_Barred Owl" --min_conf .1 --audio "E:\BirdNet Audio GGOW 2023\Missions" --o "E:\BirdNet Audio GGOW 2023\Missions-BDOW"

# Directories are used for location names
baseDirectory = "E:\\BirdNet Audio 2023\\"
inputPath = baseDirectory + "Audio\\*\\"
speciesList = {("Strix varia_Barred Owl",baseDirectory + "speciesBDOW.txt"),("Strix nebulosa_Great Gray Owl",baseDirectory + "speciesGGOW.txt"),("Asio otus_Long-eared Owl",baseDirectory + "speciesLEOW.txt"),
               ("Glaucidium gnoma_Northern Pygmy-Owl",baseDirectory + "speciesNOPO.txt"),("Aegolius acadicus_Northern Saw-whet Owl",baseDirectory + "speciesNSWO.txt")}


def processLocation(directory):
    parts = directory.split("\\")
    location = parts[len(parts)-2]
    print("Splitting species for location: " + directory)
    #run split results process
    subprocess.call(['python', splitResultsScript,directory])

    for species in speciesList:
        outputDirectoryBase =baseDirectory + "Segments" +"\\" + location
        if not glob.glob(outputDirectoryBase):
            print("Creating: " + outputDirectoryBase)
            os.mkdir(outputDirectoryBase)
        outputDirectory =baseDirectory + "Segments" +"\\" + location + "\\" + species[0]
        if not glob.glob(outputDirectory):
            print("Creating: " + outputDirectory)
            os.mkdir(outputDirectory)

        print("results: " + directory + species[0])
        print("segments for: " + outputDirectory)
        subprocess.call(['python',segmentsScript,"--min_conf",".05","--threads","1", "--slist",species[1],"--results",directory + species[0],"--audio", directory, "--o", outputDirectory])



if __name__ == '__main__':

    #if not glob.glob(outputPath):
    #    print("Creating: " + outputPath)
    #    os.mkdir(outputPath)

    if not glob.glob(inputPath):
        print("path not found: " + inputPath)
    else:
        for file in glob.glob(inputPath):
            processLocation(file)

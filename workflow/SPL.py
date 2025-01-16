#!/usr/bin/python
import librosa
import numpy as np
import glob
from multiprocessing import Pool, Manager
import os


def calculateRMS(audio_file, result_queue):

    print("Analyzing: " + audio_file)
    results = []
    offset = 0
    duration = 3600
    length = librosa.get_duration(path=audio_file)
    while offset < length:
        y, sr = librosa.load(audio_file, sr=None, mono=True,offset=offset,duration=duration)

        # Calculate RMS
        rms = librosa.feature.rms(y=y)
        rms_value = rms.mean()
        rms_dB = 20 * np.log10(rms_value)
        offset += duration
        results.append(rms_dB)

    rms_avg = sum(results)/len(results)
    base_fileName = os.path.basename(audio_file)
    result_queue.put((base_fileName, rms_avg ))


def write_results_to_file(results, output_file):
    with open(output_file, 'w') as f:
        for audio_file, rms_dB in results:
            f.write(f"{audio_file},")
            f.write(f"{122-40+rms_dB}\n")


if __name__ == '__main__':
    inputPath = "D:\\NAS\\ORI Audio\\2024\\Audio\\*.flac"
    # outputPath = "E:\\delete\\output.txt"
    output_file = "D:\\NAS\\ORI Audio\\2024\\SPL.txt"

    if not glob.glob(inputPath):
        print("audio not found: " + inputPath)
    else:
        files = glob.glob(inputPath)

        manager = Manager()
        result_queue = manager.Queue()

        with Pool(16) as p:
            # Pass result_queue to each process
            p.starmap(calculateRMS, [(file, result_queue) for file in files])

        # Collect results from the queue
        
        compiledResults = {}
        while not result_queue.empty():
            item = result_queue.get()
            keyBase = item[0].split('-')
            key = keyBase[0] + '-' + keyBase[1]
            if key not in compiledResults:
                results = []
                results.append(item[1])
                compiledResults[key] = results
            else:
                compiledResults[key].append(item[1])


        #print(compiledResults)
        results = []
        for key in compiledResults:
            levels = compiledResults[key]
            rmsLevel = sum(levels)/len(levels)
            results.append((key,rmsLevel))
        # Write results to file
        write_results_to_file(results, output_file)

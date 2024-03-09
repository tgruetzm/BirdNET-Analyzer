#!/usr/bin/python

import soundfile as sf
import torch
import torchaudio
import torchaudio.functional as F
import torchaudio.transforms as T


# Variables
#samplingRate = 12000 #12k audio, but actual is a bit slower 

#inputPath = "D:\\Audio Import\\QA Audio\\*.pcm"
#inputPath  = "D:\\24k PCM audio\\*.pcm" 
#outputPath = "E:\\BirdNet-Audio\\"
#outputPath = "E:\\BirdNet-Audio\\QA Audio\\"


#def writeOutputFile(outputFile, data, samplerate):
    #sf.write(outputFile, data, samplerate=samplerate)

if __name__ == '__main__':

# load data
    inputFile = "C:\\Users\\Troy\\Downloads\\BM-18-466f9_24000.flac"
    outputFile = inputFile.replace(".flac","resamp.3.flac")
    data, rate = sf.read(inputFile)
    waveform, sample_rate = torchaudio.load(inputFile)
    resampler = T.Resample(24000, 48000, dtype=waveform.dtype, lowpass_filter_width=64,rolloff=0.3,resampling_method="kaiser_window")
    sig = resampler(waveform).numpy()[0]

    sf.write(outputFile,sig, 48000)

"""Module containing audio helper functions.
"""
import numpy as np

import config as cfg
import soundfile as sf
import noisereduce as nr
import torchaudio.transforms as T
import torch
import torchaudio
import numpy
import datetime

RANDOM = np.random.RandomState(cfg.RANDOM_SEED)


def openAudioFile(path: str, sample_rate=48000, offset=0.0, duration=None):
    """Open an audio file.

    Opens an audio file with librosa and the given settings.

    Args:
        path: Path to the audio file.
        sample_rate: The sample rate at which the file should be processed.
        offset: The starting offset.
        duration: Maximum duration of the loaded content.

    Returns:
        Returns the audio time series and the sampling rate.
    """
    # Open file with librosa (uses ffmpeg or libav)
    import librosa

    start_time = datetime.datetime.now()
    #//fileSampleRate = librosa.get_samplerate(path)
    #print(fileSampleRate)
    #torch.set_num_threads(1)
    sig, rate = librosa.load(path, sr=sample_rate, offset=offset, duration=duration, mono=True, res_type='kaiser_fast')#kaiser_best,'kaiser_fast'
    #//waveform, sample_rate = torchaudio.load(path, frame_offset=offset*fileSampleRate, num_frames=duration*fileSampleRate)
    #reduced_noise = nr.reduce_noise(y=waveform.numpy(), sr=fileSampleRate, prop_decrease=.95) # .95 seems to increase positives quite a bit, might be ideal.  Does require filtering by .2 min_conf to get false positives under control
    #defaultRolloff= 0.9475937167399596
    #.6 seems to be around 3700hz
    #.5 filters at 3000, seems to greatly increase detectability
    #.3 might be ideal for GGOW filtering, very low FP and good detectability
    #.15 is 900hz
    #.125 might work well to filter frogs from the audio
    #.25 worked slightly better than .3, trying .225
    #//resampler = T.Resample(fileSampleRate, 48000, dtype=waveform.dtype, lowpass_filter_width=64,resampling_method="kaiser_window",beta=14.769656459379492)
    #sig = resampler(torch.from_numpy(reduced_noise)).numpy()[0]
    #//sig = resampler(waveform).numpy()[0]
    #//rate = 48000
    delta_time = (datetime.datetime.now() - start_time).total_seconds()
    print("Finished resample {} in {:.2f} seconds".format(path, delta_time), flush=True)

    return sig, rate

def getAudioFileLength(path, sample_rate=48000):    
    
    # Open file with librosa (uses ffmpeg or libav)
    import librosa

    return librosa.get_duration(filename=path, sr=sample_rate)

def saveSignal(sig, fname: str):
    """Saves a signal to file.

    Args:
        sig: The signal to be saved.
        fname: The file path.
    """
    import soundfile as sf

    sf.write(fname, sig, 48000, "PCM_16")


def noise(sig, shape, amount=None):
    """Creates noise.

    Creates a noise vector with the given shape.

    Args:
        sig: The original audio signal.
        shape: Shape of the noise.
        amount: The noise intensity.

    Returns:
        An numpy array of noise with the given shape.
    """
    # Random noise intensity
    if amount == None:
        amount = RANDOM.uniform(0.1, 0.5)

    # Create Gaussian noise
    try:
        noise = RANDOM.normal(min(sig) * amount, max(sig) * amount, shape)
    except:
        noise = np.zeros(shape)

    return noise.astype("float32")


def splitSignal(sig, rate, seconds, overlap, minlen):
    """Split signal with overlap.

    Args:
        sig: The original signal to be split.
        rate: The sampling rate.
        seconds: The duration of a segment.
        overlap: The overlapping seconds of segments.
        minlen: Minimum length of a split.
    
    Returns:
        A list of splits.
    """
    sig_splits = []

    for i in range(0, len(sig), int((seconds - overlap) * rate)):
        split = sig[i : i + int(seconds * rate)]

        # End of signal?
        if len(split) < int(minlen * rate):
            break

        # Signal chunk too short?
        if len(split) < int(rate * seconds):
            split = np.hstack((split, noise(split, (int(rate * seconds) - len(split)), 0.5)))

        sig_splits.append(split)

    return sig_splits


def cropCenter(sig, rate, seconds):
    """Crop signal to center.

    Args:
        sig: The original signal.
        rate: The sampling rate.
        seconds: The length of the signal.
    """
    if len(sig) > int(seconds * rate):
        start = int((len(sig) - int(seconds * rate)) / 2)
        end = start + int(seconds * rate)
        sig = sig[start:end]

    # Pad with noise
    elif len(sig) < int(seconds * rate):
        sig = np.hstack((sig, noise(sig, (int(seconds * rate) - len(sig)), 0.5)))

    return sig

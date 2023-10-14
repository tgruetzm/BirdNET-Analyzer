import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

audio_file = 'C:\\Users\\Troy\\OneDrive\\Desktop\\Spectrogram audio\\OS-2-3_Female Begging.wav'
y, sr = librosa.load(audio_file)



# Set the desired FFT parameters
n_fft = 4096  # Number of FFT points (adjust as needed)
hop_length = 128  # Hop length between windows (adjust as needed)

fmin = 100
fmax = 6000

# Generate the spectrogram and set the y-axis limits
plt.figure(figsize=(10, 6), dpi=150)
#librosa.display.specshow(librosa.amplitude_to_db(librosa.stft(y), ref=np.max), y_axis='linear', x_axis='time', sr=sr, cmap='viridis', vmin=-60, vmax=0)
librosa.display.specshow(librosa.amplitude_to_db(librosa.stft(y, n_fft=n_fft, hop_length=hop_length), ref=np.max), y_axis='linear', x_axis='time', sr=sr, vmin=-40, vmax=0)
plt.ylim(fmin, fmax)  # Set the y-axis limits
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
#plt.colorbar(format='%+2.0f dB')
plt.title('GGOW Begging Female')
plt.show()






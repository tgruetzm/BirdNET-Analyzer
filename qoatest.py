
import qoa
import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write

# Define the input and output file paths
# Define the input and output file paths
input_wav_file = 'e:\SP-5-958fb_2024-03-13_T19-38-02.wav'  # Replace with your input WAV file path
output_qoa_file = 'e:\SP-5-958fb_2024-03-13_T19-38-02.qoa'  # Replace with your desired output QOA file path


# Read the WAV file
sample_rate, samples = wavfile.read(input_wav_file)

# Ensure samples are in the correct format (int16)
if samples.dtype != np.int16:
    raise ValueError(f"Expected int16 samples, but got {samples.dtype} instead.")

# Convert to QOA format
qoa_data = qoa.encode(samples)

# Save the QOA data to a file
with open(output_qoa_file, 'wb') as qoa_file:
    qoa_file.write(qoa_data)

print(f"Converted {input_wav_file} to {output_qoa_file} successfully!")


# Define the input and output file paths
input_qoa_file = 'e:\SP-5-958fb_2024-03-13_T19-38-02.qoa'  # Replace with your input QOA file path
output_wav_file = 'e:\SP-5-958fb_2024-03-13_T19-38-02.qoa.wav'  # Replace with your desired output WAV file path


# Decode the QOA file to get the samples and sample rate
buffer,shape = qoa.decode(input_qoa_file)
print(buffer)
print(shape)

# Convert the CFFI buffer to a NumPy array
samples_np = np.frombuffer(buffer, dtype=np.int16)

# Reshape the NumPy array according to the shape
#samples_np = samples_np.reshape(shape)
print(samples_np)
# Write the samples to a WAV file
write(output_wav_file, 16000, samples_np)

print(f"Converted {input_qoa_file} back to {output_wav_file} successfully!")
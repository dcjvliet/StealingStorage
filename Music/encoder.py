import numpy as np
import os
from scipy.io.wavfile import write


# spotify and soundcloud use 16-bit samples at a maximum sample rate of 44.1kHz (technically higher for soundcloud)
def file_to_audio(path):
    with open(path, 'rb') as f:
        file_bytes = f.read()

    ext = os.path.splitext(path)[1]  # includes the dot, like '.png'
    ext_bytes = ext.encode('utf-8')
    ext_len = len(ext_bytes)

    if ext_len > 255:
        raise ValueError("Extension too long")

    # Create header: [1-byte ext_len] + [ext] + [file_bytes]
    header = bytes([ext_len]) + ext_bytes
    data_with_header = header + file_bytes

    # Pad if needed
    if len(data_with_header) % 2 != 0:
        data_with_header += b'\x00'

    samples = np.frombuffer(data_with_header, dtype=np.int16)
    write('output.wav', 44100, samples)

    print('File successfully encoded!')


file_path = input("Enter the file path: ")
file_to_audio(file_path)

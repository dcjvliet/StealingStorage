from scipy.io import wavfile


def decode(path='output.wav', output_path='recovered'):
    # convert .wav to binary
    sample_rate, samples = wavfile.read(path)
    byte_data = samples.tobytes()

    # get the file extension
    extension_len = byte_data[0]
    extension = byte_data[1:1+extension_len].decode('utf-8')
    file_bytes = byte_data[1+extension_len:]

    with open(f'{output_path}{extension}', 'wb') as f:
        f.write(file_bytes)

    print('File successfully decoded!')


decode()
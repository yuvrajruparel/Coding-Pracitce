from scipy.io import wavfile
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

def read_data_from_file(filename: str) -> tuple[np.uint64,np.ndarray]:
    """Provided function to read WAV audio data into NumPy array

    Takes a filename string and uses scipy.io.wavfile module to read
    data from file.
    Returns the sampling rate and audio data, where each channel is a column.
    """
    fs, data = wavfile.read(filename)
    print(f'data has shape {data.shape} and type {data.dtype}')
    return fs, data


def convert_twochannel(data: np.ndarray):
    # TODO: Write me!
    n_channels = data.shape[1]
    half = n_channels // 2
    left = np.sum(data[:, :half], axis=1)
    right = np.sum(data[:, half:], axis=1)
    return np.stack((left, right), axis=1)

def play_audio(fs: np.uint64, data: np.ndarray) -> None: 
    """Provided function to play audio using sounddevice module

    Takes a sampling rate and audio data (max two channels) and
    plays the sound.
    """
    n, n_channels = data.shape
    if n_channels > 2:
        print(f'Sorry! sounddevice.play function only works with 2 or fewer channels, but this data has {n_channels} channels and {n} data points')
        print('You may also want to double check you have column data')
        return
    sd.play(data, fs)
    sd.wait()


def make_plots(fs: np.uint64, data):
    # TODO: Write me!
    n_samples = data.shape[0]
    n_channels = data.shape[1]
    time = np.arange(n_samples) / fs

    # Combined channels plot
    plt.figure()
    for i in range(n_channels):
        plt.plot(time, data[:, i], label=f'Channel {i+1}')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('Combined Channels')
    plt.legend()
    plt.savefig('combined_channels_plot.png')
    plt.close()

    fig, axes = plt.subplots(n_channels, 1, figsize=(10, 8), sharex=True)
    for i in range(n_channels):
        axes[i].plot(time, data[:, i])
        axes[i].set_ylabel(f'Ch {i+1}')
    axes[-1].set_xlabel('Time [s]')
    plt.suptitle('Separate Channels')
    plt.savefig('separate_channels_plot.png')
    plt.close()


def main():
    # TODO: Write me!
    # Read data from sample file "Nums_5dot1_24_48000.wav" to get sampling rate and data as array
    fs, data = read_data_from_file("data/Nums_5dot1_24_48000.wav")

    # Plot the data on two figures as specified
    make_plots(fs, data)

    # Create two channels of data from possibly more
    two_channel_data = convert_twochannel(data)

    # Play the two-channel version of the data
    play_audio(fs, two_channel_data)

    
if __name__ == '__main__':
    main()
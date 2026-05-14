# 2D Arrays with Audio Data

## Overview

We have been learning about how to do efficient computation with NumPy arrays (the [`ndarray`](https://numpy.org/doc/stable/reference/arrays.ndarray.html) type). In this activity, we explore two dimensional arrays and practice slicing and manipulating them.

The learning objectives are:

* Determine the shape and data type of an `ndarray`
* Use NumPy documentation to find the appropriate function or method to combine arrays into one or separate an array into several arrays
* Slice or index arrays along different dimensions to obtain desired portion

We will work with audio data because it has a time dimension, as well as a dimension for how many channels it contains. If you are unfamiliar with audio channels, [read here](https://answers.wildlifeacoustics.com/r/en-US/Song-Meter-SM4-Frequently-Asked-Questions/What-is-an-Audio-Channel).

### Set Up

You will need to install the following packages to run this code:

- `scipy`
- `sounddevice`
- `portaudio`

The corresponding install commands are:

```bash
conda install scipy
conda install conda-forge::python-sounddevice
conda install conda-forge::portaudio
```

## Provided

Look in `audio.py` and see that we have provided two functions:

- `read_data_from_file`
- `play_audio`

These functions use convenient libraries to read WAV data into numpy arrays and play it.

## Code specifications

### Main

Write a main function that does the following steps:

1. Call `read_data_from_file` to get the data from sample file "Nums_5dot1_24_48000.wav".
2. Call a function you will write `make_plots` for the audio data.
3. Call a function you will write `convert_twochannel` to create two channels of data from possibly more.
4. Call `play_audio` on the two-channel version of the data.

### Plots

Write the function `make_plots` which should create and display two figures:

1. This figure has one axes object and plots time on the x-axis and each channel on the y-axis. Each channel should be plotted on top of the previous one. Save this figure as `combined_channels_plot.png`.
2. This figure has one subplot per channel. It should plot time on the x-axis and the audio channel on the y-axis for each subplot. Save this figure as `separate_channels_plot.png`.

Hint: Think about how you construct a time array from the number of samples and the sampling frequency.

### Two channels

Write the function `convert_twochannel`, which takes an array of audio data and sums it into two channels.

Specifically, if the data has N channels, it should sum the first N/2 channels along axis 1 to create the new first channel and the last N/2 channels along axis 1 to create the new second channel.

For example, if the input data had 6 channels and 100 samples (100, 6), it should sum channels 0–2 (inclusive) to create a new channel 0 and sum channels 3–5 (inclusive) to create a new channel 1 and return an array of shape (100, 2).

When you are finished writing these functions, the program should display two figures and play the audio.

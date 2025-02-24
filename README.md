Files-to-Audio-and-Back

This repository provides a collection of Python scripts designed to encode and decode data into audio and visual formats. These tools enable the conversion of files or text into audio tones or visual glitches, and subsequently, the retrieval of the original data from these media formats.
Table of Contents

    Overview
    Prerequisites
    Scripts Description
        Audio Encoding and Decoding
            encode_to_audio.py
            decode_from_audio.py
        Visual Glitch Encoding and Decoding
            encode_to_glitch_video.py
            decode_from_glitch_video.py
    Usage
        Encoding Data to Audio
        Decoding Data from Audio
        Encoding Data to Glitch Video
        Decoding Data from Glitch Video
    Notes
    License

Overview

The scripts in this repository allow users to:

    Encode files or text into audio files (.wav) or visual glitch videos (.mp4).
    Decode these audio files or videos back into the original data.
(Works well with - https://github.com/TheGodRX/rtl-sdr-send-message-receive-message/tree/main )
This functionality can be useful for data transmission over audio channels or for creative data storage solutions.
Prerequisites

Before using these scripts, ensure you have the following installed:

    Python 3.x
    Required Python packages:
        numpy
        scipy
        matplotlib
        pygame
        opencv-python

You can install the required packages using:

pip install numpy scipy matplotlib pygame opencv-python

Scripts Description
Audio Encoding and Decoding
encode_to_audio.py

This script encodes binary data from a file or text into an audio file (.wav). It converts each bit of the data into a specific frequency tone:

    FREQ_HIGH: 528 Hz for binary '1'
    FREQ_LOW: 432 Hz for binary '0'

The resulting audio file represents the original data through a sequence of these tones.
decode_from_audio.py

This script decodes an audio file (.wav) back into the original binary data. It analyzes the frequencies present in the audio to reconstruct the binary sequence, which is then converted back into the original file or text.
Visual Glitch Encoding and Decoding
encode_to_glitch_video.py

This script encodes binary data from a file or text into a visual glitch video (.mp4). Each bit is represented by a visual pattern:

    '1': White screen
    '0': Black screen

The sequence of these frames creates a glitch effect that visually represents the original data.
decode_from_glitch_video.py

This script decodes a glitch video (.mp4) back into the original binary data. It analyzes each frame's average brightness to determine whether it represents a '1' or '0', reconstructing the original binary sequence and converting it back into the original file or text.
Usage
Encoding Data to Audio

    Run the encode_to_audio.py script:

    python encode_to_audio.py

    Choose whether to encode a file or text.

    If encoding a file, provide the file path.

    Specify the output audio file name (e.g., encoded_audio.wav).

Decoding Data from Audio

    Run the decode_from_audio.py script:

    python decode_from_audio.py

    Provide the path to the encoded audio file.

    Choose whether to save the decoded content as a file or display it as text.

Encoding Data to Glitch Video

    Run the encode_to_glitch_video.py script:

    python encode_to_glitch_video.py

    Choose whether to encode a file or text.

    If encoding a file, provide the file path.

    Specify the output video file name (e.g., glitch_output.mp4).

Decoding Data from Glitch Video

    Run the decode_from_glitch_video.py script:

    python decode_from_glitch_video.py

    Provide the path to the encoded video file.

    Choose whether to save the decoded content as a file or display it as text.

Notes

    Ensure that the encoding and decoding parameters (e.g., frequencies, durations) match between the encoding and decoding scripts.
    The quality of the decoded data depends on the integrity of the audio or video file. Noise or compression artifacts may affect the accuracy of the decoding process.

License

This project is licensed under the MIT License.

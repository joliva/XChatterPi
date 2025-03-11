# audio_recorder.py Documentation

## Overview

`audio_recorder.py` is a Python script that records audio from a microphone using Voice Activity Detection (VAD). It leverages the `pvrecorder`, `webrtcvad`, and `pydub` libraries to detect speech, record audio segments, and save the recorded audio to a file in either WAV or MP3 format.

## Functionality

The script provides the following functionality:

-   **Voice Activity Detection (VAD):** Uses the `webrtcvad` library to detect speech in real-time. The VAD helps to automatically start and stop recording based on the presence of speech, reducing the amount of unnecessary silence in the recorded audio.
-   **Audio Recording:** Employs the `PvRecorder` library to capture audio from the microphone. The `PvRecorder` provides a simple interface for accessing audio input devices and recording audio data.
-   **File Format Support:** Saves the recorded audio to a file in either WAV or MP3 format. The `pydub` library is used to convert the audio to MP3 format if specified.
-   **Command-Line Interface:** Provides a command-line interface for specifying the output file name and format.

## Design

The script's design can be broken down into the following steps:

1.  **Initialization:**
    -   Initializes a `webrtcvad.Vad` object for voice activity detection. The aggressiveness of the VAD can be set from 0 to 3 (3 is the most aggressive).
    -   Initializes a `PvRecorder` object for recording audio from the microphone. The device index and frame length can be specified.

2.  **Recording Loop:**
    -   Starts the `PvRecorder` to begin listening for audio.
    -   Reads audio frames from the microphone in a loop.
    -   Uses the `webrtcvad` to check if the current frame contains speech.
    -   If speech is detected:
        -   Appends the frame to an audio buffer.
        -   Resets a silence counter.
    -   If speech is not detected and the script is currently recording:
        -   Appends the frame to the audio buffer.
        -   Increments the silence counter.
        -   If the silence counter exceeds a threshold (e.g., 1 second of silence), the recording is stopped.

3.  **Saving Audio:**
    -   After the recording loop finishes (either by detecting a long period of silence or by user interruption), the recorded audio is saved to a file.
    -   If the specified format is MP3:
        -   The audio buffer is first saved to a temporary WAV file.
        -   The temporary WAV file is then converted to MP3 using `pydub`.
    -   If the specified format is WAV:
        -   The audio buffer is saved directly to a WAV file.

## Function: `record_with_vad(filename, file_format, device_index=-1, sample_rate=16000, frame_duration_ms=30)`

This function is the core of the `audio_recorder.py` script. It encapsulates the entire process of recording audio with VAD and saving it to a file.

**Args:**

-   `filename` (str): The name of the output file.
-   `file_format` (str): The format of the output file ('wav' or 'mp3').
-   `device_index` (int, optional): The index of the audio device to use. Defaults to -1 (default device).
-   `sample_rate` (int, optional): The sample rate of the audio. Defaults to 16000 Hz.
-   `frame_duration_ms` (int, optional): The duration of each audio frame in milliseconds. Defaults to 30 ms.

**Returns:**

-   `None`

**Usage Example:**

To record audio to a file named "output.wav" in WAV format, you can run the script from the command line like this:


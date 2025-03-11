# audio_recorder.py Documentation

## Overview

`audio_recorder.py` is a Python script that records audio from a microphone using Voice Activity Detection (VAD). It leverages the `pvrecorder`, `webrtcvad`, and `pydub` libraries to detect speech, record audio segments, and save the recorded audio to a file in either WAV or MP3 format.

## Functionality

The script provides the following functionality:

-   **Voice Activity Detection (VAD):** Uses the `webrtcvad` library to detect speech in real-time. The VAD helps to automatically start and stop recording based on the presence of speech, reducing the amount of unnecessary silence in the recorded audio.
-   **Adjustable VAD Sensitivity:** Allows users to control the aggressiveness level of the Voice Activity Detection (0-3) to better handle different noise environments.
-   **Audio Recording:** Employs the `PvRecorder` library to capture audio from the microphone. The `PvRecorder` provides a simple interface for accessing audio input devices and recording audio data.
-   **File Format Support:** Saves the recorded audio to a file in either WAV or MP3 format. The `pydub` library is used to convert the audio to MP3 format if specified.
-   **Command-Line Interface:** Provides a comprehensive command-line interface for specifying the output file name, format, device index, and VAD sensitivity level.

## Design

The script's design can be broken down into the following steps:

1.  **Initialization:**
    -   Initializes a `webrtcvad.Vad` object for voice activity detection. The aggressiveness of the VAD can be set from 0 to 3 (3 is the most aggressive, 0 is the least aggressive).
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

## Function: `record_with_vad(filename, file_format, device_index=-1, sample_rate=16000, frame_duration_ms=30, vad_aggressiveness=3)`

This function is the core of the `audio_recorder.py` script. It encapsulates the entire process of recording audio with VAD and saving it to a file.

**Args:**

-   `filename` (str): The name of the output file.
-   `file_format` (str): The format of the output file ('wav' or 'mp3').
-   `device_index` (int, optional): The index of the audio device to use. Defaults to -1 (default device).
-   `sample_rate` (int, optional): The sample rate of the audio. Defaults to 16000 Hz.
-   `frame_duration_ms` (int, optional): The duration of each audio frame in milliseconds. Defaults to 30 ms.
-   `vad_aggressiveness` (int, optional): The aggressiveness level of the VAD (0-3). Defaults to 3.
    - Level 0: Least aggressive (more likely to detect background noise as speech)
    - Level 1: Moderately aggressive
    - Level 2: More aggressive
    - Level 3: Most aggressive (less likely to detect background noise as speech)

**Returns:**

-   `None`

## Command Line Interface

The script provides a command-line interface with the following arguments:

-   `output` (optional): Output file name (defaults to "output")
-   `--format {wav,mp3}`: Output file format (defaults to "wav")
-   `--device DEVICE`: Audio device index (defaults to -1, system default)
-   `--vad-level {0,1,2,3}`: VAD aggressiveness level (defaults to 3)
-   `--help`: Show detailed help information and exit

**Usage Examples:**

1. Basic recording with default settings (creates output.wav):
   ```
   python audio_recorder.py
   ```

2. Record audio to a specific file in WAV format:
   ```
   python audio_recorder.py my_recording
   ```

3. Record audio to a file in MP3 format:
   ```
   python audio_recorder.py --format mp3
   ```

4. Specify a different audio device (e.g., device index 1):
   ```
   python audio_recorder.py --device 1
   ```

5. Adjust the VAD sensitivity to be less aggressive:
   ```
   python audio_recorder.py --vad-level 1
   ```

6. Display detailed help information:
   ```
   python audio_recorder.py --help
   ```

To list available audio devices, you can use:
```
python -c "from pvrecorder import PvRecorder; print(PvRecorder.get_audio_devices())"
```

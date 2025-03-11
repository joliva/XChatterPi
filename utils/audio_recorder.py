import argparse
from pvrecorder import PvRecorder
import webrtcvad
import wave
import struct
import numpy as np
from pydub import AudioSegment

def record_with_vad(filename, file_format, device_index=-1, sample_rate=16000, frame_duration_ms=30, vad_aggressiveness=3):
    """
    Records audio using Voice Activity Detection (VAD) to automatically stop recording when speech ends.

    Args:
        filename (str): The name of the output file.
        file_format (str): The format of the output file ('wav' or 'mp3').
        device_index (int, optional): The index of the audio device to use. Defaults to -1 (default device).
        sample_rate (int, optional): The sample rate of the audio. Defaults to 16000 Hz.
        frame_duration_ms (int, optional): The duration of each audio frame in milliseconds. Defaults to 30 ms.
        vad_aggressiveness (int, optional): The aggressiveness level of the VAD (0-3). Defaults to 3.
            - Level 0: Least aggressive (more likely to detect background noise as speech)
            - Level 1: Moderately aggressive
            - Level 2: More aggressive
            - Level 3: Most aggressive (less likely to detect background noise as speech)

    Usage Examples:
        1. Record audio and save it as a WAV file:
           python audio_recorder.py output.wav

        2. Record audio and save it as an MP3 file:
           python audio_recorder.py output.mp3 --format mp3

        3. Specify a different audio device index (e.g., device index 1):
           python audio_recorder.py output.wav --device 1

        4. Use a lower VAD aggressiveness level (e.g., level 1):
           python audio_recorder.py output.wav --vad-level 1

    Note: Use `PvRecorder.get_audio_devices()` to list available device indices.
    """

    # Initialize VAD with specified aggressiveness level.
    vad = webrtcvad.Vad(vad_aggressiveness)

    # Initialize PvRecorder with specified device index and frame length.
    recorder = PvRecorder(device_index=device_index, frame_length=int(sample_rate * frame_duration_ms / 1000))

    audio_buffer = []
    is_speech = False
    silence_frames = 0
    max_silence_frames = int(1 * (1000 / frame_duration_ms))  # 1 second of silence

    try:
        recorder.start()
        print("Listening... Press Ctrl+C to stop.")

        # Main loop to capture audio frames and detect speech.
        while True:
            frame = recorder.read()

            # Check if the current frame contains speech using VAD.
            is_speech_frame = vad.is_speech(struct.pack("<" + "h" * len(frame), *frame), sample_rate)

            if is_speech_frame:
                # If speech is detected, add the frame to the buffer and reset the silence counter.
                if not is_speech:
                    print("Speech detected, recording...")
                    is_speech = True
                audio_buffer.extend(frame)
                silence_frames = 0
            elif is_speech:
                # If no speech is detected but we were previously recording speech,
                # add the frame to the buffer and increment the silence counter.
                audio_buffer.extend(frame)
                silence_frames += 1

                # If the silence counter exceeds the maximum allowed silence frames, stop recording.
                if silence_frames >= max_silence_frames:
                    print("End of speech detected.")
                    break

    except KeyboardInterrupt:
        print("Recording stopped by user")
    finally:
        # Ensure the recorder is stopped and resources are released.
        recorder.stop()
        recorder.delete()

    # Save the recorded audio to a file.
    if audio_buffer:
        temp_wav = "temp.wav"

        # Save the audio buffer to a temporary WAV file.
        with wave.open(temp_wav, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(struct.pack("<" + "h" * len(audio_buffer), *audio_buffer))

        # If the desired format is MP3, convert the WAV file to MP3 using pydub.
        if file_format == 'mp3':
            audio = AudioSegment.from_wav(temp_wav)
            audio.export(filename, format="mp3")
            print(f"Audio saved to {filename}")
        else:
            # If the desired format is WAV, rename the temporary WAV file to the output file.
            import os
            os.rename(temp_wav, filename)
            print(f"Audio saved to {filename}")
    else:
        print("No speech detected, no file saved.")

def print_detailed_help():
    """Prints detailed help information about the script."""
    help_text = """
AUDIO RECORDER WITH VOICE ACTIVITY DETECTION

This script records audio from a microphone and automatically stops recording
when speech ends, using Voice Activity Detection (VAD).

DEPENDENCIES:
  - pvrecorder: For audio recording
  - webrtcvad: For voice activity detection
  - pydub: For audio format conversion
  - numpy: For audio processing

COMMAND LINE ARGUMENTS:
  output                    Output file name
  --format {wav,mp3}        Output file format (default: wav)
  --device DEVICE           Audio device index (default: -1, system default)
  --vad-level {0,1,2,3}     VAD aggressiveness level (default: 3)
                            0: Least aggressive (more sensitive to background noise)
                            3: Most aggressive (less sensitive to background noise)
  --detailed-help           Show this detailed help message and exit

EXAMPLES:
  1. Basic recording to WAV:
     python audio_recorder.py output.wav

  2. Recording to MP3:
     python audio_recorder.py output.mp3 --format mp3

  3. Using a specific audio device:
     python audio_recorder.py output.wav --device 1

  4. Adjusting VAD sensitivity:
     python audio_recorder.py output.wav --vad-level 1

  5. List available audio devices:
     python -c "from pvrecorder import PvRecorder; print(PvRecorder.get_audio_devices())"

BEHAVIOR:
  - The script starts listening immediately when run
  - Recording begins automatically when speech is detected
  - Recording stops automatically after 1 second of silence
  - Press Ctrl+C at any time to stop recording manually

OUTPUT:
  - The recorded audio is saved to the specified file
  - If no speech is detected, no file is saved
    """
    print(help_text)

if __name__ == "__main__":
    # Set up argument parser to accept command-line arguments.
    parser = argparse.ArgumentParser(description="Record audio with VAD and save as WAV or MP3.", add_help=False)
    parser.add_argument("output", nargs='?', default="output", help="Output file name (default: output)")
    parser.add_argument("--format", choices=["wav", "mp3"], default="wav", help="Output file format (default: wav)")
    parser.add_argument("--device", type=int, default=-1, help="Audio device index (default: -1, system default)")
    parser.add_argument("--vad-level", type=int, choices=[0, 1, 2, 3], default=3,
                        help="VAD aggressiveness level (0-3, where 0 is least aggressive and 3 is most aggressive)")
    parser.add_argument("--help", action="store_true", help="Show detailed help information and exit")

    args = parser.parse_args()

    if args.help:
        print_detailed_help()
        exit(0)

    output_file = args.output

    # Ensure the output file has the correct extension.
    if not output_file.endswith(f".{args.format}"):
        output_file += f".{args.format}"

    # Call the record_with_vad function with the specified parameters.
    record_with_vad(output_file, args.format, device_index=args.device, vad_aggressiveness=args.vad_level)


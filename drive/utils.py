import os
import tempfile

import speech_recognition as sr
from pydub import AudioSegment


def speech_to_text_pipeline(audio_file):
    try:
        # Convert the audio file to PCM WAV format
        audio = AudioSegment.from_file(audio_file)
        wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio.export(wav_file.name, format="wav")

        # Perform speech recognition on the converted WAV file
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file.name) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)

        # Clean up temporary file
        os.remove(wav_file.name)

        return text
    except Exception as e:
        return str(e)

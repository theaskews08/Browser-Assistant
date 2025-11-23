"""
Enhanced Speech-to-Text with support for multiple engines including Whisper.
Provides high-quality local speech recognition.
"""

import speech_recognition as sr
import threading
import queue
import time

class EnhancedSTT:
    """Enhanced speech recognition with multiple engine support."""

    def __init__(self, engine='google', model_size='base'):
        """
        Initialize the STT engine.

        Args:
            engine: 'google' (online, fast) or 'whisper' (offline, high quality)
            model_size: For Whisper: 'tiny', 'base', 'small', 'medium', 'large'
                       Recommended: 'base' for good balance of speed and accuracy
        """
        self.engine = engine
        self.model_size = model_size
        self.recognizer = sr.Recognizer()
        self.whisper_model = None

        # Configure recognizer for better performance
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3

        if engine == 'whisper':
            self._initialize_whisper()

    def _initialize_whisper(self):
        """Initialize Whisper model for offline recognition."""
        try:
            import whisper
            print(f"Loading Whisper model ({self.model_size})... This may take a moment.")
            self.whisper_model = whisper.load_model(self.model_size)
            print("✓ Whisper model loaded successfully")
        except ImportError:
            print("⚠ Whisper not installed. Install with: pip install openai-whisper")
            print("Falling back to Google Speech Recognition")
            self.engine = 'google'
        except Exception as e:
            print(f"Error loading Whisper: {e}")
            print("Falling back to Google Speech Recognition")
            self.engine = 'google'

    def listen_for(self, timeout=5, phrase_time_limit=None):
        """
        Listen for voice input and return recognized text.

        Args:
            timeout: Maximum time to wait for speech to start
            phrase_time_limit: Maximum time for the phrase

        Returns:
            String containing recognized speech or empty string on failure
        """
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)

                # Listen for audio
                print(f"Listening for {timeout} seconds...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit or timeout
                )

                # Recognize speech using selected engine
                return self._recognize_audio(audio)

        except sr.WaitTimeoutError:
            print("Listening timed out - no speech detected")
            return ""
        except Exception as e:
            print(f"Error with microphone: {e}")
            return ""

    def _recognize_audio(self, audio):
        """Recognize audio using the configured engine."""
        try:
            if self.engine == 'whisper' and self.whisper_model:
                return self._recognize_whisper(audio)
            else:
                return self._recognize_google(audio)
        except Exception as e:
            print(f"Recognition error: {e}")
            return ""

    def _recognize_whisper(self, audio):
        """Recognize audio using Whisper."""
        try:
            # Convert audio to the format Whisper expects
            import numpy as np
            import io
            from scipy.io import wavfile

            # Get raw audio data
            wav_data = audio.get_wav_data()

            # Convert to numpy array
            audio_io = io.BytesIO(wav_data)
            sample_rate, audio_array = wavfile.read(audio_io)

            # Convert to float32 and normalize
            audio_array = audio_array.astype(np.float32) / 32768.0

            # Transcribe using Whisper
            result = self.whisper_model.transcribe(
                audio_array,
                fp16=False,
                language='en'
            )

            text = result['text'].strip()
            print(f"You said (Whisper): {text}")
            return text.lower()

        except Exception as e:
            print(f"Whisper recognition error: {e}")
            # Fallback to Google
            return self._recognize_google(audio)

    def _recognize_google(self, audio):
        """Recognize audio using Google Speech Recognition."""
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said (Google): {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google; {e}")
            return ""

    def listen_continuous(self, callback, stop_event):
        """
        Continuously listen for speech and call callback with recognized text.

        Args:
            callback: Function to call with recognized text
            stop_event: Threading event to stop listening
        """
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Continuous listening started")

            while not stop_event.is_set():
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    text = self._recognize_audio(audio)

                    if text:
                        callback(text)

                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"Error in continuous listening: {e}")
                    time.sleep(0.5)


class StreamingSTT:
    """Streaming speech recognition for real-time transcription."""

    def __init__(self, callback):
        """
        Initialize streaming STT.

        Args:
            callback: Function to call with each recognized phrase
        """
        self.callback = callback
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.microphone = None
        self.stop_listening = None

    def start(self):
        """Start streaming recognition."""
        if self.is_listening:
            return

        self.microphone = sr.Microphone()
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone,
            self._audio_callback,
            phrase_time_limit=5
        )

        self.is_listening = True
        print("Streaming STT started")

    def stop(self):
        """Stop streaming recognition."""
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        self.is_listening = False
        print("Streaming STT stopped")

    def _audio_callback(self, recognizer, audio):
        """Internal callback for processing audio."""
        try:
            text = recognizer.recognize_google(audio)
            self.callback(text.lower())
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Recognition error: {e}")


# Convenience function
def listen_for(timeout=5, engine='google', model_size='base'):
    """
    Quick function to listen for speech.

    Args:
        timeout: Maximum seconds to listen
        engine: 'google' or 'whisper'
        model_size: Whisper model size if using whisper

    Returns:
        Recognized text or empty string
    """
    stt = EnhancedSTT(engine=engine, model_size=model_size)
    return stt.listen_for(timeout)


# Test function
if __name__ == "__main__":
    print("Testing Enhanced STT...")
    print("\n1. Testing Google Speech Recognition:")
    text1 = listen_for(timeout=5, engine='google')
    print(f"Result: '{text1}'")

    print("\n2. Testing Whisper (if available):")
    text2 = listen_for(timeout=5, engine='whisper', model_size='base')
    print(f"Result: '{text2}'")

    print("\nSTT test complete!")
